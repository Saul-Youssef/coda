#
#    Data with a capital D is a collection of lower case data.
#    This has various operations related to search and classification.
#
from base import *

def logic(D):
    if D.empty(): return 'true'
    if D.atomic(): return 'false'
    return 'undecided'
def equal(A,B): return data((da('=')+A)|B)

class Data(object):
    def __init__(self,*Ds):
        self._datas = Ds
        self._codas = set([])
        for d in Ds:
            for c in d: self._codas.add(c)
        self._evals = {}
        self._logic = {}
        for d in Ds: self._logic[d] = logic(d)
        self._depth = 0
        self._evaluated = len(Ds)==0 
    def space(self,width,depth):
        return Data(*[d for d in alldata(width,depth)]) 
    def __repr__(self):
        nt,nf,nu = self.lstat()
        return 'true: '+str(nt)+', false:'+str(nf)+', undecided:'+str(nu)+', codas:'+str(len(self._codas))+', datas:'+str(len(self._datas))
    def __iter__(self):
        for D in self._datas: yield D
    def __getitem__(self,i): return self._datas[i]
    def __len__(self): return len(self._datas)
    def evaluated(self): return self._evaluated
    def eval(self,depth,nproc):
        import Evaluate
        self._logic,self._evals = {},{} 
        for D in self:  # do this in parallel!
            D2,n = Evaluate.depth(D,depth)
            self._evals[D] = D2
            self._logic[D] = logic(D2)
        self._depth = depth
        self._evaluated = True 
        return self
    def lstat(self):
        ntrue,nfalse,nundecided = 0,0,0
        for D,result in self._logic.items():
            if   result=='false': nfalse     += 1
            elif result=='true' : ntrue      += 1
            else                : nundecided += 1
        return ntrue,nfalse,nundecided
    def distance(self,D):
        if len(self)==0 or len(D)==0: raise error('Distance from empty Data is undefined')
        st,sf,su = self.lstat()
        dt,df,du =    D.lstat()
        LD = st*(df+du)+sf*(dt+du)+su*(dt+df) # of pairs (s,d) where logic(s)!=logic(d)
        return float(LD)/float(len(self)*len(D))
    def idempotent(self,d):
        L = []
        for D in self:
            i1 = data(d|D)
            i2 = data(d|i1)
            L.append(equal(i1,i2))
        return Data(*L)
    def distributive(self,d):
        L = []
        for A in self:
            for B in self:
                l = data(d|(A+B))
                r = data(d|A) + data(d|B)
                L.append(equal(l,r))
        return Data(*L)
    def category(self,d):
        L = []
        for A in self:
            for B in self:
                l = data(d|(A+B))
                r = data(d|A) + data(d|B)
                rr = data(d|r)
                L.append(equal(l,rr))
        return Data(*L)
    def classify(self,d): return Data(*[data(d|D) for D in self])
    def logic(self):
        t,f,u = self.lstat()
        if t>0 and f>0:
            return 'mixed'
        elif t==0:
            if u==0: return 'false'
            else   : return 'nevertrue'
        elif f==0:
            if u==0: return 'true'
            else   : return 'neverfalse'
        else:
            return 'undecided'
    def __or__(self,Bs):
        L = []
        for A in self:
            for B in Bs: L.append(data(A|B))
        return Data(*L)
    def __add__(self,Bs): return Data(*([A for A in self]+[B for B in Bs]))
#
#     Generate one definition at random
#
    def genDef(self):
        import random
        codas = [c for c in self._codas if not c in CONTEXT]
        datas = [d for d in self._datas] 
        print(len(codas),len(datas))
        c = random.choice(codas)
        d = random.choice(datas)
        return c,d

import itertools

def alldata(width,depth):  # all data leq specified width and depth
    datas = []
    if depth==0:
        datas.append(data())
    else:
        codas = [c for c in allcoda(width,depth)]
        for w in range(0,width+1):
            for T in itertools.product(codas,repeat=w): datas.append(data(*T))
    return datas

def allcoda(width,depth):
    codas = []
    if depth==0:
        return (coda(data(),data()),)
    else:
        datas = [d for d in alldata(width,depth-1)]
        for T in itertools.product(datas,repeat=2): codas.append(coda(T[0],T[1]))
    return codas
