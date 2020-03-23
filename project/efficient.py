#KMP and prefixFunction methods are adapted from CLSR pages 1005-1006
#KMP returns true if a match is found
def KMP(txt, ptrn):
    txt = txt.split()
    ptrn = ptrn.split()
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


import re
#returns the paragraphs of a text file
def getParagraphs(file):
    #get file contents as a string
    path = 'data/master/'
    f = open(path + file, 'r')
    try:
        contents = f.read()
    except:
        contents = ''
    #split contents on specified delimiters
    delimiters = "\n{2,}|={2,}|-{2,}"
    paragraphs = re.split(delimiters, contents)
    return paragraphs


#print(KMP("ab aba ba b bc ab ba bc bb ac", "b")) #test KMP
#print(LCS(getParagraphs('EXAMPLE-PLAGIARIZED-DOC.txt'), getParagraphs('hayes.txt'))) #test LCS