#
#   Theorem
#
from base import *
#
#   Get undefined codas from input data
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
#
#   Tests if input data is invariant
#
#   demo: invariant : a b c
#   demo: invariant : a b? c
#   demo: invariant : a b (bin:c?)
#   demo: atomic : a b c
#   demo: atomic : a b? c
#   demo: atomic : nat : 0
#
def Invariant(context,domain,A,B):
    if B.rigid(context): return B
CONTEXT.define('invariant',Invariant)
def Atomic(context,domain,A,B):
    if B.irred(context): return B
CONTEXT.define('atomic',Atomic)
#
#   demo: assign (x?=y?) : ap put : a b
#   demo: assign (x?=y?) : permutation 3 : a b
#   demo: eval : theorem (bool:(x?=y?)) : permutation 2 : a b
#   demo: get with : eval : theorem (bool:(x?=y?)) : permutation 2 : a b
#
def stable(A,context):
    import Evaluation
    return Evaluation.Evaluate(context,100,2)(A)==A
#    import Evaluate
#    return Evaluate.Eval(100,Evaluate.SECONDS,context).evaluate(A)==A

def assign(context,domain,A,B):
    AS = da('let')
    if B.atomic(context) and stable(A,context):
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
#    if A==context.evaluate(1,A) and B.atomic(context):
