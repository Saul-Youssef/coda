

from base import *
import Evaluate 

class Status(object):
    def __init__(self,datas,depth):
        self._depth = depth
        self._datas = datas
        self._true,self._false,self._undecided = 0,0,0
    def result(self):
        res = Result()
        for d in self._datas:
            D,n = Evaluate.depth(d,self._depth)
            res.update(D)
            if res.mixed(): break
        return res 

class Result(object):
    def __init__(self):
        self._true  = 0
        self._false = 0
        self._undecided = 0
    def update(self,D):
        if   D.atomic(): self._false += 1
        elif D.empty() : self._true += 1
        else           : self._undecided += 1
    def      mixed(self): return self._true>0 and self._false>0
    def neverFalse(self): return self._false==0
    def  neverTrue(self): return self._true==0
    def       true(self): return self._true>0 and self._false==0 and self._undecided==0
    def      false(self): return self._false>0 and self._true==0 and self._undecided==0
    def  undecided(self): return self._true==0 and self._false==0 
    def __str__(self): return ', '.join([str(self._true),str(self._false),str(self._undecided)])
    def zen(self):
        if self.mixed(): return 'mixed'
        if self.neverFalse(): return 'never false'
        if self.neverTrue(): return 'never true'
        if self.true(): return 'true'
        if self.false(): return 'false'
        if self.undecided(): return 'undecided'

def equal(A,B): return data((da('=')+A)|B)

class Idempotents(object):
    def __init__(self,candidates,ambients,depth=100):
        self._candidates = candidates
        self._ambients   = ambients
        self._result = {}
        self._depth = depth
    def query(self,c,a): return equal(data(c|data(c|a)),data(c|a))
    def search(self):
        n = 0
        for c in self._candidates:
            n += 1 
            if 10*(n//10)==n: print(n,'...',str(self))
            datas = [self.query(c,a) for a in self._ambients]
            self._result[c] = Status(datas,self._depth).result()
        return self
    def __str__(self):
        result = {}
        for c in self._candidates:
            if c in self._result: 
                res = self._result[c]
                z = res.zen()
                if not z in result: result[z] = 0
                result[z] += 1 
        return str(result)
            
import itertools

def alldata(depth,width):  # all data leq specified width and depth
    datas = []
    if depth==0:
        datas.append(data())
    else:
        codas = [c for c in allcoda(depth,width)]
        for w in range(0,width+1):
            for T in itertools.product(codas,repeat=w): datas.append(data(*T))
    return datas

def allcoda(depth,width):
    codas = []
    if depth==0:
        return (coda(data(),data()),)
    else:
        datas = [d for d in alldata(depth-1,width)]
        for T in itertools.product(datas,repeat=2): codas.append(coda(T[0],T[1]))
    return codas
#
#   Return the universe all data with width and depth less than
#   specified values.
#
#def universe(width,depth):
#    U = [data()]; T = U[:]
#    for i in range(depth):
#        T = G(T,width)
#        U.extend(T)
#    return U
#
#def G(L,width):
#    L2 = []
#    from itertools import product
#    for w in range(1,width+1):
#        for p in product(L,repeat=w): L2.append(data(*p))
#    return L2
#
