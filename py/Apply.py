#
#    Applications are foundational combinatorial
#    definitions.  ap, especially, is everywhere.
#
from base import *
#
#  Apply argument to input in various ways.
#
#  demo: ap bin a b c : 1 2 3 4
#  demo: aq bin a b c : 1 2 3 4
#  demo: ar bin a b c : 1 2 3 4
#  demo: ai bin a b c : 1 2 3 4
#  demo: aj bin : a b c d
#  demo: ak bin a : b c d e f
#  demo: aj {bin A:B} : 1 2 3 4
#  demo: aj {nat_sum : A B} : 1 2 3 4 5
#  demo: apby 2 bin a b c : 1 2 3 4 5 6
#  demo: apby 2 count : a b c d e f g
#  demo: apby 2 last  : a b c d e f g
#  demo: ap {if (count:get bin:B)=2:B} : (bin:a b) (bin:a b c) (bin:x y) (bin:a b c d)
#
def ap_(context,domain,A,B):
    if B.atom(context): return data(A|B)
    return data(*[(domain+A)|data(b) for b in B])
CONTEXT.define('ap',ap_)

def aq2_1(context,domain,A,B):
    A0,AR =  A.split()
    A1,AR = AR.split()
    if A0.atom(context) and A1.atom(context): return ((A0+A1)|B) + ((domain+A0+AR)|B)
def aq2_0(context,domain,A,B):
    A0,AR = A.split()
    A1,AR = AR.split()
    if A0.empty() or A1.empty(): return data()
CONTEXT.define('aq',aq2_1,aq2_0)

def ar_1(context,domain,A,B):
    if A.atomic(context) and B.atomic(context):
        if len(A)<=1: return data()
        op,AR = A.split()
        L = []
        for a in AR:
            for b in B: L.append((op+data(a))|data(b))
        return data(*L)
CONTEXT.define('ar',ar_1)

def ari_1(context,domain,A,B):
    A0,AR =  A.split()
    A1,AR = AR.split()
    if A0.atom(context) and A1.atom(context):
        return data((A0+A1)|data((domain+A0+AR)|B))
def ari_0(context,domain,A,B):
    A0,AR = A.split()
    if A0.atom(context) and AR.empty(): return B
CONTEXT.define('ai',ari_0,ari_1)

def aj_1(context,domain,A,B):
    if B.atomic(context):
        BL,BR = B.split()
        if BR.empty(): return BL
        return data((A+BL)|data((domain+A)|BR))
CONTEXT.define('aj',aj_1)
