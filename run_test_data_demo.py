# run_test_data_demo.py
from notifications import Notifications
from ipa_scraper import IPAScraper
from user_input import UserInput
from ipa_processor import IPAProcessor
from data_handler import DataHandler


def main():
    """
    Executes the app passing it test data,
    handling output to the user.
    """
    notifications = Notifications()
    data_handler = DataHandler()
    ipa_scraper = IPAScraper()
    ipa_processor = IPAProcessor()
    json_data = None
    
    notifications.output_test_demo_alert()
    for i in data_handler.TEST_FILE_KEYS:
        notifications.output_delimiter()
        json_data = data_handler.get_test_json_file(i)
        for key, value in json_data.items():
            for sub_key, sub_value in value.items():
                if isinstance(sub_value, list):
                    print()
                    for item in sub_value:
                        raw_ipa_string_result = None
                        ipa_string_result = None
                        

                        ipa_obj = ipa_scraper.get_ipa_object(item, json_data[key]["noun_class"], json_data[key]["gender"])
                        # If no IPA string was found.
                        if ipa_obj["ipa_str"] != None:
                            ipa_obj = ipa_processor.transform_ipa_to_lv(ipa_obj)
                                    
                        ipa_string_result = ipa_obj["processed_ipa_to_lv"]
                        
                        if ipa_obj["raw_ipa_to_lv"] != None:
                            if len(ipa_obj["raw_ipa_to_lv"]) > 0: 
                                raw_ipa_string_result = "".join(ipa_obj["raw_ipa_to_lv"])
                        # -> {raw_ipa_string_result}
                        print(f"{item} -> {ipa_obj["ipa_str"]}  -> {ipa_string_result} : {ipa_obj["language"]}")
                        
                              
                    print("\n")
                else:
                    print(f"{sub_key}: {sub_value}")
    
    print("END DEMO")
    
main()