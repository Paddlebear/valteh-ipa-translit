ipapy
=====

**ipapy** is a Python module to work with International Phonetic
Alphabet (IPA) strings.

-  Version: 0.0.9
-  Date: 2019-05-05
-  Developer: `Alberto Pettarin <http://www.albertopettarin.it/>`__
-  License: the MIT License (MIT)
-  Contact: `click here <http://www.albertopettarin.it/contact.html>`__
-  Links: `GitHub <https://github.com/pettarin/ipapy>`__ -
   `PyPI <https://pypi.python.org/pypi/ipapy>`__

Installation
------------

.. code:: bash

   $ pip install ipapy

or

.. code:: bash

   $ git clone https://github.com/pettarin/ipapy.git
   $ cd ipapy

Usage
-----

As A Python Module
~~~~~~~~~~~~~~~~~~

.. code:: python

   ###########
   # IMPORTS #
   ###########
   from ipapy import UNICODE_TO_IPA
   from ipapy import is_valid_ipa
   from ipapy.ipachar import IPAConsonant
   from ipapy.ipachar import IPAVowel
   from ipapy.ipastring import IPAString


   ###########
   # IPAChar #
   ###########

   # Def.: an IPAChar is an IPA letter or diacritic/suprasegmental/tone mark

   # create IPAChar from its Unicode representation
   c1 = UNICODE_TO_IPA[u"a"]                   # vowel open front unrounded
   c2 = UNICODE_TO_IPA[u"e"]                   # vowel close-mid front unrounded
   c3 = UNICODE_TO_IPA[u"\u03B2"]              # consonant voiced bilabial non-sibilant-fricative
   tS1 = UNICODE_TO_IPA[u"t͡ʃ"]                 # consonant voiceless palato-alveolar sibilant-affricate
   tS2 = UNICODE_TO_IPA[u"t͜ʃ"]                 # consonant voiceless palato-alveolar sibilant-affricate
   tS3 = UNICODE_TO_IPA[u"tʃ"]                 # consonant voiceless palato-alveolar sibilant-affricate
   tS4 = UNICODE_TO_IPA[u"ʧ"]                  # consonant voiceless palato-alveolar sibilant-affricate
   tS5 = UNICODE_TO_IPA[u"\u0074\u0361\u0283"] # consonant voiceless palato-alveolar sibilant-affricate
   tS6 = UNICODE_TO_IPA[u"\u0074\u035C\u0283"] # consonant voiceless palato-alveolar sibilant-affricate
   tS7 = UNICODE_TO_IPA[u"\u0074\u0283"]       # consonant voiceless palato-alveolar sibilant-affricate
   tS8 = UNICODE_TO_IPA[u"\u02A7"]             # consonant voiceless palato-alveolar sibilant-affricate
   c1 == c2    # False
   c1 == c3    # False
   c1 == tS1   # False
   tS1 == tS2  # True (they both point to the same IPAChar object)
   tS1 == tS3  # True (idem)
   tS1 == tS4  # True (idem)
   tS1 == tS5  # True (idem)
   tS1 == tS6  # True (idem)
   tS1 == tS7  # True (idem)
   tS1 == tS8  # True (idem)

   # create custom IPAChars
   my_a1 = IPAVowel(name="my_a_1", descriptors=u"open front unrounded", unicode_repr=u"a")
   my_a2 = IPAVowel(name="my_a_2", descriptors=[u"open", "front", "unrounded"], unicode_repr=u"a")
   my_a3 = IPAVowel(name="my_a_3", height=u"open", backness=u"front", roundness=u"unrounded", unicode_repr=u"a")
   my_a4 = IPAVowel(name="my_a_4", descriptors=[u"low", u"fnt", "unr"], unicode_repr=u"a")
   my_ee = IPAVowel(name="my_e_1", descriptors=u"close-mid front unrounded", unicode_repr=u"e")
   my_b1 = IPAConsonant(name="bilabial fricative", descriptors=u"voiced bilabial non-sibilant-fricative", unicode_repr=u"\u03B2")
   my_b2 = IPAConsonant(name="bf", voicing=u"voiced", place=u"bilabial", manner=u"non-sibilant-fricative", unicode_repr=u"\u03B2")
   my_tS = IPAConsonant(name="tS", voicing=u"voiceless", place=u"palato-alveolar", manner=u"sibilant-affricate", unicode_repr=u"t͡ʃ")
   my_a1 == my_a2                  # False (two different objects)
   my_a1 == c1                     # False (two different objects)
   my_a1 == UNICODE_TO_IPA["a"]    # False (two different objects)

   # associate non-standard Unicode representation
   my_aa = IPAVowel(name="a special", descriptors=[u"low", u"fnt", u"unr"], unicode_repr=u"a{*}")
   print(my_aa)    # "a{*}"

   # equality vs. equivalence
   my_tS == tS1                # False (my_tS is a different object than tS1)
   my_tS.is_equivalent(tS1)    # True  (my_tS is equivalent to tS1...)
   tS1.is_equivalent(my_tS)    # True  (... and vice versa)

   # compare IPAChar objects
   my_a1.is_equivalent(my_a2)  # True
   my_a1.is_equivalent(my_a3)  # True
   my_a1.is_equivalent(my_a4)  # True
   my_a1.is_equivalent(my_ee)  # False
   my_a1.is_equivalent(my_b1)  # False
   my_b1.is_equivalent(my_b2)  # True
   my_b1.is_equivalent(my_tS)  # False

   # compare IPAChar and a Unicode string
   my_b1.is_equivalent(u"\u03B2")  # True
   my_b1.is_equivalent(u"β")       # True
   my_b1.is_equivalent(u"b")       # False
   my_tS.is_equivalent(u"tS")      # False
   my_tS.is_equivalent(u"tʃ")      # False (missing the combining diacritic)
   my_tS.is_equivalent(u"t͡ʃ")      # True (has combining diacritic)

   # compare IPAChar and a string listing descriptors
   my_a1.is_equivalent(u"open front unrounded")                                # False (missing 'vowel')
   my_a1.is_equivalent(u"open front unrounded vowel")                          # True
   my_a1.is_equivalent(u"low fnt unr vwl")                                     # True (known abbreviations are good as well)
   my_ee.is_equivalent(u"open front unrounded vowel")                          # False
   my_b1.is_equivalent(u"voiced bilabial non-sibilant-fricative")              # False (missing 'consonant')
   my_b1.is_equivalent(u"voiced bilabial non-sibilant-fricative consonant")    # True
   my_b1.is_equivalent(u"consonant non-sibilant-fricative bilabial voiced")    # True (the order does not matter)
   my_b1.is_equivalent(u"consonant non-sibilant-fricative bilabial voiceless") # False

   # compare IPAChar and list of descriptors
   my_a1.is_equivalent([u"open", u"front", u"unrounded"])              # False
   my_a1.is_equivalent([u"vowel", u"open", u"front", u"unrounded"])    # True
   my_a1.is_equivalent([u"open", u"unrounded", u"vowel", u"front"])    # True
   my_a1.is_equivalent([u"low", u"fnt", u"unr", u"vwl"])               # True


   #############
   # IPAString #
   #############

   # Def.: an IPAString is a list of IPAChar objects

   # check if Unicode string contains only IPA valid characters
   s_uni = u"əˈkiːn æˌkænˈθɑ.lə.d͡ʒi"   # Unicode string of the IPA pronunciation for "achene acanthology"
   is_valid_ipa(s_uni)                 # True
   is_valid_ipa(u"LoL")                # False (uppercase letter L is not IPA valid)

   # create IPAString from list of IPAChar objects
   new_s_ipa = IPAString(ipa_chars=[c3, c2, tS1, c1])

   # create IPAString from Unicode string
   s_ipa = IPAString(unicode_string=s_uni)

   # IPAString is similar to regular Python string object
   print(s_ipa)                            # "əˈkiːn æˌkænˈθɑ.lə.d͡ʒi"
   len(s_ipa)                              # 21
   s_ipa[0]                                # (first IPA char)
   s_ipa[5:8]                              # (6th, 7th, 8th IPA chars)
   s_ipa[19:]                              # (IPA chars from the 20th)
   s_ipa[-1]                               # (last IPA char)
   len(new_s_ipa)                          # 4
   new_s_ipa.append(UNICODE_TO_IPA[u"a"])  # (append IPA char "a")
   len(new_s_ipa)                          # 5
   new_s_ipa.append(UNICODE_TO_IPA[u"t͡ʃ"]) # (append IPA char "t͡ʃ")
   len(new_s_ipa)                          # 6
   new_s_ipa.extend(s_ipa)                 # (append s_ipa to new_s_ipa)
   len(new_s_ipa)                          # 27
   double = s_ipa + new_s_ipa              # (concatenate s_ipa and new_s_ipa)
   len(double)                             # 48

   # new IPAString objects containing only...
   print(s_ipa.consonants)                 # "knknθld͡ʒ"                (consonants)
   print(s_ipa.vowels)                     # "əiææɑəi"                 (vowels)
   print(s_ipa.letters)                    # "əkinækænθɑləd͡ʒi"         (vowels and consonants)
   print(s_ipa.cns_vwl)                    # "əkinækænθɑləd͡ʒi"         (vowels and consonants)
   print(s_ipa.cns_vwl_pstr)               # "əˈkinækænˈθɑləd͡ʒi"       (  + primary stress marks)
   print(s_ipa.cns_vwl_pstr_long)          # "əˈkiːnækænˈθɑləd͡ʒi"      (    + long marks)
   print(s_ipa.cns_vwl_str)                # "əˈkinæˌkænˈθɑləd͡ʒi"      (  + stress marks)
   print(s_ipa.cns_vwl_str_len)            # "əˈkiːnæˌkænˈθɑləd͡ʒi"     (    + length marks)
   print(s_ipa.cns_vwl_str_len_wb)         # "əˈkiːn æˌkænˈθɑləd͡ʒi"    (      + word breaks)
   print(s_ipa.cns_vwl_str_len_wb_sb)      # "əˈkiːn æˌkænˈθɑ.lə.d͡ʒi"  (        + syllable breaks)
   cns = s_ipa.consonants                  # (store new IPA string)
   cns == s_ipa.consonants                 # False (two different objects)
   cns.is_equivalent(s_ipa.consonants)     # True
   cns.is_equivalent(s_ipa)                # False

   # print representation and name of all IPAChar objects in IPAString
   for c in s_ipa:
       print(u"%s\t%s" % (c, c.name))
   # ə vowel mid central unrounded
   # ˈ suprasegmental primary-stress
   # k consonant voiceless velar plosive
   # i vowel close front unrounded
   # ː suprasegmental long
   # n consonant voiced alveolar nasal
   #   suprasegmental word-break
   # æ vowel near-open front unrounded
   # ˌ suprasegmental secondary-stress
   # k consonant voiceless velar plosive
   # æ vowel near-open front unrounded
   # n consonant voiced alveolar nasal
   # ˈ suprasegmental primary-stress
   # θ consonant voiceless dental non-sibilant-fricative
   # ɑ vowel open back unrounded
   # . suprasegmental syllable-break
   # l consonant voiced alveolar lateral-approximant
   # ə vowel mid central unrounded
   # . suprasegmental syllable-break
   # d͡ʒ   consonant voiced palato-alveolar sibilant-affricate
   # i vowel close front unrounded

   # compare IPAString objects
   s_ipa_d = IPAString(unicode_string=u"diff")
   s_ipa_1 = IPAString(unicode_string=u"at͡ʃe")
   s_ipa_2 = IPAString(unicode_string=u"aʧe")
   s_ipa_3 = IPAString(unicode_string=u"at͡ʃe", single_char_parsing=True)
   s_ipa_d == s_ipa_1              # False
   s_ipa_1 == s_ipa_2              # False (different objects)
   s_ipa_1 == s_ipa_3              # False (different objects)
   s_ipa_2 == s_ipa_3              # False (different objects)
   s_ipa_d.is_equivalent(s_ipa_1)  # False
   s_ipa_1.is_equivalent(s_ipa_2)  # True
   s_ipa_2.is_equivalent(s_ipa_1)  # True
   s_ipa_1.is_equivalent(s_ipa_3)  # True
   s_ipa_2.is_equivalent(s_ipa_3)  # True

   # compare IPAString and list of IPAChar objects
   s_ipa_1.is_equivalent([my_a1, my_tS, my_ee])    # True

   # compare IPAString and Unicode string
   s_ipa_d.is_equivalent(u"diff")                  # True
   s_ipa_1.is_equivalent(u"atse")                  # False
   s_ipa_1.is_equivalent(u"atSe")                  # False
   s_ipa_1.is_equivalent(u"at͡ʃe")                  # True
   s_ipa_1.is_equivalent(u"at͜ʃe")                  # True
   s_ipa_1.is_equivalent(u"aʧe")                   # True
   s_ipa_1.is_equivalent(u"at͡ʃeLOL", ignore=True)  # True (ignore chars non IPA valid)
   s_ipa_1.is_equivalent(u"at͡ʃeLoL", ignore=True)  # False (ignore chars non IPA valid, note extra "o")


   ########################
   # CONVERSION FUNCTIONS #
   ########################
   from ipapy.kirshenbaummapper import KirshenbaumMapper
   kmapper = KirshenbaumMapper()                                    # mapper to Kirshenbaum ASCII IPA
   s_k_ipa = kmapper.map_ipa_string(s_ipa)                          # u"@'ki:n#&,k&n'TA#l@#dZi"
   s_k_uni = kmapper.map_unicode_string(s_uni)                      # u"@'ki:n#&,k&n'TA#l@#dZi"
   s_k_ipa == s_k_uni                                               # True
   s_k_lis = kmapper.map_unicode_string(s_uni, return_as_list=True) # [u'@', u"'", u'k', u'i', u':', u'n', u'#', u'&', u',', u'k', u'&', u'n', u"'", u'T', u'A', u'#', u'l', u'@', u'#', u'dZ', u'i']

   from ipapy.arpabetmapper import ARPABETMapper
   amapper = ARPABETMapper()                                                    # mapper to ARPABET ASCII IPA (stress marks not supported yet)
   s_a = amapper.map_unicode_string(u"pɹuːf")                                   # error: long suprasegmental not mapped
   s_a = amapper.map_unicode_string(u"pɹuːf", ignore=True)                      # u"PRUWF"
   s_a = amapper.map_unicode_string(u"pɹuːf", ignore=True, return_as_list=True) # [u'P', u'R', u'UW', u'F']

