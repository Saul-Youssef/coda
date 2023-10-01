#
#    In the boot context, the following definitions are active.
#
#    env, =, with, eval, multi, base?
#
#    env A          -- imports external definitions, if any
#    =              -- pure data equality
#    with A : B     -- Data B with definitions A
#    eval 100 : B   -- Evaluate one (with X:Y) at most A times resulting in (with X:Y') where Y=Y' with definitions X.
#    multi 100 : B  --
#    base?          -- Standard collection of imported definitions from internal py and co files.
#
#    with is a pure atom, eval evaluates up to specified number of tries.
#    multi evaluates it's inputs, possibly with multiprocessing.
#
#    env /a/b/c a.b.c/foo : eval 100 : with base? x?=45 : ...
#
#    Suppose T is a "theorem".  This means T is "never false", meaning...
#
#    o T is never false independent of future definitions.  This is the same as
#    o with X : T is never false for any X
#
#    not : right : eval X : with Y : T  is true for any X, Y
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
#
def eval(domain,A,B):
    if A.rigid() and B.atom():
        n = Number.intdef(DEFAULT_DEPTH,A)
        left  = B[0].left()
        right = B[0].right()
        dom,arg = left.split()
        if dom==da('with'):
            while not arg==arg.evaluate(CONTEXT): arg = arg.evaluate(CONTEXT)
            context = CONTEXT.subcontext(arg)
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
