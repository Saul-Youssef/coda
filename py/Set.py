#
#    A data "Set" is an undordered collection of datas
#
from base import *
from Theorem import theorem
from Log import LOG
import multiprocessing

def Eval(S): return S.eval(100)
def eval100(S): return S.eval(100)
def eval10(S): return S.eval(10)
def eval1000(S): return S.eval(1000)
LOG.register('multi')

def multiEval(S,nproc=8):
    n = len(S)//nproc
    S_split = [T for T in S.split(n)]
    from multiprocessing.pool import Pool
    pool = Pool(nproc)
    results = []
    for result in pool.imap_unordered(Eval,S_split): results.append(result)
    return Space.sum(*results)

def pow(n,s,x):
    if    n==0: raise error('s^0 is not defined')
    elif  n==1: return s|x
    else      : return s|data(pow(n-1,s,x))

class Subset(object):
    def __init__(self): self._map = {}
    def __len__(self): return len(self._map)
    def __repr__(self): return str(len(self))
    def __iter__(self):
        for key,value in self._map.items(): yield key
    def set(self,d,D):
        self._map[d] = D
        return self
    def __getitem__(self,D): return self._map[D]
    def __add__(self,S):
        R = Subset()
        for D in self: R.set(D,self[D])
        for D in S   : R.set(D,   S[D])
        return R
    def multieval(self,eval,nproc=None):
        if nproc is None:
            nproc = multiprocessing.cpu_count()-4
        n = len(self)//nproc
        S_split = [T for T in self.split(n)]
        from multiprocessing.pool import Pool
        pool = Pool(nproc)
        results = []
        n = 0
        LOG('multi','Number of processors',str(nproc))
        for result in pool.imap_unordered(eval,S_split):
            n += 1
            LOG('multi',str(n)+'...')
            results.append(result)
        def f(s,t): return s+t
        from functools import reduce
        return reduce(f,results)
    def eval(self,maxiter):
        for d,D in self._map.items():
            i = 0
            while D.undecided() and i<maxiter: D,i = D.eval(),i+1
            self._map[d] = D
        return self
    def empty    (self): return Set(*[D for D in self if self[D].empty()])
    def atomic   (self): return Set(*[D for D in self if self[D].atomic()])
    def undecided(self): return Set(*[D for D in self if self[D].undecided()])
    def split(self,nmax):
        sub = Subset()
        for D in self:
            sub.set(D,self[D])
            if len(sub)>=nmax:
                yield sub; sub = Subset()
        if len(sub)>0: yield sub
    def sample(self,n):  # random subsample
        import random
        keys = self._map.keys()
        keys2 = random.sample(keys,n)
        sub = Subset()
        for key in keys2: sub.set(key,self[key])
        return sub

class Set(object):
    def __init__(self,*Ds): self._datas = Ds
    def __len__(self): return len(self._datas)
    def __repr__(self): return str(len(self))
    def __iter__(self):
        for D in self._datas: yield D
    def __add__(self,Ds): return Set(*[D for D in self]+[D for D in Ds])
    def __getitem__(self,i): return self._datas[i]
    def reduce(self):
        S = set([])
        for s in self: S.add(s)
        return Set(*[s for s in S])
    def equal(self,A,B): return data((da('=')+A)|B)
    def bin(self): return data(*[da('bin')|d for d in self])

    def eval(self,depth):
        import Evaluate
        L = []
        for D in self:
            D2,n = Evaluate.depth(D,depth)
            L.append(D2)
        return Set(*L)
    def subset (self,F): return Set(*[D for D in self if F(D)])
    def empty    (self): return self.subset(lambda D:D.empty())
    def atomic   (self): return self.subset(lambda D:D.atomic())
    def undecided(self): return self.subset(lambda D:not D.empty() and not D.atomic())

    def sample(self,n):
        import random
        return Set(*random.sample([D for D in self],n))

    def split(self,nmax):
        L = []
        for D in self:
            L.append(D)
            if len(L)>=nmax:
                yield Set(*L); L = []
        if len(L)>0: yield Set(*L)

    def theorem(self,X):
        sub = Subset()
        for s in self: sub.set(s,theorem(s,X))
        return sub
    def property(self,P,X):
        sub = Subset()
        for s in self: sub.set(s,theorem(data(P|s),X))
        return sub
    def nilpotent(self,n,X):
        sub = Subset()
        for s in self: sub.set(s,data(*[pow(n,s,x) for x in X]))
        return sub
    def involution(self,n,X):
        sub = Subset()
        for s in self: sub.set(s,data(*[self.eqco(data(pow(n,s,x)),x) for x in X]))
        return sub
    def eqco(self,A,B): return (da('=')+A)|B
    def idempotent(self,X):
        sub = Subset()
        for s in self: sub.set(s,data(*[self.eqco(data(s|data(s|x)),data(s|x)) for x in X]))
        return sub
    def distributive(self,X,Y):
        sub = Subset()
        for s in self:
            L = []
            for x in X:
                for y in Y: L.append( self.eqco( data(s|(x+y)) , (s|x)+(s|y) ) )
            sub.set(s,data(*L))
        return sub
    def space(self,X,Y):
        sub = Subset()
        for s in self:
            L = []
            for x in X:
                for y in Y: L.append( self.eqco( data(s|(x+y)) , data(s|((s|x)+(s|y))) ) )
            sub.set(s,data(*L))
        return sub
    def morphism(self,A,B,X):  # morphism from space A to space B
        sub = Subset()
        for F in self:
            for x in X: sub.set(F,self.eqco( self.eqco( data(F|data(A|x)) , data(B|data(F|x)) ) ))
        return sub
    def equivalence(self,X,Y,Z):
        sub = Subset()
        def f(s,x,y): return data((s+x)|y)
        def e(x,y): return self.eqco(x,y)
        for s in self:
            L = []
            for x in X:
                for y in Y:
                    L.append((s+x)|x)
                    L.append(e(f(s,x,y),f(s,y,x)))
                    for z in Z: L.append(e(f(s,x,y)+f(s,y,z),f(s,x,z)))
            sub.set(s,data(*L))
        return sub
#
#     in this context, a "pure ring" is data ring such that
#     ring A B : C = ring : (ring A : C ) (ring B : C) and
#     ring A : B C = ring : (ring A : B ) (ring A : C)
#
    def ring(self,A,B,C):
        sub = Subset()
        for ring in self:
            L = []
            for a in A:
                for b in B:
                    for c in C:
                        e1l = data((ring+a+b)|c    ); e1r = data( ring | ( ((ring+a)|c) + ((ring+b)|c) ) )
                        e2l = data((ring+a  )|(b+c)); e2r = data( ring | ( ((ring+a)|b) + ((ring+a)|c) ) )
                        L.append(self.eqco(e1l,e1r))
                        L.append(self.eqco(e2l,e2r))
            sub.set(ring,data(*L))
        return sub
