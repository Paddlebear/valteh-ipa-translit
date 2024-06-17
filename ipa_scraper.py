# ipa_scraper.py

from user_input import UserInput

import requests
import re
from bs4 import BeautifulSoup


class IPAScraper:
    ACCEPTED_LANGUAGES = ["Mandarin", "French", "Standard German", "Ukrainian", "Japanese", "English"]
    WIKIPEDIA_URL_EN = "https://en.wikipedia.org/wiki/"
    HTML_PARSER = "html.parser"
    
    def get_ipa_object(
        self, 
        proper_noun, 
        noun_class,
        gender,
        ):
        """_summary_

        Args:
            proper_noun (_type_): _description_
            noun_class (_type_): _description_
            gender (_type_): _description_

        Returns:
            _type_: _description_
        """        
        
        wiki_url = self._get_proper_noun_wiki_url(proper_noun)
        raw_ipa_html_obj_and_language = self._get_scraped_ipa_html_obj(wiki_url)
        
        # Handle cities explicitly.
        if (
            raw_ipa_html_obj_and_language["raw_ipa_html_obj"] == None and 
            raw_ipa_html_obj_and_language["language"] == None and 
            noun_class == UserInput.PI
            ):
            
            wiki_url = wiki_url + "_City"
            raw_ipa_html_obj_and_language = self._get_scraped_ipa_html_obj(wiki_url)
        
        result = {
            "proper_noun_str": proper_noun, 
            "wiki_url_to_proper_noun": wiki_url,
            "noun_class": noun_class,
            "gender": gender,
            "language": raw_ipa_html_obj_and_language["language"],
            "raw_ipa_html_obj": raw_ipa_html_obj_and_language["raw_ipa_html_obj"],
            "ipa_str": self._get_ipa_string(
                    raw_ipa_html_obj_and_language["raw_ipa_html_obj"], 
                    raw_ipa_html_obj_and_language["language"]
                    ),
            "ipa_to_lv": None    
        }
        
        return result
    
    def _get_proper_noun_wiki_url(self, proper_noun):
        """_summary_

        Args:
            proper_noun (_type_): _description_

        Returns:
            _type_: _description_
        """     
           
        return f"{self.WIKIPEDIA_URL_EN}{proper_noun}"
    
    def _get_scraped_ipa_html_obj(self, wiki_url):
        """_summary_

        Args:
            wiki_url (_type_): _description_

        Returns:
            _type_: _description_
        """      
          
        page = requests.get(wiki_url)
        soup = BeautifulSoup(page.content, self.HTML_PARSER)
        
        html_element = None
        language = None

        for l in self.ACCEPTED_LANGUAGES:
            
            result = soup.find_all(title=f"Help:IPA/{l}")
            if len(result) > 0:
                language = l
                for r in result:
                
                    if ">[" in str(r) or ">/" in str(r):
                        html_element = r
                        break
                
                if html_element != None:
                    break
        
        if not html_element:
            return {"language": None, "raw_ipa_html_obj": None}
        else:
            return {"language": language, "raw_ipa_html_obj": str(html_element)}
    
    def _get_ipa_string(self, raw_ipa_obj, language):
        """_summary_

        Args:
            raw_ipa_obj (_type_): _description_
            language (_type_): _description_

        Returns:
            _type_: _description_
        """        
        
        ipa_string = None
        extracted_text = None
        pattern_span = re.compile(r'<span[^>]*>(.*?)</span>')
        pattern_brackets = re.compile(r'\[(.*?)\]')
        
        if raw_ipa_obj == None or language == None:
            return ipa_string
        
        if language == "English":
            matches = pattern_span.findall(raw_ipa_obj)
            
            for match in matches:
                clean_match = re.sub(r'<[^>]*>', '', match)
                extracted_text += clean_match

            ipa_string = extracted_text.strip()
        
        else:
            match = pattern_brackets.search(raw_ipa_obj)
            
            if match:
                extracted_text = match.group(1)
                cleaned_text = extracted_text.replace('<span class="wrap"> </span>', ' ')
                ipa_string = cleaned_text
            
            else:
                matches = pattern_span.findall(raw_ipa_obj)
                span_texts = [match for match in matches if 'title' not in match]

                if span_texts:
                    span_text = ''.join(span_texts)
                    ipa_string = span_text
    
        return ipa_string
    
    
    
    
    
    
    # def get_article_ipa_obj(self, noun_class, proper_noun):
    #     url = self.generate_proper_noun_wiki_url(proper_noun)
    #     result = self.get_ipa_element(url)
        
    #     if not result and noun_class == 'pi':
    #         url = url + "_City"
    #         result = self.get_ipa_element(url)
        
    #     if not result:
    #         print(f"Netika atrasts IPA identifikators dotajā šķirklī: {url}")
    #         return None
        
    #     element = result["element"]
    #     language = result["language"]
    #     return {
    #         "noun_class": "",
    #         "language": language,
    #         "gender": "",
    #         "raw_ipa_string": str(element),
    #         "ipa_string": ""
    #     }



    # def process_ipa_obj(self, noun_class, gender, raw_ipa_obj):
    #     raw_ipa_obj["noun_class"] = noun_class
    #     raw_ipa_obj["gender"] = gender

    #     if raw_ipa_obj["language"] != "English":
    #         pattern_brackets = re.compile(r'\[(.*?)\]')
    #         match = pattern_brackets.search(raw_ipa_obj["raw_ipa_string"])

    #         if match:
    #             extracted_text = match.group(1)
    #             cleaned_text = extracted_text.replace('<span class="wrap"> </span>', ' ')
    #             raw_ipa_obj["ipa_string"] = cleaned_text
    #         else:
    #             pattern_span = re.compile(r'<span[^>]*>(.*?)</span>')
    #             matches = pattern_span.findall(raw_ipa_obj["raw_ipa_string"])
    #             span_texts = [match for match in matches if 'title' not in match]

    #             if span_texts:
    #                 span_text = ''.join(span_texts)
    #                 raw_ipa_obj["ipa_string"] = span_text
    #             else:
    #                 print("No nested ipa_string found with the present regular expression rules.")
    #         return raw_ipa_obj

    #     if raw_ipa_obj["language"] == "English":
    #         pattern_span = re.compile(r'<span[^>]*>(.*?)</span>')
    #         matches = pattern_span.findall(raw_ipa_obj["raw_ipa_string"])

    #         extracted_text = ''
    #         for match in matches:
    #             clean_match = re.sub(r'<[^>]*>', '', match)
    #             extracted_text += clean_match

    #         raw_ipa_obj["ipa_string"] = extracted_text.strip()
    #         return raw_ipa_obj


    # def get_ipa_element(self, url):
    #     page = requests.get(url)
    #     soup = BeautifulSoup(page.content, self.HTML_PARSER)
    #     element, language = None, None

    #     for lang in self.ACCEPTED_LANGUAGES:
    #         result = soup.find_all(title=f"Help:IPA/{lang}")
    #         if result:
    #             language = lang
    #             for r in result:
    #                 if ">[" in str(r) or ">/" in str(r):
    #                     element = r
    #                     break
    #             if element:
    #                 break
        
    #     if not element:
    #         return None
    #     return {"element": element, "language": language}


    # def generate_proper_noun_wiki_url(self, proper_noun):
    #     return f"{self.WIKIPEDIA_URL_EN}{proper_noun}"
