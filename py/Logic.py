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
#   some A -> 1 if A is atomic, () if A is empty
#   none A -> 1 if A is empty, () if A is atomic
#
def some(domain,A,B):
    if B.atomic(): return da('1')
    if B.empty (): return data()
def none(domain,A,B):
    if B.atomic(): return data()
    if B.empty (): return da('1')
CONTEXT.define('some',some)
CONTEXT.define('none',none)
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
def complement(domain,A,B):
    if B.atomic(): return data()
    if B.empty (): return da('#')
CONTEXT.define('^',complement)

def eq_L(domain,A,B):
    AL,AR = data(*A[:1]),data(*A[1:])
    BL,BR = data(*B[:1]),data(*B[1:])
    if AL.atom() and BL.atom(): return ((domain+AL)|BL) + ((domain+AR)|BR) 
def eq_R(domain,A,B):
    AL,AR = data(*A[:-1]),data(*A[-1:])
    BL,BR = data(*B[:-1]),data(*B[-1:])
    if AR.atom() and BR.atom(): return ((domain+AL)|BL) + ((domain+AR)|BR)
def eq_r(domain,A,B):
    if A.atom () and B.empty(): return da('#')
    if A.empty() and B.atom (): return da('#')
    if A.empty() and B.empty(): return data()
    if A.atom () and B.atom (): return ((domain+(A[0].left ()))|B[0].left ()) + \
                                       ((domain+(A[0].right()))|B[0].right()) 
CONTEXT.define('=',eq_r,eq_L,eq_R)
