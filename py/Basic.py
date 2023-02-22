#
#   Basic definitions
#
from base import *
import Number
#
#    pass is the identity.  null returns empty data independent of B.
#
CONTEXT.add(DEF(da('pass'),lambda domain,A,B:B))
CONTEXT.add(DEF(da('null'),lambda domain,A,B:data()))

def first_1(domain,A,B):
    if B.empty(): return data()
def first_2(domain,A,B):
    if A.empty(): return data(domain+da('1')|B)
def first_3(domain,A,B):
    if Number.ints(A)==[0]: return data()
def first_4(domain,A,B):
    ns = Number.ints(A)
    if len(ns)==1:
        n = ns.pop()
        if n>=1 and len(B)>0 and B[0].atom():
            return B[0] + ((domain+da(str(n-1))) | data(*B[1:]))
CONTEXT.add(DEF(da('first'),first_1,first_2,first_3,first_4))

def rev(domain,A,B):
    if   B.empty(): return data()
    elif B.atom(): return B
    elif len(B)>1:
        L,R = B.split()
        return ((domain+A)|R) + ((domain+A)|L)
CONTEXT.add(DEF(da('rev'),rev))

def nat(domain,A,B):
    ns = Number.ints(B)
    if len(ns)==1:
        n = ns.pop()
        return co(str(n)) + (domain|da(str(n+1)))
CONTEXT.add(DEF(da('nat'),nat))
