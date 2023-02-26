#
#    Definition definitions
#
from base import * 
import Evaluate
#
#   Create a definition.
#
#   demo: def foo : {first 2 : rev : B}
#   demo: foo : a b c d e f
#   demo: def first2 : {first A:B} 2
#   demo: first2 : a b c d
#   
def Def(domain,D,V):
    D = Evaluate.resolve(D,100)
    V = Evaluate.resolve(V,100)
    
    if (not D is None) and (not V is None):
        if V.empty():
            CONTEXT.add(DEF(D)) # domain D -> identity
        else:
            CONTEXT.add(DEF(D,lambda domain,A,B:data((V+A)|B)))
        return data()
CONTEXT.define('def',Def)
#
#   Named constant storage 
#
#   demo: const stuff : 1 2 3
#   demo: stuff:
#
def Const(domain,D,V):
    D = Evaluate.resolve(D,100)
    V = Evaluate.resolve(V,100)
    
    if (not D is None) and (not V is None):
        CONTEXT.add(DEF(D,lambda A,B:V))
        return data()
CONTEXT.define('const',Const)
#
#   Assign values to "variables"
#
#   demo: let x? : 1 2 3 4
#   demo: x?
#
def Let(domain,D,V):
    D = Evaluate.resolve(D,100)
    V = Evaluate.resolve(V,100)
    
    if (not D is None) and (not V is None) and len(D)>0:
        cod = D[0]
        CONTEXT.add(DEF(cod.left(),lambda domain,A,B: assign(A,B,cod.right(),V)))
        return data()
CONTEXT.define('let',Let)

def assign(A,B,N,V):
    if A.empty() and B==N: return V
