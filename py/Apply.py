#
#    Applications are foundational combinatorial
#    definitions.  ap, especially, is everywhere.
#
from base import *
#
#  Apply A to each b in B.
#
#  This is one of the most important basic
#  combinatorial operations.  ap A is guaranteed
#  to be distributive data for any data A.
#
#  ap A : B C -> (ap A:B) (ap A:C)
#  ap A : B -> A:B if B is atom
#  ap A : () -> ()
#
#  demo: foo : 1 2 3
#  demo: ap foo : 1 2 3
#  demo: ap {foo : B} : 1 2 3
#  demo: apall a b c : 1 2 3
#  demo: apeach a b c : 1 2 3
#  demo: apall  {put 1:B} {put 2:B} {put 3:B} : a b c
#  demo: apeach {put 1:B} {put 2:B} {put 3:B} : a b c
#  demo: aparg a b c : 1 2 3
#  demo: aparg first 2 3 : a b c d e f g
#  demo: apbin foo : a b c d
#  demo: apbin int_add : 1 2 3 4 5
#  demo: apby 2 foo : a b c d e f g
#  demo: apif {(count:get bin:B)=2} : (bin:a b) (bin:a b c) (bin:x y) (bin:a b c d)
#
def ap_0(domain,A,B):
    if B.empty(): return data()
def ap_1(domain,A,B):
    if B.atom(): return data(A|B)
def ap_2(domain,A,B):
    BL,BR = B.split()
    if len(BL)>0: return ((domain+A)|BL) + ((domain+A)|BR)
CONTEXT.define('ap',ap_0,ap_1,ap_2)
def apall(domain,A,B):
    A0,AR = A.split()
    if A0.atom(): return (A0|B) + ((domain+AR)|B)
def apall_0(domain,A,B):
    if A.empty(): return data()
def apall_1(domain,A,B):
    if B.empty(): return data()
CONTEXT.define('apall',apall_1,apall_0,apall)
def apeach_1(domain,A,B):
    A0,AR = A.split()
    if A0.atom(): return ((da('ap')+A0)|B) + ((domain+AR)|B)
def apeach_2(domain,A,B):
    if A.empty(): return data()
CONTEXT.define('apeach',apeach_1,apeach_2)
def aparg_1(domain,A,B):
    if all([a.atom() for a in A]+[b.atom() for b in B]):
        L = []
        As = [a for a in A]
        Bs = [b for b in B]
        if len(As)>0:
            c = As.pop(0)
            for a in As:
                for b in Bs: L.append((c+a)|data(b))
        return data(*L)
def aparg_0(domain,A,B):
    if B.empty(): return data()
CONTEXT.define('aparg',aparg_1,aparg_0)
def apbin_0(domain,A,B):
    B0,BR = B.split()
    B1,BX = BR.split()
    if B0.atom() and B1.atom(): return data((A+B0)|data((domain+A)|BR))
def apbin_1(domain,A,B):
    if B.atom(): return B
def apbin_2(domain,A,B):
    if B.empty(): return data()
CONTEXT.define('apbin',apbin_0,apbin_1,apbin_2)
def apby(domain,A,B):
    AL,AR = A.split()
    import Number
    if AL.atom() and len(Number.ints(AL))==1:
        n = Number.ints(AL)[0]
        if n>0:
            if all([b.atom() for b in B[:n]]):
                return (AR|data(*B[:n])) + ((domain+A)|data(*B[n:]))
def apby_0(domain,A,B):
    if B.empty(): return data()
CONTEXT.define('apby',apby_0,apby)
def apif_0(domain,A,B):
    if B.empty(): return data()
def apif_1(domain,A,B):
    BL,BR = B.split()
    if BL.atom(): return ((domain+A)|BL) + ((domain+A)|BR)
def apif_2(domain,A,B):
    if B.atom(): return data((da('if')+data(A|B))|B)
CONTEXT.define('apif',apif_0,apif_2,apif_1)
#
#   Collect inputs b with the same value of (A:b).
#
#   demo: collect pass : a b aa bb aaa cccc zz xxx xxx
#   demo: get ((:):(:)) : a b aa bb aaa cccc zz xxx xxx
#   demo: collect {count:get ((:):(:)):B} : a b aa bb aaa cccc zz xxx xxx
#   demo: equiv {count:get ((:):(:)):B} : a b aa bb aaa cccc zz xxx xxx
#
def collect(domain,A,B):
    if all([b.atom() for b in B]):
        classes = {}
        for b in B:
            equiv = data(A|data(b))
            import Evaluate
            equiv = Evaluate.resolve(equiv,500)
            if not equiv in classes: classes[equiv] = []
            classes[equiv] = classes[equiv] + [b]
        if not None in classes:
            L = []
            for equiv,cls in classes.items(): L.append(da('bin')|data(*cls))
            return data(*L)
def collect_0(domain,A,B):
    if B.empty(): return data()
CONTEXT.define('collect',collect,collect_0)
def equiv(domain,A,B):
    if all([b.atom() for b in B]):
        classes = {}
        for b in B:
            equiv = data(A|data(b))
            import Evaluate
            equiv = Evaluate.resolve(equiv,500)
            if not equiv in classes: classes[equiv] = []
            classes[equiv] = classes[equiv] + [b]
        if not None in classes:
            L = []
            for equiv,cls in classes.items(): L.append((da('bin')+equiv)|data(*cls))
            return data(*L)
