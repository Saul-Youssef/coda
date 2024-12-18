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
def   nats(D):
    L = []
    for d in D:
        try:
            i = int(str(d))
            if i>=0: L.append(i)
        except ValueError:
            pass
    return L
def floats(D): return [tryfloat(d) for d in D if not tryfloat(d) is None]
def  codes(D): return [str(c) for c in D]
def intdef(n,D):
    ns = ints(D)
    if len(ns)>0: return ns[0]
    return n
def floatdef(x,D):
    xs = floats(D)
    if len(xs)>0: return xs[0]
    return x
#
#    The natural numbers as a whole
#
#    nat : n -> n (nat:n+1)
#
#    demo: nat:0
#    demo: rev : nat : 0
#    demo: rev : rev : nat : 0
#
def nat(context,domain,A,B):
    if B.rigid(context):
        ns = ints(B)
        if len(ns)>=1:
            n = ns.pop(0)
            return co(str(n)) + (domain|da(str(n+1)))
        else:
            return data()
CONTEXT.define('nat',nat)

class Reduce(object):
    def __init__(self,name,reduce):
        self._name   = name
        self._reduce = reduce # atoms to atoms
        CONTEXT.define(name,self)
    def split(self,context,B):
        atoms,rest = [],[b for b in B]
        while len(rest)>0 and rest[0].atom(context): atoms.append(rest.pop(0))
        return data(*atoms),data(*rest)
    def __call__(self,context,domain,A,B):
        atoms,rest = self.split(context,B)
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
#   demo: nats : a b 3.14 2 3 -45
#   demo: nat_sum : a b 3.14 2 3 -45
#   demo: nat_prod : a b 3.14 2 3 -45
#   demo: nat_min : a b 3.14 2 3 -45
#   demo: nat_max : a b 3.14 2 3 -45
#   demo: nat_sort : a b 3.14 2 3 -45
#
#   demo: ints : a b 3.14 2 3 -45
#   demo: int_sum : a b 3.14 2 3 -45
#   demo: int_prod : a b 3.14 2 3 -45
#   demo: int_min : a b 3.14 2 3 -45
#   demo: int_max : a b 3.14 2 3 -45
#   demo: int_sort : a b 3.14 2 3 -45
#   demo: int_inv : a b 3.14 2 3 -45
#   demo: int_div 2 : 1 2 3 4 5 6
#
#   demo: floats : a b 3.14 2 3 -45
#   demo: float_sum : a b 3.14 2 3 -45
#   demo: float_prod : a b 3.14 2 3 -45
#   demo: float_min : a b 3.14 2 3 -45
#   demo: float_max : a b 3.14 2 3 -45
#   demo: float_sort : a b 3.14 2 3 -45
#   demo: float_inv : a b 3.14 2 3 -45
#   demo: float_div 2 : 1 2 3 4 5 6
#
def ints_(context,domain,A,B):
    if B.empty(): return data()
    BL,BR = B.split()
    if BL.atom(context):
        try:
            n = int(str(BL[0]))
            return da(str(n)) + data(domain|BR)
        except ValueError:
            return data(domain|BR)
#CONTEXT.define('ints',ints_)
def nats_(context,domain,A,B):
    if B.empty(): return data()
    BL,BR = B.split()
    if BL.atom(context):
        try:
            n = int(str(BL[0]))
            if n>=0:
                return da(str(n)) + data(domain|BR)
            else:
                return data(domain|BR)
        except ValueError:
            return data(domain|BR)
CONTEXT.define('nats',nats_)
def floats_(context,domain,A,B):
    if B.empty(): return data()
    BL,BR = B.split()
    if BL.atom(context):
        try:
            x = float(str(BL[0]))
            return da(str(x)) + data(domain|BR)
        except ValueError:
            return data(domain|BR)
#CONTEXT.define('floats',floats_)
def int_sum(context,domain,A,B):
    if B.atomic(context):
        ns = ints(B)
        sum = 0
        for n in ns: sum += n
        return da(str(sum))
#CONTEXT.define('int_sum',int_sum)
def nat_sum(context,domain,A,B):
    if B.atomic(context):
        ns = nats(B)
        sum = 0
        for n in ns: sum += n
        return da(str(sum))
CONTEXT.define('nat_sum',nat_sum)
def float_sum(context,domain,A,B):
    if B.atomic(context):
        fs = floats(B)
        sum = 0.0
        for f in fs: sum += f
        return da(str(sum))
#CONTEXT.define('float_sum',float_sum)
def int_prod(context,domain,A,B):
    if B.atomic(context):
        ns = ints(B)
        prod = 1
        for i in ns: prod = prod * i
        return da(str(prod))
