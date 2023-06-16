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
            return replace(AL[0],AR,B)
        else:
            return B
CONTEXT.define('rreplace',RReplace)

def replace(c,D,A):
    L = []
    for a in A:
        if a==c:
            for d in D: L.append(d)
        else:
            L.append(replace(c,D,a.left())|replace(c,D,a.right()))
    return data(*L)

#  replace coda c with data D within data A.

#
#def  replace(A,v1,v2): return data(*[creplace(a,v1,v2) for a in A])
#def creplace(c,v1,v2):
#    if c==v1: return v2
#    return replace(c.left(),v1,v2)|replace(c.right(),v1,v2)
