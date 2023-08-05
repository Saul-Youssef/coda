#
#    Sequence related definitions
#
from base import *
import Number
#
#   some/none define the coarsest data classification
#
#   demo: some : a b c
#   demo: some :
#   demo: none : a b c
#   demo: none :
#
def some(domain,A,B):
    if A.atomic(): return A
    if A.empty (): return B
CONTEXT.define('some',some)

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
def rev_1(domain,A,B):
    BL,BR = B.split()
    if len(BL)>0 and len(BR)>0: return ((domain+A)|BR) + ((domain+A)|BL)
def rev_2(domain,A,B):
    if B.atom(): return B
def rev_3(domain,A,B):
    if B.empty(): return data()
CONTEXT.define('rev',rev_3,rev_2,rev_1)
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
def first_1(domain,A,B):
    if B.empty(): return data()
def first_2(domain,A,B):
    if A.empty(): return data(domain+da('1')|B)
def first_3(domain,A,B):
    if Number.ints(A)==[0]: return data()
def first_4(domain,A,B):
    ns = Number.ints(A)
    if len(ns)==1:
        n = ns.pop()
        if n>=1 and len(B)>0 and B[0].atom():
            return B[0] + ((domain+da(str(n-1))) | data(*B[1:]))
CONTEXT.define('first',first_1,first_2,first_3,first_4)
#
#   Get the tail items of a sequence.
#
#   demo: tail 2 : a b c d e
#   demo: tail 1 : a b c d e
#   demo: tail : a b c d e
#
def tail_0(domain,A,B):
    L,R = B.split()
    ns = Number.ints(A)
    if len(ns)==1 and L.atom() and ns[0]>=0:
        n = ns[0]
        if n>0: return     data((domain+da(str(n-1)))|R)
        else  : return L + data((domain+da(str(  0)))|R)
def tail_1(domain,A,B):
    if B.empty(): return data()
def tail_2(domain,A,B):
    if A.empty(): return data((domain+da('1'))|B)
CONTEXT.define('tail',tail_0,tail_1,tail_2)
#
#   Gets the argument-specified last items from input
#
#   last : B -> (last 1 : B)
#   last 0 : B -> ()
#   last n : L R -> (last n-1:L) R if R is atom
#
#   demo: last : a b c
#   demo: last 1 : a b c
#   demo: last 2 : a b c
#
def last_0(domain,A,B):
    if B.empty(): return data()
def last_1(domain,A,B):
    if A.empty(): return data((domain+da('1'))|B)
def last_2(domain,A,B):
    ns = Number.ints(A)
    if ns==[0]: return data()
def last_3(domain,A,B):
    ns = Number.ints(A)
    if len(ns)==1:
        n = ns.pop()
        if n>=1:
            L,R = data(*B[:-1]),data(*B[-1:])
            if R.atom(): return data((domain+da(str(n-1)))|L) + R
CONTEXT.define('last',last_0,last_1,last_2,last_3)
#
#   Repeats the arguments for each input.
#
#   demo: rep $ : a b c
#   demo: rep $ # : a b c
#   demo: rep <*> : a b c
#   demo: rep <*> : first 10 : nat : 0
#
def rep_1(domain,A,B):
    BL,BR = B.split()
    if BL.atom(): return A + data((domain+A)|BR)
def rep_0(domain,A,B):
    if B.empty(): return data()
CONTEXT.define('rep',rep_1,rep_0)
#
#   Select the n'th item(s) from input.
#
def nth1_0(domain,A,B):
    A0,AR = A.split()
    B0,BR = B.split()
    if A0.atom() and B0.atom():
        ns = Number.ints(A0)
        if len(ns)>0:
            n = ns[0]
            if   n==1: return B0
            elif n> 1: return data(domain+da(str(n-1))|BR)
        else:
            return data()
def nth1_1(domain,A,B):
    if B.empty(): return data()
CONTEXT.define('nth1',nth1_0,nth1_1)
#
#   Pre and post avoids parentheses
#
#   demo: pre 0 : 1 2 3
#   demo: post 99 : 1 2 3
#
CONTEXT.define('pre', lambda domain,A,B : A+B)
CONTEXT.define('post',lambda domain,A,B : B+A)
#
#    invariant(A) is true iff A is recursively invariant
#
#def invariant(A):
#    return A.invariant() and \
#        all([invariant(a.left ()) for a in A]) and \
#        all([invariant(a.right()) for a in A])

#
#   once returns input with duplicates removed.
#
#   demo: once : a b c
#   demo: once : a b c c c d e f
#
def once_1(domain,A,B):
    if A.rigid():
        AA = set([a for a in A])
        BL,BR = B.split()
        if BL.empty():
            return data()
        elif BL.atom() and BL.rigid():
            if BL[0] in AA:
                return data(domain+A|BR)
            else:
                return BL+data(domain+A+BL|BR)
def once_0(domain,A,B):
    if B.empty(): return data()
CONTEXT.define('once',once_1,once_0)

def In(domain,A,B):
    if A.rigid():
        AA = set([a for a in A])
        BL,BR = B.split()
        if BL.empty():
            return data()
        elif BL.atom() and BL.rigid():
            if BL[0] in AA:
                return BL+data(domain+A|BR)
            else:
                return data(domain+A|BR)
def In_0(domain,A,B):
    if B.empty(): return data()
CONTEXT.define('in',In,In_0)
