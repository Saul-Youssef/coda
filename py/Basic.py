#
#   Basic definitions
#
from base import * 
#
#    pass is the identity.  null returns empty data independent of B.
#
DEF.add(PF(da('pass'),lambda A,B:B))
DEF.add(PF(da('null'),lambda A,B:data()))

def first_1(A,B):
    if B.empty(): return data()
def first_2(A,B):
    if A.empty(): return da('first')**da('1')|B
def first_3(A,B):
    import Number
    ns = Number.ints(A)
    if ns==[0]: return data()
def first_4(A,B):
    import Number
    if len(ns)==1:
        n = ns.pop()
        if n>=1:
            L,R = B.split()
            if DEF.atom(L): return L + (da('first') & da(str(n-1))) | R

DEF.add(PF(da('first'),first_1,first_2,first_3,first_4))