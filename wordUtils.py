import wordfreq
import re

def isValid(word, length):
    return re.search("^[a-z]*$", word) and len(word) == length

def top(cutoff, wordLength):
    words = wordfreq.top_n_list('en', cutoff, wordlist='best')
    return list(filter(lambda w: isValid(w, wordLength), words));