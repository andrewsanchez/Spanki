#!/usr/bin/env python3

import re, argparse
from subprocess import call
from os import getcwd, path, remove
from numpy.random import rand

def from_gdoc(file):
    chunked_name = path.splitext(file)[0]+".org"

    # lines = []
    # with open(file, encoding="utf-8") as outline:
    #     for line in outline:
    #         lines.append(line)
    #     # lines = outline.readlines()

    lines = []
    with open(file) as outline:
        for line in outline:
            line = line.encode("ascii", "ignore")
            lines.append(line.decode("ascii", "ignore"))

    p1 = re.compile("^\* ")
    p2 = re.compile("^ {3}\* ")
    p3 = re.compile("^ {6}\* ")
    p4 = re.compile("^ {9}\* ")
    p5 = re.compile("^ {12}\* ")
    p6 = re.compile("^ {15}\* ")
    p7 = re.compile("^ {18}\* ")

    l1  = []
    l2  = []
    l3  = []
    l4  = []
    l5  = []
    l6 = []
    l7 = []

    cards = []

    for line in lines:
        if p1.match(line):
            l1.append(line)
        elif p2.match(line):
            l2.append(line)
        elif p3.match(line):
            l3.append(line)
        elif p4.match(line):
            l4.append(line)
            try:
                if not p5.match(lines[lines.index(line)+1]):
                    cards.append((l1[-1], l2[-1], l3[-1], l4[-1]))
            except:
                continue
        elif p5.match(line):
            l5.append(line)
            try:
                if not p6.match(lines[lines.index(line)+1]):
                    cards.append((l1[-1], l2[-1], l3[-1], l4[-1], l5[-1]))
            except:
                continue
        elif p6.match(line):
            l6.append(line)
            try:
                if not p7.match(lines[lines.index(line)+1]):
                    cards.append((l1[-1], l2[-1], l3[-1], l4[-1], l5[-1], l6[-1]))
            except:
                continue
        elif p7.match(line):
            l7.append(line)
            cards.append((l1[-1], l2[-1], l3[-1], l4[-1], l5[-1], l6[-1], l7[-1]))


    for card in cards:
        flashcard = []
        for i in card[0:3]:
            flashcard.append(i.strip())
        for x in card[3:]:
            flashcard.append(x)
        print(" ".join(flashcard[0:3]) + "\n")
        print("".join(flashcard[3:]))

    # with open(chunked_name, "a") as chunked:
    #     for card in cards:
    #         flashcard = []
    #         for i in card[0:3]:
    #             flashcard.append(i.strip())
    #         for x in card[3:]:
    #             flashcard.append(x)
    #         chunked.write(" ".join(flashcard[0:3]) + "\n")
    #         chunked.write("".join(flashcard[3:]))
            # chunked.write(" ".join(flashcard[0:3]) + "\n")
            # chunked.write("".join(flashcard[3:]))

def from_org(file):
    pass

def html_to_anki(file):

    html_file = path.splitext(file)[0]+".html"
    call(["pandoc", "-f", "org", "-t", "html", file, "-o", html_file])

    replace_id = re.compile('<h1 id.*"')
    replace_h1 = re.compile(r"h1>")
    replace_newlines = re.compile(r"\n")
    h3 = re.compile('^"<h3')
    last_line_of_card = re.compile(r"</ul><br>")

    with open(html_file) as in_file:
        lines = list(in_file)
        in_file.close()

    for line in lines:
        i = lines.index(line)
        line = re.sub(replace_id, '"<h3 id='+str(rand()), line)
        line = re.sub(replace_h1, "h3>", line)
        line = re.sub(replace_newlines, "<br>", line)
        lines[i] = line
        if h3.match(line):
            i = lines.index(line)
            previous_line = lines[i-1]
            lines[i-1] = previous_line + '"'

    out_file = path.splitext(html_file)[0]+".csv"
    with open (out_file, "a") as csv:
        card = []
        for line in lines:
            end = re.compile('.*>"$')
            card.append(line)
            if end.match(line):
                csv.write("".join(card))
                csv.write("\n")
                del card[:]
                continue

    remove(html_file)

def main():
    ap = argparse.ArgumentParser(description = "Turn your outlines in more manageable chunks of information.")
    ap.add_argument("file", help = "Path to the file you want to parse.")
    ap.add_argument("-c", "--chunk", help = "Generate the chunked version of your outline.", action="store_true")
    ap.add_argument("-a", "--anki", help = "Generate a .csv from HTML to import into Anki.", action="store_true")
    args = ap.parse_args()

    if args.chunk:
        from_gdoc(args.file)
    elif args.anki:
        html_to_anki(args.file)

main()
