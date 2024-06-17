# notifications.py

class Notifications:
    """
    Notification class, that handles outputting cosmetic 
    and informative notifications to the user.
    """    
    
    def output_signature(self):
        """
        Outputs the trademark ASCII art.
        """
        
        print("""
 \033[31m██ ██████   █████      ████████ ██████   █████  ███    ██ ███████ ██      ██ ████████ 
 \033[91m██ ██   ██ ██   ██        ██    ██   ██ ██   ██ ████   ██ ██      ██      ██    ██    
 \033[33m██ ██████  ███████ █████  ██    ██████  ███████ ██ ██  ██ ███████ ██      ██    ██    
 \033[32m██ ██      ██   ██        ██    ██   ██ ██   ██ ██  ██ ██      ██ ██      ██    ██    
 \033[94m██ ██      ██   ██        ██    ██   ██ ██   ██ ██   ████ ███████ ███████ ██    ██                                                                                  
 \033[0mVeidoja: @paddlebear & @JJeris, 2024                                                                                        
        """)
        
    def output_guide(self):
        """
        Outputs the guide.
        """    
    
        print("""
 IPA-TRANSLIT ļauj pārveidot ievadītu īpašvārdu angļu valodā uz tā izcelsmes valodas
 IPA simboliem, kuri pēc tam tiek atveidoti latviešu valodā, sekojot latviešu valodas likumam un autoru personīgai interpretācijai. 
 
 Prorgramma ir atkarīga no tā, vai eksistē Wikipedia šķirklis dotajam īpašvārdam. Ja tas tiek ievadīts 
 nepareizi vai dotajā šķirklī neeksistē IPA simboli, tad programma nebūs spējīga parādīt nepieciešamo
 transliterāciju.    
 
 Atbalstītās valodas:
 - "Mandarin",
 - "French", 
 - "Standard German", 
 - "Ukrainian", 
 - "Japanese", 
 - "English".
        """)
        
    def output_delimiter(self):
        """
        Output a delimiter.
        """        
        
        print("\n\n###-###-###-###-###-###-###-###-###\n")
        
    def output_no_ipa_string_found(self, wiki_url):
        """
        Output a `no ipa string found`.
        """
                
        print("Netika atrasts IPA identifikators dotajā šķirklī: {0}\n".format(wiki_url))
