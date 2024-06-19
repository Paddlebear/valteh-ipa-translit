# main.py
from notifications import Notifications
from ipa_scraper import IPAScraper
from user_input import UserInput
from ipa_processor import IPAProcessor

def main():
    """
    Executes the main part of the app,
    handling output to the user.
    """
    
    # Instancing classes
    notifications = Notifications()
    user_input = UserInput()
    scraper = IPAScraper()
    processor = IPAProcessor()
    exit_condition = True
    
    try:
        notifications.output_signature()
        notifications.output_guide()
        
        while exit_condition:
            proper_noun = None
            noun_class = None
            gender = None
            # Get user input.
            proper_noun = user_input.get_proper_noun()
            noun_class = user_input.get_noun_class()
            # All cities will be female gender, so only need to check the gender
            # for person proper nouns.
            if (noun_class == user_input.PV):
                gender = user_input.get_gender()    
            else:
                gender = user_input.FEMALE    
            
            notifications.output_delimiter()
            notifications.output_retrieving_ipa_from_wiki()
            # Get the IPA string and its related data with web scraping and the user inputs.
            ipa_obj = scraper.get_ipa_object(proper_noun, noun_class, gender)
          
            notifications.print_ipa_obj(ipa_obj)
            
            # If no IPA string was found.
            if ipa_obj["ipa_str"] == None:
                notifications.output_delimiter()
                notifications.output_no_ipa_string_found(ipa_obj["wiki_url_to_proper_noun"])
            # If an IPA string was found in the wiki article.
            else:
                notifications.output_delimiter()
                # Transforms the scaped IPA string to the Latvian language.
                notifications.output_transforming_ipa_to_lv()
                ipa_obj = processor.transform_ipa_to_lv(ipa_obj)
                notifications.print_ipa_obj(ipa_obj)
                
            exit_condition = user_input.get_exit_condition()
            notifications.output_delimiter()
            
    except Exception as e:
        notifications.output_delimiter()
        print(f"Error: {str(e)}")
        input("Press Enter to exit...")
    
    print("END PROGRAM")

if __name__ == "__main__":
    main()
