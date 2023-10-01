#
#   Numbers
#
#   Basic, low level computing python integers or python floats from code
#
from base import *
#
#    Low level standard coersion from unicode to numbers
#
def tryint(x):
    y = None
    try:
        y = int(str(x))
    except (ValueError,TypeError):
        pass
    return y

def tryfloat(x):
    y = None
    try:
        y = float(str(x))
    except (ValueError,TypeError):
        pass
    return y

def trynat(x):
    y = tryint(x)
    if not y is None and y>=0: return y
#
#   Try to get the integers from data D, ignoring colons and non-integer codes
#
def   ints(D): return [tryint  (d) for d in D if not tryint  (d) is None]
def floats(D): return [tryfloat(d) for d in D if not tryfloat(d) is None]
def  codes(D): return [str(c) for c in D]
def intdef(n,D):
    ns = ints(D)
    if len(ns)>0: return ns[0]
    return n
#
#    The natural numbers as a whole
#
#    nat : n -> n (nat:n+1)
#
#    demo: nat:0
#    demo: rev : nat : 0
#    demo: rev : rev : nat : 0
#
def nat(domain,A,B):
    ns = ints(B)
    if len(ns)==1:
        n = ns.pop()
        return co(str(n)) + (domain|da(str(n+1)))
CONTEXT.define('nat',nat)

class Reduce(object):
    def __init__(self,name,reduce):
        self._name   = name
        self._reduce = reduce # atoms to atoms
        CONTEXT.define(name,lambda domain,A,B:self(domain,A,B))
    def split(self,B):
        atoms,rest = [],[b for b in B]
        while len(rest)>0 and rest[0].atom(): atoms.append(rest.pop(0))
        return data(*atoms),data(*rest)
    def __call__(self,domain,A,B):
        atoms,rest = self.split(B)
        reduce = self._reduce(atoms)
        if len(rest)==0 and atoms==reduce: return data(*reduce)
        return data((domain+A)|(reduce+rest))

class RE(Reduce):
    def __init__(self,name,coerce,F):
        def wrap(A):
            L = [coerce(a) for a in A if not coerce(a) is None]
            return data(*[co(str(l)) for l in F(L)])
        Reduce.__init__(self,name,wrap)

def _sum(L): return [sum(L)]
def _prod(L):
    p = 1
    for l in L: p = p * l
    return [p]
def _min(L):
    if len(L)==0: return []
    return [min(L)]
def _max(L):
    if len(L)==0: return []
    return [max(L)]
def _sort(L): return sorted(L)
#
#   demo: ints : a b c 1 2 -45
#   demo: nats : a b c 1 2 -45
#   demo: int_sum : 1 2 3 -10
#   demo: int_prod: 1 2 3 -10
#   demo: int_max: 1 2 3 -10
#   demo: int_max:
#   demo: int_min: 1 2 3 -10
#   demo: int_inv: 1 2 3 -10
#   demo: int_div 2 : 1 2 3 4 5 6
#   demo: int_div 1 : 1 2 3 4 5 6
#   demo: int_div 0 : 1 2 3 4 5 6
#   demo: int_div : 1 2 3 4 5 6
#   demo: floats : 1 2 a 3.14 -99.9
#   demo: float_sum : 1 2 a 3.14 -99.9
#   demo: float_prod : 1 2 a 3.14 -99.9
#   demo: float_min : 1 2 a 3.14 -99.9
#   demo: float_min :
#   demo: float_max : 1 2 a 3.14 -99.9
#   demo: float_div 2.1 : 1 2 a 3.14 -99.9
#   demo: code_sort : a b c c b a
#
RE('code_sort',str,_sort)
RE('ints',tryint,lambda L:L)
RE('int_sum',tryint,_sum)
RE('int_prod',tryint,_prod)
RE('int_sort',tryint,_sort)
RE('int_min',tryint,_min)
RE('int_max',tryint,_max)
def int_inv_0(domain,A,B):
    if B.empty(): return data()
def int_inv_1(domain,A,B):
    BL,BR = B.split()
    if BL.atom():
        L  = ints(BL)
        Li = [co(str(-l)) for l in L]
        return data(*Li)+data((domain+A)|BR)
CONTEXT.define('int_inv',int_inv_0,int_inv_1)
def int_div_0(domain,A,B):
    if B.empty(): return data()
def int_div_2(domain,A,B):
    if A.empty(): return B
def int_div_1(domain,A,B):
    if A.rigid() and len(A)==1:
        BL,BR = B.split()
        if BL.atom():
            num = tryint(BL)
            den = tryint(A)
            if den is None: return None
            if num is None: return data((domain+A)|BR)
            if not den==0:
                return da(str(num//den)) + data((domain+A)|BR)
CONTEXT.define('int_div',int_div_0,int_div_1,int_div_2)

RE('nats',trynat,lambda L:L)

RE('floats',tryfloat,lambda L:L)
RE('float_sum',tryfloat,_sum)
RE('float_prod',tryfloat,_prod)
RE('float_sort',tryfloat,_sort)
RE('float_min',tryfloat,_min)
RE('float_max',tryfloat,_max)
def float_inv_0(domain,A,B):
    if B.empty(): return data()
def float_inv_1(domain,A,B):
    BL,BR = B.split()
    if BL.atom():
        L  = floats(BL)
        Li = [co(str(-l)) for l in L]
        return data(*Li)+data((domain+A)|BR)
CONTEXT.define('float_inv',int_inv_0,int_inv_1)
def float_div_0(domain,A,B):
    if B.empty(): return data()
def float_div_2(domain,A,B):
    if A.empty(): return B
def float_div_1(domain,A,B):
    if A.rigid() and len(A)==1:
        BL,BR = B.split()
        if BL.atom():
            num = tryfloat(BL)
            den = tryfloat(A)
            if den is None: return None
            if num is None: return data((domain+A)|BR)
            if not den==0:
                return da(str(num/den)) + data((domain+A)|BR)
CONTEXT.define('float_div',float_div_0,float_div_1,float_div_2)
