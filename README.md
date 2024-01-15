(This repository is first discussed and coded in our term project whatsapp student group then after deciding the last shape of the code we conveyed it to Github.)


This Python script implements a spelling correction algorithm that suggests possible corrections for input words. The algorithm considers variations such as keyboard distance, shortenings, vowel swaps, and other spelling variations.

Dependencies
Make sure you have the following dependencies installed:

Python 3
NLTK (Natural Language Toolkit)

You can install NLTK using the following command:
pip install nltk

Usage

-Clone the repository:
git clone https://github.com/aysbukre/TermProject303.git
cd TermProject303

-Run the script:
python3 main.py

*Enter a word when prompted, and the script will generate spelling suggestions along with keyboard distances.
*To exit the program, enter 'q' when prompted.

Notes
The script uses a keyboard layout to calculate the distance between characters, which may influence the suggestions.
Suggestions are generated based on various transformations, including shortenings, vowel swaps, and spelling variations.
Keyboard distances between the input word and suggestions are displayed for each suggestion.
