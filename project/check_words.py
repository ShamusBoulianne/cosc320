#!/usr/bin/python
import re
# source doc
src = "data/master/EXAMPLE-PLAGIARIZED-DOC.txt" 
# reference doc
ref = "data/1-1000.txt" 
# remove all occurances of the n most common words
idx = "100"
# path to outwritten file
out = "data/"
# read common words into an array for later
with open(ref, "r") as fin:
    comm_words=[line.strip("\n").lower() for line in fin]
# split on paragraphs
delimiters = r"\n{2,}|={2,}|-{2,}"
with open(src,"r") as fin:
    contents = fin.read()
    paragraphs = re.split(delimiters, contents)
# remove common words from each paragraph
for paragraph in paragraphs:
    src_words = [word for word in paragraph.split(" ") 
                 if not word.lower() in comm_words]
    paragraph = " ".join(src_words)
# reform into original structure
with open(out + "cleaned.txt","w") as fout:
    for paragraph in paragraphs:
        fout.write(paragraph)
        fout.write("\n\n")