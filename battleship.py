import numpy as np
from battleshipUtils import *
np.set_printoptions(precision=3)


probabilities = np.zeros((len(LEGAL_BOATS), 2, 10, 10))
for i, length in enumerate(LEGAL_BOATS):
    probabilities[i, 0, 0:1-length, :] = 1/(10*(10-length+1))*0.5
    probabilities[i, 1, :, 0:1-length] = 1/(10*(10-length+1))*0.5

def inputCoordsSwitch(x,y):
    return (11-x, 11-y)

def argmaxArrayNotInQueries(a, q):
    maxVal = float('-inf')
    ret=(0,0)
    for i in range(len(a)):
        for j in range(len(a[i])):
            if (i,j) not in q and a[i,j]>maxVal:
                maxVal=a[i,j]
                ret=(i,j)
    return ret
shipRV = battleRV(probabilities)
#print(shipRV.probabilities)
#print(shipRV.getShipHitDistribution())
#print(shipRV.getHitDistribution())
remainingShips=[1,1,1,1,1]
previousQueries=[]
while 1 in remainingShips:
    print(remainingShips)
    (x,y)= argmaxArrayNotInQueries(shipRV.getHitDistribution(), previousQueries) #(np.unravel_index(shipRV.getHitDistribution().argmax(),(10,10))[i].item() for i in [0,1])
    previousQueries.append((x,y))
    result = (input("Hit at "+str(inputCoordsSwitch(x,y))+"? Answer y or n.")=="y")
    if result:
        shipRV.condition(x,y,'hit')
        shipSunk = int(input("Sunk ship? 0 if nothing sunk otherwise size of ship."))
        if shipSunk==2:
            remainingShips[0]=0
        elif shipSunk==3:
            if remainingShips[1]==1:
                remainingShips[1]=0
            else:
                remainingShips[2]=0
        elif shipSunk==4:
            remainingShips[3]=0
        elif shipSunk==5:
            remainingShips[4]=0
        elif shipSunk!=0:
            print("what are you doing")
    else:
        shipRV.condition(x,y,'miss')

#shipRV.condition(4, 4, 'miss')
# print(shipRV.probabilities)
# print(shipRV.getShipHitDistribution())
# print(shipRV.getHitDistribution())

#shipRV.condition(5, 4, 'hit')
# print(shipRV.probabilities)
# print(shipRV.getShipHitDistribution())
# print(shipRV.getHitDistribution())

# guess(0, 3, guesses, game)
# guess(0, 4, guesses, game)

# guess(2, 0, guesses, game)
# guess(3, 0, guesses, game)
# guess(4, 0, guesses, game)

# guess(3, 8, guesses, game)
# guess(4, 8, guesses, game)
# guess(5, 8, guesses, game)
# guess(6, 8, guesses, game)
 

