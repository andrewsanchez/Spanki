#!/usr/bin/env python

import re, argparse
from subprocess import call
from os import getcwd, path
from numpy.random import rand

def from_gdoc(file):
    collapsed_name = file.strip(".txt")+"_collapsed.txt"
    lines = []
    with open(file) as outline:
        for line in outline:
            line = line.encode("ascii", "ignore")
            lines.append(line.decode("ascii"))

    p1 = re.compile("^\* ")
    p2 = re.compile("^ {3}\* ")
    p3 = re.compile("^ {6}\* ")
    p4 = re.compile("^ {9}\* ")
    p5 = re.compile("^ {12}\* ")
    p6 = re.compile("^ {15}\* ")

    l1  = []
    l2  = []
    l3  = []
    l4  = []
    l5  = []

    cards = []

    for line in lines:
        if p1.match(line):
            l1.append(line)
        elif p2.match(line):
            l2.append(line)
            l2.insert(0, l1[-1])
            l1.insert(-1, line)
        elif p3.match(line):
            l3.append(line)
    #         cards.append((l1[-1], l2[-1], l3[-1]))
        elif p4.match(line):
            l4.append(line)
            if not p5.match(lines[lines.index(line)+1]):
                cards.append((l1[-1], l2[-1], l3[-1], l4[-1]))
        elif p5.match(line):
            l5.append(line)
            cards.append((l1[-1], l2[-1], l3[-1], l4[-1], l5[-1]))

    with open(collapsed_name, "a") as collapsed:
        for card in cards:
            flashcard = []
            for i in card[0:3]:
                flashcard.append(i.strip())
            for x in card[3:]:
                flashcard.append(x)
            collapsed.write(" ".join(flashcard[0:3]) + "\n")
            collapsed.write("".join(flashcard[3:]))

def from_org(file):
    pass

def to_html(file):
    out_file = file.replace(".txt", ".html")
    call(["pandoc", "-f", "org", "-t", "html", file, "-o", out_file])

def html_to_anki(file):
    replace_id = re.compile('<h1 id.*"')
    replace_h1 = re.compile(r"h1>")
    replace_newlines = re.compile(r"\n")
    h3 = re.compile('^"<h3')
    last_line_of_card = re.compile(r"</ul><br>")

    with open(file) as in_file:
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

    out_file = file.replace(".html", ".csv")
    with open (out_file, "a") as out_file:
        card = []
        for line in lines:
            end = re.compile('.*>"$')
            card.append(line)
            if end.match(line):
                out_file.write("".join(card))
                out_file.write("\n")
                del card[:]
                continue

def main():
    ap = argparse.ArgumentParser(description = "Turn your outlines in more manageable chunks of information.")
    ap.add_argument("file", help = "Path to the file you want to parse.")
    ap.add_argument("-f", "--from", help = "Specify the format of your notes, i.e. gdocs or org")
    ap.add_argument("-f", "--from", help = "Specify the format of your notes, i.e. gdocs or org")
    ap.add_argument("-f", "--from", help = "Specify the format of your notes, i.e. gdocs or org")
    args = ap.parse_args()

    from_gdoc(args.file)

main()
