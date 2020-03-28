import re
from os import listdir

def efficient(file, lcs_threshold, commonality_threshold):
    #output will be a list of corpus files from which the input file is plagiarized
    output = []
    ift = fileToString(file)
    ifp = getParagraphs(ift)
    corpus = [f for f in listdir('data/master') if f != file]
    for corpus_file in corpus:
        cft = fileToString(corpus_file)
        commonality = 0
        #run KMP on each corpus file with each input sentence as a pattern
        for paragraph in ifp:
            ifs = getSentences(paragraph)
            for sentence in ifs:
                #if a match is found add sentence length to commonality and remove sentence from cft
                if KMP(cft, sentence):
                    commonality += len(getWords(sentence))
                    cft = cft.replace(sentence, " ")
        if commonality >= commonality_threshold:
            #remove corpus_file from corpus and add it to output
            corpus.remove(corpus_file)
            output.append(corpus_file)
            continue
        #run LCS on each input-corpus paragraph pair
        cfp = getParagraphs(cft)
        for input_paragraph in cfp:
            for corpus_paragraph in ifp:
                lcs = LCS(corpus_paragraph, input_paragraph)
                if lcs >= lcs_threshold:
                    #eliminate paragraph from cfp
                    cfp.remove(corpus_paragraph)
                commonality += lcs
        if commonality >= commonality_threshold:
            #remove corpus_file from corpus and add it to output
            corpus.remove(corpus_file)
            output.append(corpus_file)
    return output


def bruteForce(file, threshold):
    #output will be a list of corpus files from which the input file is plagiarized
    output = []
    #split the input file into sentences
    ift = fileToString(file)
    ifp = getParagraphs(ift)
    ifs = []
    for paragraph in ifp:
        ifs.extend(getSentences(paragraph))
    #get all corpus files and split into sentences
    corpus = [f for f in listdir('data/master') if f != file]
    for corpus_file in corpus:
        cft = fileToString(corpus_file)
        cfp = getParagraphs(cft)
        cfs = []
        for paragraph in cfp:
            cfs.extend(getSentences(paragraph))
        #count the number of sentences each corpus file shares with the input file
        count = 0
        for input_sentence in ifs:
            for corpus_sentence in cfs:
                if input_sentence == corpus_sentence:
                    count += 1
        #if count of sentence matches meets or exceeds threshold add corpus file to output
        if count >= threshold:
            output.append(corpus_file)
    return output

#KMP and prefixFunction methods are adapted from CLSR pages 1005-1006
#Returns true if a match is found
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
            q = lps[q-1]
    return False


def prefixFunction(ptrn):
    M = len(ptrn)
    lps = [0]*M
    k = -1
    for i in range(2, M):
        while k >= 0 and ptrn[k] != ptrn[i]:
            k = lps[k]
        if ptrn[k] == ptrn[i]:
            k = k + 1
        lps[i] = k
    return lps

#LCS function is adapted from https://www.geeksforgeeks.org/python-program-for-longest-common-subsequence/
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
            if i == 0 or j == 0 : 
                L[i][j] = 0
            elif txt1[i-1] == txt2[j-1]: 
                L[i][j] = L[i-1][j-1]+1
            else: 
                L[i][j] = max(L[i-1][j], L[i][j-1]) 
    return L[M][N]

def fileToString(file):
    #get file contents as a string
    path = 'data/master/'
    f = open(path + file, 'r')
    try:
        contents = f.read()
    except:
        contents = ''
    return contents

#returns the paragraphs of a text
def getParagraphs(txt):
    delimiters = "\n{2,}|={2,}|-{2,}"
    paragraphs = re.split(delimiters, contents)
    return paragraphs


#returns the sentences in a paragraph
def getSentences(paragraph):
    delimiters = "\.|\?|!"
    sentences = [s.strip() for s in re.split(delimiters, paragraph) if len(s.split()) > 1]
    return sentences

def getWords(txt):
    delimiters = "\.|\?|!| |,|;|:|\'|\"|\n{2,}|={2,}|-{2,}"
    words = [w.strip() for w in re.split(delimiters, txt) if len(w) > 1 ]
    return words



# input_file = 'EXAMPLE-PLAGIARIZED-DOC.txt'
# threshold = 1
# print(bruteForce(input_file, threshold))

# paragraphs = getParagraphs('EXAMPLE-PLAGIARIZED-DOC.txt')
# for p in paragraphs:
#     print(getSentences(p))

