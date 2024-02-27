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
def rev_1(context,domain,A,B):
    BL,BR = B.split()
    if len(BL)>0 and len(BR)>0: return ((domain+A)|BR) + ((domain+A)|BL)
def rev_2(context,domain,A,B):
    if B.atom(context): return B
def rev_3(context,domain,A,B):
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
#   demo: tail 2 : a b c d e
#   demo: tail 1 : a b c d e
#   demo: tail : a b c d e
#   demo: last : a b c
#   demo: last 1 : a b c
#   demo: last 2 : a b c
#   demo: skip : a b c
#   demo: skip 2 : a b c d e
#   demo: by 2 : a b c d e
#   demo: by : a b c d e
#   demo: by 2 : nat : 0
#
def first_(context,domain,A,B):
    if B.empty(): return data()
    if A.rigid(context):
        ns = Number.nats(A)
        n = sum(ns)
#        n = 0
#        if len(ns)>0: n = ns.pop(0)
        if n==0: return data()
        Bs = [b for b in B]
        if not Bs[0].atom(context): return
        front = []
        while n>0 and len(Bs)>0 and Bs[0].atom(context):
            front.append(Bs.pop(0))
            n -= 1
        return data(*front) + data((domain+da(str(n)))|data(*Bs))
CONTEXT.define('first',first_)
#def tail_(context,domain,A,B):
#    if B.empty(): return data()
#    if A.rigid(context):
#        ns = Number.nats(A)
#        n = 0
#        if len(ns)>0: n = ns.pop(0)
#        if n==0: return B
#        Bs = [b for b in B]
#        if not Bs[-1].atom(context): return
#        back = []
#        while n>0 and len(Bs)>0 and Bs[-1].atom(context):
#            back.insert(0,Bs.pop())
#            n -= 1
#        return data((domain+da(str(n)))|data(*Bs)) + data(*back)
#CONTEXT.define('last',tail_)

#def OLDfirst_(context,domain,A,B):
#    if B.empty(): return data()
#    if A.rigid(context):
#        ns = Number.nats(A)
#        if len(ns)==0: n = 1
#        else: n = ns.pop(0)
#        if n==0: return data()
#        Bs = [b for b in B]
#        front = []
#        while n>0 and len(Bs)>0 and Bs[0].atom(context):
#           front.append(Bs.pop(0))
#           n -= 1
#        return data(*front) + data((domain+da(str(n)))|data(*Bs))
#
#def first_1(context,domain,A,B):
#    if B.empty(): return data()
#def first_2(context,domain,A,B):
#    if A.empty(): return data(domain+da('1')|B)
#def first_3(context,domain,A,B):
#    if Number.ints(A)==[0]: return data()
#def first_4(context,domain,A,B):
#    ns = Number.ints(A)
#    if len(ns)==1:
#        n = ns.pop()
##        if n>=1 and len(B)>0 and B[0].atom(context):
#            return B[0] + ((domain+da(str(n-1))) | data(*B[1:]))
#CONTEXT.define('first',first_1,first_2,first_3,first_4)
def tail_0(context,domain,A,B):
    if B.empty(): return data()
    if A.rigid(context):
        L,R = B.split()
        ns = Number.ints(A)
        n = sum(ns)
#    if len(ns)==0: return B
        if n==0: return B
        if L.atom(context):
            if n>0: return     data((domain+da(str(n-1)))|R)
            else  : return L + data((domain+da(str(  0)))|R)
#def tail_1(context,domain,A,B):
#    if B.empty(): return data()
#def tail_2(context,domain,A,B):
#    if A.empty(): return data((domain+da('1'))|B)
CONTEXT.define('last',tail_0)
def last_0(context,domain,A,B):
    if B.empty(): return data()
def last_1(context,domain,A,B):
    if A.empty(): return data((domain+da('1'))|B)
def last_2(context,domain,A,B):
    ns = Number.ints(A)
    if ns==[0]: return data()
def last_3(context,domain,A,B):
    ns = Number.ints(A)
    if len(ns)==1:
        n = ns.pop()
        if n>=1:
            L,R = data(*B[:-1]),data(*B[-1:])
            if R.atom(context): return data((domain+da(str(n-1)))|L) + R
#CONTEXT.define('last',last_0,last_1,last_2,last_3)
def skip_0(context,domain,A,B):
    if B.empty(): return data()
def skip_1(context,domain,A,B):
    if A.rigid(context):
        n = Number.intdef(1,A)
        if n==0: return B
        BL,BR = B.split()
        if BL.atom(context): return data((domain+da(str(n-1)))|BR)
CONTEXT.define('skip',skip_0,skip_1)

def By(context,domain,A,B):
    if A.rigid(context):
        import Number
        ns = Number.ints(A)
        n = 1
        if len(ns)>0 and ns[0]>1: n = ns[0]
        if data(*B[:n]).atomic(context): return (data()|data(*B[:n])) + ((domain+A)|data(*B[n:]))
def By_0(context,domain,A,B):
    if B.empty(): return data()
CONTEXT.define('by',By_0,By)
#
#   Repeats the arguments for each input.
#
#   demo: rep 5 : x
#   demo: rep 4 : a (:)
#
def rep_0(context,domain,A,B):
    if A.rigid(context) and B.atomic(context):
        try:
            n = int(str(A[0]))
            Bs = [b for b in B]
            L = []
            for i in range(n):
                for b in Bs: L.append(b)
            return data(*L)
        except Exception as e:
            return B
CONTEXT.define('rep',rep_0)
#
#   Select the n'th item(s) from input.
#
def nth1_0(context,domain,A,B):
    A0,AR = A.split()
    B0,BR = B.split()
    if A0.empty(): return data()
    elif A0.atom(context) and B0.atom(context):
        ns = Number.nats(A0)
        if len(ns)>0:
            n = ns[0]
            if n==0: return data()
            if n==1: return B0
            if n> 1: return data(domain+da(str(n-1))|BR)
        else:
            return data()
def nth1_1(context,domain,A,B):
    if B.empty(): return data()
CONTEXT.define('nth1',nth1_0,nth1_1)
#
#   once returns input with duplicates removed.
#
#   demo: once : a b c
#   demo: once : a b c c c d e f
#
def Once_1(context,domain,A,B):
    if B.rigid(context):
        S = set([b for b in B])
        L = []
        for b in B:
            if not b in L:
                L.append(b)
                S.add(b)
        return data(*L)
CONTEXT.define('once',Once_1)
#
#   Count counts the number of atoms
#
#   demo: count : a b c d
#   demo: int_sum : ap const 1 : a b c d
#   demo: count : nat : 0
#
def count(context,domain,A,B):
    if all([b.atom(context) for b in B]): return da(str(len(B)))
def count_0(context,domain,A,B):
    if B.empty(): return data()
CONTEXT.define('count',count,count_0)
