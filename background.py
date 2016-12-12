import re
import os
import pandas as pd

def instantiate_record(path="/Users/andrew/Projects/Spanki/resources/record.csv"):

    try:
        record = pd.read_csv(path, index_col=0)
    except OSError:
        record = pd.DataFrame(index=letter_combos, columns=["Person", "Action", "Object"])

    return record

def get_out_file(in_file):

    out_dir = '/'.join(in_file.split("/")[:-1])
    out_file = in_file.split("/")[-1]
    out_file = re.sub("(.txt)|(.csv)", "_mnemonics.csv", out_file)
    mnem_df_path = os.path.join(out_dir, out_file) # check if exists

    return mnem_df_path

def instantiate_mnem_df(in_file):

    mnem_df_path = get_out_file(in_file)
    try:
        mnem_df = pd.read_csv(mnem_df_path, index_col=0)
    except OSError:
        # make sure open and listening the file here doesn't fuck up open the file later
        # maybe change columns here to p, a, o
        ix = [i.strip() for i in list(open(in_file))]
        mnem_df = pd.DataFrame(index=ix, columns=["Person", "Action", "Object"])

    return mnem_df

def update_mnem_df(mnem_df, mnem_df_path, mnem, PAO, word):
    
    if PAO == 'Object':
        try:
            print(word)
            print(PAO)
            current_mnems = mnem_df.loc[word, PAO]
            if mnem not in current_mnems:
                mnem_df.loc[word, PAO] = ','.join([mnem_df.loc[word, PAO], mnem])
        except TypeError:
            mnem_df.loc[word, PAO] = mnem
            mnem_df.to_csv(mnem_df_path)
    else:
        mnem_df.loc[word, PAO] = mnem
        mnem_df.to_csv(mnem_df_path)

def record_mnemonic(record, pair, PAO, mnem):

    current_mnems = record.loc[pair, PAO]
    try:
        current_mnems = current_mnems.split(",")
        if mnem not in current_mnems:
            record.loc[pair, PAO] = ",".join([record.loc[pair, PAO],mnem])
    except AttributeError:
        record.loc[pair, PAO] = mnem

    record.to_csv("/Users/andrew/Projects/Spanki/resources/record.csv")
