import infoTheoryUtils
import numpy as np
from scipy.ndimage import correlate


LEGAL_BOATS = [2,3,3,4,5]

CONV_KERNEL = np.zeros((5, 2, 5, 5))
for i, length in enumerate(LEGAL_BOATS):
    CONV_KERNEL[i, 0, -length:, -1] = 1
    CONV_KERNEL[i, 1, -1, -length:] = 1

# print(CONV_KERNEL)

# extending RV is really annoying if you're not using a dictionary, maybe I should have thought of that
class battleRV():

    # Probabilities: A 4d numpy array: (ship, orientation, x, y) -> probability that there is a ship with orientation rooted there
    def __init__(self, probabilities):
        self.probabilities = probabilities

    # returns a 3d numpy array: (ship, x, y) -> probability that there is a specific ship there (not necessarily rooted)
    def getShipHitDistribution(self):
        # convolve over each ship and orientation
        # vConvolve = np.vectorize(convolve(mode='constant'))
        # i'm using a for loop for now but i will try to replace it with a vectorized version bc funny
        ret = np.zeros(self.probabilities.shape)
        for i in range(len(LEGAL_BOATS)):
            # correlate is convolve but it doesn't flip
            ret[i, 0] = correlate(self.probabilities[i, 0], CONV_KERNEL[i, 0], mode='constant', origin=(2, 2))
            ret[i, 1] = correlate(self.probabilities[i, 1], CONV_KERNEL[i, 1], mode='constant', origin=(2, 2))

        # ignore orientation
        return ret.sum(axis=1)

        
    # returns a 2d numpy array: (x, y) -> probability of hit
    def getHitDistribution(self):
        # ignore ship
        return self.getShipHitDistribution().sum(axis=0)

    # state = 'hit' / 'miss'    
    def condition(self, x, y, state):
        kernel = translateKernel(x, y).astype(bool)
        
        hitSlice = np.where(kernel, self.probabilities, 0)
        missSlice = np.where(kernel, 0, self.probabilities)
        pHit = np.sum(hitSlice)

        if state == 'hit':
            for i in range(len(LEGAL_BOATS)):
                missSlice[i] = missSlice[i]/np.sum(missSlice[i])
            for i in range(len(LEGAL_BOATS)):
                self.probabilities[i] = (self.probabilities[i] - missSlice[i]*(1-pHit))/pHit
        elif state == 'miss':
            for i in range(len(LEGAL_BOATS)):
                missSlice[i] = missSlice[i]/np.sum(missSlice[i])
            self.probabilities = missSlice
        else:
            raise RuntimeError("oops")


def translateKernel(x, y):
    ret = np.pad(CONV_KERNEL, ((0, 0), (0, 0), (5, 10), (5, 10)))
    ret = np.roll(ret, x - 9, axis=2)
    ret = np.roll(ret, y - 9, axis=3)
    return ret[:, :, 0:10, 0:10]
