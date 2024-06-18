from ipa_scraper import IPAScraper
from data_handler import DataHandler
from notifications import Notifications
from user_input import UserInput

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'ipapy-0.0.9')))
from ipapy import UNICODE_TO_IPA
from ipapy import is_valid_ipa
from ipapy.ipachar import IPAConsonant
from ipapy.ipachar import IPAVowel
from ipapy.ipachar import IPASuprasegmental
from ipapy.ipastring import IPAString

class IPAProcessor:
    #* Prob not needed - if you do, import user_inputs and use the values defined there.
    # PI = "pi"
    # PV = "pv"
    # MALE = "v"
    # FEMALE = "s"
    
    def transform_ipa_to_lv(self, ipa_obj):
        """
        Transforms the ipa_obj>ipa_str into its appropriate
        Latvian language characters.

        Args:
            ipa_obj (JSON): contains the data relating to the
                        user provided proper noun.

        Returns:
            JSON: the ipa_obj with modified fields.
        """        
        notifications = Notifications()
        user_input = UserInput()
        
        # print(user_input.PI)
        
        notifications.output_transforming_ipa_to_lv()
        
        language_ipa_arr = self._get_language_ipa_arr(ipa_obj["language"])
        
        # TODO if language_ipa_arr == none, return error.
        
        ipa_chars = IPAString(unicode_string=ipa_obj["ipa_str"], ignore=True)
        is_added = False
        processed_chars = []
        
        print(language_ipa_arr)
        for c in ipa_chars:
            is_added = False
            for item in language_ipa_arr:
                for key, value in item.items():
                    if key != ":":
                        char = UNICODE_TO_IPA[u"{0}".format(key)]
                    if char == c:
                        processed_chars.append(value)
                        is_added = True
                        break
                    if c.is_equivalent("long suprasegmental"):
                        processed_chars.append(":")
                        is_added = True
                        break
                    if c.is_equivalent("word-break suprasegmental"):
                        processed_chars.append(" ")
                        is_added = True
                        break
                if is_added == True:
                    break
                        
        print(processed_chars)
        print(ipa_chars, type(ipa_chars))
        
        ipa_obj["raw_ipa_to_lv"] = ''.join(processed_chars)
        
        
        #TODO post process the "raw_ipa_to_lv" and place that into "processed_ipa_to_lv"
        
        return ipa_obj
        
        
    def _process_ipa_string_chars(self, language, noun_class, gender, ipa_chars):
        """_summary_

        Args:
            language (_type_): _description_
            noun_class (_type_): _description_
            gender (_type_): _description_
            ipa_chars (_type_): _description_
        """ 
        
        
               
        print()
        
    def _post_process_ipa_to_lv(self, language, noun_class, gender, ipa_chars):
        """_summary_

        Args:
            language (_type_): _description_
            noun_class (_type_): _description_
            gender (_type_): _description_
            ipa_chars (_type_): _description_
        """        
        print()
    
    def _convert_ipa_str_to_array(self, initial_ipa_string):
        """
        Converts ipa string into an appropriate
        array of appropriate ipa characters.

        Args:
            initial_ipa_string (str): the initial ipa string that was
                                    identified from the user inputted 
                                    proper noun.
        Returns:
            str: _description_
        """        
        
        chars = IPAString(unicode_string="")
        ipa_string = IPAString(unicode_string=initial_ipa_string, ignore=True)
        for c in ipa_string:
            chars.append(c)
            
        # TODO does this actually turn into an array, @paddlebear? 
        return chars
        
    def _get_language_ipa_arr(self, language):
        """
        Returns a specific languages ipa json file data
        in a list format for parsing.

        Args:
            language (str): the language, for the user provided
                        proper nouns ipa_string.


        Returns:
            _type_: _description_
        """        
        
        scraper = IPAScraper()
        data_handler = DataHandler()
        ipa_transliteration_arr = []
        
        # https://www.freecodecamp.org/news/python-switch-statement-switch-case-example/
        
        if language == scraper.ACCEPTED_LANGUAGES[0]:
            print(data_handler.IPA_FILE_KEYS[0])
            ipa_transliteration_arr = data_handler.get_ipa_json_file(data_handler.IPA_FILE_KEYS[0])
            
        elif language == scraper.ACCEPTED_LANGUAGES[1]:
            print(data_handler.IPA_FILE_KEYS[1])
            ipa_transliteration_arr = data_handler.get_ipa_json_file(data_handler.IPA_FILE_KEYS[1])
        
        elif language == scraper.ACCEPTED_LANGUAGES[2]:
            print(data_handler.IPA_FILE_KEYS[2])
            ipa_transliteration_arr = data_handler.get_ipa_json_file(data_handler.IPA_FILE_KEYS[2])
            
        elif language == scraper.ACCEPTED_LANGUAGES[3]:
            print(data_handler.IPA_FILE_KEYS[3])
            ipa_transliteration_arr = data_handler.get_ipa_json_file(data_handler.IPA_FILE_KEYS[3])
        
        elif language == scraper.ACCEPTED_LANGUAGES[4]:
            print(data_handler.IPA_FILE_KEYS[4])
            ipa_transliteration_arr = data_handler.get_ipa_json_file(data_handler.IPA_FILE_KEYS[4])

        elif language == scraper.ACCEPTED_LANGUAGES[5]:
            print(data_handler.IPA_FILE_KEYS[5])
            ipa_transliteration_arr = data_handler.get_ipa_json_file(data_handler.IPA_FILE_KEYS[5])
        
        if len(ipa_transliteration_arr) == 0:
            return None

        return ipa_transliteration_arr
       
    
    def ipa_to_array(self, ipa_obj):
        nounclass = ipa_obj["noun_class"]
        noungender = ipa_obj["gender"]
        nounlang = ipa_obj["language"]
        initstring = ipa_obj["ipa_string"]
        
        chars = IPAString(unicode_string="")
        ipastring = IPAString(unicode_string=initstring, ignore=True)
        for c in ipastring:
            chars.append(c)
            
        # print(nounclass)
        # print(noungender)
        # print(nounlang)
        # print(chars)
        # for c in chars:
        #     print(c)
            
        return chars
            
    
    def ch_to_lv(self, chars):
        data = {
            "ipa_consonants": [
                {
                    "ɕ": "šj"
                },
                {
                    "f": "f"
                },
                {
                    "j": "j"
                },
                {
                    "k": "k"
                },
                {
                    "l": "l"
                },
                {
                    "m": "m"
                },
                {
                    "n": "n"
                },
                {
                    "ŋ": "n"
                },
                {
                    "p": "p"
                },
                {
                    "ʐ": "ž"
                },
                {
                    "s": "s"
                },
                {
                    "ʂ": "š"
                },
                {
                    "t": "t"
                },
                {
                    "tɕ": "dzj"
                },
                {
                    "ts": "c"
                },
                {
                    "ʈʂ": "dž"
                },
                {
                    "w": "v"
                },
                {
                    "x": "h"
                },
                {
                    "ɥ": "ju"
                }
            ],
            "ipa_vowels": [
                {
                    "a": "a"
                },
                {
                    "ɑ": "a"
                },
                {
                    "ɛ": "e"
                },
                {
                    "e": "e"
                },
                {
                    "ɪ": "i"
                },
                {
                    "ə": "e"
                },
                {
                    "ɚ": "er"
                },
                {
                    "ɤ": "ē"
                },
                {
                    "i": "i"
                },
                {
                    "o": "o"
                },
                {
                    "u": "u"
                },
                {
                    "ʊ": "o"
                },
                {
                    "y": "i"
                },
                {
                    ":": ":"
                }
            ]
        }
        
        
        ipachars = IPAString(unicode_string=chars, ignore=True)
        
        combined_list = []
        for key in data:
            combined_list.extend(data[key])
            
        isAdded = False
        processchars = []
        for c in ipachars:
            isAdded = False
            for item in combined_list:
                for key, value in item.items():
                    if key != ":":
                        char = UNICODE_TO_IPA[u"{0}".format(key)]
                    if char == c:
                        processchars.append(value)
                        isAdded = True
                        break
                    if c.is_equivalent("long suprasegmental"):
                        processchars.append(":")
                        isAdded = True
                        break
                    if c.is_equivalent("word-break suprasegmental"):
                        processchars.append(" ")
                        isAdded = True
                        break
                if isAdded == True:
                    break
                        
        print(processchars)
        print(ipachars, type(ipachars))
        
    def jp_to_lv(self, chars):
        data = {
                "ipa_consonants": [
                {
                    "b":"b"
                },
                {
                    "ç":"hi"
                },
                {
                    "ɕ":"šj"
                },
                {
                    "d":"d"
                },
                {
                    "dz":"dz"
                },
                {
                    "dʑ":"dž"
                },
                {
                    "ɸ":"f"
                },
                {
                    "ɡ":"g"
                },
                {
                    "h":"hi"
                },
                {
                    "j":"j"
                },
                {
                    "k":"k"
                },
                {
                    "m":"m"
                },
                {
                    "n":"n"
                },
                {
                    "ɲ":"ņ"
                },
                {
                    "ŋ":"n"
                },
                {
                    "ɴ":"n"
                },
                {
                    "p":"p"
                },
                {
                    "ɾ": "r"
                },
                {
                    "s": "s"
                },
                {
                    "t": "t"
                },
                {
                    "tɕ": "č"
                },
                {
                    "ts": "c"
                },
                {
                    "w": "v"
                },
                {
                    "z": "z"
                },
                {
                    "ʑ": "ž"
                },
                {
                    "ʲ": "i"
                }
            ],
            "ipa_vowels": [
                {
                    "a": "a"
                },
                {
                    "e": "e"
                },
                {
                    "i": "i"
                },
                {
                    "o": "o"
                },
                {
                    "ɯ": "u"
                },
                {
                    ":": ":"
                }
            ],
            "ipa_suprasegmentals": [
                {
                    "ː": ""
                },
                {
                    "ꜜ": ""
                },
                {
                    ".": ""
                }
            ]
        }
        
        # stoplist = ["ʰ", "ꜜ", "(", ")"]
        
        # newchars = ""
        # for c in chars:
        #     if c in stoplist:
        #         continue
        #     else: newchars = newchars+c
            
        # print(newchars)
        
        ipachars = IPAString(unicode_string=chars, ignore=True)
        
        print(ipachars, type(ipachars))
        
        combined_list = []
        for key in data:
            combined_list.extend(data[key])
            
        isAdded = False
        processchars = []
        for c in ipachars:
            isAdded = False
            for item in combined_list:
                for key, value in item.items():
                    if key != ":":
                        char = UNICODE_TO_IPA[u"{0}".format(key)]
                    if char == c:
                        processchars.append(value)
                        isAdded = True
                        break
                    if c.is_equivalent("long suprasegmental"):
                        processchars.append(":")
                        isAdded = True
                        break
                    if c.is_equivalent("word-break suprasegmental"):
                        processchars.append(" ")
                        isAdded = True
                        break
                if isAdded == True:
                    break
                        
        print(processchars)
        print(ipachars, type(ipachars))
        
        
    def de_to_lv(self, chars):
        data = {
            "ipa_consonants": [
                {
                    "b": "b"
                },
                {
                    "ç": "h"
                },
                {
                    "d": "d"
                },
                {
                    "f": "f"
                },
                {
                    "ɡ": "g"
                },
                {
                    "h": "h"
                },
                {
                    "j": "j"
                },
                {
                    "k": "k"
                },
                {
                    "l": "l"
                },
                {
                    "m": "m"
                },
                {
                    "n": "n"
                },
                {
                    "ŋ": "n"
                },
                {
                    "p": "p"
                },
                {
                    "r": "r"
                },
                {
                    "ʁ": "r"
                },
                {
                    "s": "s"
                },
                {
                    "ʃ": "š"
                },
                {
                    "t": "t"
                },
                {
                    "ts": "c"
                },
                {
                    "tʃ": "č"
                },
                {
                    "v": "v"
                },
                {
                    "x": "h"
                },
                {
                    "z": "z"
                },
                {
                    "s": "s"
                },
                {
                    "dʒ": "dz"
                },
                {
                    "ð": "t"
                },
                {
                    "ɹ": "r"
                },
                {
                    "θ": "t"
                },
                {
                    "w": "v"
                },
                {
                    "ʒ": "ž"
                }
            ],
            "ipa_monophthongs": [
                {
                    "a": "a"
                },
                {
                    "ɛ": "e"
                },
                {
                    "ɪ": "e"
                },
                {
                    "ɔ": "o"
                },
                {
                    "o": "o"
                },
                {
                    "œ": "o"
                },
                {
                    "ø": "o"
                },
                {
                    "ʊ": "u"
                },
                {
                    "u": "ū"
                },
                {
                    "ʏ": "i"
                },
                {
                    "y": "i"
                }
            ],
            "ipa_reduced_vowels": [
                {
                    "ɐ": "a"
                },
                {
                    "e": "e"
                },
                {
                    "ə": "a"
                },
                {
                    ":": ":"
                }
            ]
        }
        
        ipachars = IPAString(unicode_string=chars, ignore=True)
        
        # print (ipachars)
        # for c in ipachars:
        #     print(c, c.name, type(c))
            
        
        combined_list = []
        for key in data:
            combined_list.extend(data[key])
            
        isAdded = False
        processchars = []
        for c in ipachars:
            isAdded = False
            for item in combined_list:
                for key, value in item.items():
                    if key != ":":
                        char = UNICODE_TO_IPA[u"{0}".format(key)]
                    if char == c:
                        processchars.append(value)
                        isAdded = True
                        break
                    if c.is_equivalent("long suprasegmental"):
                        processchars.append(":")
                        isAdded = True
                        break
                    if c.is_equivalent("word-break suprasegmental"):
                        processchars.append(" ")
                        isAdded = True
                        break
                if isAdded == True:
                    break
                        
        print(processchars)
        print(ipachars, type(ipachars))

    
    def eng_to_lv(self, chars):
        data = {
            "ipa_consonants": [
                {
                    "b": "b"
                },
                {
                    "d": "d"
                },
                {
                    "dʒ": "dž"
                },
                {
                    "ð": "t"
                },
                {
                    "f": "f"
                },
                {
                    "ɡ": "g"
                },
                {
                    "h": "h"
                },
                {
                    "j": "j"
                },
                {
                    "k": "k"
                },
                {
                    "l": "l"
                },
                {
                    "m": "m"
                },
                {
                    "n": "n"
                },
                {
                    "ŋ": "n"
                },
                {
                    "p": "p"
                },
                {
                    "r": "r"
                },
                {
                    "s": "s"
                },
                {
                    "ʃ": "š"
                },
                {
                    "t": "t"
                },
                {
                    "tʃ": "č"
                },
                {
                    "θ": "t"
                },
                {
                    "v": "v"
                },
                {
                    "w": "v"
                },
                {
                    "z": "z"
                },
                {
                    "ʒ": "ž"
                }
            ],
            "ipa_strong_vowels": [
                {
                    "ɑ": "a"
                },
                {
                    "ɒ": "a"
                },
                {
                    "æ": "a"
                },
                {
                    "ɛ": "e"
                },
                {
                    "ɜ": "ē"
                },
                {
                    "e": "e"
                },
                {
                    "ɪ": "e"
                },
                {
                    "i": "i"
                },
                {
                    "ɔ": "o"
                },
                {
                    "o": "o"
                },
                {
                    "ʊ": "u"
                },
                {
                    "u": "u"
                },
                {
                    "ʌ": "a"
                }
            ],
            "ipa_weak_vowels": [
                {
                    "ə": "a"
                },
                {
                    "a": "a"  
                },
                {
                    "i": "i"
                },
                {
                    "u": "u"
                },
                {
                    ":": ":"
                }
            ]
        }
        
        ipachars = IPAString(unicode_string=chars, ignore=True)
        
        # print (ipachars)
        # for c in ipachars:
        #     print(c, c.name, type(c))
            
        
        combined_list = []
        for key in data:
            combined_list.extend(data[key])
            
        isAdded = False
        processchars = []
        for c in ipachars:
            isAdded = False
            for item in combined_list:
                for key, value in item.items():
                    if key != ":":
                        char = UNICODE_TO_IPA[u"{0}".format(key)]
                    if char == c:
                        processchars.append(value)
                        isAdded = True
                        break
                    if c.is_equivalent("long suprasegmental"):
                        processchars.append(":")
                        isAdded = True
                        break
                    if c.is_equivalent("word-break suprasegmental"):
                        processchars.append(" ")
                        isAdded = True
                        break
                if isAdded == True:
                    break
                        
        print(processchars)
        print(ipachars, type(ipachars))
    
    def fr_to_lv(self, chars):
        data = {
            "ipa_consonants": [
                {
                    "b": "b"
                },
                {
                    "d": "d"
                },
                {
                    "f": "f"
                },
                {
                    "ɡ": "g"
                },
                {
                    "k": "k"
                },
                {
                    "l": "l"
                },
                {
                    "m": "m"
                },
                {
                    "n": "n"
                },
                {
                    "ɲ": "ņ"
                },
                {
                    "ŋ": "n"
                },
                {
                    "p": "p"
                },
                {
                    "ʁ": "r"
                },
                {
                    "s": "s"
                },
                {
                    "ʃ": "š"
                },
                {
                    "t": "t"
                },
                {
                    "v": "v"
                },
                {
                    "z": "z"
                },
                {
                    "ʒ": "ž"
                }
            ],
            "ipa_semivowels": [
                {
                    "j": "j"
                },
                {
                    "w": "v"
                },
                {
                    "ɥ": "ju"
                }
            ],
            "ipa_oral_vowels": [
                {
                    "a": "a"
                },
                {
                    "ɑ": "a"
                },
                {
                    "e": "e"
                },
                {
                    "ɛ": "e"
                },
                {
                    "ə": "a"
                },
                {
                    "i": "i"
                },
                {
                    "œ": "o"
                },
                {
                    "ø": "o"
                },
                {
                    "o": "o"
                },
                {
                    "ɔ": "o"
                },
                {
                    "u": "u"
                },
                {
                    "y": "i"
                }
            ],
            "ipa_nasal_vowels": [
                {
                    "ɑ̃": "a"
                },
                {
                    "ɛ̃": "e"
                },
                {
                    "œ̃": "o"
                },
                {
                    "ɔ̃": "o"
                }
            ],
            "ipa_suprasegmentals": [
                {
                    ".": ""
                },
                {
                    "‿": ""
                }
            ]
        }
    
        ipachars = IPAString(unicode_string=chars, ignore=True)
        
        combined_list = []
        for key in data:
            combined_list.extend(data[key])
            
        isAdded = False
        processchars = []
        for c in ipachars:
            isAdded = False
            for item in combined_list:
                for key, value in item.items():
                    if key != ":":
                        char = UNICODE_TO_IPA[u"{0}".format(key)]
                    if char == c:
                        processchars.append(value)
                        isAdded = True
                        break
                    if c.is_equivalent("long suprasegmental"):
                        processchars.append(":")
                        isAdded = True
                        break
                    if c.is_equivalent("word-break suprasegmental"):
                        processchars.append(" ")
                        isAdded = True
                        break
                if isAdded == True:
                    break
                        
        print(processchars)
        print(ipachars, type(ipachars))

    
    def lt_to_lv(self, chars):
        # data = {
        #     "ipa_consonants": [
        #         {
        #             "b": "b"
        #         },
        #         {
        #             "d": "d"
        #         },
        #         {
        #             "dz": "dz"
        #         },
        #         {
        #             "dʒ": "dž"
        #         },
        #         {
        #             "f": "f"
        #         },
        #         {
        #             "ɡ": "g"
        #         },
        #         {
        #             "ɣ": "h"
        #         },
        #         {
        #             "k": "k"
        #         },
        #         {
        #             "j": "j"
        #         },
        #         {
        #             "ɫ": "l"
        #         },
        #         {
        #             "m": "m"
        #         },
        #         {
        #             "n": "n"
        #         },
        #         {
        #             "ŋ": "n"
        #         },
        #         {
        #             "p": "p"
        #         },
        #         {
        #             "r": "r"
        #         },
        #         {
        #             "s": "s"
        #         },
        #         {
        #             "ɕ": "š"
        #         },
        #         {
        #             "ʃ": "š"
        #         },
        #         {
        #             "t": "t"
        #         },
        #         {
        #             "ts": "c"
        #         },
        #         {
        #             "tɕ": "č"
        #         },
        #         {
        #             "tʃ": "č"
        #         },
        #         {
        #             "v": "v"
        #         },
        #         {
        #             "x": "h"
        #         },
        #         {
        #             "z": "z"
        #         },
        #         {
        #             "ʑ": "ž"
        #         },
        #         {
        #             "ʒ": "ž"
        #         },
        #         {
        #             "ʲ": "j"
        #         }
        #     ],
        #     "ipa_vowels": [
        #         {
        #             "a": "a"
        #         },
        #         {
        #             "ɛ": "e"
        #         },
        #         {
        #             "æ": "a"
        #         },
        #         {
        #             "ɐ": "a"
        #         },
        #         {
        #             "e": "e"
        #         },
        #         {
        #             "ɛ": "e"
        #         },
        #         {
        #             "i": "i"
        #         },
        #         {
        #             "ɪ": "i"
        #         },
        #         {
        #             "o": "o"
        #         },
        #         {
        #             "ɔ": "o"
        #         },
        #         {
        #             "u": "u"
        #         },
        #         {
        #             "ʊ": "u"
        #         }
        #     ]
        # }
    
        # ipachars = IPAString(unicode_string=chars)
        
        # for c in ipachars:
        #     print(c, c.name)
        
        # combined_list = []
        # for key in data:
        #     combined_list.extend(data[key])
            
        # isAdded = False
        # processchars = []
        # for c in ipachars:
        #     isAdded = False
        #     for item in combined_list:
        #         for key, value in item.items():
        #             if key != ":":
        #                 char = UNICODE_TO_IPA[u"{0}".format(key)]
        #             if char == c:
        #                 processchars.append(value)
        #                 isAdded = True
        #                 break
        #             if c.is_equivalent("long suprasegmental"):
        #                 processchars.append(":")
        #                 isAdded = True
        #                 break
        #             if c.is_equivalent("word-break suprasegmental"):
        #                 processchars.append(" ")
        #                 isAdded = True
        #                 break
        #         if isAdded == True:
        #             break
                        
        # print(processchars)
        print(chars)
    
    def ua_to_lv(self, chars):
        data = {
            "ipa_hard_consonants": [
                {
                    "b": "b"
                },
                {
                    "d": "d"
                },
                {
                    "dz": "dz"
                },
                {
                    "dʒ": "dž"
                },
                {
                    "f": "f"
                },
                {
                    "ɡ": "g"
                },
                {
                    "ɣ": "h"
                },
                {
                    "ɦ": "h"
                },
                {
                    "k": "k"
                },
                {
                    "l": "l"
                },
                {
                    "m": "m"
                },
                {
                    "n": "n"
                },
                {
                    "p": "p"
                },
                {
                    "r": "r"
                },
                {
                    "s": "s"
                },
                {
                    "ʃ": "š"
                },
                {
                    "t": "t"
                },
                {
                    "ts": "c"
                },
                {
                    "tʃ": "č"
                },
                {
                    "v": "v"
                },
                {
                    "w": "v"
                },
                {
                    "x": "h"
                },
                {
                    "z": "z"
                },
                {
                    "ʒ": "ž"
                }
            ],
            "ipa_vowels": [
                {
                    "ɑ":"a"
                },
                {
                    "ɛ":"e"
                },
                {
                    "i":"i"
                },
                {
                    "ɪ":"i"
                },
                {
                    "ɔ":"o"
                },
                {
                    "u":"u"
                },        
                {
                    "ɐ":"a"
                },
                {
                    "e":"e"
                },
                {
                    "o":"o"
                },
                {
                    "ʊ": "u"
                }
            ],
            "ipa_suprasegmentals": [
                {
                    "ː":""
                }
            ]
        }
        
        ipachars = IPAString(unicode_string=chars, ignore=True)
        
        combined_list = []
        for key in data:
            combined_list.extend(data[key])
            
        isAdded = False
        processchars = []
        for c in ipachars:
            isAdded = False
            for item in combined_list:
                for key, value in item.items():
                    if key != ":":
                        char = UNICODE_TO_IPA[u"{0}".format(key)]
                    if char == c:
                        processchars.append(value)
                        isAdded = True
                        break
                    if c.is_equivalent("long suprasegmental"):
                        processchars.append(":")
                        isAdded = True
                        break
                    if c.is_equivalent("word-break suprasegmental"):
                        processchars.append(" ")
                        isAdded = True
                        break
                if isAdded == True:
                    break
                        
        print(processchars)
        print(ipachars, type(ipachars))