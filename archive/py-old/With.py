#
#    In the boot context, the following definitions are active.
#
#    env, =, with, eval, multi, base?
#
#
#        .....
from base import *
import Number

DEFAULT_DEPTH = 100
#
#   Evaluate (with A : B) to a specified depth.
#
#   demo: rev : a b c
#   demo: with : rev : a b c
#   demo: eval : with : rev : a b c
#   demo: right : eval : with (defs:) : rev : a b c
#   demo: eval : with (:) ((:):(:)) language : rev : a b c
#   demo: eval : with (:) ((:):(:)) language rev : rev : a b c
#   demo: eval : with (:) ((:):(:)) language rev (x?=5) : {rev : a b c x?}:
#
def eval(domain,A,B):
    newcontext = context.copy(A)
    n = Number.intdef(DEFAULT_DEPTH,A)
    E = B.eval(newcontext)
    while not B==E and n>0:
        n = n - 1
        B = E.eval(newcontext)
    if B==E: return B
    else   : return data(data(domain+A)|E)

def eval(domain,A,B):
    if A.rigid() and B.atom():
        n = Number.intdef(DEFAULT_DEPTH,A)
        left  = B[0].left()
        right = B[0].right()
        dom,arg = left.split()
        if dom==da('with'):
            while not arg==arg.evaluate(CONTEXT): arg = arg.evaluate(CONTEXT)
            context = CONTEXT.subcontext(arg)
            context = context.add_variables(arg)
            R = withEval(n,context,right)
            return data((dom+arg)|R)
        else:
            return data()
CONTEXT.define('eval',eval)
CONTEXT.define('with')

#def evalOLD(domain,A,B):
#    if A.rigid() and B.atom():
#        import Number
#        ns = Number.ints(A)
#        n = 100
#        if len(ns)==1: n = ns[0]
#
#        b = B[0]
#        if b.domain()==da('with'):
#            BL,BR = b.left().split()
#            print('aaaaa 1',CONTEXT)
#            print('aaaaa 2',BR)
#            context = CONTEXT.subcontext(BR)
#            print('aaaa',context)
#            R = withEval(n,context,b.right())
#            if not R is None: return data(b.left()|R)
#        else:
#            return data()
#
#   evaluate recursively at most n times.
#
#   Evaluation preserves the equality of D within the supplied context.
#
def withEval(n,context,D):
    if n<=0: return D.evaluate(context)
    else:
        D2 = D.evaluate(context)
        if D==D2:
            return D
        else:
            return withEval(n-1,context,D2)
