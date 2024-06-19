from ipa_scraper import IPAScraper
from data_handler import DataHandler
from notifications import Notifications
from user_input import UserInput

import json
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
    """
    Handles IPA processing.
    """    
    
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
        scraper = IPAScraper()
        
        
        language = ipa_obj["language"]
        
        language_ipa_arr = self._get_language_ipa_arr(ipa_obj["language"])
        
        # Major issue, if this happens.
        if language_ipa_arr == None:
            return ipa_obj
        
        ipa_chars = IPAString(unicode_string=ipa_obj["ipa_str"], ignore=True)
        is_added = False
        # Array of processed chars.
        processed_chars = [] 
        
        for c in ipa_chars: ## CHAR MAPPING TO TRANSLIT MAPS
            is_added = False
            for item in language_ipa_arr:
                for key, value in item.items():
                    if key != ":":
                        char = UNICODE_TO_IPA[u"{0}".format(key)]
                    if char == c:
                        processed_chars.append(value)
                        is_added = True
                        break
                    if c.is_equivalent("long suprasegmental"): ##exceptions for : and space because we need them, but UNICODE_TO_IPA can't process
                        processed_chars.append(":")
                        is_added = True
                        break
                    if c.is_equivalent("word-break suprasegmental"):
                        processed_chars.append(" ")
                        is_added = True
                        break
                if is_added == True:
                    break
                        
        processed_chars.append(" ")
        ipa_obj["raw_ipa_to_lv"] = processed_chars
        if language == scraper.ACCEPTED_LANGUAGES[0]: ## switch case - correct function based on language (processing is diff for each lang)
            result_ipa_obj = self.post_ch_to_lv(ipa_obj)
            
        elif language == scraper.ACCEPTED_LANGUAGES[1]:
            result_ipa_obj = self.post_fr_to_lv(ipa_obj)
        
        elif language == scraper.ACCEPTED_LANGUAGES[2]:
            result_ipa_obj = self.post_ua_to_lv(ipa_obj)
            
        elif language == scraper.ACCEPTED_LANGUAGES[3]:
            result_ipa_obj = self.post_jp_to_lv(ipa_obj)
        
        elif language == scraper.ACCEPTED_LANGUAGES[4]:
            result_ipa_obj = self.post_de_to_lv(ipa_obj)

        elif language == scraper.ACCEPTED_LANGUAGES[5]:
            result_ipa_obj = self.post_eng_to_lv(ipa_obj)
        
        else: 
            print("unknown error, contact developers")
        
        return result_ipa_obj
        
    def _get_language_ipa_arr(self, language): # GET CORRECT TRANSLIT MAP
        """
        Returns a specific languages ipa json file data
        in a list format for parsing.

        Args:
            language (str): the language, for the user provided
                        proper nouns ipa_string.


        Returns:
            Array: array of transliteration map.
        """        
        
        scraper = IPAScraper()
        data_handler = DataHandler()
        ipa_transliteration_arr = []
        
        # https://www.freecodecamp.org/news/python-switch-statement-switch-case-example/
        
        if language == scraper.ACCEPTED_LANGUAGES[0]: #switch based on language
            # print(data_handler.IPA_FILE_KEYS[0])
            ipa_transliteration_arr = data_handler.get_ipa_json_file(data_handler.IPA_FILE_KEYS[0])
            
        elif language == scraper.ACCEPTED_LANGUAGES[1]:
            # print(data_handler.IPA_FILE_KEYS[1])
            ipa_transliteration_arr = data_handler.get_ipa_json_file(data_handler.IPA_FILE_KEYS[1])
        
        elif language == scraper.ACCEPTED_LANGUAGES[2]:
            # print(data_handler.IPA_FILE_KEYS[2])
            ipa_transliteration_arr = data_handler.get_ipa_json_file(data_handler.IPA_FILE_KEYS[2])
            
        elif language == scraper.ACCEPTED_LANGUAGES[3]:
            # print(data_handler.IPA_FILE_KEYS[3])
            ipa_transliteration_arr = data_handler.get_ipa_json_file(data_handler.IPA_FILE_KEYS[3])
        
        elif language == scraper.ACCEPTED_LANGUAGES[4]:
            # print(data_handler.IPA_FILE_KEYS[4])
            ipa_transliteration_arr = data_handler.get_ipa_json_file(data_handler.IPA_FILE_KEYS[4])

        elif language == scraper.ACCEPTED_LANGUAGES[5]:
            # print(data_handler.IPA_FILE_KEYS[5])
            ipa_transliteration_arr = data_handler.get_ipa_json_file(data_handler.IPA_FILE_KEYS[5])
        
        if len(ipa_transliteration_arr) == 0:
            return None

        return ipa_transliteration_arr 
    
    def post_ch_to_lv(self, ipa_obj): ## MANDARIN
        """
        Post-processing of basic transliterated IPA-LV string - Mandarin.

        Args:
            ipa_obj (JSON): contains the data relating to the
                        user provided proper noun.
        Returns:
            JSON: the ipa_obj with modified fields.
        """        
        # Create a copy to the raw_ipa_to_lv.
        array = ipa_obj["raw_ipa_to_lv"][:]
        gender = ipa_obj["gender"]
        noun_class = ipa_obj["noun_class"]
        i = 0
        while i < len(array): ## STRING CLEANUP ACCORDING TO RULES
            if array[i] == "^": # aspirated consonants - the little h is replaced by ^ in the mapping
                if array[i-1] == "dz":
                    array[i-1] = "c"
                if array[i-1] == "dž":
                    array[i-1] = "č"
                if array[i-1] == "dzj":
                    array[i-1] = "cj"
                del array[i]
                i = i-1
            if array[i] == "j": # consonant merging/deleting of extra j
                if array[i-1] == "l" or array[i-1] == "n" or array[i-1] == "cj" or array[i-1] == "dzj":
                    if array[i-1] == "l":
                        array[i-1] = "ļ"
                    if array[i-1] == "n":
                        array[i-1] = "ņ"
                    del array[i]
                    i = i-1
            if array[i] == " ": ##deletion of i in dipthongs ai, ei, oi, ui - in each case the ending becomes ajs, ejs, ojs, ujs and the respective ones for female gender
                if i-2 >= 0:
                    if (array[i-2] == "a" or array[i-2] == "e" or array[i-2] == "o" or array[i-2] == "u") and array[i-1] == "i":
                        del array[i-1]
                        i = i-1
            i = i+1
        
        i = 0
        while i < len(array): ## NAME ENDINGS
            if array[i] == ".": #delete syllable delimiter - was necessary so that ..n.j... doesn't become ņ, but stays two sep syllables
                del array[i]
                i = i-1
            if array[i] == " ":
                if (array[i-1] == "a" or array[i-1] == "e" or array[i-1] == "o") and array[i-2] != "a" and array[i-2] != "e" and array[i-2] != "i" and array[i-2] != "u" and array[i-2] != "o":
                    if gender == UserInput.MALE: # if a, e, o, except a bunch of dipthongs like ao
                        array.insert(i, "js")
                        i = i+1
                    else:
                        array.insert(i, "ja")
                        i = i+1
                elif array[i-1] != "u": # u never gets an ending
                    if gender == UserInput.MALE:
                        if array[i-1] != "i": # i also never gets an ending
                            array.insert(i, "s")
                            i = i+1
                    else:
                        if array[i-1] != "i":
                            array.insert(i, "a")
                            i = i+1
                    
            i = i+1
            
        ipa_obj["processed_ipa_to_lv"] = "".join(array).title() # capitalize
        return ipa_obj
        
    def post_de_to_lv(self, ipa_obj): ## STANDARD GERMAN
        """
        Post-processing of basic transliterated IPA-LV string - Standard German.

        Args:
            ipa_obj (JSON): contains the data relating to the
                        user provided proper noun.
        Returns:
            JSON: the ipa_obj with modified fields.
        """  
        # Create a copy to the raw_ipa_to_lv.
        array = ipa_obj["raw_ipa_to_lv"][:]
        gender = ipa_obj["gender"]
        noun_class = ipa_obj["noun_class"]
        ## STRING CLEANUP ACCORDING TO RULES
        i = 0
        while i < len(array):
            if array[i] == "dž" and array[i+1] == " ": #left over from ukr processing, useful if slav name shows up
                array[i] = "č"
            if array[i] == "j":
                if i != 0 and array[i-1] == "n": # consonant merge
                    if array[i+1] == "i" or array[i+1] == "a" or array[i+1] == "o" or array[i+1] == "u" or array[i+1] == "e" or array[i+1] == "j" or array[i+1] == " ":
                        array[i-1] = "ņ"
                elif i != 0 and array[i-1] == "l": # consonant merge
                    if array[i+1] == "i" or array[i+1] == "a" or array[i+1] == "o" or array[i+1] == "u" or array[i+1] == "e" or array[i+1] == "j" or array[i+1] == "v" or array[i+1]==" ":
                        array[i-1] = "ļ"
                
                if (i != 0 and array[i-1] != "i" and array[i-1] != " " and array[i-1] != "u" and array[i-1] != "o" and array[i-1] != "e" and array[i-1] != "a" and array[i-1] != "v" and array[i-1] != "t"):
                    del array[i] #if in front of a consonant that is not v or t, delete (also delete if merged)
                    
            if i != 0 and (array[i] == "n" or array[i] == "m"):
                if array[i-1] != "a" and array[i-1] != "e" and array[i-1] != "i" and array[i-1] != "o" and array[i-1] != "u" and array[i-1] != "l" and array[i-1] != "n" and array[i-1] != "m" and array[i-1] != " " and array[i-1] != "t":
                    array.insert(i, "e") ## so consonant clusters like pm, kn, fm etc. get separated
                    i = i+1
            if i != 0 and (array[i] == "l"):
                if array[i-1] != "a" and array[i-1] != "e" and array[i-1] != "i" and array[i-1] != "o" and array[i-1] != "u" and array[i-1] != "l" and array[i-1] != "n" and array[i-1] != "m" and array[i-1] != " " and array[i-1] != "f":
                    array.insert(i, "e") ## so consonant clusters like pl, kl, tl etc. get separated
                    i = i+1
            if array[i] == ":": # doubling of n
                if array[i-1] == "n":
                    array[i] = array[i-1]
            if array[i] == "er": # doubling of l before er
                if array[i-1] == "l":
                    array.insert(i, "l")
                    i = i+1
            if array[i] == ":": # long vowels except before more vowels
                if array[i+1] != "i" and array[i+1] != "e" and array[i+1] != "a" and array[i+1] != "u" and array[i+1] != "o":
                    if array[i-1] == "a":
                        array[i-1] = "ā"
                    if array[i-1] == "e":
                        array[i-1] = "ē"
                    if array[i-1] == "i":
                        array[i-1] = "ī"
                    if array[i-1] == "u":
                        array[i-1] = "ū"
                if array[i+1] == "er": #if er after long vowel, change er to r
                    array[i+1] = "r"
                del array[i]
            if (array[i] == ":" and gender == UserInput.FEMALE): # leftover from ukr proc, leave alone
                if array[i-1] == "č" or array[i-1] == "š" or array[i-1] == "ž":
                    array[i] = "j"
            if array[i] == "t" and array[i+1] == "v": #in LV translit, tv becomes dv
                array[i] = "d"
            if array[i] == " ": #end part of word
                if array[i-1] == "k": #voiced g except after vowels
                    if array[i-2] != "a" and array[i-2] != "e" and array[i-2] != "i" and array[i-2] != "o" and array[i-2] != "u":
                        array[i-1] = "g"
                if array[i-1] == "t": # voiced t except after r and s
                    if array[i-2] != "r" and array[i-2] != "s":
                        array[i-1] = "d"
                if array[i-1] == "h" and (array[i-2] == "i" or array[i-2] == "e" or array[i-2] == "a" or array[i-2] == "u" or array[i-2] == "o") and array[i-3] != "r":
                    array[i-1] = "g" #ig, eg, ag... except after r (rih)
                if array[i-2] == "a" and array[i-1] == "r":
                    array[i-2] = "e" # schwa handling
            if array[i] == " " and i+1 < len(array) and noun_class == UserInput.PI:
                del array[i] #concat city name
            i = i+1
            
        ## NAME ENDINGS
        
        i = 0
        while i < len(array):
            if array[i] == " ":
                if (array[i-3] == "n" or array[i-3] == "l" or array[i-3] == "ņ" or array[i-3] == "ļ" or array[i-3] == "g") and array[i-2] == "i" and array[i-1] == "j":
                    if(gender == UserInput.MALE): #leftover from ukr, leave alone
                        array.insert(i, "s")
                    else: array.insert(i,"a")
                    i = i+1
                elif array[i-2] == "i" and array[i-1] == "j": #leftover from ukr, leave alone
                    if(gender == UserInput.MALE):
                        array[i-1] = "s"
                    elif (gender == UserInput.FEMALE): 
                        array[i-1] = "a"
                        del array[i-2]
                    i = i+1
                else:
                    if (array[i-2] == "i" or array[i-2] == "e" or array[i-2] == "a" or array[i-2] == "o") and array[i-1] == "a":
                        array.insert(i-1, "j") #separate ia, oa, ea, aa
                        i = i+1
                    if (gender == UserInput.MALE): # if declinable, add ending
                        if (array[i-1] != "o" and array[i-1] != "e"):
                            array.insert(i, "s")
                            i = i+1
                    else: 
                        if array[i-2] == "a" and array[i-1] == "u": ##ua female handling
                            array.insert(i,"a")
                            i = i+1
                        if array[i-1] != "a" and array[i-1] != "e" and array[i-1] != "o" and array[i-1] != "i" and array[i-1] != "ē" and array[i-1] != "u" and array[i-1] != "ū": #if declinable
                            if array[i-1] == "l" or array[i-1] == "n" or array[i-1] == "t" or array[i-1] == "d" or array[i-1] == "er" or array[i-1] == "r":
                                array.insert(i, "e") # a except after a bunch of exceptions
                            else: array.insert(i,"a")
                            i = i+1
                        if array[i-1] == "i": # ija handling
                            array.insert(i, "ja")
                            i = i+1
            if i != 0 and array[i] == "er" and (array[i-1] == "i" or array[i-1] == "e" or array[i-1] == "a" or array[i-1] == "u" or array[i-1] == "o"):
                    array[i] = "r" #handles aer, ier, eer, uer, oer
            if i != 0 and array[i] == "e" and array[i-1] =="a":
                    array[i] = "i" # ae -> ai                
            i = i+1
            
        ipa_obj["processed_ipa_to_lv"] = "".join(array).title()
        return ipa_obj
        
    def post_eng_to_lv(self, ipa_obj): ## ENGLISH
        """
        Post-processing of basic transliterated IPA-LV string - English.

        Args:
            ipa_obj (JSON): contains the data relating to the
                        user provided proper noun.
        Returns:
            JSON: the ipa_obj with modified fields.
        """  
        # Create a copy to the raw_ipa_to_lv.
        array = ipa_obj["raw_ipa_to_lv"][:]
        gender = ipa_obj["gender"]
        noun_class = ipa_obj["noun_class"]

        ## STRING CLEANUP ACCORDING TO RULES
        i = 0
        while i < len(array):
            if array[0] == "o" and array[1] == "u": # ou at start -> o
                del array[1]
                i = i-1
            if array[i] == "dž" and array[i+1] == " ": #leftover from ukr
                array[i] = "č"
            if array[i] == "j":
                if i != 0 and array[i-1] == "n": #consonant merge
                    if array[i+1] == "i" or array[i+1] == "a" or array[i+1] == "o" or array[i+1] == "u" or array[i+1] == "e" or array[i+1] == "j" or array[i+1] == " ":
                        array[i-1] = "ņ"
                elif i != 0 and array[i-1] == "l": #consonant merge
                    if array[i+1] == "i" or array[i+1] == "a" or array[i+1] == "o" or array[i+1] == "u" or array[i+1] == "e" or array[i+1] == "j" or array[i+1] == "v" or array[i+1]==" ":
                        array[i-1] = "ļ"
                
                if (i != 0 and array[i-1] != "i" and array[i-1] != " " and array[i-1] != "u" and array[i-1] != "o" and array[i-1] != "e" and array[i-1] != "a" and array[i-1] != "v" and array[i-1] != "t"):
                    del array[i] #delete j if no vowel
                    
            if array[i] == ":": #lengthen n
                if array[i-1] == "n":
                    array[i] = array[i-1]
            if array[i] == "er": #double l before er
                if array[i-1] == "l":
                    array.insert(i, "l")
                    i = i+1
            if array[i] == "i" and array[i+1] == "e" and array[i+2] == "i":
                del array[i+2] #take care of vowel i and diphthong ei sequentially - leave just ie
            if array[i] == ":":
                if array[i+1] != "i" and array[i+1] != "e" and array[i+1] != "a" and array[i+1] != "u" and array[i+1] != "o":
                    if array[i-1] == "a":
                        array[i-1] = "ā" #long vowel a and i (no other long vowel is transliterated)
                    if array[i-1] == "i":
                        array[i-1] = "ī"
                if array[i+1] == "er": #if er before vowel, er -> r
                    array[i+1] = "r"
                del array[i] #delete long vowel marker
                i = i-1
            if (array[i] == ":" and gender == UserInput.FEMALE): #leftover from ukr 
                if array[i-1] == "č" or array[i-1] == "š" or array[i-1] == "ž":
                    array[i] = "j" 
            if array[i] == " ": #schwa handling
                if array[i-2] == "a" and (array[i-1] == "r" or array[i-1] == "m" or array[i-1] == "n" or array[i-1] == "t"): #
                    array[i-2] = "e" # er, em, en, et
                if array[i-2] == "a" and (array[i-1] == "l"):
                    array[i-2] = "o" # ol
                if i+1 < len(array): #ou at beginning of next word -> o
                    if array[i+1] == "o" and array[i+2] == "u":
                        del array[i+2]
            if array[i] == " " and i+1 < len(array) and noun_class == UserInput.PI: #concat city name
                del array[i]
            i = i+1
            
        ## NAME ENDINGS
        
        i = 0
        while i < len(array):
            if array[i] == " ": #leftover from ukr
                if (array[i-3] == "n" or array[i-3] == "l" or array[i-3] == "ņ" or array[i-3] == "ļ" or array[i-3] == "g") and array[i-2] == "i" and array[i-1] == "j":
                    if(gender == UserInput.MALE):
                        array.insert(i, "s")
                    else: array.insert(i,"a")
                    i = i+1
                elif array[i-2] == "i" and array[i-1] == "j": #leftover from ukr
                    if(gender == UserInput.MALE):
                        array[i-1] = "s"
                    elif (gender == UserInput.FEMALE): 

                        array[i-1] = "a"
                        del array[i-2]
                        # i = i-1
                    i = i+1
                elif array[i-2] == "o" and array[i-1] == "u": #ou at end -> o
                    del array[i-1]
                    i = i-1
                else:
                    if (array[i-2] == "i" or array[i-2] == "e" or array[i-2] == "a" or array[i-2] == "o") and array[i-1] == "a":
                        array.insert(i-1, "j") #separate vowels in ending
                        i = i+1
                    if (gender == UserInput.MALE):
                        if (array[i-1] != "a" and array[i-1] != "e" and array[i-1] != "o" and array[i-1] != "i" and array[i-1] != "ē" and array[i-1] != "u" and array[i-1] != "ū" and array[i-1] != "ā" and array[i-1] != "ī"):
                            array.insert(i, "s") #if declinable
                            i = i+1
                        elif (array[i-1] == "i"): #except if i, then js
                            array.insert(i, "js")
                            i = i+1
                    else: 
                        if array[i-2] == "a" and array[i-1] == "u": #leftover from de
                            array.insert(i,"a")
                            i = i+1
                        if array[i-1] != "a" and array[i-1] != "e" and array[i-1] != "o" and array[i-1] != "i" and array[i-1] != "ē" and array[i-1] != "u" and array[i-1] != "ū":
                            if array[i-2] == "e" and array[i-1] == "l": # if declinable and if el at end -> ele
                                array.insert(i, "e")
                                i = i+1
                            else:
                                array.insert(i,"a") #else if declinable
                                i = i+1
                        if array[i-1] == "i":
                            array.insert(i, "ja")
                            i = i+1
            if i != 0 and array[i] == "er" and (array[i-1] == "i" or array[i-1] == "e" or array[i-1] == "a" or array[i-1] == "u" or array[i-1] == "o"):
                    array[i] = "r" #er after vowel -> r
            if i != 0 and array[i] == "e" and array[i-1] =="a":
                    array[i] = "i" # ae -> ai             
            i = i+1
        ipa_obj["processed_ipa_to_lv"] = "".join(array).title()
        return ipa_obj
        
    def post_fr_to_lv(self, ipa_obj): ## FRENCH
        """
        Post-processing of basic transliterated IPA-LV string - French.

        Args:
            ipa_obj (JSON): contains the data relating to the
                        user provided proper noun.
        Returns:
            JSON: the ipa_obj with modified fields.
        """  
        # Create a copy to the raw_ipa_to_lv.
        array = ipa_obj["raw_ipa_to_lv"][:]
        gender = ipa_obj["gender"]
        noun_class = ipa_obj["noun_class"]

        ## STRING CLEANUP ACCORDING TO RULES
        i = 0
        while i < len(array):
            if array[i] == "j":
                if i != 0 and array[i-1] == "n": # consonant merge
                    if array[i+1] == "i" or array[i+1] == "a" or array[i+1] == "o" or array[i+1] == "u" or array[i+1] == "e" or array[i+1] == "j" or array[i+1] == " ":
                        array[i] = "i"
                elif i != 0 and array[i-1] == "l": # consonant merge
                    if array[i+1] == "i" or array[i+1] == "a" or array[i+1] == "o" or array[i+1] == "j" or array[i+1] == "v" or array[i+1]==" ":
                        array[i] = "i"
            if array[i] == ":": # double n
                if array[i-1] == "n":
                    array[i] = array[i-1]
            if (array[i] == ":" and gender == UserInput.FEMALE): #leftover from ukr
                if array[i-1] == "č" or array[i-1] == "š" or array[i-1] == "ž":
                    array[i] = "j"
            if array[i] == ":": #long vowels, delete delim after
                if array[i-1] == "a":
                    array[i-1] = "ā"
                if array[i-1] == "e":
                    array[i-1] = "ē"
                if array[i-1] == "i":
                    array[i-1] = "ī"
                if array[i-1] == "u":
                    array[i-1] = "ū"
                del array[i]
            if (array[i] == " "):
                if (array[i-1] == "l" and gender == UserInput.FEMALE):
                    array.insert(i-1, array[i-1]) #double l at end if female
                    i = i+1
                if (array[i-1] == "i"): #don't end work with i, make it ijs/ija
                    array.insert(i, "j")
                    i = i+1
                if i+2 < len(array) and array[i+1] == "g" and array[i+2] == "z": #gz transliterated as unvoiced
                    array[i+1] = "k"
                    array[i+2] = "s"
            if array[i] == " " and i+1 < len(array) and noun_class == UserInput.PI: #concat city names
                del array[i]
            i = i+1
            
        ## NAME ENDINGS
        
        i = 0
        while i < len(array):
            if array[i] == " ": #long vowels in a lot of exceptions
                if array[i-2] == "u" and array[i-1] !="a":
                    array[i-2] = "ū"
                if array[i-2] == "a" and array[i-1] == "r":
                    array[i-2] = "ā"
                if array[i-2] == "a" and array[i-1] == "n" and (array[i-3] =="e" or array[i-3] =="u"):
                    array[i-2] = "ā"
                if array[i-1] == "a" and (array[i-2] == "u" or array[i-2] == "e"):
                    array[i-1] = "ā"
                if array[i-1] == "e":
                    array[i-1] = "ē"
                if array[i-2] == "e" and (array[i-1] == "r" or array[i-1] == "n"):
                    array[i-2] = "ē"
                if (gender == UserInput.MALE):
                    if (array[i-1] != "o" and array[i-1] != "e" and array[i-1] != "i" and array[i-1] != "ē" and array[i-1] != "u" and array[i-1] != "ū" and array[i-1] != "a" and array[i-1] != "ā"):
                        array.insert(i, "s") #if declinable
                        i = i+1
                else: 
                    if array[i-1] != "a" and array[i-1] != "ā" and array[i-1] != "e" and array[i-1] != "o" and array[i-1] != "i" and array[i-1] != "ē" and array[i-1] != "u" and array[i-1] != "ū":
                        if array[i-1] == "l" or array[i-1] == "t": #if declinable and le or te
                            array.insert(i, "e")
                        else: array.insert(i,"a") #else if declinable
                        i = i+1              
            i = i+1
        ipa_obj["processed_ipa_to_lv"] = "".join(array).title()
        return ipa_obj
        
    def post_jp_to_lv(self, ipa_obj): ## JAPANESE
        """
        Post-processing of basic transliterated IPA-LV string - Japanese.

        Args:
            ipa_obj (JSON): contains the data relating to the
                        user provided proper noun.
        Returns:
            JSON: the ipa_obj with modified fields.
        """  
        # Create a copy to the raw_ipa_to_lv.
        array = ipa_obj["raw_ipa_to_lv"][:]
        gender = ipa_obj["gender"]
        noun_class = ipa_obj["noun_class"]

        i = 0
        while i < len(array): ## STRING CLEANUP ACCORDING TO RULES
            # print(array[i])
            if array[i] == "j": # consonant merge, then delete j
                if array[i-1] == "l" or array[i-1] == "n" or array[i-1] == "cj" or array[i-1] == "dzj":
                    if array[i-1] == "l":
                        array[i-1] = "ļ"
                    if array[i-1] == "n":
                        array[i-1] = "ņ"
                    del array[i]
                    i = i-1
            if array[i] == "i": # take care of doubled i (ii -> i)
                if i-1 >= 0:
                    if array[i-1] == "hi" or array[i-1] == "i":
                        del array[i]
                        i = i-1
            if array[i] == ":": # ignore all long vowels (historical LV translit)
                del array[i]
                i = i-1
            i = i+1
        
        i = 0
        while i < len(array): ## NAME ENDINGS
            if array[i] == ".": #remove syllable delim
                del array[i]
                i = i-1
            if array[i] == " ":
                if array[i-1] != "a" and array[i-1] != "e" and array[i-1] != "i" and array[i-1] != "o" and array[i-1] != "u": #if ending is not vowel (really if ending is n because no other possibilities)
                    if gender == UserInput.MALE:
                        array.insert(i, "s")
                        i = i+1
                    else:
                        array.insert(i, "a")
                        i = i+1
                    
            i = i+1
            
        ipa_obj["processed_ipa_to_lv"] = "".join(array).title()
        return ipa_obj
        
    def post_ua_to_lv(self, ipa_obj): ## UKRAINIAN
        """
        Post-processing of basic transliterated IPA-LV string - Ukrainian.

        Args:
            ipa_obj (JSON): contains the data relating to the
                        user provided proper noun.
        Returns:
            JSON: the ipa_obj with modified fields.
        """  
        # Create a copy to the raw_ipa_to_lv.
        array = ipa_obj["raw_ipa_to_lv"][:]
        gender = ipa_obj["gender"]
        noun_class = ipa_obj["noun_class"]

        ## STRING CLEANUP ACCORDING TO RULES
        i = 0
        while i < len(array):
            if array[i] == "dž" and array[i+1] == " ": #things like ič, so not left as idž
                array[i] = "č"
            if array[i] == "j": 
                if i != 0 and array[i-1] == "n":  # consonant merge
                    if array[i+1] == "i" or array[i+1] == "a" or array[i+1] == "o" or array[i+1] == "u" or array[i+1] == "e" or array[i+1] == "j" or array[i+1] == " ":
                        array[i-1] = "ņ"
                elif i != 0 and array[i-1] == "l": # consonant merge
                    if array[i+1] == "i" or array[i+1] == "a" or array[i+1] == "o" or array[i+1] == "u" or array[i+1] == "e" or array[i+1] == "j" or array[i+1] == "v" or array[i+1]==" ":
                        array[i-1] = "ļ"
                
                if (i != 0 and array[i-1] != "i" and array[i-1] != " " and array[i-1] != "u" and array[i-1] != "o" and array[i-1] != "e" and array[i-1] != "a" and array[i-1] != "v" and array[i-1] != "t"):
                    del array[i] #delete j after
            if array[i] == ":": #double n
                if array[i-1] == "n":
                    array[i] = array[i-1]
            if (array[i] == ":" and gender == UserInput.FEMALE):
                if array[i-1] == "č" or array[i-1] == "š" or array[i-1] == "ž": #if fricatives indicated as long in female name (žia -> žja)
                    array[i] = "j"
            if array[i] == " " and i+1 < len(array) and noun_class == UserInput.PI:
                del array[i] #concat city name
            if array[i] == " ": #sergijs, but riha (g = g in gi, g = h in ih)
                if array[i-2] == "i" and array[i-1] == "g":
                    array[i-1] = "h"
            i = i+1
        ## NAME ENDINGS
        
        i = 0
        while i < len(array):
            if array[i] == " ": #nijs, ņijs, ļijs, gijs etc
                if (array[i-3] == "n" or array[i-3] == "l" or array[i-3] == "ņ" or array[i-3] == "ļ" or array[i-3] == "g") and array[i-2] == "i" and array[i-1] == "j":
                    if(gender == UserInput.MALE):
                        array.insert(i, "s")
                    else: array.insert(i,"a")
                    i = i+1
                elif array[i-2] == "i" and array[i-1] == "j": #skij -> skis, ska
                    if(gender == UserInput.MALE):
                        array[i-1] = "s"
                    elif (gender == UserInput.FEMALE): 
                        array[i-1] = "a"
                        del array[i-2]
                        # i = i-1
                    i = i+1
                else:
                    if (gender == UserInput.MALE):
                        if (array[i-1] != "o" and array[i-1] != "e"):
                            array.insert(i, "s") #if declinable
                            i = i+1
                    else: 
                        if array[i-1] != "a" and array[i-1] != "e" and array[i-1] != "o" and array[i-1] != "i":
                            array.insert(i,"a") #if declinable
                            i = i+1              
            i = i+1
        ipa_obj["processed_ipa_to_lv"] = "".join(array).title()
        return ipa_obj
    