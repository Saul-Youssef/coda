#
#   Data which is never false is called a theorem.
#
from base import *
from Variable import rreplace,undefined
from Log import LOG
LOG.register('theorem')

def theorem(T,S):
    vars = undefined(T)
    X = [s for s in S]
    import itertools
    xts = [xt for xt in itertools.product(X,repeat=len(vars))]
    if len(vars)==0 or len(X)==0: return T
    TS = []
    LOG('theorem','undecided: ',','.join([str(v) for v in vars]))
    for xt in xts:
        T2 = data(*[t for t in T])
        xl = [x for x in xt]
        vl = [v for v in vars]
        if not len(xl)==len(vl): raise error('unexpected length')
        while len(xl)>0:
            x = xl.pop()
            v = vl.pop()
            T2 = rreplace(v,x,T2)
#            LOG('theorem','replace',str(v),str(x),str(T2))
        TS.append(T2)
    L = []
    for t in TS:
        for c in t: L.append(c)
    return data(*L)

def unbin(A): return [a.right() for a in A]
#
#   theorem tests if the argument is a theorem with respect to it's input
#
#   demo: theorem (X?=X?) : ap put : 1 2 3
#   demo: theorem (X?=Y?) : ap put : 1 2 3
#   demo: theorem (rev:rev:X?=X?) : (put : 1 2 3 ) (put : 4 5 6 )
#   demo: theorem (nth 3:X?) : (put : 1 2) (put : a b)
#   demo: theorem (nth 3:X?) : (put : 1 2) (put : a b) (put : 1 2 3)
#   demo: theorem (X?=Y?) : (put : x? y?) (:1 2 3 4)
#
def Theorem(domain,A,B):
    if A.eval()==A and B.eval()==B and B.invariant(): return theorem(A,unbin(B))
CONTEXT.define('theorem',Theorem)
