from math import log2

# Represents a random variable.
class RV:
    def __init__(self, dict):
        self.pdf = dict
        pass

    def printPDF(self):
        for k,v in sorted(self.pdf.items(), key=lambda p:p[1], reverse=True):
            print(k,v)

    def entropy(self):
        return sum(-p*log2(p) for p in self.pdf.values())
    
    # Treating this as the distribution of X, gets the distribution of f(X).
    def marginal(self, f):
        ret = {}
        for x, p in self.pdf.items():
            xPrime = f(x)
            if xPrime in ret:
                ret[xPrime] += p
            else:
                ret[xPrime] = p
        return RV(ret)
    
    # Treating this as the distribution of X, gets the distribution of X | f(X) = value
    def condition(self, f, value):
        ret = {}
        for x, p in self.pdf.items():
            xPrime = f(x)
            if xPrime == value:
                ret[x] = p
        return RV(normalize(ret))


def normalize(pdf):
    norm = sum(pdf.values())
    return {x: p/norm for x, p in pdf.items()}


