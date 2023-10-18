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
    if B.atom(context) and B.rigid(context) and B[0].domain()==da('def'):
        b = B[0]
        if not context.has(b.arg()):
            context.add(b.arg(),lambda cont,dom,AA,BB: data((b.right()+AA)|BB))
            return data()
CONTEXT.define('use1',Use1)
CONTEXT.define('def')
