#
#   The basic operators
#
from base import *
#
#  pass : B is defined to be B, as is id : B.
#
#  pass : B -> B
#  id : B -> B
#
#  demo: pass : a b c
#  demo: null : a b c
#  demo: id : a b c
#  demo:  : a b c
#
DEF.add(data(b'pass'), lambda A,B:      B)
DEF.add(data()       , lambda A,B:      B)
DEF.add(data(b'null'), lambda A,B: data())
DEF.add(data(b'error'))
#
#   if A : B -> () if A is false
#   if A : B -> B  if A is true
#
#   demo: if x : 1 2 3
#   demo: if () : 1 2 3
#   demo: if : 1 2 3
#   demo: if (foo:bar) : 1 2 3
#   demo: if (bin:x y) : 1 2 3
#   demo: if (bin:) : 1 2 3
#
def if_1(A,B):
    for a in A:
        if data(a).atom(): return data()
def if_0(A,B):
    if A.empty(): return B
DEF.add(data(b'if'),if_1,if_0)
#
#   put A : B creates A:B, it "puts B into A".
#
#   put A : B -> (A:B)
#
#   demo: put x : 1 2 3
#   demo: put x y : 1 2 3
#   demo: ap put x : 1 2 3
#
DEF.add(data(b'put'),lambda A,B: data(colon(A,B)))
#
#   Singleton versions of left, right, has, get and atom
#
def select(A,B):
    if B.atom():
        col = B.colonize()[0]
        guard = one(b'=',A,col.left())
        return one(b'if',guard,B)
def get(A,B):
    if B.atom():
        col = B.colonize()[0]
        guard = one(b'=',A,col.left())
        return one(b'if',guard,col.right())
def atom(A,B):
    if B.atom(): return B
DEF.add(data(b'sel1'),select)
DEF.add(data(b'atom1'),atom)
DEF.add(data(b'get1'),get)
#
#   Star is syntactic sugar with A*B:X defined to be A:B:X.
#
#   If you think of A and B as functions with actions X |-> A:X,
#   then A*B is function composition.
#
#   star (star L,R):B -> L:(R:B)
#
#   demo: count*first:a b c
#   demo: first*count:a b c
#   demo: {first 2:B} * {first 3:B} : 1 2 3 4 5
#   demo: {first 2:B} * {rev:B} : 1 2 3 4 5
#
def star(A,B):
    if len(A)==1 and is_colon(A[0]):
        L = A[0].left()
        R = A[0].right()
        S,LL = L.split()
        if S==data(b'*'): return data(colon(LL,data(colon(R,B))))
DEF.add(data(b'*'),star)
