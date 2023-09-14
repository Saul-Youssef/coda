
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
#
#   Get undefined codas from input data
#
#   demo: undefined :
#   demo: undefined : a b c
#   demo: undefined : (foo:bar) x? y? z?
#   demo: undefined : (bin: bin: bin : x? y? z?)
#
def undefined(A):
    vs = set([])
    for a in A:
        if not a in CONTEXT: vs.add(a)
        vs = vs.union(undefined(a.left())).union(undefined(a.right()))
    return vs

def Undefined(domain,A,B):
    if B.eval()==B: return data(*[u for u in undefined(B)])
CONTEXT.define('undefined',Undefined)

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
#def Variables(domain,A,B):
#    if B.eval()==B: return data(*[v for v in variables(B)])
#CONTEXT.define('variables',Variables)
