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
#
def ap_0(domain,A,B):
    if B.empty(): return data()
def ap_1(domain,A,B):
    if B.atom(): return data(A|B)
def ap_2(domain,A,B):
    BL,BR = B.split()
    if len(BL)>0: return ((domain+A)|BL) + ((domain+A)|BR)
CONTEXT.add(DEF(da('ap'),ap_0,ap_1,ap_2))
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
def app_0(domain,A,B):
    B0,BR = B.split()
    B1,BX = BR.split()
    if B0.atom() and B1.atom(): return data((A+B0)|data((domain+A)|BR))
def app_1(domain,A,B):
    if B.atom(): return B
def app_2(domain,A,B):
    if B.empty(): return data()
CONTEXT.add(DEF(da('app'),app_0,app_1,app_2))
#
#   dis and disr distributes the first argument over the
#   rest and applies each combination to B.
#
#   dis  a a1 a2 a3..an : B -> (a a1:B) (a a2:B)... (a an:B)
#   disr a1 a2 a3..an a : B -> (a1 a:B) (a2 a:B)... (an a:B)
#
#   demo: dis first 1 2 3 : a b c d e f g
#   demo: disr first last first last 1 : a b c d
#   demo: disr first last first last 2 : a b c d
#
def dis_1(domain,A,B):
    A0,AR =  A.split()
    A1,AR = AR.split()
    if A0.atom() and A1.atom():
        return ((A0+A1)|B) + ((domain+A0+AR)|B)
def dis_0(domain,A,B):
    A0,AR = A.split()
    A1,AR = AR.split()
    if A0.empty() or A1.empty(): return data()
CONTEXT.add(DEF(da('dis'),dis_1,dis_0))

#def disr_1(domain,A,B):
#    AF,AR = A .split_left()
#    AR,AL = AR.split_right()
#    if AF.atom() and AL.atom():
#        return data(colon(AF+AL,B)) + one(b'disr',AR+AL,B)
#def disr_0(domain,A,B):
#    AF,AR = A.split_left()
#    AR,AL = AR.split_right()
#    if AF.empty() or AL.empty(): return data()
#DEF.add(data(b'disr'),disr_1,disr_0)

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
def adis_1(domain,A,B):
    A0,AR = A.split()
    if A0.atom(): return ((da('ap')+A0)|B) + ((domain+AR)|B)
def adis_2(domain,A,B):
    if A.empty(): return data()
CONTEXT.add(DEF(da('adis'),adis_1,adis_2))
#DEF.add(data(b'adis'),adis_1,adis_2)
#    if A0.atom(): return one(b'ap',A0,B) + one(b'adis',AR,B)

#
#   apall applies each argument to the entire input.
#
#   demo: apall pass : a b c
#   demo: apall pass pass : a b c
#   demo: apall {first:B} {rev:last 3:B} : a b c d e
#
def apall(domain,A,B):
    A0,AR = A.split()
    if A0.atom():
        print('aaaaa A0',A0)
        print('aaaaa B',B)
        print('aaaaa R',((domain+AR)|B) )
        print('aaaaa ALL',(A0|B) + ((domain+AR)|B) )
        return (A0|B) + ((domain+AR)|B)
def apall_0(domain,A,B):
    if A.empty(): return data()
CONTEXT.add(DEF(da('apall'),apall,apall_0))
#    if A0.atom(): return data(colon(A0,B)) + one(b'apall',AR,B)
#DEF.add(data(b'apall'),apall,apall_0)

#
#   apx X A : B gives (X a1:b1) (X a1:b2)... for all ai in A and bi in B.
#
#   This is useful, for instance for making pairs.
#
#   demo: apx {put bin : A B} 1 2 3 : a b c
#   demo: apx int_add 1 2 3 : 1000 2000 3000
#
def apx_1(domain,A,B):
    if all([a.atom() for a in A] and [b.atom() for b in B]):
        L = []
        As = [a for a in A]
        Bs = [b for b in B]
        if len(As)>0:
            c = As.pop(0)
            for a in As:
                for b in Bs: L.append((c+a)|b)
        return data(*L)
def apx_0(domain,A,B):
    if B.empty(): return data()
CONTEXT.add(DEF(da('apx'),apx_1,apx_0))

#DEF.add(data(b'apx'),apx_1,apx_0)
#
#    if all([data(a).atom() for a in A]) and \
#       all([data(b).atom() for b in B]):
#        L = []
#        As = [a for a in A]
#        Bs = [b for b in B]
#        if len(As)>0:
#            X = As.pop(0)
#            for a in As:
#                for b in Bs:
#                    L.append(colon(data(X,a),data(b)))
#        return data(*L)


#
#   apif A : B gets the elements of b with A:b true.
#
#   apif A : B C -> (apif A:B) (apif A:C)
#   apif A : () -> ()
#   apif A : B -> if (A:B):B if B is an atom
#
#   demo: apif pass : a b c
#   demo: apif null : a b c
#   demo: apif {not:B} : a b c
#   demo: apif null : (foo:bar)
#
def apif_0(domain,A,B):
    if B.empty(): return data()
def apif_1(domain,A,B):
    BL,BR = B.split()
    return ((domain+A)|BL) + ((domain+A)|BR)
def apif_2(domain,A,B):
    if B.atom(): return data((co('if')+(A|B))|B)
CONTEXT.add(DEF(da('apif'),apif_1,apif_2,apif_0))

#DEF.add(data(b'apif'),apif_1,apif_2,apif_0)
#return one(b'apif',A,BL) + one(b'apif',A,BR)
#    if B.atom(): return one(b'if',data(colon(A,B)),B)


#
#   apleft1 A : b B -> ((A:b) : B) (apleft A : B)
#
#   demo: apleft1 count : a
#   demo: ap aleft1 count : a b c
#
#   This is a useful operation in for example, making equivalence classes.
#
#def apleft1(domain,A,B):
#    if B.atom(): return
#    if B.atom(): return data(colon(data(colon(A,B)),B))
#DEF.add(data(b'apleft1'),apleft1)
#
#   apby processes it's input by an A-specified number of items at a time.
#
#   For instance, the first demo processes it's input two at a time.
#
#   demo: apby 2 count : a b c d e f g
#
#def apby(A,B):
#    A0,AR = A.split()
#    import Number
#    if A0.atom() and len(Number.ints(A0))==1:
#        n = Number.ints(A0)[0]
#        B2 = []; BR = B
#        while not BR.empty() and len(B2)<n:
#            B0,BR = BR.split()
#            if B0.atom(): B2.append(B0[0])
#        if len(B2)==n:
#            return data(colon(AR,data(*B2))) + one(b'apby',A,BR)
#def apby_0(A,B):
#    if B.empty(): return data()
#def apby_1(A,B):
#    A0,AR = A.split()
#    import Number
#    if A0.atom() and len(Number.ints(A0))==1:
#        n = Number.ints(A0)[0]
#        if all([data(b).atom() for b in B]) and len(B)<n:
#            return data()
#DEF.add(data(b'apby'),apby,apby_0,apby_1)
