import json
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'ipapy-0.0.9')))
from ipapy import UNICODE_TO_IPA
from ipapy import is_valid_ipa
from ipapy.ipachar import IPAConsonant
from ipapy.ipachar import IPAVowel
from ipapy.ipastring import IPAString

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
            "l̩": "l"
        },
        {
            "m": "m"
        },
        {
            "m̩": "m"
        },
        {
            "n": "n"
        },
        {
            "n̩": "n"
        },
        {
            "ŋ": "n"
        },
        {
            "p": "p"
        },
        {
            "pf": "pf"
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
            "eː": "ē"
        },
        {
            "ɪ": "i"
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
            "ʏ": "u"
        },
        {
            "y": "i"
        }
    ],
    "ipa_dipthongs": [
        {
            "aɪ": "ai"
        },
        {
            "aʊ": "au"
        },
        {
            "ɔʏ": "oi"
        }
    ],
    "ipa_reduced_vowels": [
        {
            "ɐ": "a"
        },
        {
            "ər": "ar"
        },
        {
            "ə": "e"
        },
        {
            "ɛ": "e"
        }
    ],
    "ipa_semivowels": [
        {
            "ɐ̯": "a"
        },
        {
            "i̯": "ij"
        },
        {
            "o̯": "o"
        },
        {
            "u̯": "u"
        },
        {
            "y̑": "vi"
        }
    ],
    "ipa_non_native_vowels": [
        {
            "ãː": "ān"
        },
        {
            "ɛ̃ː": "ēn"
        },
        {
            "ɛɪ": "ei"
        },
        {
            "õː": "on"
        },
        {
            "ɔʊ": "ou"
        },
        {
            "œ̃ː": "un"
        },
        {
            "œːɐ̯": "eur"
        }
    ],
    "ipa_vowels": [
        {
            "ã": "an"
        },
        {
            "ɛ̃": "en"
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
            "õ": "on"
        },
        {
            "œ̃": "un"
        },
        {
            "ø": "o"
        },
        {
            "u": "u"
        },
        {
            "y": "i"
        }
    ]
}

# Combine all lists into one
combined_list = []
for key in data:
    combined_list.extend(data[key])

# Iterate over the combined list and print each key-value pair
# for item in combined_list:
#     for key, value in item.items():
#         print(f"Key: {key}, Value: {value}")

for item in combined_list:
    for key, value in item.items():
        char = IPAString(unicode_string=key, ignore=True)
        for c in char:
            print(u"%s\t%s" % (c, c.name))
