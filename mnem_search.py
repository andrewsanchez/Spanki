#!/usr/bin/env python

import string
import re
import argparse
import pandas as pd
from time import sleep
from numpy import float64
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

def record_mnemonic(record, pair, PAO, mnem):


    current_mnems = record.loc[pair, PAO]
    try:
        current_mnems = current_mnems.split(",")
        if mnem not in current_mnems:
            record.loc[pair, PAO] = ",".join([record.loc[pair, PAO],mnem])
    except AttributeError:
        record.loc[pair, PAO] = mnem

   #current_mnems = record.loc[pair, PAO]
   #if type(current_mnems) == float64:
   #    record.loc[pair, PAO] = mnem
   #else:
   #    current_mnems = current_mnems.split(",")
   #    if mnem not in current_mnems:
   #        record.loc[pair, PAO] = ",".join([record.loc[pair, PAO],mnem])

    record.to_csv("/Users/andrew/Projects/Spanki/resources/record.csv")

def instantiate_record(path="/Users/andrew/Projects/Spanki/resources/record.csv"):

    try:
        record = pd.read_csv(path, index_col=0)
    except OSError:
        record = pd.DataFrame(index=letter_combos, columns=["Person", "Action", "Object"])

    return record

def choose_mnem(PAO, pair, names, nouns, verbs, record, mnem_list):

    #TODO Add ability to back up if you chose wrong mnemonic
    #TODO What to do if there are not any matches?
    #TODO Give option for modifying and/or annotating the mnemonic word for clarity
    #TODO Remove "h" from list of consonants?

    if PAO == "Person":
        people = sorted(set(list(names.index[names["initials"] == pair])))
        people_and_nums = zip(range(0,len(people)), people)
        for item in people_and_nums:
            if int(item[0]) % 6 != 0 or item[0] == 0:
                print("{}-{}".format(item[0], item[1]), end=", ")
            else:
                print("{}-{}".format(item[0], item[1]))
        print("\n")
        choice = int(input("Enter the number that corresponds to the desired person:  "))
        mnem = people[choice]
        mnem_list.append((pair, mnem))
        record_mnemonic(record, pair, PAO, mnem)
        print("{} - > {}".format(pair, mnem), end="\n\n")
        sleep(.5)
        return mnem

    elif PAO == "Action":
        actions = sorted(set(verbs.loc[pair, "Words"].split(",")))
        actions_and_nums = zip(range(0,len(actions)), actions)
        for item in actions_and_nums:
            if int(item[0]) % 6 != 0 or item[0] == 0:
                print("{}-{}".format(item[0], item[1]), end=", ")
            else:
                print("{}-{}".format(item[0], item[1]))
        print("\n")
        choice = int(input("Enter the number that corresponds to the desired action:  "))
        mnem = actions[choice]
        mnem_list.append((pair, mnem))
        record_mnemonic(record, pair, PAO, mnem)
        print("{} - > {}".format(pair, mnem), end="\n\n")
        sleep(.5)
        return mnem

    elif PAO == "Object":
        objects = sorted(set(nouns.loc[pair, "Words"].split(",")))
        objects_and_nums = zip(range(0,len(objects)), objects)
        for item in objects_and_nums:
            if int(item[0]) % 6 != 0 or item[0] == 0:
                print("{}-{}".format(item[0], item[1]), end=", ")
            else:
                print("{}-{}".format(item[0], item[1]))
        print("\n")
        choice = int(input("Enter the number that corresponds to the desired object:  "))
        mnem = objects[choice]
        mnem_list.append((pair, mnem))
        print("{} - > {}".format(pair, mnem), end="\n\n")
        sleep(.5)
        record_mnemonic(record, pair, PAO, mnem)

        return mnem

def split_words(word):

    if " " in word:
        words = word.split(" ")
    elif "," in word:
        words = word.split(",")
    else:
        words = [word]
    return words

def mnem_search(in_file, names, nouns, verbs, record):

    with open(in_file) as f:
        for line in f:
            words = split_words(line)
            word_bones = []
            for word in words:
                reduced = reduce_word(word)
                word_bones.append(reduced)
            print("{} -> {}".format(line, [i for i in word_bones]))

            mnem_list=[]
            for word in word_bones:
                pairs = wrap(word, 2)
                print("Letter pairs:  {}".format(pairs))

                for pair in pairs:
                    if pairs.index(pair) == 0:
                        person = choose_mnem("Person", pair, names, nouns, verbs, record, mnem_list)
                    elif pairs.index(pair) == 1:
                        print("************************************")
                        action = choose_mnem("Action", pair, names, nouns, verbs, record, mnem_list)
                    elif pairs.index(pair) == 2:
                        print("************************************")
                        object = choose_mnem("Object", pair, names, nouns, verbs, record, mnem_list)
                    elif pairs.index(pair) > 2:
                        print("************************************")
                        object = choose_mnem("Object", pair, names, nouns, verbs, record, mnem_list)
                print("Mnemonic for {} ({})".format(line.strip(), " ".join([i for i in word_bones])))
                for mnem in mnem_list:
                    print("{} -> {}".format(mnem[0], mnem[1]))
                print("\n")
                
def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("in_file")
    args = parser.parse_args()

    names = pd.read_csv("/Users/andrew/Projects/Spanki/resources/names.csv", index_col=0)
    verbs = pd.read_csv("/Users/andrew/Projects/Spanki/resources/verbs.csv", index_col=0)
    nouns = pd.read_csv("/Users/andrew/Projects/Spanki/resources/nouns.csv", index_col=0)

    record = instantiate_record()
    mnem_search(args.in_file, names, nouns, verbs, record)

main()
