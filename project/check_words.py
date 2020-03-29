#!/usr/bin/python
import re
# source doc
src = "../data/master/EXAMPLE-PLAGIARIZED-DOC.txt" 
# reference doc
ref = "../data/1-1000.txt"
# remove all occurances of the n most common words
idx = "100"
with open(ref, "r") as fin:
    comm_words=[line.strip("\n").lower() for line in fin]
src_words = []
with open(src, "r") as fin:
    for line in fin:
        for word in line.split():
            word = word.lower()
            if not word in comm_words:
                src_words.append(word)