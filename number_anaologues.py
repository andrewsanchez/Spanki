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
