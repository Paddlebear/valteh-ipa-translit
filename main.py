# print("hello wowld uwu") #@Paddlebear was here UwU
WIKIPEDIA_URL_EN = "https://en.wikipedia.org/wiki/"
ACCEPTED_LANGUAGES = ["English", "Spanish", "Japanese", "French", "Ukrainian"]

def main():
    """
    Main function.
    """
    user_input = get_input()
    generate_proper_noun_wiki_url(user_input)
    # scrape_ipa()

def get_input():
    proper_noun = str(input("Enter proper noun:"))
    return proper_noun

    
def sanitize_input():
    # TODO Agneses job :3
    print("uwu")

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