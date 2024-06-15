# print("hello wowld uwu") #@Paddlebear was here UwU
import requests
# import json
import re
from bs4 import BeautifulSoup



ACCEPTED_LANGUAGES = ["French", "Standard German", "Ukrainian", "Japanese",  "English"] # The order is deliberate. #TODO Add Lithuanian, Korean.
PI = "pi" # city proper noun.
PV = "pv" # person proper noun.
MALE = "v" # male gender.
FEMALE = "s" # female gender.

WIKIPEDIA_URL_EN = "https://en.wikipedia.org/wiki/"
HTML_PARSER = "html.parser"
DELIMITERS = ["[", "]", "/"]

def main():
    """
    Main function.
    """
    while True:
        user_input = get_proper_noun()
        noun_class = get_noun_class()
        
        if (noun_class == PV):
            gender = get_gender()
        elif (noun_class == PI):
            gender = FEMALE
            
        sanitized_input = sanitize_input(user_input)
        
        raw_ipa_obj = get_article_ipa_object(generate_proper_noun_wiki_url(sanitized_input))
        
        if raw_ipa_obj != 0:
            processed_ipa_obj = process_ipa_obj(noun_class, gender, raw_ipa_obj)
    
        print(processed_ipa_obj["ipa_string"])
    
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

def get_article_ipa_object(url):
    """
    Scrapes the IPA string from a provided Wikipedia URL.

    Args:
        url (str): url to Wikipedia
    """   
    page = requests.get(url)
    soup = BeautifulSoup(page.content, HTML_PARSER)
    result = None
    language = None
    
    # TODO if city and no IPA is found, attempt to modify the url to end with <city_name>_(city) OR <city_name>_City.
    for i in ACCEPTED_LANGUAGES:
        # TODO consider looking for both title and href.
        result = soup.find(title=f"Help:IPA/{i}")
        if result != None:
            language = i
            break
    
    if result == None:
        print(f"Netika atrasts IPA identifikators dotajā šķirklī: {url}")    
        return 0
    
    else:
        return_obj = {
            "noun_class": "",
            "language": language,
            "gender": "",
            "raw_ipa_string": str(result),
            "ipa_string": ""   
        }
        
        return return_obj

def process_ipa_obj(noun_class, gender, raw_ipa_obj):
    """
    Returns a processed ipa_obj.
    """   
    # TODO find the ipa char list, and update the function so that it returns that list. @Paddlebear :333 
    
    raw_ipa_obj["noun_class"] = noun_class
    raw_ipa_obj["gender"] = gender
    
    # TODO process the .ipa_string to the raw characters?
    # print(raw_ipa_obj["raw_ipa_string"])
    
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

main()