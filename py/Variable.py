
from base import *

def Replace(domain,A,B):
    if A.eval()==A and B.eval()==B:
        AL,AR = A.split()
        L = []
        for b in B:
            if data(b)==AL:
                for a in AR: L.append(a)
            else:
                L.append(b)
        return data(*L)
CONTEXT.define('replace',Replace)

def RReplace(domain,A,B):
    if A.eval()==A and B.eval()==B:
        AL,AR = A.split()
        if len(AL)>0:
            return rreplace(AL[0],AR,B)
        else:
            return B
CONTEXT.define('rreplace',RReplace)

def With(domain,A,B):
    if A.eval()==A and B.eval()==B:
        eqs = [a for a in A if a.domain()==da('=')]
        BR = data(*[b for b in B])
        for eq in eqs:
            L,R = eq.left().split()
            if len(R)==1: BR = rreplace(R[0],eq.right(),BR)
        return BR
CONTEXT.define('with',With)

def rreplace(c,D,A):
    L = []
    for a in A:
        if a==c:
            for d in D: L.append(d)
        else:
            L.append(rreplace(c,D,a.left())|rreplace(c,D,a.right()))
    return data(*L)

def theorem(T,S):
    import Evaluate
    T = Evaluate.default(T)
    if not T.eval()==T: return
    vars = variables(T)
    X = [s for s in S]
    import itertools
    xts = [xt for xt in itertools.product(X,repeat=len(vars))]
    if len(vars)==0 or len(X)==0: return T
    TS = []
    for xt in xts:
        T2 = data(*[t for t in T])
        xl = [x for x in xt]
        vl = [v for v in vars]
        if not len(xl)==len(vl): raise error('unexpected length')
        while len(xl)>0:
            x = xl.pop()
            v = vl.pop()
            T2 = rreplace(v,x,T2)
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

def variables(A):
    vs = set([])
    for a in A:
        if a.domain()==da('?'): vs.add(a)
        else:
            vl = variables(a.left())
            vr = variables(a.right())
            vs = vs.union(vl).union(vr)
    return vs
#
#   Get variables from input
#
#   demo: variables : X? 1 2 3 Y?
#
def Variables(domain,A,B):
    if B.eval()==B: return data(*[v for v in variables(B)])
CONTEXT.define('variables',Variables)
