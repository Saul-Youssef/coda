#
#   Basic definitions
#
from base import *
#
#    pass : B -> B and null : B -> ()
#
#    demo: pass : 1 2 3
#    demo: null : 1 2 3
#
CONTEXT.define('pass',lambda context,domain,A,B:B)
CONTEXT.define('null',lambda context,domain,A,B:data())
CONTEXT.define('bin') # generic built-in container
#
#   put A : B creates A:B, it "puts B into A".
#
#   put A : B -> (A:B)
#
#   demo: put bin : 1 2 3
#   demo: put bin a b c : 1 2 3
#   demo: ap put bin : 1 2 3
#   demo: (put:)
#   demo: pure : put :
#
CONTEXT.define('put',lambda context,domain,A,B: data(A|B))
#
#   demo: get bin : bin : 1 2 3
#   demo: get bin : (bin x y z : 1 2 3)
#   demo: get : (:a b c) (put : 1 2 3)
#
def get(context,domain,A,B):
    if context.rigid(A):
        if B.empty(): return data()
        L = []; Bs = [b for b in B]
        while len(Bs)>0 and Bs[0].atom():
            b = Bs.pop(0)
            if b.domain()==A:
                for r in b.right(): L.append(r)
        front = data(*L)
        back  = data((domain+A)|data(*Bs))
        return front+back
CONTEXT.define('get',get)
#
#   demo: left : bin 1 2 3 : a b c
#   demo: right : bin 1 2 3 : a b c
#   demo: domain : bin 1 2 3 : a b c
#
def domain_0(context,domain,A,B):
    BL,BR = B.split()
    if context.atom(BL): return BL[0].domain() + data((domain+A)|BR)
def domain_1(context,domain,A,B):
    if B.empty(): return data()
CONTEXT.define('domain',domain_0,domain_1)
def left(context,domain,A,B):
    BL,BR = B.split()
    if context.atom(BL):
        L = BL[0].left()
        LL,LR = L.split()
        return LR + data((domain+A)|BR)
    if BL.empty(): return data()
CONTEXT.define('left',left)
def right(context,domain,A,B):
    BL,BR = B.split()
    if context.atom(BL): return BL[0].right() + data((domain+A)|BR)
    if BL.empty(): return data()
CONTEXT.define('right',right)
#
#   if and nif return output depending on argument logic.
#
#   demo: if (1=1) : 1 2 3
#   demo: if (1=2) : 1 2 3
#   demo: if x : 1 2 3
#   demo: if () : 1 2 3
#   demo: if : 1 2 3
#   demo: if (foo:bar) : 1 2 3
#   demo: if (bin:x y) : 1 2 3
#   demo: if (bin:) : 1 2 3
#   demo: nif (bin:) : 1 2 3
#
def if_1(context,domain,A,B):
    if context.irred(A): return data()
def if_0(context,domain,A,B):
    if A.empty(): return B
CONTEXT.define('if',if_1,if_0)
def nif_1(context,domain,A,B):
    if A.empty(): return data()
def nif_0(context,domain,A,B):
    if context.irred(A): return B
CONTEXT.define('nif',nif_1,nif_0)
#
#    Star is syntactic sugar with A*B:X defined to be A:B:X
#
#    If you think of A and B as functions, with action X -> A:X,
#    this is function composition.
#
#   demo: count*first:a b c
#   demo: first*count:a b c
#   demo: {first 2:B} * {first 3:B} : 1 2 3 4 5
#   demo: {first 2:B} * {rev:B} : 1 2 3 4 5
#   demo: first 2 * pass : 1 2 3
#   demo: first * pass 2 : 1 2 3
#   demo: (first * pass) 2 : 1 2 3
#
def star(context,domain,A,B):
    AL,AR = A.split()
    if context.atom(AL):
        L,R = AL[0].left(),AL[0].right()
        LL,LR = L.split()
        if LL==da('bin'): return data((LR+AR)|data((R+AR)|B))
CONTEXT.define('*',star)
