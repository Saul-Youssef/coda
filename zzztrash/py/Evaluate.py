#
#    Evaluation of definitions
#
from base import *
#
#    Evaluation guaranteed to make progress and not to loop
#
def invariant(D): return evaluate(D)==D
#
#   Generic evaluation to maximum depth n, returning
#   the depth evaluated.
#
def depth(D,n):
    if n<=0:
        return D,n
    else:
        D2 = evaluate(D)
        if D==D2: return D2,n
        return depth(D2,n-1)
#
#   Generic evaluation of specified language code
#
def code2data(code,n):
    D = data(colon(data(('{'+code+'}').encode()),data()))
    return generic(D,n)
#
#   Do a generic evaluation of at most depth n
#
def generic(D,n):
    if n<=0:
        return D
    else:
        D2 = evaluate(D)
        if D==D2: return D2
        return generic(D2,n-1)
def Eval(A,B):
    import Number
    ns = Number.ints(A)
    if len(ns)==1:
        n = ns[0]
        if n>=0: return generic(B,n)
DEF.add(data(b'eval'),Eval)

def evaluate(B):
    L = []
    for b in B:
        if is_code(b):
            L.append(b)
        else:
            L.append(colon(evaluate(b.left()),evaluate(b.right())))
    return eval(data(*L))
DEF.add(data(b'evaluate'),lambda A,B:evaluate(B))

def eval(D):
    L = []
    for d in D:
        if is_code(d):
            L.append(d)
        else:
            for dd in eval_colon(d): L.append(dd)
    return data(*L)
#
#   A colon evaluation using all definitions associated with it's flag
#
def eval_colon(d):
    F,A = d.left().split()
    D = data(colon(F+A,d.right()))
    for definition in DEF.get(D): D = definition(D)
    return D
