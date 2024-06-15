# print("hello wowld uwu") #@Paddlebear was here UwU
import requests
# import json
import re
from bs4 import BeautifulSoup

ACCEPTED_LANGUAGES = ["Mandarin", "Lithuanian", "French", "Standard German", "Ukrainian", "Japanese", "English"] # The order is deliberate.
PI = "pi" # city proper noun.
PV = "pv" # person proper noun.
MALE = "v" # male gender.
FEMALE = "s" # female gender.

WIKIPEDIA_URL_EN = "https://en.wikipedia.org/wiki/"
HTML_PARSER = "html.parser"

def main():
    """
    Main function.
    """
    
    exit_condition = True
    while exit_condition == True:
        user_input = get_proper_noun()
        noun_class = get_noun_class()
        
        if (noun_class == PV):
            gender = get_gender()
        elif (noun_class == PI):
            gender = FEMALE
            
        sanitized_input = sanitize_input(user_input)
        
        raw_ipa_obj = get_article_ipa_obj(noun_class, generate_proper_noun_wiki_url(sanitized_input))
        
        if raw_ipa_obj != 0:
            processed_ipa_obj = process_ipa_obj(noun_class, gender, raw_ipa_obj)

        # print(processed_ipa_obj["language"])    
        # print(processed_ipa_obj["raw_ipa_string"])
        print(processed_ipa_obj["ipa_string"])
        
        raw_exit_condition = None
        while raw_exit_condition not in ["y", "n"]:
            raw_exit_condition = input("Izvēlēties jaunu īpašvārdu? (y/n): ").strip().lower()

            if raw_exit_condition == "y":
                exit_condition = True
            elif raw_exit_condition == "n":
                exit_condition = False
            else:
                print("Nederīga ievade! Lūdzu, ievadiet 'y' vai 'n'.")

    print("Programma beidzās.")
    
def get_proper_noun():
    """_summary_

    Returns:
        _type_: _description_
    """    
    proper_noun = str(input("Ievadiet izvēlēto īpašvārdu:"))
    while (len(proper_noun.strip(" ")) <= 0):
        print("Nederīga ievade - nevar būt tukša ievade")
        proper_noun = str(input("Ievadiet izvēlēto īpašvārdu:"))
    return proper_noun

def get_noun_class():
    """_summary_

    Returns:
        _type_: _description_
    """    
    noun_class = str(input("Vai īpašvārds ir pilsēta vai personvārds? (pi/pv)"))
    while (noun_class != PI and noun_class != PV):
        print("Nederīga izvēle.")
        noun_class = str(input("Vai īpašvārds ir pilsēta vai personvārds? (pi/pv)"))
    return noun_class
    
def get_gender():
    """_summary_

    Returns:
        _type_: _description_
    """    
    gender = str(input("Vai personvārds ir vīrieša vai sievietes? (v/s)"))
    while (gender != MALE and gender != FEMALE):
        print("Nederīga izvēle.")
        gender = str(input("Vai personvārds ir vīrieša vai sievietes? (v/s)"))
    return gender
    
def sanitize_input(input):
    """
    Sanitizes the users input, capitalizing the first letter and replacing spaces with an "_".

    Args:
        input (str): The provided proper noun.

    Returns:
        str: Sanitized proper noun, that can be used as part of a wikipedia link.
    """    
    input = input.title()
    input = input.replace(' ', '_')
    return input

def generate_proper_noun_wiki_url(proper_noun):
    """
    _summary_

    Args:
        proper_noun (_type_): _description_

    Returns:
        _type_: _description_
    """    
    print(f"{WIKIPEDIA_URL_EN}{proper_noun}")
    return f"{WIKIPEDIA_URL_EN}{proper_noun}"

## IGNORE, THIS HAS BEEN REFACTORED INTO TWO SEPERATE FUNCTIONS
def get_article_ipa_object(noun_class, url):
    """
    Scrapes the IPA string from a provided Wikipedia URL.

    Args:
        url (str): url to Wikipedia
    """   
    page = requests.get(url)
    soup = BeautifulSoup(page.content, HTML_PARSER)
    result = None
    language = None
    element = None
    
    # TODO if city and no IPA is found, attempt to modify the url to end with <city_name>_(city) OR <city_name>_City.
    for i in ACCEPTED_LANGUAGES:
        # TODO consider looking for both title and href.
        result = soup.find_all(title=f"Help:IPA/{i}") # TODO loop for 1 language multiple time until you find something that 
                                                  # TODO resembles ipa and not "IPA", and starts with "[" and ends with "]" or ""/
        if result != None:
            language = i
            for r in result:
                if ">[" in str(r) or ">/" in str(r):
                    element = r
                    break
            if element != None:
                break
    
    if result == None:
        # if noun_class == PI:
        #     page = requests.get(url+"_(city)")
        #     soup = BeautifulSoup(page.content, HTML_PARSER)
        #     result = None
        #     language = None
        #     element = None
        
        #     # TODO if city and no IPA is found, attempt to modify the url to end with <city_name>_(city) OR <city_name>_City.
        #     for i in ACCEPTED_LANGUAGES:
        #         # TODO consider looking for both title and href.
        #         result = soup.find_all(title=f"Help:IPA/{i}") # TODO loop for 1 language multiple time until you find something that 
        #                                                 # TODO resembles ipa and not "IPA", and starts with "[" and ends with "]" or ""/
        #         if result != None:
        #             language = i
        #             for r in result:
        #                 if ">[" in str(r) or ">/" in str(r):
        #                     element = r
        #                     break
        #             if element != None:
        #                 break
                
        #         if result == None:
        #             print(f"Netika atrasts IPA identifikators dotajā šķirklī: {url}")    
        #             return 0
                    
        #         else:    
        #             return_obj = {
        #                 "noun_class": "",
        #                 "language": language,
        #                 "gender": "",
        #                 "raw_ipa_string": str(element), # Vrbt nevajag to str šeit. //vajag jo beautifulsoup
        #                 "ipa_string": ""   
        #             }
            
        #             return return_obj
        # else:        
            print(f"Netika atrasts IPA identifikators dotajā šķirklī: {url}")    
            return 0
    
    else:
        return_obj = {
            "noun_class": "",
            "language": language,
            "gender": "",
            "raw_ipa_string": str(element), # Vrbt nevajag to str šeit. //vajag jo beautifulsoup
            "ipa_string": ""   
        }
        
        return return_obj
    
