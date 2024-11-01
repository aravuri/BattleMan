import numpy as np

# game1 = np.zeros((10,10))
# game2 = np.zeros((10,10))

LEGAL_BOATS = [2,3,3,4,5]

def printBoard(arr):
    for i in range(len(arr)):
        print(arr[i])


game = [[0,0,0,1,1,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[2,0,0,0,0,0,0,0,0,0],[2,0,0,0,0,0,0,0,4,0],[2,0,0,0,0,0,0,0,4,0],[0,0,0,0,0,0,0,0,4,0],[0,0,3,3,3,0,0,0,4,0],[0,0,0,0,0,0,0,0,0,0],[0,5,5,5,5,5,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]
remainingShips = [1,2,3,4,5]
printBoard(game)

guesses=np.zeros((10,10),dtype=int)

def guess(x, y, guesses, game):
    print("Guessing ("+str(x)+","+str(y)+")!")
    guesses[x][y]=1
    if game[x][y]!=0:
        game[x][y]=6
    printBoard(game) 
    checkShips(remainingShips, game)
    print("Remaining ships:"+str(remainingShips))
def checkShips(remainingShips, game):
    for n in remainingShips:
        if n not in np.array(game).flatten():
            print(str(n)+" is down!")
            remainingShips.remove(n)
            break


guess(0, 3, guesses, game)
guess(0, 4, guesses, game)

guess(2, 0, guesses, game)
guess(3, 0, guesses, game)
guess(4, 0, guesses, game)

guess(3, 8, guesses, game)
guess(4, 8, guesses, game)
guess(5, 8, guesses, game)
guess(6, 8, guesses, game)
 

