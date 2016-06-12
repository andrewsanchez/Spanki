#!/usr/bin/env python3

import string, re, itertools
import pandas as pd
from collections import Counter
from nltk.corpus import wordnet as wn

ls = [["sz",
       "td",
       "nm",
       "ck",
       "rl",
       "fv",
       "hj",
       "gq",
       "wx" ]]

ls = ls[0]

ns = [str(n) for n in range(0,10)]

replacements = list(zip(ls,ns))
replacements = tuple(replacements)
filename = "".join(ls)+".csv"

with open(filename, "w") as out:
    out.write("".join(ls) + "\n")
    out.close()

nums_from_words = []

for synset in list(wn.all_synsets('n')):
    word = synset.name().split(".")[0]
    word = word.lower()
    word = re.sub("[aeiou\W]", "", word)
    word = re.sub(r'([a-z])\1+', r'\1', word)
    number = []

    for letter in word:
        for lset, num in replacements:
            if letter in lset:
                number.append(num)

    if len(number) <= 3:
        number = "".join(number)
        nums_from_words.append(number)

nums_from_words = Counter(nums_from_words)

columns=["matches"]
df = pd.DataFrame.from_dict(nums_from_words, orient="index")
df = df.sort_index()
df.to_csv(filename, mode="a")
