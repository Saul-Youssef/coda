#
#    Selection definitions
#
from base import *
#
#   collect_left : D collects items (A:B) in D where the
#   left parts of their colons are equal.
#
#   demo: apleft count : a b c
#   demo: collect_left : apleft count : a b c
#   demo: apleft {count:get bin:B} : (bin:1 2 3) (bin:a b c) (bin:x)
#   demo: collect_left : apleft {count:get bin:B} : (bin:1 2 3) (bin:a b c) (bin:x)
#
def collect_left(A,B):
    import Evaluate
    if all([b.left().atom() and Evaluate.invariant(b.left()) for b in B]):
        eq = {}; L = []
        for b in B:
            if not b.left() in eq: eq[b.left()] = []
            eq[b.left()] = eq[b.left()] + [bb for bb in b.right()]
        for key,value in eq.items():
            L.append(colon(key,data(*value)))
        return data(*L)
def collect_left_0(A,B):
    if B.empty(): return data()
#DEF.add(data(b'collect_left'),collect_left,collect_left_0)