As A Command Line Tool
~~~~~~~~~~~~~~~~~~~~~~

**ipapy** comes with a command line tool to perform operations on a
given Unicode UTF-8 encoded string, representing an IPA string.
Therefore, it is recommended to run it on a shell supporting UTF-8.

Currently, the supported operations are:

-  ``canonize``: canonize the Unicode representation of the IPA string
-  ``chars``: list all IPA characters appearing in the IPA string
-  ``check``: check if the given Unicode string is IPA valid
-  ``clean``: remove characters that are not IPA valid
-  ``u2a``: print the corresponding ARPABET (ASCII IPA) string
-  ``u2k``: print the corresponding Kirshenbaum (ASCII IPA) string

Run with the ``--help`` parameter to list all the available options:

.. code:: bash

   $ python -m ipapy --help

   usage: __main__.py [-h] [-i] [-p] [--separator [SEPARATOR]] [-s] [-u]
                      command string

   ipapy perform a command on the given IPA/Unicode string

   positional arguments:
     command               [canonize|chars|check|clean|u2a|u2k]
     string                String to canonize, check, clean, or convert

   optional arguments:
     -h, --help            show this help message and exit
     -i, --ignore          Ignore Unicode characters that are not IPA valid
     -p, --print-invalid   Print Unicode characters that are not IPA valid
     --separator [SEPARATOR]
                           Print IPA chars separated by this character (default:
                           '')
     -s, --single-char-parsing
                           Perform single character parsing instead of maximal
                           parsing
     -u, --unicode         Print each Unicode character that is not IPA valid
                           with its Unicode codepoint and name

