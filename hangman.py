import re

def guessChar(string):
    return "a"

n = int(input("How many letters?\n"))
finished = False
info = []


while not finished:
    # guess a character
    c = guessChar(info)

    # have them input where it is ("_a__a_")
    answer = input(f'{c}?\n')
    while len(answer) != n or not re.match(f'^[{c}_]*$', answer):
        answer = input("Invalid answer. Try again.\n")
    
    info.append((c, answer))
    print(info)
    