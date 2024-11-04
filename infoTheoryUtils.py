from math import log2

# Represents a random variable, X.
class RV:
    # dict: a mapping from an object to a probability
    def __init__(self, dict):
        self.pdf = dict
        pass

    # P(X = x)
    def __getitem__(self, x):
        return self.pdf[x]

    def printPDF(self):
        for x,p in sorted(self.pdf.items(), key=lambda p:p[1], reverse=True):
            print(x,p)
    
    # Gets the distribution of f(X).
    def apply(self, f):
        ret = {}
        for x, p in self.pdf.items():
            xPrime = f(x)
            if xPrime in ret:
                ret[xPrime] += p
            else:
                ret[xPrime] = p
        return RV(ret)
    
    # Gets the distribution of X | f(X) = value
    def condition(self, f, value):
        ret = {}
        for x, p in self.pdf.items():
            xPrime = f(x)
            if xPrime == value:
                ret[x] = p
        return RV(normalize(ret))
    
    # Gets H(X)
    def entropy(self):
        return sum(-p*log2(p) for x, p in self.pdf.items())
    
    # Gets H(X | f(X))
    def conditionalEntropy(self, f):
        y = self.apply(f)
        return sum(-p*log2(p/y[f(x)]) for x, p in self.pdf.items())
        



def normalize(pdf):
    norm = sum(pdf.values())
    return {x: p/norm for x, p in pdf.items()}


