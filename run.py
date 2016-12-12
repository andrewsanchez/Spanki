#!/usr/bin/env python

import argparse
from background import *
from mnem_search import *

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("in_file")
    args = parser.parse_args()

    in_file = args.in_file
    mnem_df_path = get_out_file(in_file)
    names, verbs, nouns, record, mnem_df = instantantiate_dfs(in_file)

    print('*'*80, '\n\n')
    with open(in_file) as f:
        for line in f:
            word = line.strip()
            reduced_word = reduce_word(word)
            pairs = get_letter_pairs(word, reduced_word)
            mnem_list=[]
            for pair in pairs:
                PAO = check_PAO(pair, pairs)
                mnems, df = list_mnem_options(PAO, pair, names, nouns, verbs, record, mnem_list)
                mnem = choose_mnem(df, mnems, PAO, pair, mnem_list, record)
                update_mnem_df(mnem_df, mnem_df_path, mnem, PAO, word)
            
            print("Mnemonic for {}:".format(line.strip()))
            print(mnem_df.loc[line.strip()], end='\n\n')

        print(mnem_df, end="\n\n")

main()
