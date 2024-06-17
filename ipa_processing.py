import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'ipapy-0.0.9')))
from ipapy import UNICODE_TO_IPA
from ipapy import is_valid_ipa
from ipapy.ipachar import IPAConsonant
from ipapy.ipachar import IPAVowel
from ipapy.ipachar import IPASuprasegmental
from ipapy.ipastring import IPAString

class IPAProcessing:
    PI = "pi"
    PV = "pv"
    MALE = "v"
    FEMALE = "s"
    
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
                    "ʈʂ": "č"
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
                    "ʊ": "u"
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
                    "æ": "e"
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
                    "ʌ": "o"
                }
            ],
            "ipa_weak_vowels": [
                {
                    "ə": "a"
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
        print("hi")
    
    
    def ua_to_lv(self, chars):
        print("hi")