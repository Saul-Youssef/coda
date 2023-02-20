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

def rev_1(A,B):
    if B.empty(): return data()
def rev_2(A,B):
    if B.atomic(): return B 
def rev_3(A,B):
    if len(B)>0: return col('rev',B[1:]) + col('rev',B[:1])
CONTEXT.add(PF(co('rev'),rev_1,rev_2,rev_3))

def nat_1(A,B):
    ns = Number.ints(B)
    if len(ns)==1:
        n = ns.pop()
        if n>=0: return data(co(str(n))) + col('nat',[co(str(n+1))])
CONTEXT.add(PF(co('nat'),nat_1))