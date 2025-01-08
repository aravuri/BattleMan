import re
import string
import numpy as np
from functools import partial
from wordUtils import *
from hangmanGUI import *
import math

def entropy(wordRVList):
    return sum(list(map(lambda x: x.entropy(), wordRVList)))

def optimization(c, rv=None, rvTruth=None, p=0):
    queryRV = [rv[i].apply(query(c)) for i in range(len(rv))]
    def transition(i):
        def ret(input, output):
            if (output == input):
                return 1 - p*lieDistribution(rv, rvTruth, c, output)
            return p*lieDistribution(rv, rvTruth, c, output)*queryRV[i][output]/(1 - queryRV[i][input])
        return ret
                
    c = [Channel(list(queryRV[i].pdf.keys()), list(queryRV[i].pdf.keys()), transition(i)) for i in range(len(rv))]
    queryRVReal = [c[i].transformDistribution(queryRV[i]) for i in range(len(rv))]
    h = entropy(queryRVReal)
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

n = list(map(int,re.split(",\\s*",startCall(root))))
info = []

wordRV = [topRV(n[i], cutoff=1000000, sampling='frequency') for i in range(len(n))] # the distribution of words given that there have been either 0 or 1 lies so far.
wordRVTruth = [topRV(n[i], cutoff=1000000, sampling='frequency') for i in range(len(n))] # the distribution of words given that every statement so far has been true
pTruth = 1.0 # the probability that every statement so far has been true
count = 1
mistakes = 0
while entropy(wordRV) > 1E-3:
    if mistakes==7:
        break
    # guess a character
    #for rev in wordRV:
    #    rev.printPDF(n=3)
    c = possibleGuesses[np.argmax(np.array(list(map(partial(optimization, rv=wordRV, rvTruth=wordRVTruth, p = pTruth), possibleGuesses))))]
    
    outStr = [ch for ch in " ".join(["_"*n[i] for i in range(len(n))])]
    for (l, ans) in info:
        for i in range(len(ans)):
            if outStr[i]==" ":
                continue
            if outStr[i]==l and ans[i]=="_":
                outStr[i] = "_"
            if ans[i]!="_":
                outStr[i] = l

    # have them input where it is ("_a__a_")
    answer = guessCall(root, "".join(outStr), c, count, mistakes, wordRV)
    # removing hanged man because it really sucks now
    # if answer == "_"*len(answer): mistakes+=1
    #answer = input(f'{c}?\n')
    while len(answer.split(" ")) != len(n):
        answer = input("Invalid answer. Try again.\n")
    print(c, ': ', answer)
    info.append((c, answer))
    answer=answer.split(" ")

    # update word pdf
    # truthValue = wordRV.apply(queryResult(c, answer))
    # print(truthValue[False])
    pLieHere = pTruth * lieDistribution(wordRV, wordRVTruth, c, answer)
    wordRV = [wordRV[i].fuzzyCondition(wordRVTruth[i], query(c), answer[i], pLieHere) for i in range(len(n))]
    wordRVTruth = [wordRVTruth[i].condition(query(c), answer[i]) for i in range(len(n))]
    pTruth = pTruth - pLieHere
    # print(f'Current most likely word: {max(wordRV.pdf, key=wordRV.pdf.get)}, p={max(wordRV.pdf.values())}')
    count += 1
# print([len(list(wordRV[i].pdf.keys())) for i in range(len(n))])
if mistakes == 7 or 0 in [len(list(wordRV[i].pdf.keys())) for i in range(len(n))]:
    finishCall(root, "I failed.")
else:
    finishCall(root, f'The word is {" ".join([list(wordRV[i].pdf.keys())[0] for i in range(len(n))])}!')
