# valteh-ipa-translit
Valodu tehnoloģijas - praktiskais darbs "Svešvalodas-IPA-latviešu transliterācija"

oogabooga

pip install requests, beautifulsoup4, ipapy

**the current release for ipapy is broken on a Python release no later than 3.12. To fix this, the library files ipastring.py and mapper.py need to be edited with the following:
from collections.abc import MutableSequence //MutableMapper respectively