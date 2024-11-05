from math import log2
import numpy as np

# Represents a random variable, X.
class RV:
    # dict: a mapping from an object to a probability
    def __init__(self, dict):
        self.pdf = dict

    # P(X = x)
    def __getitem__(self, x):
        if x in self.pdf.keys():
            return self.pdf[x]
        return 0
            

    # gets a string the n most likely values
    def topString(self, n=1000):
        return '\n'.join(list(map(lambda pair: f'{pair[0]}, p={pair[1]}', sorted(self.pdf.items(), key=lambda p:p[1], reverse=True)[0:n])))

    # prints the n most likely values
    def printPDF(self, n=1000):
        for x,p in sorted(self.pdf.items(), key=lambda p:p[1], reverse=True)[0:n]:
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
    
    # E[X]
    def expectation(self):
        return sum(x*p for x, p in self.pdf.items())
    

# Represents a channel taking X to Y
class Channel:

    # inputSet = sampleSpace(X)
    # outputSet = sampleSpace(Y) 
    # transitionFunction(x ϵ sampleSpace(X), y ϵ sampleSpace(Y)) = P(Y=y | X=x)
    def __init__(self, inputSet: list, outputSet: list, transitionFunction: function):
        self.inputSet = inputSet
        self.inputCode = {k: v for v, k in enumerate(inputSet)}
        self.outputSet = outputSet
        self.outputCode = {k: v for v, k in enumerate(outputSet)}
        self.transitionMatrix = np.fromfunction(lambda inId, outId: transitionFunction(inputSet[inId], outputSet[outId]), (len(inputSet), len(outputSet)))
    
    # type = input or output
    def vectorizeRV(self, rv: RV, type: str):
        if type == 'input':
            code = self.inputCode
            set = self.inputSet
        elif type == 'output':
            code = self.outputCode
            set = self.outputSet
        
        codeRV = rv.apply(lambda x: self.code[x])
        return np.array([codeRV[i] for i in range(len(self.set))])
    
    def devectorizeRV(self, vector: np.ndarray, type: str):
        if type == 'input':
            code = self.inputCode
            set = self.inputSet
        elif type == 'output':
            code = self.outputCode
            set = self.outputSet
        
        return RV({set[id]: p for id, p in enumerate(vector)})


    def transformDistribution(self, inputRV: RV):
        inputVector = self.vectorizeRV(inputRV, type='input')
        outputVector = self.transitionMatrix * inputVector
        return self.devectorizeRV(outputVector, type='output')
        
        
        

        


    

        



def normalize(pdf):
    norm = sum(pdf.values())
    return {x: p/norm for x, p in pdf.items()}
