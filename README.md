# valteh-ipa-translit
Valodu tehnoloģijas - praktiskais darbs "Svešvalodas-IPA-latviešu transliterācija"

oogabooga

```
 ██ ██████   █████      ████████ ██████   █████  ███    ██ ███████ ██      ██ ████████ 
 ██ ██   ██ ██   ██        ██    ██   ██ ██   ██ ████   ██ ██      ██      ██    ██    
 ██ ██████  ███████ █████  ██    ██████  ███████ ██ ██  ██ ███████ ██      ██    ██    
 ██ ██      ██   ██        ██    ██   ██ ██   ██ ██  ██ ██      ██ ██      ██    ██    
 ██ ██      ██   ██        ██    ██   ██ ██   ██ ██   ████ ███████ ███████ ██    ██ 
```

## Local Set Up

pip install requests, beautifulsoup4, ipapy

**the current release for ipapy is broken on a Python release no later than 3.12. To fix this, the library files ipastring.py and mapper.py need to be edited with the following:
from collections.abc import MutableSequence //MutableMapper respectively

### Build

pyinstaller --onefile --paths=./ipapy-0.0.9 main.py

## You can also choose to use the releases

You can navigate to the releases page, where you'll be able to download a Windows executable, that was created via GitHub actions.

## ipapy 0.0.9

The project used the ipapy library version 0.0.9 as part of the projects code, since the pip available version has a bug, that needed to be fixed.

The library is under MIT. We give credit for the provided code to its original creators: add names here.

## Why not use hfst?

The project wast made using windows machines, and the hfst and hfst_dev are only runnable in UNIX systems. We decided to create a custom solution for 