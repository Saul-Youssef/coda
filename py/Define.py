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
        if V.empty(): CONTEXT.add(Definition(D))
        else        : CONTEXT.add(Definition(D,lambda domain,A,B:data((V+A)|B)))
        return data()
CONTEXT.define('def',Def)

VALUES = {}
def Value(domain,A,B):
    if B.invariant() and B in VALUES: return VALUES[B]
CONTEXT.define('?',Value)
def Let(domain,A,B):
    if A.invariant():
        VALUES[A] = B
        return data()
CONTEXT.define('let',Let)

#def Val(domain,A,B):
#    if A.invariant() and A in CONTEXT.var(): return CONTEXT.val(A)
#CONTEXT.define('val',Val)
#
#    if (not D is None) and (not V is None):
#        if V.empty():
##            CONTEXT.dom(D,Definition(D))
#            CONTEXT.add(Definition(D))
#        else:
#            defin = Definition(D,lambda domain,A,B:data((V+A)|B))
##            CONTEXT.dom(defin.domain(),defin)
#            CONTEXT.add(defin)
#        return data()
#
#   Named constant storage
#
#   demo: const stuff : 1 2 3
#   demo: stuff:
#
#def Const(domain,D,V):
#    D = Evaluate.resolve(D,100)
#    V = Evaluate.resolve(V,100)
#
#    if (not D is None) and (not V is None):
#        defin = Definition(D,lambda domain,A,B:V)
#        CONTEXT.dom(defin.domain(),defin)
##        CONTEXT.add(Definition(D,lambda domain,A,B:V))
#        return data()
#CONTEXT.define('const',Const)
#
#   Assign values to "variables"
#
#   demo: let x? : 1 2 3 4
#   demo: x?
#
#def Let(domain,D,V):
#    D = Evaluate.resolve(D,100)
#    V = Evaluate.resolve(V,100)
#
#    if (not D is None) and (not V is None) and len(D)>0:
#        cod = D[0]
#        CONTEXT.val(cod,V)
#    return data()
#CONTEXT.define('let',Let)
