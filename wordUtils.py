import wordfreq
from functools import partial
from hangUtils import *
import re

def isValid(word, length):
    return re.search("^[a-z]*$", word) and len(word) == length

def top(wordLength, cutoff=10000):
    words = wordfreq.top_n_list('en', cutoff, wordlist='best')
    return list(filter(partial(isValid, length=wordLength), words));

# p(word), sampling = uniform or frequency
def topRV(wordLength, cutoff=10000, sampling='uniform'):
    arr = top(wordLength, cutoff);
    if (sampling == 'uniform'):
        func = lambda word: (word, 1.0)
    elif (sampling == 'frequency'):
        func = lambda word: (word, wordfreq.word_frequency(word, 'en'))
    else:
        raise RuntimeError("oops")
    return hangRV(normalize(dict(map(func, arr))))

# returns a function that takes in a word and replaces everything in it that isn't a specific character with _.
def query(c):
    return lambda word: re.sub(f'[^{c}]', "_", word)

def queryResult(c, answer):
    return lambda word: re.sub(f'[^{c}]', "_", word) == answer