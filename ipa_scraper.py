# ipa_scraper.py

import requests
import re
from bs4 import BeautifulSoup


class IPAScraper:
    ACCEPTED_LANGUAGES = ["Mandarin", "French", "Standard German", "Ukrainian", "Japanese", "English"]
    WIKIPEDIA_URL_EN = "https://en.wikipedia.org/wiki/"
    HTML_PARSER = "html.parser"
    
    def get_article_ipa_obj(self, noun_class, proper_noun):
        url = self.generate_proper_noun_wiki_url(proper_noun)
        result = self.get_ipa_element(url)
        
        if not result and noun_class == 'pi':
            url = url + "_City"
            result = self.get_ipa_element(url)
        
        if not result:
            print(f"Netika atrasts IPA identifikators dotajā šķirklī: {url}")
            return None
        
        element = result["element"]
        language = result["language"]
        return {
            "noun_class": "",
            "language": language,
            "gender": "",
            "raw_ipa_string": str(element),
            "ipa_string": ""
        }

    def generate_proper_noun_wiki_url(self, proper_noun):
        return f"{self.WIKIPEDIA_URL_EN}{proper_noun}"

    def get_ipa_element(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, self.HTML_PARSER)
        element, language = None, None

        for lang in self.ACCEPTED_LANGUAGES:
            result = soup.find_all(title=f"Help:IPA/{lang}")
            if result:
                language = lang
                for r in result:
                    if ">[" in str(r) or ">/" in str(r):
                        element = r
                        break
                if element:
                    break
        
        if not element:
            return None
        return {"element": element, "language": language}

    def process_ipa_obj(self, noun_class, gender, raw_ipa_obj):
        raw_ipa_obj["noun_class"] = noun_class
        raw_ipa_obj["gender"] = gender

        if raw_ipa_obj["language"] != "English":
            pattern_brackets = re.compile(r'\[(.*?)\]')
            match = pattern_brackets.search(raw_ipa_obj["raw_ipa_string"])

            if match:
                extracted_text = match.group(1)
                cleaned_text = extracted_text.replace('<span class="wrap"> </span>', ' ')
                raw_ipa_obj["ipa_string"] = cleaned_text
            else:
                pattern_span = re.compile(r'<span[^>]*>(.*?)</span>')
                matches = pattern_span.findall(raw_ipa_obj["raw_ipa_string"])
                span_texts = [match for match in matches if 'title' not in match]

                if span_texts:
                    span_text = ''.join(span_texts)
                    raw_ipa_obj["ipa_string"] = span_text
                else:
                    print("No nested ipa_string found with the present regular expression rules.")
            return raw_ipa_obj

        if raw_ipa_obj["language"] == "English":
            pattern_span = re.compile(r'<span[^>]*>(.*?)</span>')
            matches = pattern_span.findall(raw_ipa_obj["raw_ipa_string"])

            extracted_text = ''
            for match in matches:
                clean_match = re.sub(r'<[^>]*>', '', match)
                extracted_text += clean_match

            raw_ipa_obj["ipa_string"] = extracted_text.strip()
            return raw_ipa_obj
