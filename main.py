import re
import nltk
from nltk.corpus import words
from fuzzywuzzy import fuzz

nltk.download("words")

class Checker:
    def __init__(self):
        pass

    def check(self, word):
        checked_word = re.sub(r"[^\w]", "", word.lower())
        if checked_word in words.words():
            print(f"The word '{checked_word}' is correctly spelled.")
        else:
            suggestions = self.get_suggestions(checked_word)
            if suggestions:
                self.show_suggestions(checked_word, suggestions)
            else:
                print(f"No suggestions found for '{checked_word}'.")

    # Suggestions are found using Levenshtein distance
    def get_suggestions(self, word, threshold=80):
        return [w for w in words.words() if fuzz.ratio(word, w.lower()) > threshold]

    def show_suggestions(self, word, suggestions):
        print(f"Suggestions for '{word}':")
        for suggestion in suggestions:
            print(suggestion)

if __name__ == "__main__":
    checker = Checker()

    while True:
        input_word = input("Enter a word without spaces (or 'exit' to end): ")

        if input_word.lower() == 'exit':
            break

        if ' ' in input_word:
            print("Please enter one word at a time.(Spaces were used or more than one word was entered.)")
        else:
            checker.check(input_word)
