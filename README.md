```
 ██ ██████   █████      ████████ ██████   █████  ███    ██ ███████ ██      ██ ████████ 
 ██ ██   ██ ██   ██        ██    ██   ██ ██   ██ ████   ██ ██      ██      ██    ██    
 ██ ██████  ███████ █████  ██    ██████  ███████ ██ ██  ██ ███████ ██      ██    ██    
 ██ ██      ██   ██        ██    ██   ██ ██   ██ ██  ██ ██      ██ ██      ██    ██    
 ██ ██      ██   ██        ██    ██   ██ ██   ██ ██   ████ ███████ ███████ ██    ██ 

"Svešvalodas-IPA-latviešu transliterācija" project for LU `Valodu tehnoloģijas` 2024 course.
```


## Local Set Up

### Python

You will need to have Python installed. The project was built using Python `3.12.3`, but any modern Python version will probably work as well.

### PIP Modules

The app uses web scraping to retrieve the IPA string from Wikipedia articles, and as such needs to both web scrape the the page and then find the IPA string with regex.

Run:
- `pip install requests`,
- `pip install beautifulsoup4`.

### [ipapy0.0.9](https://github.com/pettarin/ipapy)

The current release for `ipapy` is broken on a Python release no later than 3.12., and so cannot be installed and used through pip - it should be uninstalled, to avoid any further issues related to imports.

To use `ipapy`, the library files `ipastring.py` and `mapper.py` need to be edited with the following: `from collections.abc import MutableSequence //MutableMapper` respectively.

Alternatively follow this [issue](https://github.com/pettarin/ipapy/pull/6/files).

We use `ipapy0.0.9` source code as part of the project's code - the library is under MIT license and we give full credit for the libraries code to its original creators: [Alberto Pettarin](https://github.com/pettarin)  and [Bram Vanroy](https://github.com/BramVanroy).

## How to run?

In your terminal you can either run the main program, via:
- `python __main__.py`

Alternatively you can run a DEMO for the currently supported languages using the test data in the `test_data` directory, via
- `python run_test_data_demo.py`

## How does it work?

The program takes in the user inputted `proper noun`, `noun_class` and `gender`. 

The input should be in English, for example:
- timothee chalamet,
- angela merkel
- riga
- tokyo

The inputted proper noun will be sanitized, and used as the end part to the url leading to a Wikipedia article detailing the person or city. You can always input the actual ending for the URL that you want to scrape, but the input sanitizing function might get in the way of that.

The article is then scraped for an IPA string, based on an accepted language list, with a deliberate oder: `["Mandarin", "French", "Ukrainian", "Japanese", "Standard German", "English"]`. If no IPA is found, the program ends its iteration.

If an IPA string is found, it is then transformed to the Latvian language using the ipa maps in the `ipa_land_maps` directory and postprocessing.

Note: *The project was made using Windows machines, but was intended to utilize an FST through the `hfst` and `hfst_dev` modules, but currently they are only runnable on UNIX systems. Since our system does little in terms of morphological analysis, `hfst` was decided as unnecessary, and our solution was implemented through simple JSON mapping.*