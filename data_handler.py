from ipa_scraper import IPAScraper

import json
from pathlib import Path

class DataHandler:
    """
    Handles data retrieval.
    """
    
    IPA_JSON_DIRECTORY_PATH = "ipa_lang_maps\\modified_maps"
    TEST_JSON_DIRECTORY_PATH = "test_data"
    IPA_FILE_KEYS = [
        "zh_lv.json",
        "fr_lv.json",
        "ua_lv.json",
        "jp_lv.json",
        "de_lv.json",
        "eng_lv.json",
        ]    
    TEST_FILE_KEYS = [
        "zh.json",
        "fr.json",
        "de.json",
        "ua.json",
        "jp.json",
        "eng.json",
        ]

    def get_ipa_json_file(self, ipa_file_key):
        """
        Reads in the ipa data and and returns it.

        Args:
            language (_type_): _description_
        """        
        json_file_path = Path(self.IPA_JSON_DIRECTORY_PATH) / ipa_file_key
        json_data = None

        # Read the JSON file
        with json_file_path.open('r', encoding='utf-8') as file:
            json_data = json.load(file)

        if json_data == None:
            return None

        return self._convert_json_keys_to_array(json_data)   
    
    def get_test_json_file(self, test_file_key):
        """
        Reads in the test data and and returns it.
        
        Args:
            language (_type_): _description_
        """        
        
        # TODO read in one of the test data and return it as an array
        json_file_path = Path(self.TEST_JSON_DIRECTORY_PATH) / test_file_key
        json_data = None

        # Read the JSON file
        with json_file_path.open('r', encoding='utf-8') as file:
            json_data = json.load(file)

        if json_data == None:
            return None
        
        return json_data
        
    def _convert_json_keys_to_array(self, json_data):
        """
        Converts a JSON files first level
        contained arrays into a combined array.

        Args:
            json_data (JSOn): ipa json file data, containing
                            the transliteration from <language> ipa 
                            to the Latvian language.                        
        Returns:
            list: a combined list containing all of the key:value pairs.
        """        
        
        combined_list = []
        for key in json_data:
            combined_list.extend(json_data[key])
        return combined_list
        
        
    