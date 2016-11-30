#!/usr/bin/env python

import argparse
import os
import re
import pandas as pd
from nltk.corpus import wordnet as wn
from nltk.corpus import names, stopwords

def rm_junk_words(word, useless_words):

    for junk in useless_words:
        if junk in word:
            reduced = re.sub(junk, "", word)
        else:
            reduced = word

    return reduced

def nltk_names(dst, ghost_letters="[aeiouyh\W]"):

    index = []
    for name in names.words():
        name = name.lower().strip()
        reduced = re.sub(ghost_letters, "", name)
        reduced = re.sub(r'([a-z])\1+', r'\1', reduced) # remove repeated letters
        reduced = re.sub("[\W_]", "", reduced)
        index.append(reduced)

    index = list(set(index))
    index_len = len(list(set(index)))
    df = pd.DataFrame(index=index, columns=["Names"])
    dst = os.path.join(dst, "nltk_names.csv")

    for name in names.words():
        name = name.lower().strip()
        reduced = re.sub(ghost_letters, "", name)
        reduced = re.sub(r'([a-z])\1+', r'\1', reduced) # remove repeated letters
        reduced = re.sub("[\W_]", "", reduced)
        current_names = df.loc[reduced, "Names"]
        if type(current_names) == float:
            df.loc[reduced, "Names"] = name
        else:
            current_names = current_names.split(",")
            if name not in current_names:
                df.loc[reduced, "Names"] = ",".join([df.loc[reduced, "Names"],name])
        print(reduced, df.loc[reduced, "Names"])

    df = df.sort_index()
    df.to_csv(dst)

def get_index(POS, ghost_letters="[aeiouyh\W]"):

    useless_words = [word for word in stopwords.words("english")]
    index = []
    for synset in list(wn.all_synsets(POS[0])):
        word = synset.name().split(".")[0].lower()
        reduced = rm_junk_words(word, useless_words)
        reduced = re.sub(ghost_letters, "", word)
        reduced = re.sub(r'([a-z])\1+', r'\1', reduced) # remove repeated letters
        reduced = re.sub("[\W_]", "", reduced)
        index.append(reduced)

    return list(set(index))

def get_words(dst, POS, ghost_letters="[aeiouyh\W]"):

    index = get_index(POS, ghost_letters)
    df = pd.DataFrame(index=index, columns=["Words"])
    file_name = POS+".csv"
    dst = os.path.join(dst, file_name)

    useless_words = [word for word in stopwords.words("english")]
    for synset in list(wn.all_synsets(POS[0])):
        word = synset.name().split(".")[0].lower()
        reduced = rm_junk_words(word, useless_words)
        reduced = re.sub(ghost_letters, "", word)
        reduced = re.sub(r'([a-z])\1+', r'\1', reduced) # remove repeated letters
        reduced = re.sub("[\W_]", "", reduced)
        current_words = df.loc[reduced, "Words"]
        if type(current_words) == float:
            df.loc[reduced, "Words"] = word
        else:
            current_words = current_words.split(",")
            if word not in current_words:
                df.loc[reduced, "Words"] = ",".join([df.loc[reduced, "Words"],word])
        print(reduced, df.loc[reduced, "Words"])

    df = df.sort_index()
    df.to_csv(dst)

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("dst")
    args = parser.parse_args()
    dst = args.dst

    nltk_names(dst)
    #get_words(dst, "nouns")
    get_words(dst, "verbs")

main()
