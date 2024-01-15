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

def words(text):
    # Generates an iterator over each unique word found within `text`, including duplicates.
    return re.findall('[a-z]+', text.lower())


def train(text, model=None):
    # Train spelling correction algorithm on given `text`.
    model = collections.defaultdict(lambda: 0) if model is None else model
    for word in words(text):
        model[word] += 1
    return model

word_model = train(' '.join(nltk_words.words()))

def train_from_files(file_list, model=None):
    # Train a spelling correction algorithm using a set of files.
    for f in file_list:
        model = train(open(f).read(), model)
    return model


def variants(word):
    # Returns a generator of all known spelling variations of word.
    alphabet="abcdefghijklmnopqrstuvwxyz"
    splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes    = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
    replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
    inserts    = [a + c + b for a, b in splits for c in alphabet]
    return set(deletes + transposes + replaces + inserts)


def double_variants(word):
    # Generate double variants by applying the 'variants' function twice.
    return set(s for w in variants(word) for s in variants(w))


def suggestions(word, real_words):
    # Generate suggestions for correcting a word.
    word = word.lower()

    return ({word} & real_words or
            (set(shortenings(word))  | set(apply_vowel_swaps(word)) | set(variants(word)) | set(shortenings_and_applyVowelSwaps(word)) | set(double_variants(word))) & real_words or
            {"NO SUGGESTION"})

# The main script.
if __name__ == '__main__':
    # Train the initial word model with NLTK words dataset.
    word_model = train(" ".join(nltk_words.words()))
    real_words = set(word_model)

    # Add more training from additional text files.
    texts = [
        'lemmas.txt',
        'alice-in-wonderland.txt'
    ]

    word_model = train_from_files(texts, word_model)

    try:
        while True:
            word = input('>')
            if(word=='q'):
                break;

            # Generate suggestions for the input word and print them along with keyboard distances.
            possibilities = suggestions(word, real_words)
            sorted_results = sorted([(x, keyboard_distance(word, x)) for x in possibilities], key=lambda item: item[1])
            print(sorted_results)

    except (EOFError, KeyboardInterrupt):
        exit(0)
        
