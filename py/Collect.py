#
#    Collect and equivalence classes
#
from base import *
#
#   Collect inputs b with the same value of (A:b).
#
#   1. Equivalence classes of input codes.
#   2. Same as 1 with collected value (bin V:...)
#   3. Codes with the same length as byte sequences.
#   4. Same as 3 with the length (bin L:..codes with length L..)
#
#   demo: collect : a b c d
#   demo: collect : (bin:a) (bin:b) (bin:c) (bin:d)
#   demo: collect : ap {put bin (nchar:B):B} : a b aa bb aaa cccc zz xxx xxx
#   demo: collect : (bin 1:c) (bin 1:a b) (bin 2:aa bb zz) (:a) (:b) a b c
#   demo: equiv nchar : a b aa bb aaa cccc zz xxx xxx
#
def collect(context,domain,A,B):
    if all([b.atom(context) and b.left().stable(context) for b in B]):
        lefts = {}
        for b in B:
            if not b.left() in lefts: lefts[b.left()] = []
            lefts[b.left()] = lefts[b.left()] + [r for r in b.right()]
        L = []
        for left,rights in lefts.items(): L.append(left|data(*rights))
        return data(*L)
CONTEXT.define('collect',collect)
#    if all([b.atom(context) and b.left().rigid(context) for b in B]):
