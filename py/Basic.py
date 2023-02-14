#
#   Basic definitions
#
from base import * 
#
#    pass is the identity.  null returns empty data independent of B.
#
DEF.add(PF(co('pass'),lambda A,B:B))
DEF.add(PF(co('null'),lambda A,B:data()))

def first_1(A,B):
    print('aaaa 1',B,B.empty())
    if B.empty(): return data()
def first_2(A,B):
    if A.empty(): return data(co('first'),co('1'))|B
def first_3(A,B):
    import Number
    ns = Number.ints(A)
    if ns==[0]: return data()
def first_4(A,B):
    import Number
    ns = Number.ints(A)
    print('aaaaa 4',A,B,ns)
    if len(ns)==1:
        n = ns.pop()
        if n>=1:
            L,R = B.split()
            print('aaaaa 4',n,B,L,R)
            if L.atom(): return L + data(co('first'),co(str(n-1))) | R 

DEF.add(PF(co('first'),first_1,first_2,first_3,first_4))