def equiv_0(domain,A,B):
    if B.empty(): return data()
CONTEXT.define('equiv',equiv,equiv_0)
#
#   apby applies it's argument to inputs n items at a time.
#
#   demo: apby 2 count : a b c d e f g
#   demo: apby 3 {put bin:B} : a b c d e f g
#
#
#   Sequential version of binary operator
#
#   For instance if A x : y is a "binary operator" app
#   results in b1+b2+....
#
#   demo: int_add 10 : 5
#   demo: app int_add : 1 2 3 4
#   demo: int_mult 10 : 5
#   demo: app int_mult : 1 2 3 4
#
#def app_0(domain,A,B):
#    B0,BR = B.split()
#    B1,BX = BR.split()
#    if B0.atom() and B1.atom(): return data((A+B0)|data((domain+A)|BR))
#def app_1(domain,A,B):
#    if B.atom(): return B
#def app_2(domain,A,B):
#    if B.empty(): return data()
#CONTEXT.define('app',app_0,app_1,app_2)
#
#   Sequential version of binary operator
#
#   For instance if A x : y is a "binary operator" apbin
#   results in b1+b2+....
#
#   demo: int_add 10 : 5
#   demo: apbin int_add : 1 2 3 4
#   demo: int_mult 10 : 5
#   demo: apbin int_mult : 1 2 3 4
#
#def apbin_0(domain,A,B):
#    B0,BR = B.split()
#    B1,BX = BR.split()
#    if B0.atom() and B1.atom(): return data((A+B0)|data((domain+A)|BR))
#def apbin_1(domain,A,B):
#    if B.atom(): return B
#def apbin_2(domain,A,B):
#    if B.empty(): return data()
#CONTEXT.define('apbin',apbin_0,apbin_1,apbin_2)
#
#   Distribute the first argument over the rest and apply each pair to B.
#
#   dis  a a1 a2 a3..an : B -> (a a1:B) (a a2:B)... (a an:B)
#
#   demo: dis first 1 2 3 : a b c d e f g
#
#def dis_1(domain,A,B):
#    A0,AR =  A.split()
#    A1,AR = AR.split()
#    if A0.atom() and A1.atom():
#        return ((A0+A1)|B) + ((domain+A0+AR)|B)
#def dis_0(domain,A,B):
#    A0,AR = A.split()
#    A1,AR = AR.split()
#    if A0.empty() or A1.empty(): return data()
#CONTEXT.define('dis',dis_1,dis_0)
#
#   adis A : B applies each a in A to each b in B.
#
#   adis a A : B -> (ap a:B) (app A:B)
#   adis  () : B -> ()
#
#   demo: foo : 1 2 3
#   demo: ap foo : 1 2 3
#   demo: adis foo bar : 1 2 3
#   demo: adis {put x:B} {put y:B} : 1 2 3
#
#def adis_1(domain,A,B):
#    A0,AR = A.split()
#    if A0.atom(): return ((da('ap')+A0)|B) + ((domain+AR)|B)
#def adis_2(domain,A,B):
#    if A.empty(): return data()
#CONTEXT.define('adis',adis_1,adis_2)
#
#   apeach A : B applies each a in A to each b in B.
#
#   adis a A : B -> (ap a:B) (app A:B)
#   adis  () : B -> ()
#
#   demo: foo : 1 2 3
#   demo: ap foo : 1 2 3
#   demo: apeach foo bar : 1 2 3
#   demo: apeach {put x:B} {put y:B} : 1 2 3
#
#
#   apeach X A : B gives (X a1:b1) (X a1:b2)... for all ai in A and bi in B.
#
#   This is useful, for instance for making pairs.
#
#   demo: apeach put a b c : 1 2 3
#   demo: apeach {put bin : A B} 1 2 3 : a b c
#   demo: apeach int_add 1 2 3 : 1000 2000 3000
#
#def apeach_1(domain,A,B):
#    if all([a.atom() for a in A]+[b.atom() for b in B]):
#        L = []
#        As = [a for a in A]
#        Bs = [b for b in B]
#        if len(As)>0:
#            c = As.pop(0)
#            for a in As:
#                for b in Bs: L.append((c+a)|data(b))
#        return data(*L)
#def apeach_0(domain,A,B):
#    if B.empty(): return data()
#CONTEXT.define('apeach',apeach_1,apeach_0)
#
#   aparg X A : B gives (X a1:b1) (X a1:b2)... for all ai in A and bi in B.
#
#   demo: aparg put a b c : 1 2 3
#   demo: aparg {put bin : A B} 1 2 3 : a b c
#   demo: aparg int_add 1 2 3 : 1000 2000 3000
#
#
#   apif A : B gets the elements b of B with A:b true.
#
#   apif A : B C -> (apif A:B) (apif A:C)
#   apif A : () -> ()
#   apif A : B -> if (A:B):B if B is an atom
#
#   demo: apif pass : a b c
#   demo: apif null : a b c
#   demo: apif {not:B} : a b c
#
