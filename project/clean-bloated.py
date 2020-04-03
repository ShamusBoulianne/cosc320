'''
This script is to clean out files that are too bloated and will slow down
the execution of the algorithm
'''
from os import listdir, remove
from project import removeCommonWords, getSentences, KMP, getParagraphs, LCS
from time import time
file='EXAMPLE-PLAGIARIZED-DOC.txt'
corpus = [f for f in listdir('data/master') if f != file]

file = removeCommonWords(file, 50)
for f in corpus:
    start = time()
    cft = removeCommonWords(f, 50)
    for s in getSentences(file):
        KMP(cft, s)
    ifp = getParagraphs(file)
    cfp = getParagraphs(f)
    for paragraph in ifp:
        for cparagraph in cfp:
            LCS(cparagraph,paragraph)
    end = time()
    if (end - start > 30):
        remove(f)