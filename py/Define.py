#
#    Definition
#
from base import *
#
#    use input definitions
#
#    demo: def first2 : {first 2:B}
#    demo: first2 : a b c d e
#    demo: use : def first2 : {first 2:B}
#    demo: first2 : a b c d e
#    demo: def first2 : xxx
#    demo: use : def first2 : xxx
#    demo: use : (let x:55) (def first2 : {first 2:B}) (def first3 : {first 3:B})
#
def Use1(context,domain,A,B):
    if B.atom(context) and B[0].domain()==da('def') and B[0].stable(context):
        b = B[0]
        if not context.has(b.arg()):
            if b.right().empty():
                context.add(b.arg())
            else:
                context.add(b.arg(),PartialFunction(b.right()))
            return data()
CONTEXT.define('use1',Use1)
CONTEXT.define('def')

class PartialFunction(object):
    def __init__(self,left): self._left = left
    def __call__(self,context,domain,A,B): return data((self._left+A)|B)
