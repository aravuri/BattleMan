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

print(topPDFUniform(4))