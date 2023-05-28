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
        if A in VALUES and not VALUES[A]==B:
            return
        else:
            VALUES[A] = B
            return data()
CONTEXT.define('let',Let)
