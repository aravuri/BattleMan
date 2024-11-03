import wordfreq
from functools import partial
from math import log2
import re

def isValid(word, length):
    return re.search("^[a-z]*$", word) and len(word) == length

def top(wordLength, cutoff=10000):
    words = wordfreq.top_n_list('en', cutoff, wordlist='best')
    return list(filter(partial(isValid, length=wordLength), words));

# p(word), sampling = uniform or frequency
def topPDF(wordLength, cutoff=10000, sampling='uniform'):
    arr = top(wordLength, cutoff);
    if (sampling == 'uniform'):
        func = lambda word: (word, 1.0)
    elif (sampling == 'frequency'):
        func = lambda word: (word, wordfreq.word_frequency(word, 'en'))
    else:
        raise RuntimeError("oops")
    return normalize(dict(map(func, arr)))

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
    for word, prob in wordPDF.items():
        # replaces everything that isn't c with '_'
        queryResult = re.sub(f'[^{c}]', "_", word)
        if queryResult == string:
            ret[word] = prob
    return normalize(ret)

def printPDF(pdf):
    for k,v in sorted(pdf.items(), key=lambda p:p[1], reverse=True):
        print(k,v)

def entropy(pdf):
    return sum(-p*log2(p) for p in pdf.values())

def normalize(pdf):
    norm = sum(pdf.values())
    return {x: p/norm for x, p in pdf.items()}



# pdf = topPDF(7, 100000, 'frequency')
# marginalPDF = marginalPDFchar(pdf, 'a')
# condPDF = condition(pdf, 'c', 'c______')
# printPDF(pdf)
# print(entropy(pdf), entropy(marginalPDF), entropy(condPDF))