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
def Pass(context,domain,A,B): return B
def Null(context,domain,A,B): return data()
CONTEXT.define('pass',Pass)
CONTEXT.define('null',Null)
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
#   demo: get bin : bin : 1 2 3
#   demo: get bin : (bin x y z : 1 2 3)
#   demo: get : (:a b c) (put : 1 2 3)
#   demo: arg bin : bin a b c : 1 2 3
#   demo: get bin : (bin a b c:1 2 3) (bin d e f: 4 5 6)
#   demo: arg bin : (bin a b c:1 2 3) (bin d e f: 4 5 6)
#
def Put(context,domain,A,B): return data(A|B)
CONTEXT.define('put',Put)

def get(context,domain,A,B):
    if A.rigid(context):
        if B.empty(): return data()
        L = []; Bs = [b for b in B]
        while len(Bs)>0 and Bs[0].atom(context):
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
#   demo: arg : bin 1 2 3 : a b c
#
def domain_0(context,domain,A,B):
    BL,BR = B.split()
    if BL.atom(context): return BL[0].domain() + data((domain+A)|BR)
def domain_1(context,domain,A,B):
    if B.empty(): return data()
CONTEXT.define('domain',domain_0,domain_1)
def right(context,domain,A,B):
    BL,BR = B.split()
    if BL.atom(context): return BL[0].right() + data((domain+A)|BR)
    if BL.empty(): return data()
CONTEXT.define('right',right)
def left(context,domain,A,B):
    BL,BR = B.split()
    if BL.atom(context): return BL[0].left() + data((domain+A)|BR)
    if BL.empty(): return data()
CONTEXT.define('left',left)
def arg(context,domain,A,B):
    BL,BR = B.split()
    if BL.atom(context): return BL[0].arg() + data((domain+A)|BR)
    if BL.empty(): return data()
CONTEXT.define('arg',arg)
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
#   demo: if (not:bin:) : 1 2 3
#   demo: nif (bin:) : 1 2 3
#
def if_1(context,domain,A,B):
    if A.irred(context): return data()
def if_0(context,domain,A,B):
    if A.empty(): return B
CONTEXT.define('if',if_1,if_0)
def nif_1(context,domain,A,B):
    if A.empty(): return data()
def nif_0(context,domain,A,B):
    if A.irred(context): return B
CONTEXT.define('nif',nif_1,nif_0)
#
#   product and sum
#
#   demo: sum (:pass) (:rev) (:first 2) : a b c d
#   demo: prod (:pass) (:rev) (:first 2) : a b c d
#
def prod(context,domain,A,B):
    AL,AR = A.split()
    if AL.empty(): return B
    if AL.atom(context): return data(AL[0].right()|data((domain+AR)|B))
def sum(context,domain,A,B):
    AL,AR = A.split()
    if AL.empty(): return data()
    if AL.atom(context): return (AL[0].right()|B) + ((domain+AR)|B)
CONTEXT.define('prod',prod)
CONTEXT.define('sum',sum)
#
#   demo: depth :
#   demo: depth : (:)
#   demo: depth : (:):(:)
#
def depth(context,domain,A,B):
    if B.rigid(context): return da(str(B.depth()))
CONTEXT.define('depth',depth)
