#
#    Sequence related definitions
#
from base import *
import Number
#
#   Reverse the order of it's input sequence.
#
#   rev : () -> ()
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
#
#   starts, ends
#
#   demo: starts a b c : a b c d e f g
#   demo: starts a b c : a x b c d
#   demo: starts a b c : a
#   demo: starts : a b c
#
def Starts(context,domain,A,B):
    if A.rigid(context):
        n = len(A)
        Front = data(*B[:n])
        if Front.rigid(context):
            if A==Front: return B
            return data()
CONTEXT.define('starts',Starts)
def Ends(context,domain,A,B):
    if A.rigid(context):
        n = len(A)
        Back = data(*B[-n:])
        if A==Back: return B
        return data()
CONTEXT.define('ends',Ends)
#
#   shorter/longer
#
#   demo: less a b : x y z
#   demo: less a b c d : x y
#   demo: more a b : x y z
#   demo: more a b c d : x y
#   demo: aj {put : less (get:A) : (get:B)} : (:x x x x) (:x x) (:x x x)
#   demo: aj {put : more (get:A) : (get:B)} : (:x x x x) (:x x) (:x x x)
#
def less(context,domain,A,B):
    if A.atomic(context) and B.atomic(context):
        if len(A)<=len(B): return A
        return B
def more(context,domain,A,B):
    if A.atomic(context) and B.atomic(context):
        if len(A)>=len(B): return A
        return B
CONTEXT.define('less',less)
CONTEXT.define('more',more)
#
#   frontstrip, backstrip
#
#   demo: stripFront a b : a b c d
#   demo: stripFront c d : a b c d
#   demo: stripFront a b : x y z
#   demo: while stripFront a b : a b a b x y
#   demo: stripBack c d : a b c d
#   demo: stripBack a b : a b c d
#   demo: stripBack a b : x y z
#   demo: while stripBack a b : x y a b a b
#
def FrontStrip(context,domain,A,B):
    if A.rigid(context):
        n = len(A)
        Front = data(*B[:n])
        if Front.rigid(context):
            if A==Front: return data(*B[n:])
            return B
CONTEXT.define('frontstrip',FrontStrip)
def BackStrip(context,domain,A,B):
    if A.rigid(context):
        n = len(A)
        Back = data(*B[-n:])
        if Back.rigid(context):
            if A==Back: return data(*B[:-n])
            return B
CONTEXT.define('backstrip',BackStrip)

def skip_1(context,domain,A,B):
    if B.empty(): return data()
    if A.rigid(context):
        n = sum(Number.nats(A))
        Bs = [b for b in B]
        Sk = []
        while len(Bs)>0 and len(Sk)<n and Bs[0].atom(context): Sk.append(Bs.pop(0))
        if len(Sk)==n: return data(*Bs)
        return data((domain+da(str(n-len(Sk))))|data(*Bs))
CONTEXT.define('skip',skip_1)
#
#   grp batches the input into packets with the same
#   size as the size of the argument.  grp is an inverse
#   of get, so (get * grp A) is always the identity.
#
#   demo: grp x x : a b c d
#   demo: grp x x : a b c d e
#   demo: grp x : a b c d e
#   demo: grp : a b c d e
#   demo: get : grp x x : a b c
#   demo: get : grp : a b c
#   demo: grp :
#   demo: get : grp :
#
def Grp(context,domain,A,B):
    if A.atomic(context):
        if len(A)==0: return data(data()|B)
        Bfront = data(*B[:len(A)])
        Bback  = data(*B[len(A):])
        if Bfront.atomic(context):
            if Bfront.empty(): return data()
            return data(data()|Bfront) + data((domain+A)|Bback)
CONTEXT.define('grp',Grp)
#
#   demo: by 2 : a b c d
#   demo: by 2 : a b c d e
#
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
CONTEXT.define('by',By)
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
    if A.rigid(context) and B.rigid(context):
        ns = Number.nats(A)
        if len(ns)>0:
            n = ns[0]
            R = []
            for i in range(n):
                for b in B: R.append(b)
            return data(*R)
CONTEXT.define('rep',rep)
#
#   Gets first saturation point of a sequence
#
#   demo: sat :
#   demo: sat : a
#   demo: sat : a b c
#   demo: sat : a b c c
#   demo: sat : a b c c d d
#
def sat(context,domain,A,B):
    B1,BR = B.split()
    if B1.rigid(context) and B1.atom(context):
        B2,BRR = BR.split()
        if B2.rigid(context) and B2.atom(context):
            if B1==B2: return B2
            return data(domain|(B2+BRR))
#CONTEXT.define('sat',sat)
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
#
#   width A : B gives B if B has the same width as A,
#   () otherwise.
#
#   demo: width | | : a b
#   demo: width | | : a b c
#
def width(context,domain,A,B):
    if A.atomic(context) and B.atomic(context):
        if len(A)==len(B): return B
        return data()
CONTEXT.define('width',width)
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
#
#   Matrix is a general product of two data a(i) b(j)
#   producing a sequence (bin i j,a(i) b(j))
#
#   demo: freesum a b c : x y z
#   demo: freesum a : x y z 
#   demo: freeprod a b c : x y z
#   demo: collect : ap {(bin (nat_sum:arg:B):right:B)} : freeprod a b c : x y z
#
def freeprod(context,domain,A,B):
    if A.atomic(context) and B.atomic(context):
        sum = []
        for i in range(len(A)):
            for j in range(len(B)): sum.append((da('bin')+da(str(i))+da(str(j)))|data(A[i],B[j]))
        return data(*sum)
CONTEXT.define('freeprod',freeprod)

def freesum(context,domain,A,B):
    AL,AR = A.split()
    BL,BR = B.split()
    if AL.empty() and BL.empty():
        return data()
    elif AL.atom(context) and BL.empty():
        return data(data()|AL) + data((domain+AR)|BR)
    elif AL.empty() and BL.atom(context):
        return data(data()|BL) + data((domain+AR)|BR)
    elif AL.atom(context) and BL.atom(context):
        return data(data()|(AL+BL)) + data((domain+AR)|BR)
CONTEXT.define('freesum',freesum)
