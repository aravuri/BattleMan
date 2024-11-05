from infoTheoryUtils import *

class hangRV(RV):
    def __init__(self, dic):
        RV.__init__(self, dic)
    # distribution of X| f(X)=value but fuzzily with probability prob of lying
    def fuzzyCondition(self, f, value, prob):
        ret1 = {}
        ret2 = {}
        ret={}
        for x, p in self.pdf.items():
            xPrime = f(x)
            if xPrime == value:
                ret1[x] = p
            else:
                ret2[x] = p
        for x, p in normalize(ret1).items():
            ret[x] = p*(1-prob)
        for x, p in normalize(ret2).items():
            ret[x] = p*prob
        ret = {x:ret[x] for x in ret if ret[x]}
        return hangRV(ret)

