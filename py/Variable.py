#
#   Theorem
#
from base import *
#
#   Get undefined codas from input data
#
#   demo: undefined :
#   demo: undefined : a b c
#   demo: undefined : (foo:bar) x? y? z?
#   demo: undefined : (bin: bin: bin : x? y? z?)
#
def undefined(context,A):
    us = set([])
    for a in A:
        if not a in context: us.add(a)
        us = us.union(undefined(context,a.left())).union(undefined(context,a.right()))
    return us
def invariant(context,A):
    ins = set([])
    for a in A:
        if a.invar(context): ins.add(a)
        ins = ins.union(invariant(context,a.left())).union(invariant(context,a.right()))
    return ins

def Undefined(context,domain,A,B):
    if context.evaluate(1,B)==B: return data(*[u for u in undefined(context,B)])
CONTEXT.define('undefined',Undefined)
def Invariant(context,domain,A,B):
    if context.evaluate(1,B)==B: return B
CONTEXT.define('invariant',Invariant)
#
#   demo: permutation 2 : a b
#   demo: permutation 3 : a b
#   demo: permutation 3 : a
#   demo: assign (x?=y?) : ap put : a b
#   demo: assign (x?=y?) : permutation 3 : a b
#   demo: eval : theorem (bool:(x?=y?)) : permutation 2 : a b
#   demo: get with : eval : theorem (bool:(x?=y?)) : permutation 2 : a b
#
def permutation(n,B):
    import itertools
    for P in itertools.product([b for b in B],repeat=n): yield data(*[p for p in P])

def permutation_0(context,domain,A,B):
    if A.rigid(context) and B.atomic(context):
        import Number
        n = Number.intdef(1,A)
        return data(*[data()|D for D in permutation(n,B)])
CONTEXT.define('permutation',permutation_0)

def assign(context,domain,A,B):
    AS = da('let')
    if A.invar(context) and B.atomic(context):
        vars = [v.left() for v in undefined(context,A) if v.right()==data()]  # coda variables
        n = len(vars)
        L = []
        import itertools
        for P in itertools.product([b for b in B if b.left()==data()],repeat=n):
            T = []
            for i in range(n): T.append((AS+vars[i])|P[i].right())
            L.append(data()|data(*T))
        return data(*L)
CONTEXT.define('assign',assign)
