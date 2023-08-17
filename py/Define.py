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

#VALUES = {}
#def Value(domain,A,B):
#    if B.invariant() and B in VALUES: return VALUES[B]
#CONTEXT.define('?',Value)
#def Let(domain,A,B):
#    if A.invariant():
#        if A in VALUES and not VALUES[A]==B:
#            return
#        else:
#            VALUES[A] = B
#            return data()
#CONTEXT.define('let',Let)

class ConstDefinition(Definition):
    def __init__(self,domain,value):
        self._domain = domain
        self._value  = value
    def __len__(self): return 1
    def __call__(self,c):
        if c.domain()==self._domain: return self._value
        return data(c)

def Let(domain,A,B):
    if A.eval()==A and len(A)==1 and not A|data() in CONTEXT:
        CONTEXT.add(ConstDefinition(A,B))
        return data()
CONTEXT.define('let',Let)
