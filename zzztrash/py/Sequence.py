#
#    Sequence operations
#
from base import *
import Number
#
#   Reverse the order of it's input sequence.
#
#   rev : () -> ()
#   rev : b  -> b            ...if b is an atom
#   rev : b B -> (rev:B) b   ...if b is an atom
#
#   demo: rev : a b c
#   demo: rev :
#   demo: rev : nat : 0
#   demo: rev : rev : nat : 0
#
def rev_1(A,B):
    if B.empty(): return data()
def rev_2(A,B):
    if B.atom(): return B
def rev_3(A,B):
    L,R = B.split()
    if not L.empty(): return one(b'rev',A,R)+one(b'rev',A,L)
DEF.add(data(b'rev'),rev_1,rev_2,rev_3)
#def rev_4(A,B):
#    L,R = B.split()
#    if len(L)==1 and is_colon(L[0]):
#        LL,RR = L[0].left(),L[0].right()
#        if LL==data(b'rev'): return RR

#
#   Gets the A-specified leading items from input data.
#
#   first   : B -> (first 1:B)
#   first 0 : B -> ()
#   first n : L R -> L (first n-1 : R) L is atom
#
#   demo: first : a b c
#   demo: first 1 : a b c
#   demo: first 2 : a b c
#   demo: {first 3:B} : {first 2:B} : 1 2 3 4 5
#   demo: first 3 : first 2 : 1 2 3 4 5
#
def first_0(A,B):
    if B.empty(): return data()
def first_1(A,B):
    if A.empty(): return one(b'first',data(b'1'),B)
def first_2(A,B):
    ns = Number.ints(A)
    if ns==[0]: return data()
def first_3(A,B):
    ns = Number.ints(A)
    if len(ns)==1:
        n = ns.pop()
        if n>=1:
            L,R = B.split()
            if L.atom(): return L+one(b'first',data(str(n-1).encode()),R)
DEF.add(data(b'first'),first_1,first_2,first_3,first_0)
#
#   Get the tail items of a sequence.
#
#   demo: tail 2 : a b c d e
#   demo: tail 1 : a b c d e
#   demo: tail : a b c d e
#
def tail(A,B):
    L,R = B.split()
    ns = Number.ints(A)
    if len(ns)==1 and L.atom() and ns[0]>=0:
        n = ns[0]
        if n>0: return   one(b'tail',data(str(n-1).encode()),R)
        else  : return L+one(b'tail',data(b'0'),R)
def tail_0(A,B):
    if B.empty(): return data()
def tail_1(A,B):
    if A.empty(): return one(b'tail',data(b'1'),B)
DEF.add(data(b'tail'),tail_0,tail_1,tail)
#
#   Gets the A-specified last items from it's input
#
#   last : B -> (last 1 : B)
#   last 0 : B -> ()
#   last n : L R -> (last n-1:L) R if R is atom
#
#   demo: last : a b c
#   demo: last 1 : a b c
#   demo: last 2 : a b c
#
def last_1(A,B):
    if A.empty(): return one(b'last',data(b'1'),B)
def last_2(A,B):
    ns = Number.ints(A)
    if ns==[0]: return data()
def last_3(A,B):
    ns = Number.ints(A)
    if len(ns)==1:
        n = ns.pop()
        if n>=1:
            L,R = B.split_right()
            if R.atom(): return one(b'last',data(str(n-1).encode()),L)+R
DEF.add(data(b'last'),last_1,last_2,last_3)
#
#   Repeats the arguments for each input.
#
#   demo: rep $ : a b c
#   demo: rep $ # : a b c
#   demo: rep <*> : a b c
#   demo: rep <*> : first 10 : nat : 0
#
def rep_1(A,B):
    BL,BR = B.split()
    if BL.atom(): return A + one(b'rep',A,BR)
def rep_0(A,B):
    if B.empty(): return data()
DEF.add(data(b'rep'),rep_1,rep_0)
#
#   Select the n'th item from input.
#
def nth1(A,B):
    A0,AR = A.split()
    B0,BR = B.split()
    if A0.atom() and B0.atom():
        ns = Number.ints(A0)
        if len(ns)>0:
            n = ns[0]
            if   n==1: return B0
            elif n> 1: return one(b'nth1',data(str(n-1).encode()),BR)
        else:
            return data()
def nth1_0(A,B):
    if B.empty(): return data()
DEF.add(data(b'nth1'),nth1,nth1_0)
