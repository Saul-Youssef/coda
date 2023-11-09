#
#    Applications are foundational combinatorial
#    definitions.  ap, especially, is everywhere.
#
from base import *
#
#  Apply argument to input in various ways.
#
#  demo: ap foo : 1 2 3
#  demo: ap {bin : B} : 1 2 3
#  demo: ap {first A : get bin : B} 2 : (bin:a b c d e) (bin:x y z)
#  demo: aq bin bin bin bin : 1 2 3 4
#  demo: ap aq a b c : 1 2 3
#  demo: aq bin a b c : 1 2 3
#  demo: aq first 2 3 : a b c d e f g
#  demo: by 2 foo : a b c d e f g
#  demo: ap {if (count:get bin:B)=2:B} : (bin:a b) (bin:a b c) (bin:x y) (bin:a b c d)
#
def ap_0(context,domain,A,B):
    if B.empty(): return data()
def ap_1(context,domain,A,B):
    if B.atom(context): return data(A|B)
def ap_2(context,domain,A,B):
    return data(*[(domain+A)|data(b) for b in B])
CONTEXT.define('ap',ap_0,ap_1,ap_2)

def apby(context,domain,A,B):
    AL,AR = A.split()
    import Number
    if AL.atom(context) and len(Number.ints(AL))==1:
        n = Number.ints(AL)[0]
        if n>0:
            if all([b.atom(context) for b in B[:n]]):
                return (AR|data(*B[:n])) + ((domain+A)|data(*B[n:]))
def apby_0(context,domain,A,B):
    if B.empty(): return data()
CONTEXT.define('by',apby_0,apby)

def aq2_1(context,domain,A,B):
    A0,AR =  A.split()
    A1,AR = AR.split()
    if A0.atom(context) and A1.atom(context): return ((A0+A1)|B) + ((domain+A0+AR)|B)
def aq2_0(context,domain,A,B):
    A0,AR = A.split()
    A1,AR = AR.split()
    if A0.empty() or A1.empty(): return data()
CONTEXT.define('aq',aq2_1,aq2_0)
#
#   product and sum
#
#   demo: product (:first 3) (:rev) : a b c d e f g
#   demo: product (:rev) (:first 3) : a b c d e f g
#   demo: sum (:first 3) (:rev) : a b c d e f g
#   demo: sum (:rev) (:first 3) : a b c d e f g
#   demo: sum (:rev) (:{first 3:B}) : a b c d e f g
#   demo: sum (bin:rev) (bin:{first 3:B}) : a b c d e f g
#
def aprod_1(context,domain,A,B):
    if len(A)>0 and A[-1].atom(context):
        AL,a = data(*A[:-1]),A[-1]
        return data((domain+AL)|data(a.right()|B))
def aprod_0(context,domain,A,B):
    if A.empty(): return B
def aprod_2(context,domain,A,B):
    if A.atom(context): return data(A[0].right()|B)
CONTEXT.define('product',aprod_1,aprod_0,aprod_2)
