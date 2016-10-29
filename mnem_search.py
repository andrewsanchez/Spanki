#!/usr/bin/env python3

import string, re, itertools
import pandas as pd
from collections import Counter
from nltk.corpus import wordnet as wn
from nltk.corpus import names

def replacements():

    andrews_pairs = ["sz",
                    "td",
                    "nm",
                    "ck",
                    "rl",
                    "fv",
                    "hj",
                    "gq",
                    "wx",
                    "pb",]

    major_pairs = ["sz",
                "td",
                "n",
                "m",
                "r",
                "l",
                "cjgsz",
                "kgq",
                "fv",
                "pb" ]

    fourteen_pairs = ["b",
                    "c",
                    "s",
                    "fv",
                    "nm",
                    "pq",
                    "k",
                    "rl",
                    "td",
                    "gj",]

    one_through_ten = [str(n) for n in range(0,10)]

    for pairing in [andrews_pairs]:
        replacements = list(zip(pairing, one_through_ten))
        replacements = tuple(replacements)

    return replacements

def get_names(replacements):

    complete_words = []
    reduced_words = []
    number_equivalents = []
    for name in names.words():
        word = synset.name().split(".")[0].lower()
        reduced_word = re.sub("[aeiouy\W]", "", word)
        reduced_word = re.sub(r'([a-z])\1+', r'\1', reduced_word)
        numbers = []
        for letter in reduced_word:
            for pair, n in replacements:
                if letter in pair:
                    numbers.append(n)
        number = str("".join(numbers))
        complete_words.append(word)
        reduced_words.append(reduced_word)
        number_equivalents.append(number)
    data = list(zip(complete_words, number_equivalents))
    names_df = pd.DataFrame(data=data, index=reduced_words, columns=["Word", "Number"])
    names_df = df.sort_index()
    names_df.to_csv("names.csv", sep="\t")
    return names_df

def get_words(replacements):
    complete_words = []
    reduced_words = []
    number_equivalents = []

    for synset in list(wn.all_synsets('n')):
        word = synset.name().split(".")[0].lower()
        reduced_word = re.sub("[aeiouy\W]", "", word)
        reduced_word = re.sub(r'([a-z])\1+', r'\1', reduced_word)
        numbers = []
        for letter in reduced_word:
            for pair, n in replacements:
                if letter in pair:
                    numbers.append(n)
        number = str("".join(numbers))

        complete_words.append(word)
        reduced_words.append(reduced_word)
        number_equivalents.append(number)

    data = list(zip(complete_words, number_equivalents))
    words_df = pd.DataFrame(data=data, index=reduced_words, columns=["Word", "Number"])
    words_df = df.sort_index()
    words_df.to_csv("words.csv", sep="\t")
    return words_df

def get_verbs(replacements):
    complete_words = []
    reduced_words = []
    number_equivalents = []

    for synset in list(wn.all_synsets('v')):
        word = synset.name().split(".")[0].lower()
        reduced_word = re.sub("[aeiouy\W]", "", word)
        reduced_word = re.sub(r'([a-z])\1+', r'\1', reduced_word)
        numbers = []
        for letter in reduced_word:
            for pair, n in replacements:
                if letter in pair:
                    numbers.append(n)
        number = str("".join(numbers))
        complete_words.append(word)
        reduced_words.append(reduced_word)
        number_equivalents.append(number)

    data = list(zip(complete_words, number_equivalents))
    verbs_df = pd.DataFrame(data=data, index=reduced_words, columns=["Word", "Number"])
    verbs_df = df.sort_index()
    verbs_df.to_csv("verbs.csv", sep="\t")

    return verbs_df
    pass

def main():
    replacements = replacements()
    names_df = get_names(replacements)
    words_df = get_words(replacements)
    verbs_df = get_verbs(replacements)
    all_df = pd.concat([words_df, names_df, verbs_df])

main()
