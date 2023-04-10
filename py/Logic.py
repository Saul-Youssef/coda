#
#   Logic in coda is "zen logic" (truth is emptiness).
#
from base import *
#
#   some/none define the coarsest data classification
#
#   demo: some : a b c
#   demo: some :
#   demo: none : a b c
#   demo: none :
#
#   some : A -> 1 if A is atomic, () if A is empty
#   none : A -> 1 if A is empty, () if A is atomic
#
def default(domain,A,B):
    if B.atomic(): return B
    if B.empty(): return A
CONTEXT.define('default',default)

#def some(domain,A,B):
#    if B.atomic(): return A
#    if B.empty (): return data()
#def none(domain,A,B):
#    if B.atomic(): return data()
#    if B.empty (): return A
#CONTEXT.define('some',some)
#CONTEXT.define('none',none)
#
#   Context equality (=) and logical complement (^) in "Zen logic".
#
#   a A = b B -> (a=b) (A=B) if a and b are atoms
#   A a = B b -> (A=B) (a=b) if a and b are atoms
#   A = B -> () if A==B identical data
#   a = b -> (# a:b) if a and b are either atoms or empty and a and b
#
#  demo: 1=1
#  demo: 1=2
#  demo: (1=2)|(2=3)
#  demo: (1=2)|(1=1)
#  demo: 1=()
#  demo: <>=()
#  demo: x?=1
#  demo: x?=x?
#  demo: x?=y?
#  demo: =
#  demo: (=)=(())
#  demo: (bin:x?) = (bin:y?)
#  demo: 1 2 3 = 1 2 3
#  demo: 1 x 3 = 1 2 3
#  demo: 1 (foo:bar) 3 = 1 2 3
#  demo: ^:
#  demo: ^: 1 2 3 4
#  demo: ^: (foo:bar)
#
ATOM = data(coda(data(),data()))

def logic(domain,A,B):
    if B.atomic(): return ATOM
    if B.empty(): return data()
CONTEXT.define('logic',logic)

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

def Or(domain,A,B):
    if A.empty()  and B.empty(): return data()
    if A.empty()  and B.atomic(): return data()
    if A.atomic() and B.empty(): return data()
    if A.atomic() and B.atomic(): return ATOM
CONTEXT.define('or',Or)
#    if A.empty()   or B.empty(): return data()
#    if A.atomic() and B.atomic(): return ATOM
#
#def or_(domain,A,B):
#    if A.empty() or B.empty(): return data()
#def or_1(domain,A,B):
#    if A.atomic() and B.atomic(): return ATOM
#CONTEXT.define('|',or_,or_1)

def imply(domain,A,B):
    if A.empty()  and B.empty() : return data()
    if A.empty()  and B.atomic(): return ATOM
    if A.atomic() and B.empty() : return data()
    if A.atomic() and B.atomic(): return data()
CONTEXT.define('imply',imply)
