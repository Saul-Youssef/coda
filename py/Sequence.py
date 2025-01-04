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
#   front/back organically removes an argument specified number of
#   items from the front/back of the input.
#
#   front a A : b B -> b (front A:B)
#   front A : B -> () if A or B are empty
#
#   back a A : B b -> (back A:B) b
#   back A : B -> () if A or B are empty
#
#   demo: front | | : a b c d e f g
#   demo: back  | | : a b c d e f g
#   demo: item  | | : a b c d e f g
#
def front(context,domain,A,B):
    if A.empty() or B.empty(): return data()
    AL,AR = A.split()
    BL,BR = B.split()
    if AL.atom(context) and BL.atom(context): return BL + data((domain+AR)|BR)
CONTEXT.define('front',front)
def back(context,domain,A,B):
    if A.empty() or B.empty(): return data()
    AL,AR = A.split()
    BL,BR = B.splitr()
    if AL.atom(context) and BR.atom(context): return data((domain+AR)|BL) + BR
CONTEXT.define('back',back)
#
#   Basic sequence operations
#
#   demo: head 2 : a b c d e f g
#   demo: tail 2 : a b c d e f g
#   demo: first 2 : a b c d e f g
#   demo: last 2 : a b c d e f g
#   demo: head : a b c d e f g
#   demo: tail : a b c d e f g
#   demo: first : a b c d e f g
#   demo: last : a b c d e f g
#   demo: head 2 1 : a b c d e f g
#   demo: tail 2 1 : a b c d e f g
#   demo: skip : a b c
#   demo: skip 2 : a b c d e
#   demo: by 2 : a b c d e
#   demo: by : a b c d e
#   demo: by 2 : nat : 0
#
def head_(context,domain,A,B):
    if B.empty(): return data()
    if A.rigid(context):
        ns = Number.nats(A)
        n = sum(ns)
        if n==0: return data()
        Bs = [b for b in B]
        if not Bs[0].atom(context): return
        front = []
        while n>0 and len(Bs)>0 and Bs[0].atom(context):
            front.append(Bs.pop(0))
            n -= 1
        return data(*front) + data((domain+da(str(n)))|data(*Bs))
CONTEXT.define('head',head_)
def tail_0(context,domain,A,B):
    if B.empty(): return data()
    if A.rigid(context):
        L,R = B.split()
        ns = Number.ints(A)
        n = sum(ns)
        if n==0: return B
        if L.atom(context):
            if n>0: return     data((domain+da(str(n-1)))|R)
            else  : return L + data((domain+da(str(  0)))|R)
CONTEXT.define('tail',tail_0)

def last(context,domain,A,B):
    if A.rigid(context):
        ns = Number.nats(A)
        n = 1
        if len(ns)>0: n = ns.pop(0)
        if n>=1:
            L,R = data(*B[:-1]),data(*B[-1:])
            if R.atom(context): return data((domain+da(str(n-1)))|L) + R
        else:
            return data()
CONTEXT.define('last',last)

def skip_1(context,domain,A,B):
    if B.empty(): return data()
    if A.rigid(context):
        n = sum(Number.nats(A))
        Bs = [b for b in B]
        Sk = []
        while len(Bs)>0 and len(Sk)<n and Bs[0].atom(context): Sk.append(Bs.pop(0))
        if len(Sk)==n: return data(*Bs)
        return data((domain+da(str(n-len(Sk))))|data(*Bs))
#CONTEXT.define('skip',skip_1)

#
#
def BY(context,domain,A,B):
    if A.atomic(context):
        Bfront = data(*B[:len(A)])
        Bback  = data(*B[len(A):])
        if Bfront.atomic(context):
            if   len(Bfront)==0:
                return data()
            else:
                return data(data()|Bfront) + data((domain+A)|Bback)
CONTEXT.define('by',BY)

def By(context,domain,A,B):
    if B.empty(): return data()
    if A.rigid(context):
        import Number
        ns = Number.ints(A)
        n = 1
        if len(ns)>0 and ns[0]>1: n = ns[0]
        L = []
        Bs = [b for b in B]
        while len(Bs)>0 and data(*Bs[:n]).atomic(context):
            L.append(data()|data(*Bs[:n]))
            Bs = Bs[n:]
        L.append((domain+A)|data(*Bs))
        return data(*L)
#CONTEXT.define('by',By)
#
#   Input repetition
#
#   rep n A : B -> rep n : rep A : B
#   rep n : B -> B repeated n times
#   rep : B -> B
#
#   demo: rep 5 : x
#   demo: rep 4 : a b
#   demo: rep 0 : x
#   demo: rep : x
#
def rep(context,domain,A,B):
    if A.rigid(context):
        ns = Number.nats(A)
        if len(ns)==1:
            B2 = []
            n = ns[0]
            while n>0:
                for b in B: B2.append(b)
                n = n-1
            return data(*B2)
        elif len(ns)==0:
            return B
#CONTEXT.define('rep_',rep)

#
#   Input repetition
#
#   demo: dup | | | : x y
#   demo: dup | | : x y
#   demo: dup | : x y
#   demo: dup : x y
#
def dup(context,domain,A,B):
    if len(A)==1:
        if A.atom(context): return B
    if len(A)==0:
        return data()
    if len(A)>1:
        return data(*[((domain+data(a))|B) for a in A])
CONTEXT.define('dup',dup)
#
#   Maximum common data starting A and B
#
#   demo: common 1 2 3 4 : 1 2 3
#   demo: common 1 2 3 : 1 2 3 4 5
#   demo: common : 1 2
#   demo: common :
#
def common(context,domain,A,B):
    AL,AR = A.split()
    BL,BR = B.split()
    if AL.empty() or BL.empty(): return data()
    if AL.rigid(context) and BL.rigid(context):
        if AL==BL: return AL + data((domain+AR)|BR)
        else     : return data()
CONTEXT.define('common',common)

#def dup___(context,domain,A,B):
#    if len(B)==1:
#        if B.atom(context): return A
#    if len(B)==0:
#        return data()
#    if len(B)>0:
#        return data(*[(domain+A)|data(b) for b in B])
#CONTEXT.define('dup',dup)
#
#   Select the n'th item(s) from input.
#
def nth1_0(context,domain,A,B):
    if B.empty(): return data()
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
#
#   Swap transposes two elements of a sequence
#
#   demo: swap 1 3 : a b c d e
#   demo: swap 1 3 : swap 1 2 : a b c d e
#
def swap(context,domain,A,B):
    if A.rigid(context):
        ns = Number.nats(A)
        ns = [n for n in ns if n>0]
        if len(ns)==2:
            i,j = ns[0]-1,ns[1]-1
            m = max(i,j)
            Bs = [b for b in B]
            if all(b.atom(context) for b in Bs[:m]):
                if i<0 or i>=len(Bs): return B
                if j<0 or j>=len(Bs): return B
                if len(Bs)<m: return B
                x = Bs[i]
                y = Bs[j]
                Bs[i] = y
                Bs[j] = x
                return data(*Bs)
        else:
            return B
CONTEXT.define('swap',swap)
