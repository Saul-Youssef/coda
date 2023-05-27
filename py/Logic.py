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
ATOM = data(coda(data(),data()))
def bool(domain,A,B):
    if B.atomic(): return ATOM
    if B.empty(): return data()
CONTEXT.define('bool',bool)
def complement(domain,A,B):
    if B.atomic(): return data()
    if B.empty (): return ATOM
CONTEXT.define('not',complement)
def eq_L(domain,A,B):
    AL,AR = data(*A[:1]),data(*A[1:])
    BL,BR = data(*B[:1]),data(*B[1:])
    if AL.atom() and BL.atom(): return ((domain+AL)|BL) + ((domain+AR)|BR)
def eq_R(domain,A,B):
    AL,AR = data(*A[:-1]),data(*A[-1:])
    BL,BR = data(*B[:-1]),data(*B[-1:])
    if AR.atom() and BR.atom(): return ((domain+AL)|BL) + ((domain+AR)|BR)
def eq_(domain,A,B):
    if A==B: return data()
    if A.atomic () and B.empty(): return ATOM
    if A.empty() and B.atomic (): return ATOM
    if A.empty() and B.empty(): return data()
    if A.atom () and B.atom (): return ((domain+(A[0].left ()))|B[0].left ()) + \
                                       ((domain+(A[0].right()))|B[0].right())
CONTEXT.define('=',eq_,eq_L,eq_R)
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
        if i==0: return ATOM
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
def OR(domain,A,B):
    op = 'or'
    if A.empty()  and B.empty() : return T.tt(op)
    if A.empty()  and B.atomic(): return T.tf(op)
    if A.atomic() and B.empty() : return T.ft(op)
    if A.atomic() and B.atomic(): return T.ff(op)
CONTEXT.define('or',OR)
def AND(domain,A,B):
    op = 'and'
    if A.empty()  and B.empty() : return T.tt(op)
    if A.empty()  and B.atomic(): return T.tf(op)
    if A.atomic() and B.empty() : return T.ft(op)
    if A.atomic() and B.atomic(): return T.ff(op)
CONTEXT.define('and',AND)
def NOR(domain,A,B):
    op = 'nor'
    if A.empty()  and B.empty() : return T.tt(op)
    if A.empty()  and B.atomic(): return T.tf(op)
    if A.atomic() and B.empty() : return T.ft(op)
    if A.atomic() and B.atomic(): return T.ff(op)
CONTEXT.define('nor',NOR)
def XOR(domain,A,B):
    op = 'xor'
    if A.empty()  and B.empty() : return T.tt(op)
    if A.empty()  and B.atomic(): return T.tf(op)
    if A.atomic() and B.empty() : return T.ft(op)
    if A.atomic() and B.atomic(): return T.ff(op)
CONTEXT.define('xor',XOR)
def NAND(domain,A,B):
    op = 'nand'
    if A.empty()  and B.empty() : return T.tt(op)
    if A.empty()  and B.atomic(): return T.tf(op)
    if A.atomic() and B.empty() : return T.ft(op)
    if A.atomic() and B.atomic(): return T.ff(op)
CONTEXT.define('nand',NAND)
def XNOR(domain,A,B):
    op = 'xnor'
    if A.empty()  and B.empty() : return T.tt(op)
    if A.empty()  and B.atomic(): return T.tf(op)
    if A.atomic() and B.empty() : return T.ft(op)
    if A.atomic() and B.atomic(): return T.ff(op)
CONTEXT.define('xnor',XNOR)
CONTEXT.define('iff',XNOR)
def IMPLY(domain,A,B):
    op = 'imply'
    if A.empty()  and B.empty() : return T.tt(op)
    if A.empty()  and B.atomic(): return T.tf(op)
    if A.atomic() and B.empty() : return T.ft(op)
    if A.atomic() and B.atomic(): return T.ff(op)
CONTEXT.define('imply',IMPLY)
