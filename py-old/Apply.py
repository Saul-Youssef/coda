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
def ap_0(domain,A,B):
    if B.empty(): return data()
def ap_1(domain,A,B):
    if B.atom(): return data(A|B)
def ap_2(domain,A,B):
    BL,BR = B.split()
    if len(BL)>0: return ((domain+A)|BL) + ((domain+A)|BR)
CONTEXT.define('ap',ap_0,ap_1,ap_2)

def aq_0(domain,A,B):
    if A.empty(): return data()
def aq_1(domain,A,B):
    if A.atom(): return data(A|B)
def aq_2(domain,A,B):
    AL,AR = A.split()
    return ((domain+AL)|B) + ((domain+AR)|B)
CONTEXT.define('aq',aq_0,aq_1,aq_2)

def apby(domain,A,B):
    AL,AR = A.split()
    import Number
    if AL.atom() and len(Number.ints(AL))==1:
        n = Number.ints(AL)[0]
        if n>0:
            if all([b.atom() for b in B[:n]]):
                return (AR|data(*B[:n])) + ((domain+A)|data(*B[n:]))
def apby_0(domain,A,B):
    if B.empty(): return data()
CONTEXT.define('by',apby_0,apby)
def ap2_1(domain,A,B):
    A0,AR =  A.split()
    A1,AR = AR.split()
    if A0.atom() and A1.atom(): return ((A0+A1)|B) + ((domain+A0+AR)|B)
def ap2_0(domain,A,B):
    A0,AR = A.split()
    A1,AR = AR.split()
    if A0.empty() or A1.empty(): return data()
CONTEXT.define('ax',ap2_1,ap2_0)

#def app(domain,A,B):
#    A0,AR = A.split()
#    if A0.atom(): return (A0|B) + ((domain+AR)|B)
#def app_0(domain,A,B):
#    if A.empty(): return data()
#def app_1(domain,A,B):
#    if B.empty(): return data()
#CONTEXT.define('app',app_1,app_0,app)
#def aps_0(domain,A,B):
#    B0,BR = B.split()
#    B1,BX = BR.split()
#    if B0.atom() and B1.atom(): return data((A+B0)|data((domain+A)|BR))
#def aps_1(domain,A,B):
#    if B.atom(): return B
#def aps_2(domain,A,B):
#    if B.empty(): return data()
#CONTEXT.define('aps',aps_0,aps_1,aps_2)
#def apif_0(domain,A,B):
#    if B.empty(): return data()
#def apif_1(domain,A,B):
#    BL,BR = B.split()
#    if BL.atom(): return ((domain+A)|BL) + ((domain+A)|BR)
#def apif_2(domain,A,B):
#    if B.atom(): return data((da('if')+data(A|B))|B)
#CONTEXT.define('apif',apif_0,apif_2,apif_1)
#
#   Apply argument datas to input sequentially
#
#   demo: apcon (:pass) (:rev) : a b c
#   demo: apcon (:first 2) (:last 2) : a b c d e
#   demo: apcon (2:first) (:last 2) : a b c d e
#   demo: apcon (bin 3 3 2:nth 1) (:rev) : a b c d e f g
#   demo: apcon (bin 2:first 2) (:last 2) : a b c d e
#   demo: apcon (bin:pass) (bin:rev) : a b c
#
#def apcon_0(domain,A,B):
#    if B.empty(): return data()
#def apcon_1(domain,A,B):
#    if A.invariant():
#        L = []
#        for a in A:
#            aL1,aL2 = a.left().split()
#            L.append((a.right()+aL2)|B)
#        return data(*L)
#CONTEXT.define('apcon',apcon_1,apcon_0)
#def apcon_1(domain,A,B):
#    if A.invariant():
#        Fs = [a.right() for a in A]
#        return data(*[f|B for f in Fs])
#
#   Reduce
#
#   demo:reduce pass : a a b b c c a
#   demo:reduce {count:get ((:):(:)):B} : a b cc ddd eee eeee
#
#def reduce_1(domain,A,B):
#    B1,BR = B.split()
#    if A.atomic() and B1.atom():
#        B2,BR2 = BR.split()
#        def eqco(A,B1,B2): return (co('=')+(A|B1))|data(A|B2)
#        if B2.atom():
#            return ((co('nif')+eqco(A,B1,B2))|B1) + ((domain+A)|BR)
#        elif B2.empty():
#            return B1
#def reduce_0(domain,A,B):
#    if B.empty(): return data()
#CONTEXT.define('reduce',reduce_0,reduce_1)
#
#   While creates an idempotent
#