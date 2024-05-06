# print("hello wowld uwu") #@Paddlebear was here UwU
WIKIPEDIA_URL_EN = "https://en.wikipedia.org/wiki/"
ACCEPTED_LANGUAGES = ["English", "Spanish", "Japanese", "French", "Ukrainian"]
PI = "pi"
PV = "pv"
MALE = "v"
FEMALE = "s"

def main():
    """
    Main function.
    """
    user_input = get_input()
    noun_class = get_noun_class()
    if (noun_class == PV):
        gender = get_gender()
    elif (noun_class == PI):
        gender = FEMALE
    sanitized_input = sanitize_input(user_input)
    generate_proper_noun_wiki_url(sanitized_input)
    # scrape_ipa()

def get_input():
    proper_noun = str(input("Enter proper noun:"))
    return proper_noun

def get_noun_class():
    noun_class = str(input("Vai īpašvārds ir pilsēta vai personvārds? (pi/pv)"))
    while (noun_class != PI and noun_class != PV):
        print("Nederīga izvēle.")
        noun_class = str(input("Vai īpašvārds ir pilsēta vai personvārds? (pi/pv)"))
    return noun_class
    
def get_gender():
    gender = str(input("Vai personvārds ir vīrieša vai sievietes? (v/s)"))
    while (gender != MALE and gender != FEMALE):
        print("Nederīga izvēle.")
        gender = str(input("Vai personvārds ir vīrieša vai sievietes? (v/s)"))
    return gender
    
def sanitize_input(input):
    input = input.title()
    input = input.replace(' ', '_')
    return input

def generate_proper_noun_wiki_url(proper_noun):
    print(f"{WIKIPEDIA_URL_EN}{proper_noun}")

def scrape_ipa(url) -> str:
    """
    Scrapes the IPA string from a provided Wikipedia URL

    Args:
        url (str): url to Wikipedia
    """   
    return url



main()