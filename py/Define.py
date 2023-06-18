#
#    Definition definitions
#
from base import *
import Evaluate
#
#   Create a definition.
#
#   demo: def foo : {first 2 : rev : B}
#   demo: foo : a b c d e f
#   demo: def first2 : {first A:B} 2
#   demo: first2 : a b c d
#
def Def(domain,D,V):
    D = Evaluate.resolve(D,100)
    V = Evaluate.resolve(V,100)

    if (not D is None) and (not V is None):
        if V.empty(): CONTEXT.add(Definition(D))
        else        : CONTEXT.add(Definition(D,lambda domain,A,B:data((V+A)|B)))
        return data()
CONTEXT.define('def',Def)

VALUES = {}
def Value(domain,A,B):
    if B.invariant() and B in VALUES: return VALUES[B]
CONTEXT.define('?',Value)
def Let(domain,A,B):
    if A.invariant():
        if A in VALUES and not VALUES[A]==B:
            return
        else:
            VALUES[A] = B
            return data()
CONTEXT.define('let',Let)

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

def theorem(T,B):
    T = Evaluate.default(T)
    if not T.eval()==T: return
    vars = variables(T)
    X = []
    for b in B:
        if b.domain()==da('bin'): X.append(b.right())
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
#
#   theorem tests if the argument is a theorem with respect to it's input
#
#   demo: theorem (X?=X?) : ap put bin : 1 2 3
#   demo: theorem (X?=Y?) : ap put bin : 1 2 3
#   demo: theorem (rev:rev:X?=X?) : (put bin : 1 2 3 ) (put bin : 4 5 6 )
#
def Theorem(domain,A,B):
    if A.eval()==A and B.eval()==B: return theorem(A,B)
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
