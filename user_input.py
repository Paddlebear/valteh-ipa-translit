# user_input.py
class UserInput:
    """
    Handles user inputs.    
    """        
    PI = "pi"
    PV = "pv"
    
    MALE = "v"
    FEMALE = "s"
    
    POSITIVE_EXIT_CONDITION = "y"
    NEGATIVE_EXIT_CONDITION = "n"

    def get_proper_noun(self):
        """
        Gets the user inputted `proper noun`.

        Returns:
            string: the user provided proper noun, not sanitized.
        """        
        
        proper_noun = input("\nIevadiet īpašvārdu (pilsētu vai personas vārdu):").strip()
        while not proper_noun:
            proper_noun = input("Nederīga ievade - nevar būt tukša ievade!\nIevadiet īpašvārdu (pilsētu vai personas vārdu):").strip()
        return self._sanitize_proper_noun(proper_noun)

    def get_noun_class(self):
        """
        Gets the user inputted `noun_class`

        Returns:
            str: the `proper_noun` class.
        """     
           
        noun_class = input("\nVai īpašvārds ir pilsēta vai personvārds? ({0}/{1}):".format(self.PI, self.PV)).strip()
        while noun_class not in [self.PI, self.PV]:
            noun_class = input("Nederīga izvēle - jāizvēlas `{0}` vai `{1}`!\nVai īpašvārds ir pilsēta vai personvārds? ({0}/{1}):".format(self.PI, self.PV)).strip()
        return noun_class

    def get_gender(self):
        """
        Get the gender for the provided `proper_noun`
        if its for a person and not a city.

        Returns:
            str: the `proper_noun`'s gender.
        """        
        
        gender = input("\nVai personvārds ir vīrieša vai sievietes? ({0}/{1}):".format(self.MALE, self.FEMALE)).strip()
        while gender not in [self.MALE, self.FEMALE]:
            gender = input("Nederīga izvēle - jāizvēlas `{0}` vai `{1}`!\nVai personvārds ir vīrieša vai sievietes? ({0}/{1}):".format(self.MALE, self.FEMALE)).strip()
        return gender

    def get_exit_condition(self):
        """
        Gets the user inputted `exit_condition`,
        that decern the continuation of the program.
        
        Returns:
            str: the `exit_condition` value.
        """        
        
        raw_exit_condition = input("\nTurpināt programmu? ({0}/{1}):".format(self.POSITIVE_EXIT_CONDITION, self.NEGATIVE_EXIT_CONDITION)).strip().lower()
        while raw_exit_condition not in [self.POSITIVE_EXIT_CONDITION, self.NEGATIVE_EXIT_CONDITION]:
            raw_exit_condition = input("Nederīga izvēle - jāizvēlas `{0}` vai `{1}`!\nTurpināt programmu? ({0}/{1}):".format(self.POSITIVE_EXIT_CONDITION, self.NEGATIVE_EXIT_CONDITION)).strip().lower()
        return raw_exit_condition == self.POSITIVE_EXIT_CONDITION

    def _sanitize_proper_noun(self, proper_noun):
        """
        Sanitizes the user provided proper noun, 
        lowercasing all letters and uppercase the first letter 
        for each individual word.
        
        Args:
            proper_noun (str): the user provided proper noun, not sanitized.

        Returns:
            str: the user provided proper noun, sanitized.
        """        
        
        return proper_noun.lower().title().replace(' ', '_')
    