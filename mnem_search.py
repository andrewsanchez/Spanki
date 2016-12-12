#!/usr/bin/env python

import string
import re
import argparse
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

    word = word.lower().strip()
    reduced_word = re.sub(ghost_letters_regex, "", word)
    reduced_word = re.sub(r'([a-z])\1+', r'\1', reduced_word)

    return reduced_word

def split_words(word):

    if " " in word:
        words = word.split(" ")
    elif "," in word:
        words = word.split(",")
    else:
        words = [word]

    return words

def get_word_bones(line):

    #words = split_words(line.strip())
    word_bones = reduce_word(line.strip())
    pairs = wrap(word_bones, 2)
    print("{} -> {}".format(line.strip(), pairs), end='\n\n')

    return pairs

def choose_PAO(df, mnems, PAO, pair, mnem_list, record):

    print("Mnemonics for '{}':".format(pair), end="\n\n")
    mnems_and_nums = zip(range(0,len(mnems)), mnems)
    for item in mnems_and_nums:
        print("{}-{}".format(item[0], item[1]))
    print('')
    choice = int(input("Enter the number that corresponds to the desired mnemonic:  "))
    mnem = mnems[choice]
    mnem_list.append((pair, mnem))
    record_mnemonic(record, pair, PAO, mnem)
    print("{} - > {}".format(pair, mnem), end="\n\n")
    print("*"*80)
    sleep(.5)

    return mnem

def choose_mnem(PAO, pair, names, nouns, verbs, record, mnem_list):

    # redundant code in these conditionals.  consolidate into a function
    if PAO == "Person":
        df = names
        mnems = sorted(set(list(df.index[names["initials"] == pair])))
        mnem = choose_PAO(df, mnems, PAO, pair, mnem_list, record)
        return mnem

    elif PAO == "Action":
        df = verbs
        mnems = sorted(set(df.loc[pair, "Words"].split(",")))
        mnem = choose_PAO(df, mnems, PAO, pair, mnem_list, record)
        return mnem

    elif PAO == "Object":
        df = nouns
        mnems = sorted(set(df.loc[pair, "Words"].split(",")))
        mnem = choose_PAO(df, mnems, PAO, pair, mnem_list, record)
        return mnem

def check_PAO(pair, pairs):

    if pairs.index(pair) == 0:
        PAO = 'Person'
    elif pairs.index(pair) == 1:
        PAO = 'Action'
    elif pairs.index(pair) >= 2:
        PAO = 'Object'

    return PAO

def mnem_search(in_file, names, nouns, verbs, record, mnem_df):

    mnem_df_path = get_out_file(in_file)
    with open(in_file) as f:
        for line in f:
            word = line.strip()
            pairs = get_word_bones(line)
            mnem_list=[]
            for pair in pairs:
                PAO = check_PAO(pair, pairs)
                mnem = choose_mnem(PAO, pair, names, nouns, verbs, record, mnem_list)
                update_mnem_df(mnem_df, mnem_df_path, mnem, PAO, word)
            
            print("Mnemonic for {}:".format(line.strip()))
            print(mnem_df.loc[line.strip()], end='\n\n')

        print(mnem_df, end="\n\n")
                
def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("in_file")
    args = parser.parse_args()

    record = instantiate_record()
    mnem_df = instantiate_mnem_df(args.in_file)
    names = pd.read_csv("/Users/andrew/Projects/Spanki/resources/names.csv", index_col=0)
    verbs = pd.read_csv("/Users/andrew/Projects/Spanki/resources/verbs.csv", index_col=0)
    nouns = pd.read_csv("/Users/andrew/Projects/Spanki/resources/nouns.csv", index_col=0)

    print('*'*80, '\n\n')
    mnem_search(args.in_file, names, nouns, verbs, record, mnem_df)

main()
