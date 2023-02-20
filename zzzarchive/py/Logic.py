#
#    In Zen logic,
#
#    o Data A is "true" A=()
#    o Data A is "false"
#
from base import *

def zen(D):
    if   D.empty() : return 'e'
    elif D.atomic(): return 'a'
    else           : return 'u'
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
def some(A,B):
    if B.atomic(): return data(b'1')
    if B.empty (): return data()
def none(A,B):
    if B.atomic(): return data()
    if B.empty (): return data(b'1')
DEF.add(data(b'some'),some)
DEF.add(data(b'none'),none)
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
#  demo: {}=()
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
def complement(A,B):
    if B.atomic(): return data()
    if B.empty (): return data(b'F')
DEF.add(data(b'^'),complement)

def eq_L(AA,BB):
    A0,A = AA.split_left()
    B0,B = BB.split_left()
    if A0.atom() and B0.atom(): return one(b'=',A0,B0) + one(b'=',A,B)
def eq_R(AA,BB):
    A,A0 = AA.split_right()
    B,B0 = BB.split_right()
    if A0.atom() and B0.atom(): return one(b'=',A,B) + one(b'=',A0,B0)
def eq_(A,B):
    if A==B: return data()
def eq_base(A,B):
    if base_notequal(A,B): return one(b'#',A,B)
def base_notequal(A,B):
    if A.empty() and B.atom() : return True
    if A.atom()  and B.empty(): return True
    if A.atom() and B.atom() and A.decided() and B.decided() and not A==B: return True
DEF.add(data(b'='),eq_L,eq_R,eq_,eq_base)
