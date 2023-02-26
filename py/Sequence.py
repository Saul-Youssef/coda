#
#    Sequence related definitions
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
def rev(domain,A,B):
    if   B.empty(): return data()
    elif B.atom(): return B
    elif len(B)>1:
        L,R = B.split()
        return ((domain+A)|R) + ((domain+A)|L)
CONTEXT.define('rev',rev)
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
CONTEXT.define('last',last_1,last_2,last_3)
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
#   Select the n'th item from input.
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
