#!/usr/bin/env python

import string
import re
import pandas as pd
from time import sleep
from background import *
from textwrap import wrap
from itertools import permutations
from string import ascii_lowercase
from nltk.corpus import stopwords

useless_words = [word for word in stopwords.words("english")]
ghost_letters = "aeiouyh"
ghost_letters_regex = "[{}\W]".format(ghost_letters)
consonants = [l for l in ascii_lowercase if l not in ghost_letters]
letter_combos = ["".join(l) for l in permutations(consonants, 2)]
[letter_combos.append(l) for l in consonants]

def reduce_word(word):

    """
    Reduce the input word to just its consosants.
    No duplicate letters and no Hs.
    """
    
    word = word.lower().strip()
    reduced_word = re.sub(ghost_letters_regex, "", word)
    reduced_word = re.sub(r'([a-z])\1+', r'\1', reduced_word)

    return reduced_word

def split_words(word):

    """
    Split input word at ' '  or ','
    """

    if " " in word:
        words = word.split(" ")
    elif "," in word:
        words = word.split(",")
    else:
        words = [word]

    return words

def get_letter_pairs(word, reduced_word):

    """
    Split up reduced word into pairs of 2 consonants
    """

    pairs = wrap(reduced_word, 2)
    print("{} -> {}".format(word, pairs), end='\n\n')

    return pairs

def list_mnem_options(PAO, pair, names, nouns, verbs, record, mnem_list):

    if PAO == "Person":
        df = names
        mnems = sorted(set(list(df.index[names["initials"] == pair])))
    elif PAO == "Action":
        df = verbs
        mnems = sorted(set(df.loc[pair, "Words"].split(",")))
    elif PAO == "Object":
        df = nouns
        mnems = sorted(set(df.loc[pair, "Words"].split(",")))

    print("Mnemonics for '{}':".format(pair), end="\n\n")
    mnems_and_nums = zip(range(0,len(mnems)), mnems)
    for item in mnems_and_nums:
        print("{}-{}".format(item[0], item[1]))
    print('')

    return mnems, df

def verify_choice():

def choose_mnem(df, mnems, PAO, pair, mnem_list, record):

    choice = int(input("Enter the number that corresponds to the desired mnemonic:  "))
    mnem = mnems[choice]
    mnem_list.append((pair, mnem))
    record_mnemonic(record, pair, PAO, mnem)
    print("{} - > {}".format(pair, mnem), end="\n\n")
    print("*"*80)
    sleep(.5)

    return mnem

def check_PAO(pair, pairs):

    """
    Determine whether the current pair of letters should be represented 
    by a person, action, or object, based on it's position in the word.
    The first 2 letters are represented by a person, the second 2 by an
    action, and anything after that by an object.
    """

    if pairs.index(pair) == 0:
        PAO = 'Person'
    elif pairs.index(pair) == 1:
        PAO = 'Action'
    elif pairs.index(pair) >= 2:
        PAO = 'Object'

    return PAO
