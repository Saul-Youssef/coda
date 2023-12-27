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
#def arg(context,domain,A,B):
#    if A.rigid(context):
#        if B.empty(): return data()
#        L = []; Bs = [b for b in B]
#        while len(Bs)>0 and Bs[0].atom(context):
#            b = Bs.pop(0)
#            if b.domain()==A:
#                for r in b.arg(): L.append(r)
#        front = data(*L)
#        back = data((domain+A)|data(*Bs))
#        return front+back
#CONTEXT.define('arg',arg)
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
#    Star is syntactic sugar with A*B:X defined to be A:B:X
#    Star is syntactic sugar where A*B X : Y is defined to be A : B X : Y.
#
#    If you think of A and B as functions, with action X -> A:X,
#    this is function composition.
#
#   demo: count*first:a b c
#   demo: first*count:a b c
#   demo: {first 2:B} * {first 3:B} : 1 2 3 4 5
#   demo: {first 2:B} * {rev:B} : 1 2 3 4 5
#   demo: (pass*first) 2 : 1 2 3
#   demo: (first * pass) 2 : 1 2 3
#
#def star(context,domain,A,B):
#    AL,AR = A.split()
#    if AL.atom(context):
#        L,R = AL[0].left(),AL[0].right()
#        LL,LR = L.split()
#        if LL==da('bin'): return data((LR)|data((R+AR)|B))
#CONTEXT.define('*',star)


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
#   product and sum
#
#   demo: product (:first 3) (:rev) : a b c d e f g
#   demo: product (:rev) (:first 3) : a b c d e f g
#   demo: (prod : (:rev) (:first 3)) : a b c d e f g
#   demo: (prod : (:rev) (:first)) : a b c d e f g
#   demo: (prod 3 : (:rev) (:first)) : a b c d e f g
#   demo: sum (:first 3) (:rev) : a b c d e f g
#   demo: sum (:rev) (:first 3) : a b c d e f g
#   demo: sum (:rev) (:{first 3:B}) : a b c d e f g
#   demo: sum (bin:rev) (bin:{first 3:B}) : a b c d e f g
#
#def aprod_1(context,domain,A,B):
#    if len(A)>0 and A[-1].atom(context):
#        AL,a = data(*A[:-1]),A[-1]
#        return data((domain+AL)|data(a.right()|B))
#def aprod_0(context,domain,A,B):
#    if A.empty(): return B
#def aprod_2(context,domain,A,B):
#    if A.atom(context): return data(A[0].right()|B)
#CONTEXT.define('product',aprod_1,aprod_0,aprod_2)
#
#def bprod_1(context,domain,A,B):
#    if B.atomic(context):
#        if len(B)>0:
#            B2 = [b for b in B]
#            b = B2.pop()
#            b = b.left()|(b.right()+A)
#            B2.append(b)
#            return da('product')+data(*B2)
#        else:
#            return da('product')
#CONTEXT.define('prod',bprod_1)