def get_ipa_element(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, HTML_PARSER)
    result = None
    language = None
    element = None
    
    # TODO if city and no IPA is found, attempt to modify the url to end with <city_name>_(city) OR <city_name>_City.
    for i in ACCEPTED_LANGUAGES:
        # TODO consider looking for both title and href.
        result = soup.find_all(title=f"Help:IPA/{i}") # TODO loop for 1 language multiple time until you find something that 
                                                  # TODO resembles ipa and not "IPA", and starts with "[" and ends with "]" or ""/
        if result != None:
            language = i
            for r in result:
                if ">[" in str(r) or ">/" in str(r):
                    element = r
                    break
            if element != None:
                break
            
    if result == None or element == None:
        return None
    else:
        result_obj = {
            "element": element,
            "language": language
        }
        return result_obj
    
def get_article_ipa_obj(noun_class, url):
    result = get_ipa_element(url)
    if result == None:
        if noun_class == PI:
            url = url + "_City"
            result = get_ipa_element(url)
            if result == None:
                print(f"Netika atrasts IPA identifikators dotajā šķirklī: {url}")    
                return 0
            else:
                element = result["element"]
                language = result["language"]
                return_obj = {
                    "noun_class": "",
                    "language": language,
                    "gender": "",
                    "raw_ipa_string": str(element), # Vrbt nevajag to str šeit. //vajag jo beautifulsoup
                    "ipa_string": ""   
                }
        
                return return_obj
                
        else: 
            print(f"Netika atrasts IPA identifikators dotajā šķirklī: {url}")    
            return 0
    else:
        element = result["element"]
        language = result["language"]
        return_obj = {
            "noun_class": "",
            "language": language,
            "gender": "",
            "raw_ipa_string": str(element), # Vrbt nevajag to str šeit. //vajag jo beautifulsoup
            "ipa_string": ""   
        }
        
        return return_obj
    


def process_ipa_obj(noun_class, gender, raw_ipa_obj):
    """
    Returns a processed ipa_obj.
    """   
    raw_ipa_obj["noun_class"] = noun_class
    raw_ipa_obj["gender"] = gender
    
    print(raw_ipa_obj["raw_ipa_string"])
    
    if raw_ipa_obj["language"] != "English":
        pattern_brackets = re.compile(r'\[(.*?)\]')
        match = pattern_brackets.search(raw_ipa_obj["raw_ipa_string"])

        if match:
            extracted_text = match.group(1)
            cleaned_text = extracted_text.replace('<span class="wrap"> </span>', ' ')
            raw_ipa_obj["ipa_string"] = cleaned_text
            # print(cleaned_text)
        else:
            # Extract text within nested span tags
            pattern_span = re.compile(r'<span[^>]*>(.*?)</span>')
            matches = pattern_span.findall(raw_ipa_obj["raw_ipa_string"])

            # Filter out only the contents of the inner spans
            span_texts = [match for match in matches if not 'title' in match]

            if span_texts:
                span_text = ''.join(span_texts)
                raw_ipa_obj["ipa_string"] = span_text
                # print(span_text)
                
            else:
                print("No nested ipa_string found with the present regular expression rules.")
        
        return raw_ipa_obj
    
    if raw_ipa_obj["language"] == "English":
        # Define the regex pattern to find content within <span> tags
        pattern_span = re.compile(r'<span[^>]*>(.*?)</span>')
        
        # Search for matches using the regex pattern
        matches = pattern_span.findall(raw_ipa_obj["raw_ipa_string"])
        
        # Process each match to extract text content only
        extracted_text = ''
        for match in matches:
            # Remove any HTML tags and attributes using regex
            clean_match = re.sub(r'<[^>]*>', '', match)
            extracted_text += clean_match
        
        # Update raw_ipa_obj with the extracted IPA string
        raw_ipa_obj["ipa_string"] = extracted_text.strip()
        
        return raw_ipa_obj

main()