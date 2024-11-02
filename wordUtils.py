import wordfreq
from functools import partial
import re

def isValid(word, length):
    return re.search("^[a-z]*$", word) and len(word) == length

def top(wordLength, cutoff=10000):
    words = wordfreq.top_n_list('en', cutoff, wordlist='best')
    return list(filter(partial(isValid, length=wordLength), words));

def topPDFUniform(wordLength, cutoff=10000):
    arr = top(wordLength, cutoff);
    return dict(map(lambda word: (word, 1.0/len(arr)), arr))

def marginalPDFchar(wordPdf, c):
    ret = {}
    for word, prob in pdf.items():
        queryResult = re.sub(f'[^{c}]', "_", word)
        if queryResult in ret:
            ret[queryResult] += prob
        else:
            ret[queryResult] = prob
    return ret

def printPDF(pdf):
    for k,v in sorted(pdf.items(), key=lambda p:p[1], reverse=True):
        print(k,v)


pdf = topPDFUniform(7)
marginalPDF = marginalPDFchar(pdf, 'a')
printPDF(marginalPDF)