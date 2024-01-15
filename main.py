import re
import collections
from itertools import product
import nltk

# Download the NLTK words dataset.
nltk.download("words")
from nltk.corpus import words as nltk_words

# Define the keyboard layout.
keyboard_layout = {
        # Lowercase letters.
        'q': (0, 0), 'w': (0, 1), 'e': (0, 2), 'r': (0, 3), 't': (0, 4), 'y': (0, 5), 'u': (0, 6),
        'o': (0, 7), 'p': (0, 8), 'a': (1, 0), 's': (1, 1), 'd': (1, 2), 'f': (1, 3), 'g': (1, 4),
        'h': (1, 5), 'j': (1, 6), 'k': (1, 7), 'l': (1, 8), 'i': (1, 9), 'z': (2, 0), 'x': (2, 1), 
        'c': (2, 2), 'v': (2, 3), 'b': (2, 4), 'n': (0, 5), 'm': (0, 6),
        # Uppercase letters.
        'Q': (0, 0), 'W': (0, 1), 'E': (0, 2), 'R': (0, 3), 'T': (0, 4), 'Y': (0, 5), 'U': (0, 6),
        'O': (0, 7), 'P': (0, 8), 'A': (1, 0), 'S': (1, 1), 'D': (1, 2), 'F': (1, 3), 'G': (1, 4),
        'H': (1, 5), 'J': (1, 6), 'K': (1, 7), 'L': (1, 8), 'I': (1, 9), 'Z': (2, 0), 'X': (2, 1), 
        'C': (2, 2), 'V': (2, 3), 'B': (2, 4), 'N': (0, 5), 'M': (0, 6)            
}

def keyboard_distance(word1, word2):
    # Calculate the keyboard distance between two words based on the defined keyboard layout.
    total_distance = 0
    for i in range(min(len(word1), len(word2))):
        char1, char2 = word1[i], word2[i]
        pos1, pos2 = keyboard_layout.get(char1, (-1, -1)), keyboard_layout.get(char2, (-1, -1))
        total_distance += abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    return total_distance


def shortenings(word):
    # Return flat option list of all possible variations of the word by removing duplicate letters.
    word = list(word)
    for i, l in enumerate(word):
        n = count_duplicates(word, i)
        if n:
            flat_dupes = [l*(r+1) for r in range(n+1)][:3]
            for _ in range(n):
                word.pop(i+1)

            word[i] = flat_dupes

    for p in product(*word):
        yield ''.join(p)


def count_duplicates(string, i):
    # Count how many times a character appears after index `i` in `string`.
    initial_i = i
    last = string[i]
    while i+1 < len(string) and string[i+1] == last:
        i += 1
    return i-initial_i


def apply_vowel_swaps(word):
    # Return flat option list of all possible variations of the word by swapping vowels.
    vowels = "aeiou"
    word = list(word)
    for i, l in enumerate(word):
        if type(l) == list:
            pass
        elif l in vowels:
            word[i] = list(vowels)

    for p in product(*word):
        yield ''.join(p)


def shortenings_and_applyVowelSwaps(word):
    # Generate all possible words from the input word that can be formed by either.
    for shortened in shortenings(word):
        for version in apply_vowel_swaps(shortened):
            yield version

