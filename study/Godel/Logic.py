#
#   "Zen Logic"
#
from base import *
#
#  Data equality
#
#  Data equality is defined with respect to the current "context", meaning
#  with respect to the current definitions (see defs:).  Data A and B
#  are equal if there are definitions f,g such that f(A) and g(B) are
#  identical.  In the language, equality has syntactic sugar, so that
#  A=B is interpreted as (= A:B).
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
#
def eq_1(L,R):
    AL,A = L.split_left()
    BL,B = R.split_left()
    if AL.atom() and BL.atom(): return one(b'=',AL,BL) + one(b'=',A,B)
def eq_2(L,R):
    A,AR = L.split_right()
    B,BR = R.split_right()
    if AR.atom() and BR.atom(): return one(b'=',A,B) + one(b'=',AR,BR)
def eq_3(A,B):
    if A==B: return data()
def eq_4(A,B):
    import Evaluation
    if (A.atom() or B.atom()) and A.defined() and B.defined() and \
        Evaluation.invariant(A) and Evaluation.invariant(B):
        if A==B: return data()
        else   : return one(b'#',A,B)
DEF.add(data(b'='),eq_1,eq_2,eq_3,eq_4)
#
#   A | B is the "or" of data A and B.  If either is empty, the result is empty.
#
#   demo: 1 | (null:a b c)
#   demo: 1 | (pass:a b c)
#   demo: logic : (1 | (pass:a b c))
#   demo: (x? | (null:a b c))
#   demo: x? | y?
#
def or_1(A,B):
    if A.empty(): return data()
def or_2(A,B):
    if B.empty(): return data()
def or_3(A,B):  # "de Morgan"
    AL,AR = A.split()
    if AL.atom(): return one(b'|',AL,B) + one(b'|',AR,B)
def or_4(A,B):  # "de Morgan"
    BL,BR = B.split()
    if BL.atom(): return one(b'|',A,BL) + one(b'|',A,BR)
def or_5(A,B):
    if A.atom() and B.atom(): return one(b'#',A,B)
DEF.add(data(b'|'),or_1,or_2,or_3,or_4,or_5)
#
#  not:B is true (i.e. ()) if B is false and is false (=F) if B is empty.
#
#  not : b B -> ()
#  not : ()  -> F
#
#  demo: not : a b c
#  demo: not : (null : a b c)
#  demo: not : (foo:bar)
#
def not_0(A,B):
    if B.empty(): return data(b'F')
def not_1(A,B):
    if any([data(b).atom() for b in B]): return data()
DEF.add(data(b'not'),not_1,not_0)
#
#   logic gets the logical value of it's input
#
#   ...in other words, logic:B is () for true, F for false
#   and some undefined data if the answer is undefined.
#
#   demo: logic : a b c
#   demo: logic : ()
#   demo: logic : (foo:bar)
#
def logic_0(A,B):
    if B.empty(): return data()
def logic_1(A,B):
    if any([data(b).atom() for b in B]): return data(b'F')
DEF.add(data(b'logic'),logic_0,logic_1)
#
#    Implication imply A : B is logical implication.
#
#    If A is true (i.e. ()), B must also be true.
#
#    demo: imply () : ()
#    demo: imply () : x
#    demo: imply x : ()
#    demo: imply x : (foo:bar)
#    demo: imply (foo:bar) : x
#
#def imply(A,B):
#    if A.empty() and any([data(b).atom() for b in B]): return data(b'F')
#def imply_1(A,B):
#    if any([data(a).atom() for a in A]): return data()
#def imply_2(A,B):
#    if A.empty() and B.empty(): return data()
#DEF.add(data(b'imply'),imply,imply_1,imply_2)
