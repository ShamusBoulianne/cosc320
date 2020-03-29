'''
Efficient Algorithm:

Eliminate common words from input and corpus.

--Run LCSS for each paragraph in input on each paragraph in corpus.

--If subsequence length passes threshold eliminate paragraph from corpus document 
and eliminate subsequence from input document.

--Add subsequence length to commonality score for corpus document.

--If the commonality score for corpus document passes threshold eliminate document 
from corpus and add it to output set.

--Run KMP for each sentence in input on each sentence in corpus.

--If a sentence match is found add sentence length to commonality score of corpus 
document and eliminate sentence from corpus document.

If the commonality score for corpus document passes threshold eliminate document 
from corpus and add it to output set.
        
'''