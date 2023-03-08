#
#   Basic definitions
#
from base import *
import Number
#
#    pass : B -> B and null : B -> ()
#
#    demo: pass : 1 2 3
#    demo: null : 1 2 3
#
CONTEXT.define('pass',lambda domain,A,B:B)
CONTEXT.define('null',lambda domain,A,B:data())
#
#
def domain_0(domain,A,B):
    BL,BR = B.split()
    if BL.atom(): return BL[0].domain() + data((domain+A)|BR)
def domain_1(domain,A,B):
    if B.empty(): return data()
CONTEXT.define('dom',domain_0,domain_1)
#
#   if A : B -> () if A is false
#   if A : B -> B  if A is true
#
#   demo: if (1=1) : 1 2 3
#   demo: if (1=2) : 1 2 3
#   demo: if x : 1 2 3
#   demo: if () : 1 2 3
#   demo: if : 1 2 3
#   demo: if (foo:bar) : 1 2 3
#   demo: if (bin:x y) : 1 2 3
#   demo: if (bin:) : 1 2 3
#
def if_1(domain,A,B):
    for a in A:
        if a.atom(): return data()
def if_0(domain,A,B):
    if A.empty(): return B
CONTEXT.define('if',if_1,if_0)
#
#   put A : B creates A:B, it "puts B into A".
#
#   put A : B -> (A:B)
#
#   demo: put x : 1 2 3
#   demo: put x y : 1 2 3
#   demo: ap put x : 1 2 3
#   demo: (put:)
#   demo: pure : put :
#
CONTEXT.define('put',lambda domain,A,B: data(A|B))
#
#   Singleton versions of has, get and atom
#
def has1(domain,A,B):
    if B.atom():
        guard = data((da('=')+A)|B[0].left())
        return data((da('if')+guard)|B)
def get1(domain,A,B):
    if B.atom():
        guard = data((da('=')+A)|B[0].left())
        return data((da('if')+guard)|B[0].right())
CONTEXT.define('has1',has1)
CONTEXT.define('get1',get1)
