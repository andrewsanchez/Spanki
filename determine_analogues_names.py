characters = pd.read_csv("all_names.csv", index_col=0)
useless_words = ["mr", "dr", "ms", "mrs", "miss", "sir", "master", "lady"]

[useless_words.append(word) for word in stopwords.words("english")]

def get_initials(name):
    name = name.strip(" ,")
    if "," in name:
        names = name.split(",")
        if len(names) > 2:
            initials = "check"
        else:
            first = names[-1]
            last = names[0]
            initials = first[0]+last[0]
    elif " " in name:
        names = name.split(" ")
        if len(names) > 2:
            initials = "check"
        else:
            first = names[0]
            last = names[-1]
            initials = first[0]+last[0]
    else:
        initials = ""
    initials = re.sub("[\W]", "", initials)
    return initials

def reduce_words(word):
    letters = re.sub("[\W]", "", word)
    letters = re.sub("[aeiouy]", "", word)
    letters = re.sub(r'([a-z])\1+', r'\1', letters)
    return letters

def remove_useless_words(words):
        words = words.split(" ")
        for word in words:
            if word in english_stopwords:
                del words[words.index(word)]
        words = " ".join(words)
        return words

def set_values(df):
    for name in df.index:
        clean_name = remove_useless_words(name)
        if "," in clean_name:
            names = clean_name.split(",")
            first = names[-1]
            last = names[0]
            first = reduce_words(first)
            last = reduce_words(last)
            df.at[name, "first"] = first
            df.at[name, "last"] = last
        elif " " in clean_name:
            names = clean_name.split(" ")
            first = names[0]
            last = names[-1]
            first = reduce_words(first)
            last = reduce_words(last)
            df.at[name, "first"] = first
            df.at[name, "last"] = last
        else:
            first = reduce_words(clean_name)
            df.at[name, "first"] = first
        initials = get_initials(clean_name)
        df.at[name, "initials"] = initials
