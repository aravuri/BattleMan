import re
import string
import numpy as np
from functools import partial
from wordUtils import *
from hangmanGUI import *

def optimization(c, rv=None):
    queryRV = rv.apply(query(c))
    h = queryRV.entropy()
    # classic floating point precision
    if abs(h) <= 1e-9:
        return 0
    if abs(queryRV['_'*n]) <= 1e-9:
        return float('inf')
    return h/queryRV['_'*n]

root = initGUI()

possibleGuesses = list(string.ascii_lowercase)

n = int(startCall(root))
finished = False
info = []

wordRV = topRV(n, cutoff=100000, sampling='frequency')
count = 1
mistakes = 0
while wordRV.entropy() > 0:
    if mistakes==11:
        break
    # guess a character
    c = possibleGuesses[np.argmax(np.array(list(map(partial(optimization, rv=wordRV), possibleGuesses))))]
    
    outStr = ["_"]*n
    for (l, ans) in info:
        for i in range(len(ans)):
            if ans[i]!="_":
                outStr[i] = l

    # have them input where it is ("_a__a_")
    answer = guessCall(root, "".join(outStr), c, count, mistakes, wordRV)
    if answer == "_"*len(answer): mistakes+=1
    #answer = input(f'{c}?\n')
    while len(answer) != n or not re.match(f'^[{c}_]*$', answer):
        answer = input("Invalid answer. Try again.\n")
    
    info.append((c, answer))
    # print(info)

    # update word pdf
    wordRV = wordRV.condition(query(c), answer)
    # print(f'Current most likely word: {max(wordRV.pdf, key=wordRV.pdf.get)}, p={max(wordRV.pdf.values())}')
    count += 1
if mistakes == 11 or len(list(wordRV.pdf.keys()))==0:
    finishCall(root, "I failed.")
else:
    finishCall(root, f'The word is {list(wordRV.pdf.keys())[0]}!')
