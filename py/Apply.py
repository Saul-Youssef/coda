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
#  demo: ap bin a b c : 1 2 3
#  demo: aq bin a b c : 1 2 3
#  demo: ar bin a b c : 1 2 3
#  demo: ar {|} a b c : 1 2 3
#  demo: as {int_sum : A B} : 1 2 3 4 5
#  demo: as {int_prod : A B} : 1 2 3 4 5
#  demo: as {int_prod : A B} :
#  demo: ap {if (count:get bin:B)=2:B} : (bin:a b) (bin:a b c) (bin:x y) (bin:a b c d)
#
def ap_0(context,domain,A,B):
    if B.empty(): return data()
def ap_1(context,domain,A,B):
    if B.atom(context): return data(A|B)
def ap_2(context,domain,A,B):
    return data(*[(domain+A)|data(b) for b in B])
CONTEXT.define('ap',ap_0,ap_1,ap_2)

def aq2_1(context,domain,A,B):
    A0,AR =  A.split()
    A1,AR = AR.split()
    if A0.atom(context) and A1.atom(context): return ((A0+A1)|B) + ((domain+A0+AR)|B)
def aq2_0(context,domain,A,B):
    A0,AR = A.split()
    A1,AR = AR.split()
    if A0.empty() or A1.empty(): return data()
CONTEXT.define('aq',aq2_1,aq2_0)        

def ri_1(context,domain,A,B):
    if A.atomic(context) and B.atomic(context):
        if len(A)<=1: return data()
        OP,AR = A.split()
        L = []
        for a in AR:
            for b in B: L.append((OP[0].right()+data(a))|data(b))
        return data(*L)
CONTEXT.define('ri',ri_1)

def ar_1(context,domain,A,B):
    if A.atomic(context) and B.atomic(context):
        if len(A)<=1: return data()
        op,AR = A.split()
        L = []
        for a in AR:
            for b in B: L.append((op+data(a))|data(b))
        return data(*L)
CONTEXT.define('ar',ar_1)

def as_1(context,domain,A,B):
    if B.atomic(context):
        BL,BR = B.split()
        if BR.empty(): return BL
        return data((A+BL)|data((domain+A)|BR))
CONTEXT.define('as',as_1)
