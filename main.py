# main.py
import sys
import os

# Add the local library path to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'ipapy-0.0.9')))

from ipa_scraper import IPAScraper
from user_input import UserInput
from ipa_processing import IPAProcessing

from ipapy import UNICODE_TO_IPA
from ipapy import is_valid_ipa
from ipapy.ipachar import IPAConsonant
from ipapy.ipachar import IPAVowel
from ipapy.ipastring import IPAString

def main():
    """
    Main function.
    """

    print("""
 \033[31m██ ██████   █████      ████████ ██████   █████  ███    ██ ███████ ██      ██ ████████ 
 \033[91m██ ██   ██ ██   ██        ██    ██   ██ ██   ██ ████   ██ ██      ██      ██    ██    
 \033[33m██ ██████  ███████ █████  ██    ██████  ███████ ██ ██  ██ ███████ ██      ██    ██    
 \033[32m██ ██      ██   ██        ██    ██   ██ ██   ██ ██  ██ ██      ██ ██      ██    ██    
 \033[94m██ ██      ██   ██        ██    ██   ██ ██   ██ ██   ████ ███████ ███████ ██    ██    
                                                                                        
 \033[0mVeidoja: @paddlebear & @JJeris, 2024                                                                                        
    """)
   
    print("""
 IPA-TRANSLIT ļauj pārveidot ievadītu īpašvārdu angļu valodā uz tā izcelsmes valodas
 IPA simboliem, kuri pēc tam tiek atveidoti latviešu valodā, sekojot latviešu valodas likumam un autoru personīgai interpretācijai. 
 
 Prorgramma ir atkarīga no tā, vai eksistē Wikipedia šķirklis dotajam īpašvārdam. Ja tas tiek ievadīts 
 nepareizi vai dotajā šķirklī neeksistē IPA simboli, tad programma nebūs spējīga parādīt nepieciešamo
 transliterāciju.    
    """)
    
    print("""
 Atbalstītās valodas:
 - "Mandarin",
 - "French", 
 - "Standard German", 
 - "Ukrainian", 
 - "Japanese", 
 - "English".
    """)
    
    
    exit_condition = True
    user_input = UserInput()
    scraper = IPAScraper()
    processing = IPAProcessing()
    
    try:
        while exit_condition:
            proper_noun = user_input.get_proper_noun()
            noun_class = user_input.get_noun_class()
            
            gender = user_input.get_gender() if noun_class == 'pv' else 's'
            sanitized_input = user_input.sanitize_input(proper_noun)
            
            raw_ipa_obj = scraper.get_article_ipa_obj(noun_class, sanitized_input)
            
            if raw_ipa_obj:
                processed_ipa_obj = scraper.process_ipa_obj(noun_class, gender, raw_ipa_obj)
                chars = processed_ipa_obj["ipa_string"]
                print(processed_ipa_obj["language"])
                print(chars)
                
                # charsipa = IPAString(unicode_string="chars")
    
                # for c in charsipa:
                #     print(u"%s          %s" % (c, c.name))
                
                string = processing.ipa_to_array(processed_ipa_obj)
                
                processing.ua_to_lv(chars)
    
            exit_condition = user_input.get_exit_condition()
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        input("Press Enter to exit...")
    
    print("Programma beidzās.")

if __name__ == "__main__":
    main()
