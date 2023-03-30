#
#    A "Space" is a collection of data.
#    This has various operations related to search and classification.
#
from base import *
import Evaluate
#
#    Multiprocessing Space list evaluation 
#
#def multiEval(SL,nprocs=8):
#    from multiprocessing.pool import Pool 
#    pool = Pool(nprocs)
#    results = []
#    for result in pool.imap_unordered(Eval,SL): results.append(result)
#    return results 

def multiEval(S,nproc=8):
    n = len(S)//nproc
    S_split = [T for T in S.split(n)]
    from multiprocessing.pool import Pool
    pool = Pool(nproc)
    results = []
    for result in pool.imap(Eval,S_split): results.append(result)
    return Space.sum(*results)

def logic(D):
    if D.empty(): return 'true'
    if D.atomic(): return 'false'
    return 'undecided'
def equal(A,B): return data((da('=')+A)|B)

def Eval(S): return S.eval(100) 

class Space(object):
    def __init__(self,*Ds):
        self._datas = Ds
        T = set([])
        for d in Ds:
            for c in d: T.add(c)
        self._codas = [c for c in T]
        self._evals = {}
        self._logic = {}
#        self._depth = 0
        self._evaluated = len(Ds)==0
    def __repr__(self):
        nt,nf,nu = self.lstat()
        return 'eval: '+str(self._evaluated)+', true: '+str(nt)+', false:'+str(nf)+', undecided:'+str(nu)+', codas:'+str(len(self._codas))+', datas:'+str(len(self._datas))
    def __iter__(self):
        for D in self._datas: yield D
    def sum(*Spaces):
#        Sum = Space(*Spaces)
        L = []
        for Sp in Spaces:
            for d in Sp: L.append(d)
        Sum = Space(*L)
        for S in Spaces:
            for d in S:
                Sum._evals[d] = S._evals[d]
                Sum._logic[d] = S._logic[d]
        Sum._evaluated = all([S.evaluated() for S in Spaces])
        T = set([])
        for d in Sum:
            for c in d: T.add(c)
        Sum._codas = [c for c in T]
        return Sum 
    def __add__(self,B): 
        return Space.sum(*[self,B]) 
#        T = Space(*([a for a in self]+[b for b in B]))
#        for t in T:
#            if   t in self._evals: 
#                T._evals[t] = self._evals[t]
#                T._logic[t] = self._logic[t]
#            elif t in    B._evals: 
#                T._evals[t] = B._evals[t]
#                T._logic[t] = B._logic[t]
#        if self.evaluated() and B.evaluated(): T._evaluated = True
#        return T 
    def codas(self):
        for co in self._codas: yield co
    def __getitem__(self,i): return self._datas[i]
    def __len__(self): return len(self._datas)
    def evaluated(self): return self._evaluated
#
#   Eval is the main computation, attempting to evaluate
#   each data in the space, in parallel on nthread threads
#   at most depth recursive attempts
#
    def eval(self,depth):
        import Evaluate
        self._logic,self._evals = {},{}
#
#       map version
#
        def EVAL(D):
            D2,n = Evaluate.depth(D,depth)
            return D,D2

        m = map(EVAL,self)
        for D,D2 in m:
            self._evals[D] = D2
            self._logic[D] = logic(D2)

#        for D in self:  # do this in parallel!
#            D2,n = Evaluate.depth(D,depth)
#            self._evals[D] = D2
#            self._logic[D] = logic(D2)

#        self._depth = depth
        self._evaluated = True
        return self
#
#   Logical statistics of the space.  This may change on
#   evaluation.
#
    def lstat(self):
        ntrue,nfalse,nundecided = 0,0,0
        for D,result in self._logic.items():
            if   result=='false': nfalse     += 1
            elif result=='true' : ntrue      += 1
            else                : nundecided += 1
        return ntrue,nfalse,nundecided

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
#
#   Logical distance measure from self to space S.
#   If you think of a (t,f,u) x (t,f,u) matrix, the distance
#   between self and S is the volume of the off diagonal elements
#   divided by the total volume.
#
#    def distance(self,S):
#        if len(self)==0 or len(S)==0: raise error('Distance from empty Space is undefined')
#        t1,f1,u1 = self.lstat()
#        t2,f2,u2 =    S.lstat()
#        offdiagonal = (t1*f2) + (t1*u2) + (f1*t2) + (f1*u2) + (u1*t2) + (u1*f2)
#        return float(offdiagonal)/float((t1+f1+u1)*(t2+f2+u2))
#
#   These methods select a sub-space of self with specified properties.
#
#       the subspace satisfying d:s = () for all s in S
#
    def subspace(self,sub):
        def SUB(s):
            if sub(s): return (s)
            else     : return ()

        m = map(SUB,self); L = []
        for t in m:
            for s in t: L.append(s)
        return Space(*L)

        L = []
        n = 0
        for s in self:
            n += 1
            if 100*(n//100)==n: print(n,'...','aaaa')
            if sub(s): L.append(s)
        return Space(*L)
#        return Space(*[s for s in self if sub(s)])
#    def subop(self,op,T):
#        def F(s): return all([op(s,t) for t in T])
#        return self.subspace(F)
    def subspace_two(self,two,T):
        def F(s): return all([two(s,t) for t in T])
        return self.subspace(F)
    def subspace_three(self,three,T):
        def F(s):
            b = True
            for t in T:
                for u in T:
                    b = three(s,t,u)
                    if not b: return b
        return self.subspace(F)
#
#     Generate one definition at random
#
    def sample(self):
        import random
        return random.sample(self._datas,1)[0]
    def data_sample(self,k):
        import random
        return random.sample(self._datas,k)
    def coda_sample(self,k):
        import random
        return random.sample(self._codas,k)
    def split(self,ndata):
        L = []
        for s in self:
            L.append(s)
            if len(L)>=ndata:
                yield Space(*L)
                L = []
        if len(L)>0: yield Space(*L)
#
#     Subspaces
#
    def     evals(self): return Space(*[e for s,e in self._evals.items()]) 
    def      true(self): return Space(*[s for s,e in self._evals.items() if e.empty()]) 
    def     false(self): return Space(*[s for s,e in self._evals.items() if e.atomic()]) 
    def undecided(self): return Space(*[s for s,e in self._evals.items() if not e.empty() and not e.atomic()]) 
    def apply(self,X):
        L = []
        for s in self:
            for x in X: L.append(data(s|x))
        return Space(*L)
    def idempotent(self,X):
        L = []
        for s in self:
            for x in X:
                L.append( equal( data(s|data(s|x)) , data(s|x) ) )
        return Space(*L)
    def distributive(self,X,Y):
        L = []
        for s in self:
            for x in X:
                for y in Y:
                    L.append( equal( data(s|(x+y)) , (s|x) + (s|y) ) )
        return Space(*L)
    def category(self,X,Y):
        L = []
        for s in self:
            for x in X:
                for y in Y:
                    L.append( equal( data(s|(x+y)) , data(s|((s|x)+(s|y))) ) )
        return Space(*L)
    def morphism(self,C,X):
        L = []
        for m in self:
            for c in C:
                for x in X:
                    L.append( equal ( data(c|data(m|x)), data(m|data(c|x)) ) )
        return Space(*L)
