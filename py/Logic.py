#
#   Logic in coda is "zen logic" (truth is emptiness).
#
from base import *
#
#   Context equality (=) and logical complement (not).
#
#  demo: 1=1
#  demo: 1=2
#  demo: bool : 1=2
#  demo: or (1=2) : (2=3)
#  demo: or (1=2) : (1=1)
#  demo: 1=()
#  demo: <>=()
#  demo: x?=1
#  demo: x?=x?
#  demo: x?=y?
#  demo: =
#  demo: (=)=(())
#  demo: bin:x? = bin:y?
#  demo: 1 2 3 = 1 2 3
#  demo: 1 x 3 = 1 2 3
#  demo: 1 (foo:bar) 3 = 1 2 3
#  demo: not:
#  demo: not: 1 2 3 4
#  demo: not: (foo:bar)
#
AT = data(coda(data(),data()))
def bool(context,domain,A,B):
    if B.irred(context): return AT
    if B.empty(): return data()
CONTEXT.define('bool',bool)
def complement(context,domain,A,B):
    if B.irred(context): return data()
    if B.empty(): return AT
CONTEXT.define('not',complement)

def equal(context,domain,A,B):
    if A.empty(): return B
    if B.empty(): return A
    AL,AR = A.split()
    BL,BR = B.split()
    if AL.atom(context) and BL.atom(context):
        if AR.empty() and BR.empty():
            return ((domain+AL[0].left())|BL[0].left()) + ((domain+AL[0].right())|BL[0].right())
        else:
            return ((domain+AL)|BL) + ((domain+AR)|BR)
    AL,AR = data(*A[:-1]),data(*A[-1:])
    BL,BR = data(*B[:-1]),data(*B[-1:])
    if AR.atom(context) and BR.atom(context):
        return ((domain+AL)|BL) + ((domain+AR)|BR)

def eq_L(context,domain,A,B):
    AL,AR = data(*A[:1]),data(*A[1:])
    BL,BR = data(*B[:1]),data(*B[1:])
    if AL.atom(context) and BL.atom(context): return ((domain+AL)|BL) + ((domain+AR)|BR)
def eq_R(context,domain,A,B):
    AL,AR = data(*A[:-1]),data(*A[-1:])
    BL,BR = data(*B[:-1]),data(*B[-1:])
    if AR.atom(context) and BR.atom(context): return ((domain+AL)|BL) + ((domain+AR)|BR)
def eq_(context,domain,A,B):
    if A==B: return data()
    if A.irred(context) and B.empty(): return AT
    if A.empty() and B.irred(context): return AT
    if A.empty() and B.empty(): return data()
    if A.atom(context) and B.atom(context):
        return ((domain+(A[0].left ()))|B[0].left ()) + \
               ((domain+(A[0].right()))|B[0].right())
#CONTEXT.define('=',eq_,eq_L,eq_R)
#CONTEXT.define('equal',eq_,eq_L,eq_R)
CONTEXT.define('=',equal)
CONTEXT.define('equal',equal)
#
#    Standard binary operators
#
class TruthTable(object):
    def __init__(self):
        self._tt = {
        'nor' :[0,0,0,1],
        'xor' :[0,1,1,0],
        'nand':[0,1,1,1],
        'and' :[1,0,0,0],
        'xnor':[1,0,0,1],
        'imply':[1,0,1,1],
        'or'   :[1,1,1,0]}
    def tt(self,name): return self.value(self._tt[name][0])
    def tf(self,name): return self.value(self._tt[name][1])
    def ft(self,name): return self.value(self._tt[name][2])
    def ff(self,name): return self.value(self._tt[name][3])
    def value(self,i):
        if i==1: return data()
        if i==0: return AT
T = TruthTable()
#
#    Binary logical operators with standard truth tables
#
#    demo: or a : b
#    demo: or a :
#    demo: or : a
#    demo: or :
#    demo: and a : b
#    demo: and a :
#    demo: nor a : b
#    demo: xor a : b
#    demo: xnor a : b
#    demo: iff a : b
#    demo: nand a : b
#    demo: imply a : b
#
def OR(context,domain,A,B):
    op = 'or'
    if A.empty()  and B.empty() : return T.tt(op)
    if A.empty()  and B.irred(context): return T.tf(op)
    if A.irred(context) and B.empty() : return T.ft(op)
    if A.irred(context) and B.irred(context): return T.ff(op)
CONTEXT.define('or',OR)
def AND(context,domain,A,B):
    op = 'and'
    if A.empty()  and B.empty() : return T.tt(op)
    if A.empty()  and B.irred(context): return T.tf(op)
    if A.irred(context) and B.empty() : return T.ft(op)
    if A.irred(context) and B.irred(context): return T.ff(op)
CONTEXT.define('and',AND)
def NOR(context,domain,A,B):
    op = 'nor'
    if A.empty()  and B.empty() : return T.tt(op)
    if A.empty()  and B.irred(context): return T.tf(op)
    if A.irred(context) and B.empty() : return T.ft(op)
    if A.irred(context) and B.irred(context): return T.ff(op)
CONTEXT.define('nor',NOR)
def XOR(context,domain,A,B):
    op = 'xor'
    if A.empty()  and B.empty() : return T.tt(op)
    if A.empty()  and B.irred(context): return T.tf(op)
    if A.irred(context) and B.empty() : return T.ft(op)
    if A.irred(context) and B.irred(context): return T.ff(op)
CONTEXT.define('xor',XOR)
def NAND(context,domain,A,B):
    op = 'nand'
    if A.empty()  and B.empty() : return T.tt(op)
    if A.empty()  and B.irred(context): return T.tf(op)
    if A.irred(context) and B.empty() : return T.ft(op)
    if A.irred(context) and B.irred(context): return T.ff(op)
CONTEXT.define('nand',NAND)
def XNOR(context,domain,A,B):
    op = 'xnor'
    if A.empty()  and B.empty() : return T.tt(op)
    if A.empty()  and B.irred(context): return T.tf(op)
    if A.irred(context) and B.empty() : return T.ft(op)
    if A.irred(context) and B.irred(context): return T.ff(op)
CONTEXT.define('xnor',XNOR)
CONTEXT.define('iff',XNOR)
def IMPLY(context,domain,A,B):
    op = 'imply'
    if A.empty()  and B.empty() : return T.tt(op)
    if A.empty()  and B.irred(context): return T.tf(op)
    if A.irred(context) and B.empty() : return T.ft(op)
    if A.irred(context) and B.irred(context): return T.ff(op)
CONTEXT.define('imply',IMPLY)
#
#   some/none define the coarsest data classification
#
#   demo: some : a b c
#   demo: some x y z : a b c
#
def some(context,domain,A,B):
    if A.irred(context): return A
    if A.empty(): return B
CONTEXT.define('some',some)
