import re
import string
import numpy as np
from functools import partial
from wordUtils import *
from hangmanGUI import *
import math

def optimization(c, rv=None, rvTruth=None, p=0):
    queryRV = rv.apply(query(c))

    def transition(input, output):
        if (output == input):
            return 1 - p*lieDistribution(rv, rvTruth, c, output)
        return p*lieDistribution(rv, rvTruth, c, output)*queryRV[output]/(1 - queryRV[input])
            
    c = Channel(list(queryRV.pdf.keys()), list(queryRV.pdf.keys()), transition)
    queryRVReal = c.transformDistribution(queryRV)
    h = queryRVReal.entropy()
    # classic floating point precision

    # def cost(queryValue):
    #     if queryValue == '_'*n:
    #         return 1
    #     else:
    #         return p*lieDistribution(rv, rvTruth, c, queryValue)

    # prob = rv.apply(cost).expectation()
    prob = 1
    if abs(h) <= 1e-9:
        return 0
    if abs(prob) <= 1e-9:
        return float('inf')
    return h/prob

    # going back to regular entropy for now
    # return queryRV.entropy()

# the probability that you will lie, given that you are able to.
def lieDistribution(rv, rvTruth, c, answer):
    # rate = 1000
    # p = np.exp(-rate)*rate**n/(math.factorial(n))
    # poisson sucks lol
    return 0.25

root = initGUI()

possibleGuesses = list(string.ascii_lowercase)

n = int(startCall(root))
finished = False
info = []

wordRV = topRV(n, cutoff=100000, sampling='frequency') # the distribution of words given that there have been either 0 or 1 lies so far.
wordRVTruth = topRV(n, cutoff=100000, sampling='frequency') # the distribution of words given that every statement so far has been true
pTruth = 1.0 # the probability that every statement so far has been true
count = 1
mistakes = 0
while wordRV.entropy() > 1E-3:
    print(wordRV.entropy())
    if mistakes==7:
        break
    # guess a character
    c = possibleGuesses[np.argmax(np.array(list(map(partial(optimization, rv=wordRV, rvTruth=wordRVTruth, p = pTruth), possibleGuesses))))]
    
    outStr = ["_"]*n
    for (l, ans) in info:
        for i in range(len(ans)):
            if outStr[i]==l and ans[i]=="_":
                outStr[i] = "_"
            if ans[i]!="_":
                outStr[i] = l

    # have them input where it is ("_a__a_")
    answer = guessCall(root, "".join(outStr), c, count, mistakes, wordRV)
    # removing hanged man because it really sucks now
    # if answer == "_"*len(answer): mistakes+=1
    #answer = input(f'{c}?\n')
    while len(answer) != n or not re.match(f'^[{c}_]*$', answer):
        answer = input("Invalid answer. Try again.\n")

    print(c, ': ', answer)
    info.append((c, answer))
    # print(info)

    # update word pdf
    # truthValue = wordRV.apply(queryResult(c, answer))
    # print(truthValue[False])
    pLieHere = pTruth * lieDistribution(wordRV, wordRVTruth, c, answer)
    wordRV = wordRV.fuzzyCondition(wordRVTruth, query(c), answer, pLieHere)
    wordRVTruth = wordRVTruth.condition(query(c), answer)
    pTruth = pTruth - pLieHere
    # print(f'Current most likely word: {max(wordRV.pdf, key=wordRV.pdf.get)}, p={max(wordRV.pdf.values())}')
    count += 1
if mistakes == 7 or len(list(wordRV.pdf.keys()))==0:
    finishCall(root, "I failed.")
else:
    finishCall(root, f'The word is {list(wordRV.pdf.keys())[0]}!')
