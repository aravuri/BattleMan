import re
import string
import numpy as np
from wordUtils import *

possibleGuesses = list(string.ascii_lowercase)

n = int(input("How many letters?\n"))
finished = False
info = []

wordPDF = topPDF(n, cutoff=100000, sampling='frequency')

while entropy(wordPDF) > 0:
    # guess a character
    c = possibleGuesses[np.argmax(np.array(list(map(lambda c: entropy(marginalPDFchar(wordPDF, c)), possibleGuesses))))]

    # have them input where it is ("_a__a_")
    answer = input(f'{c}?\n')
    while len(answer) != n or not re.match(f'^[{c}_]*$', answer):
        answer = input("Invalid answer. Try again.\n")
    
    info.append((c, answer))
    # print(info)

    # update word pdf
    wordPDF = condition(wordPDF, c, answer)
    print(f'Current most likely word: {max(wordPDF, key=wordPDF.get)}, p={max(wordPDF.values())}')
    
print(f'The word is: {list(wordPDF.keys())[0]}')
