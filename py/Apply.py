#
#    Applications are foundational combinatorial
#    definitions.  ap, especially, is everywhere.
#
from base import *
#
#  Apply A to each b in B.
#
#  This is one of the most important basic
#  combinatorial operations.  ap A is guaranteed
#  to be distributive data for any data A.
#
#  ap A : B C -> (ap A:B) (ap A:C)
#  ap A : B -> A:B if B is atom
#  ap A : () -> ()
#
#  demo: ap foo : 1 2 3
#  demo: ap {bin : B} : 1 2 3
#  demo: ap {first A : get bin : B} 2 : (bin:a b c d e) (bin:x y z)
#  demo: aq bin bin bin bin : 1 2 3 4
#  demo: ap aq a b c : 1 2 3
#  demo: ax bin a b c : 1 2 3
#  demo: ax first 2 3 : a b c d e f g
#  demo: ap ax a b c : 1 2 3
#  demo: by 2 foo : a b c d e f g
#  demo: ap {if (count:get bin:B)=2:B} : (bin:a b) (bin:a b c) (bin:x y) (bin:a b c d)
#
def ap_0(context,domain,A,B):
    if B.empty(): return data()
def ap_1(context,domain,A,B):
    if B.atom(context): return data(A|B)
def ap_2(context,domain,A,B):
    BL,BR = B.split()
    if len(BL)>0: return ((domain+A)|BL) + ((domain+A)|BR)
CONTEXT.define('ap',ap_0,ap_1,ap_2)

def aq_0(context,domain,A,B):
    if A.empty(): return data()
def aq_1(context,domain,A,B):
    if A.atom(context): return data(A|B)
def aq_2(context,domain,A,B):
    AL,AR = A.split()
    if AL.atom(context): return ((domain+AL)|B) + ((domain+AR)|B)
CONTEXT.define('aq',aq_0,aq_1,aq_2)

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

def ap2_1(context,domain,A,B):
    A0,AR =  A.split()
    A1,AR = AR.split()
    if A0.atom(context) and A1.atom(context): return ((A0+A1)|B) + ((domain+A0+AR)|B)
def ap2_0(context,domain,A,B):
    A0,AR = A.split()
    A1,AR = AR.split()
    if A0.empty() or A1.empty(): return data()
CONTEXT.define('ax',ap2_1,ap2_0)
