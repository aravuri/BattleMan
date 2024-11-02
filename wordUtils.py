import wordfreq
from functools import partial
from math import log2
import re

def isValid(word, length):
    return re.search("^[a-z]*$", word) and len(word) == length

def top(wordLength, cutoff=10000):
    words = wordfreq.top_n_list('en', cutoff, wordlist='best')
    return list(filter(partial(isValid, length=wordLength), words));

# p(word)
def topPDFUniform(wordLength, cutoff=10000):
    arr = top(wordLength, cutoff);
    return dict(map(lambda word: (word, 1.0/len(arr)), arr))

# p(c?)
def marginalPDFchar(wordPDF, c):
    ret = {}
    for word, prob in wordPDF.items():
        queryResult = re.sub(f'[^{c}]', "_", word)
        if queryResult in ret:
            ret[queryResult] += prob
        else:
            ret[queryResult] = prob
    return ret

# p(word | c? = string)
def condition(wordPDF, c, string):
    ret = {}
    normConst = marginalPDFchar(wordPDF, c)[string]
    for word, prob in wordPDF.items():
        queryResult = re.sub(f'[^{c}]', "_", word)
        if queryResult == string:
            ret[word] = prob / normConst
    return ret

def printPDF(pdf):
    for k,v in sorted(pdf.items(), key=lambda p:p[1], reverse=True):
        print(k,v)

def entropy(pdf):
    return sum(-p*log2(p) for p in pdf.values())



# pdf = topPDFUniform(7)
# marginalPDF = marginalPDFchar(pdf, 'a')
# condPDF = condition(pdf, 'c', 'c______')
# printPDF(condPDF)
# print(entropy(pdf), entropy(marginalPDF), entropy(condPDF))