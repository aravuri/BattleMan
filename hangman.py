import re
import string
import numpy as np
from wordUtils import *
from hangmanGUI import *

root = initGUI()

possibleGuesses = list(string.ascii_lowercase)

n = int(startCall(root))
finished = False
info = []

wordRV = topRV(n, cutoff=100000, sampling='frequency')
count = 1
while wordRV.entropy() > 0:
    # guess a character
    c = possibleGuesses[np.argmax(np.array(list(map(lambda c: wordRV.apply(query(c)).entropy()/wordRV.apply(query(c))['_'*n], possibleGuesses))))]
    
    outStr = ["_"]*n
    for (l, ans) in info:
        for i in range(len(ans)):
            if ans[i]!="_":
                outStr[i] = l

    # have them input where it is ("_a__a_")
    answer = guessCall(root, "".join(outStr), c, count, wordRV)
    #answer = input(f'{c}?\n')
    while len(answer) != n or not re.match(f'^[{c}_]*$', answer):
        answer = input("Invalid answer. Try again.\n")
    
    info.append((c, answer))
    # print(info)

    # update word pdf
    wordRV = wordRV.condition(query(c), answer)
    # print(f'Current most likely word: {max(wordRV.pdf, key=wordRV.pdf.get)}, p={max(wordRV.pdf.values())}')
    count += 1
finishCall(root,f'The word is {list(wordRV.pdf.keys())[0]}!')
