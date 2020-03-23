import re
from os import listdir


def bruteForce(file, threshold):
    #output will be a list of corpus files from which the input file is plagiarized
    output = []
    #split the input file into sentences
    ifp = getParagraphs(file)
    ifs = []
    for paragraph in ifp:
        ifs.extend(getSentences(paragraph))
    #get all corpus files and split into sentences
    corpus = [f for f in listdir('data/master') if f != file]
    for corpus_file in corpus:
        cfp = getParagraphs(corpus_file)
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


#returns the sentences in a paragraph
def getSentences(paragraph):
    delimiters = "\.|\?|!"
    sentences = [s.strip() for s in re.split(delimiters, paragraph) if len(s.split()) >= 2]
    return sentences

input_file = 'EXAMPLE-PLAGIARIZED-DOC.txt'
threshold = 1
print(bruteForce(input_file, threshold))
# paragraphs = getParagraphs('EXAMPLE-PLAGIARIZED-DOC.txt')
# for p in paragraphs:
#     print(getSentences(p))
