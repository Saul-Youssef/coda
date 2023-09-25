#
#    eval : with x?=5 : x?
#
#    Represents data B with definitions A.  Definitions may be
#
#    1. Domain names such as ap, rev, * or language, representing
#       partial functions from coda to data as defined either in python .py files
#       or via the language in .co files.
#    2. Codas A=B where A is an undefined coda, interpreted as a new definition
#       A -> B.
#
#    coda url1 url2 url3 : eval 100 : with base? x?=5 : (x? x?) = (rev : x? x?)
#
#    T is a theorem means...
#
#    with A : T is never false for any A.
#    with A B : T = with A B : with A : T
#
#    with x?=5 : test
#    with x?=6 : test
#
#    with (isnt ap : base?) (x?=45) (y?=z?):
#        .....
from base import *

EQ   = da('=')
WITH = da('with')
CONTEXT.define('with')

def With(A):
    context = Context()
    for a in A:
        if a.domain()==EQ:
            print('aaaaa',a)
        elif a in CONTEXT:
            context._definitions[data(a)] = CONTEXT._definitions[data(a)]
        else:
            print('aaaaa error',a)
    return context

def evaluate(domain,A,B):
    if A.rigid() and B.atom():
        import Number
        ns = Number.ints(A)
        n = 100
        if len(ns)==1: n = ns[0]

        b = B[0]
        if b.domain()==WITH:
            BL,BR = b.left().split()
            context = With(BR)
            R = Eval(n,context,b.right())
            return data(b.left()|R)
        else:
            return data()
CONTEXT.define('evaluate',evaluate)

def Eval(n,context,D):
    if n<=0: return D.evaluate(context)
    else:
        D2 = D.evaluate(context)
        if D==D2:
            return D
        else:
            return Eval(n-1,context,D2)
