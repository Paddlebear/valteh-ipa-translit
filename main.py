# print("hello wowld uwu") #@Paddlebear was here UwU
import requests
from bs4 import BeautifulSoup

ACCEPTED_LANGUAGES = ["French", "Spanish", "Ukrainian", "Japanese",  "English"] # The order is deliberate.
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
    user_input = get_proper_noun()
    noun_class = get_noun_class()
    if (noun_class == PV):
        gender = get_gender()
    elif (noun_class == PI):
        gender = FEMALE
    sanitized_input = sanitize_input(user_input)
    raw_ipa_obj = get_article_ipa_object(generate_proper_noun_wiki_url(sanitized_input))
    if raw_ipa_obj[1] == None:
        return 0
    get_ipa_list(raw_ipa_obj)

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
    """_summary_

    Args:
        input (_type_): _description_

    Returns:
        _type_: _description_
    """    
    input = input.title()
    input = input.replace(' ', '_')
    return input

def generate_proper_noun_wiki_url(proper_noun):
    """_summary_

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
        result = soup.find(title=f"Help:IPA/{i}") # TODO make this into a loop that checks for the ACCEPTED_LANGUAGEs @JJeris 333:
        if result != None:
            language = i
            break
    if result == None:
        print(f"Netika atrasts IPA identifikators dotajā šķirklī: {url}")
    return [language, result]

def get_ipa_list(raw_ipa_obj):
    """
    Returns the IPA from `page` based on the `language` found in `ACCEPTED_LANGUAGES`.

    Args:
        page (str): filtered html object that should contain IPA chars.
        language (str): the language of the spcific page

    Returns:
        _type_: _description_
    """   
    # TODO find the ipa char list, and update the function so that i returns that list. @Paddlebear :333 
    print(raw_ipa_obj)
    return None

main()