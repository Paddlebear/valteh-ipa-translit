# user_input.py
class UserInput:
    PI = "pi"
    PV = "pv"
    MALE = "v"
    FEMALE = "s"

    def get_proper_noun(self):
        proper_noun = input("Ievadiet izvēlēto īpašvārdu:").strip()
        while not proper_noun:
            print("Nederīga ievade - nevar būt tukša ievade")
            proper_noun = input("Ievadiet izvēlēto īpašvārdu:").strip()
        return proper_noun

    def get_noun_class(self):
        noun_class = input("Vai īpašvārds ir pilsēta vai personvārds? (pi/pv)").strip()
        while noun_class not in [self.PI, self.PV]:
            print("Nederīga izvēle.")
            noun_class = input("Vai īpašvārds ir pilsēta vai personvārds? (pi/pv)").strip()
        return noun_class

    def get_gender(self):
        gender = input("Vai personvārds ir vīrieša vai sievietes? (v/s)").strip()
        while gender not in [self.MALE, self.FEMALE]:
            print("Nederīga izvēle.")
            gender = input("Vai personvārds ir vīrieša vai sievietes? (v/s)").strip()
        return gender

    def sanitize_input(self, input_str):
        return input_str.title().replace(' ', '_')

    def get_exit_condition(self):
        raw_exit_condition = input("Izvēlēties jaunu īpašvārdu? (y/n): ").strip().lower()
        while raw_exit_condition not in ["y", "n"]:
            print("Nederīga ievade! Lūdzu, ievadiet 'y' vai 'n'.")
            raw_exit_condition = input("Izvēlēties jaunu īpašvārdu? (y/n): ").strip().lower()
        return raw_exit_condition == "y"
