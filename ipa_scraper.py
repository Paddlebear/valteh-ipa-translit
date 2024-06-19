# ipa_scraper.py

from user_input import UserInput

import requests
import re
from bs4 import BeautifulSoup


class IPAScraper:
    ACCEPTED_LANGUAGES = ["Mandarin", "French", "Ukrainian", "Japanese", "Standard German", "English"]
    ACCEPTED_LANGUAGES_CODES = ["zh", "fr", "ua", "jp", "de", "eng"]
    WIKIPEDIA_URL_EN = "https://en.wikipedia.org/wiki/"
    HTML_PARSER = "html.parser"
    
    def get_ipa_object(
        self, 
        proper_noun, 
        noun_class,
        gender,
        ):
        """
        Creates an ipa object that contains all of the data
        about the user selected proper noun.

        Args:
            proper_noun (str): user selected proper noun.
            noun_class (str): user selected noun class.
            gender (str): user selected gender for the proper noun.

        Returns:
            JSON: `ipa_obj`.
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
            "raw_ipa_to_lv": None,
            "processed_ipa_to_lv": None    
        }
        
        return result
    
    def _get_proper_noun_wiki_url(self, proper_noun):
        """
        Create the wikipedia url to the user
        selected proper noun.

        Args:
            proper_noun (str): the user selected proper noun.

        Returns:
            str: the wikipedia url to the proper noun.
        """     
           
        return f"{self.WIKIPEDIA_URL_EN}{proper_noun}"
    
    def _get_scraped_ipa_html_obj(self, wiki_url):
        """
        Web scrapes the wiki_url for the ipa object and its parent
        html objects.

        Args:
            wiki_url (str): the wikipedia url to the proper noun.

        Returns:
            JSON: JSON collection containing the html object and the 
                language, for which the IPA string was found. 
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
        """
        Extracts the ipa_string from the ipa html object.

        Args:
            raw_ipa_obj (str): the html object, that needs to be parsed, to retrieve
                            its contained ipa_string.
            language (str): the language of the ipa_string.

        Returns:
            str: the extracted ipa_string value.
        """        
        ipa_string = None
        
        if raw_ipa_obj == None or language == None:
            return ipa_string
        
        if language != "English":
            pattern_brackets = re.compile(r'\[(.*?)\]')
            match = pattern_brackets.search(raw_ipa_obj)

            if match:
                extracted_text = match.group(1)
                cleaned_text = extracted_text.replace('<span class="wrap"> </span>', ' ')

                ipa_string = cleaned_text
            else:
                pattern_span = re.compile(r'<span[^>]*>(.*?)</span>')
                matches = pattern_span.findall(raw_ipa_obj)
                span_texts = [match for match in matches if 'title' not in match]

                if span_texts:
                    span_text = ''.join(span_texts)
                    ipa_string = span_text
                else:
                    print("No nested ipa_string found with the present regular expression rules.")

            # Replace nbsp when it appears, since it hinders word separation.
            ipa_string = ipa_string.replace("\u00A0", "\u0020")
            return ipa_string

        if language == "English":
            pattern_span = re.compile(r'<span[^>]*>(.*?)</span>')
            matches = pattern_span.findall(raw_ipa_obj)

            extracted_text = ''
            for match in matches:
                clean_match = re.sub(r'<[^>]*>', '', match)
                extracted_text += clean_match

            ipa_string = extracted_text.strip()
            # Replace nbsp when it appears, since it hinders word separation.
            ipa_string = ipa_string.replace("\u00A0", "\u0020")
            return ipa_string

        
        # Replace nbsp when it appears, since it hinders word separation.
        ipa_string = ipa_string.replace("\u00A0", "\u0020")
        return ipa_string
    
    