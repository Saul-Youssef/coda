#
#    Definition definitions
#
from base import * 
#
#   def F : D creates a new definition associated with the flag F.
#   The definition is (F A:B) -> (D A:B).  The action of def itself is
#   (def F:D) -> (defined F:D) where defined is just a record of
#   the definition after the fact.
#
#   demo: def foo : {first 2 : rev : B}
#   demo: foo : a b c d e f
#   demo: def first2 : {first A:B} 2
#   demo: first2 : a b c d
#
def Def(F,D):
    import Evaluate
    Fs = Evaluate.generic(F,100)
    Ds = Evaluate.generic(D,100)
    if Ds.empty():
        DEF.add(Fs)
    else:
        DEF.add(Fs,lambda A,B:data(colon(Ds+A,B)))
    return data()
DEF.add(data(b'def'),Def)
#
#   Specific data storage
#
#   demo: store stuff : 1 2 3
#   demo: stuff:
#
def Store(F,D):
    import Evaluate
    Fs = Evaluate.generic(F,100)
    Ds = Evaluate.generic(D,100)
    DEF.add(Fs,lambda A,B:Ds)
    return data()
DEF.add(data(b'store'),Store)
#
#   Assign values to "variables"
#
#   demo: let x? : 1 2 3 4
#   demo: x?
#
def Let(L,R):
    import Evaluate
    Ls = Evaluate.generic(L,100)
    Rs = Evaluate.generic(R,100)
    if is_colon(Ls[0]):
        col = Ls[0]
        DEF.add(col.left(),lambda A,B : assign(A,B,col.right(),Rs))
    return data()
DEF.add(data(b'let'),Let)

def assign(A,B,N,V):
    if A.empty() and B==N: return V
