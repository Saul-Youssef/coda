#
#    Definition
#
from base import *
from Log import LOG

LOG.register('context','Context operations')
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
    if B.atom(context) and B[0].domain()==da('def') and B[0].left().rigid(context):
        b = B[0]
        if not context.has(b.arg()):
            LOG('context','Number of definitions:'+str(len(context)))
            LOG('context','Adding '+str(b.arg())+'->'+str(b.right()))
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

PF = PartialFunction(data())
#
#    This is purely for the IO module to answer the question of
#    how much to resolve data before writing it to disk
#
def _Outfriendly(context,D):
    return all(_Outfriendly_coda(context,d) for d in D)
def _Outfriendly_coda(context,d):
    return _outOK      (context,d) and \
           _Outfriendly(context,d.left()) and \
           _Outfriendly(context,d.right())
def _outOK(context,d):
    action_ready = \
         d in context and len(context[d])>0 and \
         any(type(defi)==type(PF) for defi in context[d])
    return not action_ready