#CONTEXT.define('int_prod',int_prod)
def nat_prod(context,domain,A,B):
    if B.atomic(context):
        ns = nats(B)
        prod = 1
        for i in ns: prod = prod * i
        return da(str(prod))
CONTEXT.define('nat_prod',nat_prod)
def float_prod(context,domain,A,B):
    if B.atomic(context):
        fs = floats(B)
        prod = 1.0
        for f in fs: prod = prod * f
        return da(str(prod))
#CONTEXT.define('float_prod',float_prod)
def int_sort(context,domain,A,B):
    if B.atomic(context):
        ns = ints(B)
        ns.sort()
        return data(*[co(str(i)) for i in ns])
#CONTEXT.define('int_sort',int_sort)
def nat_sort(context,domain,A,B):
    if B.atomic(context):
        ns = nats(B)
        ns.sort()
        return data(*[co(str(n)) for n in ns])
CONTEXT.define('nat_sort',nat_sort)
def float_sort(context,domain,A,B):
    if B.atomic(context):
        fs = floats(B)
        fs.sort()
        return data(*[co(str(f)) for f in fs])
#CONTEXT.define('float_sort',float_sort)
def text_sort(context,domain,A,B):
    if B.atomic(context):
        txts = [str(b) for b in B]
        txts.sort()
        return data(*[co(txt) for txt in txts])
CONTEXT.define('text_sort',text_sort)
def int_max(context,domain,A,B):
    if B.atomic(context):
        L = _max(ints(B))
        return data(*[co(str(l)) for l in L])
#CONTEXT.define('int_max',int_max)
def int_min(context,domain,A,B):
    if B.atomic(context):
        L = _min(ints(B))
        return data(*[co(str(l)) for l in L])
#CONTEXT.define('int_min',int_min)
def nat_max(context,domain,A,B):
    if B.atomic(context):
        L = _max(nats(B))
        return data(*[co(str(l)) for l in L])
CONTEXT.define('nat_max',nat_max)
def nat_min(context,domain,A,B):
    if B.atomic(context):
        L = _min(nats(B))
        return data(*[co(str(l)) for l in L])
CONTEXT.define('nat_min',nat_min)
def float_max(context,domain,A,B):
    if B.atomic(context):
        L = _max(floats(B))
        return data(*[co(str(l)) for l in L])
#CONTEXT.define('float_max',float_max)
def float_min(context,domain,A,B):
    if B.atomic(context):
        L = _min(floats(B))
        return data(*[co(str(l)) for l in L])
#CONTEXT.define('float_min',float_min)

def int_inv_0(context,domain,A,B):
    if B.empty(): return data()
def int_inv_1(context,domain,A,B):
    BL,BR = B.split()
    if BL.atom(context):
        L  = ints(BL)
        Li = [co(str(-l)) for l in L]
        return data(*Li)+data((domain+A)|BR)
#CONTEXT.define('int_inv',int_inv_0,int_inv_1)
def int_div_0(context,domain,A,B):
    if B.empty(): return data()
def int_div_2(context,domain,A,B):
    if A.empty(): return B
def int_div_1(context,domain,A,B):
    if A.rigid(context) and len(A)==1:
        BL,BR = B.split()
        if BL.atom(context):
            num = tryint(BL)
            den = tryint(A)
            if den is None: return None
            if num is None: return data((domain+A)|BR)
            if not den==0:
                return da(str(num//den)) + data((domain+A)|BR)
#CONTEXT.define('int_div',int_div_0,int_div_1,int_div_2)

def float_inv_0(context,domain,A,B):
    if B.empty(): return data()
def float_inv_1(context,domain,A,B):
    BL,BR = B.split()
    if BL.atom(context):
        L  = floats(BL)
        Li = [co(str(-l)) for l in L]
        return data(*Li)+data((domain+A)|BR)
#CONTEXT.define('float_inv',float_inv_0,float_inv_1)
def float_div_0(context,domain,A,B):
    if B.empty(): return data()
def float_div_2(context,domain,A,B):
    if A.empty(): return B
def float_div_1(context,domain,A,B):
    if A.rigid(context) and len(A)==1:
        BL,BR = B.split()
        if BL.atom(context):
            num = tryfloat(BL)
            den = tryfloat(A)
            if den is None: return None
            if num is None: return data((domain+A)|BR)
            if not den==0:
                return da(str(num/den)) + data((domain+A)|BR)
#CONTEXT.define('float_div',float_div_0,float_div_1,float_div_2)
