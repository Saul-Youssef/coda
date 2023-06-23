#
#   Data which is never false is called a theorem.
#
from base import *
from Variable import rreplace,variables
from Log import LOG
LOG.register('theorem')

def theorem(T,S):
#    import Evaluate
#    T = Evaluate.default(T)
#    if not T.eval()==T: return
    vars = variables(T)
    X = [s for s in S]
    import itertools
    xts = [xt for xt in itertools.product(X,repeat=len(vars))]
    if len(vars)==0 or len(X)==0: return T
    TS = []
    LOG('theorem','Domain',str(len(vars)),str(len(xts)))
    for xt in xts:
        T2 = data(*[t for t in T])
        xl = [x for x in xt]
        vl = [v for v in vars]
        if not len(xl)==len(vl): raise error('unexpected length')
        while len(xl)>0:
            x = xl.pop()
            v = vl.pop()
            T2 = rreplace(v,x,T2)
            LOG('theorem','replace',str(v),str(x),str(T2))
        TS.append(T2)
    L = []
    for t in TS:
        for c in t: L.append(c)
    return data(*L)

def unbin(A): return [a.right() for a in A if a.domain()==da('bin')]
#
#   theorem tests if the argument is a theorem with respect to it's input
#
#   demo: theorem (X?=X?) : ap put bin : 1 2 3
#   demo: theorem (X?=Y?) : ap put bin : 1 2 3
#   demo: theorem (rev:rev:X?=X?) : (put bin : 1 2 3 ) (put bin : 4 5 6 )
#   demo: theorem (nth 3:X?) : (put bin : 1 2) (put bin: a b)
#   demo: theorem (nth 3:X?) : (put bin : 1 2) (put bin: a b) (put bin:1 2 3)
#
def Theorem(domain,A,B):
    if A.eval()==A and B.eval()==B: return theorem(A,unbin(B))
CONTEXT.define('theorem',Theorem)
