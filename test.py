import wordfreq
import re

words = wordfreq.top_n_list('en', 50000, wordlist='best')

def test(word):
    return re.search("^[a-z]*$", word) and len(word) == 7

arr=list(filter(test, words))
print(arr)