from infoTheoryUtils import *

class hangRV(RV):
    def __init__(self, dic):
        RV.__init__(self, dic)


    # distribution of X| f(X)=value but fuzzily with probability prob of lying; takes probabilities from truthDist if you are lying,
    # reflecting that only one statement can be a lie.
    def fuzzyCondition(self, truthDist, f, value, prob):
        ret1 = {}
        ret2 = {}
        ret={}
        for x in self.pdf.keys():
            xPrime = f(x)
            if xPrime == value:
                ret1[x] = self[x]
            else:
                ret2[x] = truthDist[x]
        ret1 = filterZeroes(ret1)
        ret2 = filterZeroes(ret2)
        if (len(ret1) != 0):
            for x, p in normalize(ret1).items():
                ret[x] = p*(1-prob)
        if (len(ret2) != 0):
            for x, p in normalize(ret2).items():
                ret[x] = p*prob

        # if it's impossible to lie or tell the truth, it might not be normalized.
        ret = normalize(filterZeroes(ret))
        return hangRV(ret)


def filterZeroes(dict):
    return {x:dict[x] for x in dict if dict[x]}