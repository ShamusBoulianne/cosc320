import re
from os import listdir, remove
from time import time

def efficient(file, lcs_threshold, commonality_threshold):
    # output will be a list of corpus files from which the input file is plagiarized
    output = []
    n_most_common = 50
    ift = removeCommonWords(file, n_most_common)
    corpus = [f for f in listdir('data/master') if f != file]
    for corpus_file in corpus:
        print(corpus_file)
        cft = removeCommonWords(corpus_file, n_most_common)
        commonality = 0
        
        # run KMP on each corpus file with each input sentence as a pattern
        for sentence in getSentences(ift):
            # if a match is found add sentence length to commonality and remove sentence from cft
            if KMP(cft, sentence):
                commonality += len(getWords(sentence))
                if commonality >= commonality_threshold:
                    break
                cft = cft.replace(sentence, " ")
        if commonality >= commonality_threshold:
            # add corpus file to output
            output.append(corpus_file)
            continue
        
        # run LCS on each input-corpus paragraph pair
        ifp = getParagraphs(ift)
        cfp = getParagraphs(cft)
        for input_paragraph in ifp:
            for corpus_paragraph in cfp:
                lcs = LCS(corpus_paragraph, input_paragraph)
                if lcs >= lcs_threshold:
                    commonality += lcs
                    if commonality >= commonality_threshold:
                        break
        if commonality >= commonality_threshold:
            # add corpus_file to output
            output.append(corpus_file)
    return output


def bruteForce(file, threshold):
    # output will be a list of corpus files from which the input file is plagiarized
    output = []
    # split the input file into sentences
    ift = fileToString(file)
    ifp = getParagraphs(ift)
    ifs = []
    for paragraph in ifp:
        ifs.extend(getSentences(paragraph))
    # get all corpus files and split into sentences
    corpus = [f for f in listdir('data/master') if f != file]
    for corpus_file in corpus:
        cft = fileToString(corpus_file)
        cfp = getParagraphs(cft)
        cfs = []
        for paragraph in cfp:
            cfs.extend(getSentences(paragraph))
        # count the number of sentences each corpus file shares with the input file
        count = 0
        for input_sentence in ifs:
            for corpus_sentence in cfs:
                if input_sentence == corpus_sentence:
                    count += 1
        # if count of sentence matches meets or exceeds threshold add corpus file to output
        if count >= threshold:
            output.append(corpus_file)
    return output

# KMP and prefixFunction methods are adapted from CLSR pages 1005-1006
# Returns true if a match is found
def KMP(txt, ptrn):
    txt = getWords(txt)
    ptrn = getWords(ptrn)
    N = len(txt)
    M = len(ptrn)
    lps = prefixFunction(ptrn)
    q = 0
    for i in range(N):
        while q > 0 and ptrn[q] != txt[i]:
            q = lps[q]
        if ptrn[q] == txt[i]:
            q = q + 1
        if q == M:
            #print("index = " + str(i-M+1)) #print index of match
            return True
            #q = lps[q-1] #for finding next match
    return False


def prefixFunction(ptrn):
    M = len(ptrn)
    lps = [0]*M
    k = -1
    for i in range(2, M):
        while k > 0 and ptrn[k] != ptrn[i]:
            k = lps[k]
        if ptrn[k] == ptrn[i]:
            k = k + 1
        lps[i] = k
    return lps

def RabinKarp(txt, ptrn, q):
    M = len(ptrn) 
    N = len(txt) 
    if(M>N):
        return False
    d = 256  #size of alphabet
    i = 0
    j = 0
    p = 0    # hash value for pattern 
    t = 0    # hash value for txt 
    h = 1
  
    # The value of h would be "pow(d, M-1)% q" 
    for i in range(M-1): 
        h = (h * d)% q 
  
    # Calculate the hash value of pattern and first window 
    # of text 
    for i in range(M): 
        p = (d * p + ord(ptrn[i]))% q 
        t = (d * t + ord(txt[i]))% q 
  
    # Slide the pattern over text one by one 
    for i in range(N-M + 1): 
        # Check the hash values of current window of text and 
        # pattern if the hash values match then only check 
        # for characters on by one 
        if p == t: 
            # Check for characters one by one 
            for j in range(M): 
                if txt[i + j] != ptrn[j]: 
                    break
  
            j+= 1
            # if p == t and pat[0...M-1] = txt[i, i + 1, ...i + M-1] 
            if j == M:
                return True
                #print("Pattern found at index " + str(i)) 
  
        # Calculate hash value for next window of text: Remove 
        # leading digit, add trailing digit 
        if i < N-M: 
            t = (d*(t-ord(txt[i])*h) + ord(txt[i + M]))% q 
  
            # We might get negative values of t, converting it to 
            # positive 
            if t < 0: 
                t = t + q
    return False

# LCS function is adapted from https://www.geeksforgeeks.org/python-program-for-longest-common-subsequence/
def LCS(txt1, txt2):
    txt1 = getWords(txt1)
    txt2 = getWords(txt2)
    # find the length of the strings
    M = len(txt1)
    N = len(txt2)
    # declaring the array for storing the dp values
    L = [[None]*(N + 1) for i in range(M + 1)]
    for i in range(M + 1):
        for j in range(N + 1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif txt1[i-1] == txt2[j-1]:
                L[i][j] = L[i-1][j-1]+1
            else:
                L[i][j] = max(L[i-1][j], L[i][j-1])
    return L[M][N]


def removeCommonWords(file, n):
    # remove all occurances of the n most common words
    ref = "data/1-1000.txt"
    comm_words = []
    with open(ref, "r") as fin:
        count = 0
        for word in fin:
            comm_words.append(word.strip())
            count += 1
            if (count >= n):
                break
    keep_words = ""
    lines = []
    with open('data/master/' + file, "r") as fin:
        try:
            lines = fin.readlines()
        except:
            return "this file contains an unknown character"
    for line in lines:
        if line == "\n":
            keep_words += line + '\n'
        else:
            for word in getWords(line):
                word = word.lower()
                if not word in comm_words:
                    keep_words += " " + word
    return keep_words

def fileToString(file):
    # get file contents as a string
    path = 'data/master/'
    with open(path + file, 'r') as f:
        try:
            contents = f.read()
        except:
            contents = ''
    return contents

# returns the paragraphs of a text


def getParagraphs(txt):
    delimiters = "\n{2,}|={2,}|-{2,}"
    paragraphs = re.split(delimiters, txt)
    return paragraphs


# returns the sentences in a paragraph
def getSentences(paragraph):
    delimiters = "\.|\?|!|\n{2,}|={2,}|-{2,}"
    sentences = [s.strip() for s in re.split(
        delimiters, paragraph) if len(s.split()) > 1]
    return sentences


def getWords(txt):
    delimiters = "\.|\?|!| |,|;|:|\'|\"|\*"
    words = [w.strip() for w in re.split(delimiters, txt) if len(w) > 1]
    return words


print('running:')
input_file = 'EXAMPLE-PLAGIARIZED-DOC.txt'
sentence_threshold = 5
print(bruteForce(input_file, sentence_threshold))
lcs_threshold = 20
commonality_threshold = 50
print(efficient(input_file, lcs_threshold, commonality_threshold))
#print(removeCommonWords('asp9301.txt', 50))
print('done')
