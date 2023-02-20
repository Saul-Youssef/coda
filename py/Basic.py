#
#   Basic definitions
#
from base import *
import Number
#
#    pass is the identity.  null returns empty data independent of B.
#
CONTEXT.add(PF(co('pass'),lambda A,B:B))
CONTEXT.add(PF(co('null'),lambda A,B:data()))

#def one(code,A,B):
#    return (data(co(code))+A)|B

def first_1(A,B):
    if B.empty(): return data()
def first_2(A,B):
#    if A.empty(): return cos('first','1')|B
    if A.empty(): return col('first','1',B)
def first_3(A,B):
    if Number.ints(A)==[0]: return data()
#def first_4(A,B):
#    ns = Number.ints(A)
#    if len(ns)==1:
#        n = ns.pop()
#        if n>=1 and len(B)>0 and B[0].atom(): return B[0] & (cos('first',str(n-1))|data(*B[1:]))
#CONTEXT.add(PF(co('first'),first_1,first_2,first_3,first_4))

def first_1(C):
    domain,A,B = C.left().split()
    if B.empty(): return data()
def first_2(C):
    domain,A,B = C.left().split()
    if A.empty(): return (domain+da(str(1)))|B
def first_3(C):
    domain,A,B = C.left()

def first(domain,A,B):
    if B.empty(): return data()
def first(domain,A,B):
    if A.empty(): return data(coda(domain,one,B))
def first(domain,A,B):
    if Number.ints(A)==[0]: return data()
def first(domain,A,B):
    ns = Number.ints(A)
    if len(ns)==1:
        n = ns.pop()
        if n>=1 and len(B)>0 and B[0].atom():
            return B[0] + coda(domain,co(str(n-1)),B[1:])

def rev(C):
    domain,A,B = C.left().split()
    if   B.empty(): return data()
    elif B.atomic(): return B
    elif len(B)>0:
        L,R = B.split()
        return (domain+A)|R + (domain+A)|L
CONTEXT.add(definition(da('rev'),rev))

def nat(C):
    domain,A,B = C.left().split()
    if len(Number.ints(B))==1: return B[0] + domain|Number.plus1(B[0])
CONTEXT.add(definition(da('nat'),nat))

def language(C):
    domain,A,B = C.left().split()
    if domain.curly(): pass