Examples:

.. code:: bash

   $ python -m ipapy canonize "eʧiu"
   et͡ʃiu

   $ python -m ipapy canonize "eʧiu" --separator " "
   e t͡ʃ i u

   $ python -m ipapy chars "eʧiu"
   'e' vowel close-mid front unrounded (U+0065)
   't͡ʃ'   consonant voiceless palato-alveolar sibilant-affricate (U+0074 U+0361 U+0283)
   'i' vowel close front unrounded (U+0069)
   'u' vowel close back rounded (U+0075)

   $ python -m ipapy chars "et͡ʃiu"
   'e' vowel close-mid front unrounded (U+0065)
   't͡ʃ'   consonant voiceless palato-alveolar sibilant-affricate (U+0074 U+0361 U+0283)
   'i' vowel close front unrounded (U+0069)
   'u' vowel close back rounded (U+0075)

   $ python -m ipapy chars "et͡ʃiu" -s
   'e' vowel close-mid front unrounded (U+0065)
   't' consonant voiceless alveolar plosive (U+0074)
   '͡' diacritic tie-bar-above (U+0361)
   'ʃ' consonant voiceless palato-alveolar sibilant-fricative (U+0283)
   'i' vowel close front unrounded (U+0069)
   'u' vowel close back rounded (U+0075)

   $ python -m ipapy check "eʧiu"
   True

   $ python -m ipapy check "LoL"
   False

   $ python -m ipapy check "LoL" -p
   False
   LL

   $ python -m ipapy check "LoLOL" -p -u
   False
   LLOL
   'L' 0x4c    LATIN CAPITAL LETTER L
   'O' 0x4f    LATIN CAPITAL LETTER O

   $ python -m ipapy clean "/eʧiu/"
   eʧiu

   $ python -m ipapy u2k "eʧiu"
   etSiu

   $ python -m ipapy u2k "eTa"
   The given string contains characters not IPA valid. Use the 'ignore' option to ignore them.

   $ python -m ipapy u2k "eTa" -i
   ea

   $ python -m ipapy u2a "eʧiu" --separator " "
   EH CH IH UW

Unit Testing
------------

.. code:: bash

   $ python run_all_unit_tests.py

License
-------

**ipapy** is released under the MIT License.

Acknowledgments
---------------

-  Bram Vanroy provided a fix to ``setup.py`` for Windows users
