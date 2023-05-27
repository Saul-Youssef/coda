#
#   Numbers
#
#   Basic, low level computing python integers or python floats from code
#
from base import *
#import Code

class BinaryOperation(object):
    def __init__(self,coerce,operation):
        self._coerce = coerce
        self._operation = operation
    def __call__(self,A,B):
        if A.atom() and B.atom():
            Ac = self._coerce(A); Bc = self._coerce(B)
            if len(Ac)==1 and len(Bc)==1:
                result = self._operation(Ac[0],Bc[0])
                return da(str(result))

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
#
#   Try to get the integers from data D, ignoring colons and non-integer codes
#
def   ints(D): return [tryint  (d) for d in D if not tryint  (d) is None]
def floats(D): return [tryfloat(d) for d in D if not tryfloat(d) is None]
#
#    Used multiple times below.
#
def empty(domain,A,B):
    if A.empty() or B.empty(): return data()
def default_zero(domain,A,B):
    if A.empty() or B.empty(): return da('0')
def default_one(domain,A,B):
    if A.empty() or B.empty(): return da('1')
#
#   Code version of the natural numbers 0 1 2 3...
#
#   nat : n -> n (nat:n+1)
#
#   demo: nat : 0
#   demo: nat : 100
#   demo: nat a b c : x y z
#   demo: nat : x?
#
def nat(domain,A,B):
    ns = ints(B)
    if len(ns)==1:
        n = ns.pop()
        return co(str(n)) + (domain|da(str(n+1)))
CONTEXT.define('nat',nat)
#
#   Makes a code 1 if the input is a single atom.  Used for counting.
#
#   demo: one : x
#   demo: one : (bin:x)
#   demo: one :
#   demo: one : foo : bar
#   demo: count : a b c d
#
def one(domain,A,B):
    if B.atom(): return da('1')
    if B.empty(): return data()
CONTEXT.define('one',one)
def count(domain,A,B):
    if all([b.atom() for b in B]): return da(str(len(B)))
def count_0(domain,A,B):
    if B.empty(): return data()
CONTEXT.define('count',count,count_0)
#
#   Select atoms consisting of a code that translates to an integer.
#
#   Low level.
#
#   int1 : 1
#   int1 : 1 2 3 -14
#   ap int1 : 1 2 3
#   int1 :
#   int1 : foo : bar
#   ap nat1 : a 2 3 -15
#   ap float1 : a 2 3 -15
#
def Int(domain,A,B):
    if B.atom():
        if len(ints(B))==1: return B
        else              : return data()
CONTEXT.define('int1',Int)
def Nat(domain,A,B):
    if B.atom():
        if len(ints(B))==1 and ints(B)[0]>=0: return B
        else                                : return data()
CONTEXT.define('nat1',Nat)

def Float(domain,A,B):
    if B.atom():
        if len(floats(B))==1: return B
        else                : return data()
CONTEXT.define('float1',Float)
#
#   Integer binary operations
#
#   demo: int_add 2 : 3
#   demo: int_mult 2 : 3
#   demo: int_max 2 : 3
#   demo: int_diff 2 : 3
#   demo: int_min 2 : 3
#   demo: aps int_add : 1 2 3 4 5
#
OP1 = BinaryOperation(ints,lambda x,y: x+y)
CONTEXT.define('int_add',lambda domain,A,B:OP1(A,B),empty)
OP2 = BinaryOperation(ints,lambda x,y: x*y)
CONTEXT.define('int_mult',lambda domain,A,B:OP2(A,B),empty)
OP3 = BinaryOperation(ints,lambda x,y: y-x)
CONTEXT.define('int_diff',lambda domain,A,B:OP3(A,B),empty)
OP4 = BinaryOperation(ints,lambda x,y: max(x,y))
CONTEXT.define('int_max',lambda domain,A,B:OP4(A,B),empty)
OP5 = BinaryOperation(ints,lambda x,y: min(x,y))
CONTEXT.define('int_min',lambda domain,A,B:OP5(A,B),empty)
#
#   Float binary operations and involutions
#
#   demo: float_add 2.1 : 3.1
#   demo: float_mult 2.1 : 3.1
#   demo: float_max 2.1 : 3.1
#   demo: float_diff 2.1 : 3.1
#   demo: float_min 2 : 3
#   demo: aps float_add : 1.1 2.1 3.1 4.1 5.1
#   demo: aps float_mult : 1.1 2.1 3.1 4.1 5.1
#   demo:int_inv : 1 2 -3 -4
#   demo:float_inv : 1.1 2.1 -3.1 -4.1
#
OP6 = BinaryOperation(floats,lambda x,y: x+y)
CONTEXT.define('float_add',lambda domain,A,B: OP6(A,B),empty)
OP7 = BinaryOperation(floats,lambda x,y: x*y)
CONTEXT.define('float_mult',lambda domain,A,B: OP7(A,B),empty)
OP8 = BinaryOperation(floats,lambda x,y: y-x)
CONTEXT.define('float_diff',lambda domain,A,B: OP8(A,B),empty)
OP9 = BinaryOperation(floats,lambda x,y: max(x,y))
CONTEXT.define('float_max',lambda domain,A,B: OP9(A,B),empty)
OP10 = BinaryOperation(floats,lambda x,y: min(x,y))
CONTEXT.define('float_min',lambda domain,A,B:OP10(A,B),empty)
#
def codes(D): return [str(c) for c in D]
#
#   code binary operations
#
#   demo: code_add <xx yy> : <11 22>
#   demo: code_min 1234 : 1235
#   demo: code_max 1234 : 1235
#   demo: aps code_add : 1 2 3 4 5 6
#
OP11 = BinaryOperation(codes,lambda x,y:x+y)
CONTEXT.define('code_add',lambda domain,A,B:OP11(A,B),empty)
OP12 = BinaryOperation(codes,lambda x,y:min(x,y))
CONTEXT.define('code_min',lambda domain,A,B:OP12(A,B),empty)
OP13 = BinaryOperation(codes,lambda x,y:max(x,y))
CONTEXT.define('code_max',lambda domain,A,B:OP13(A,B),empty)
#
#   sorting integers or floats
#
#   demo: int_sort : 5 4 3 2 1
#   demo: int_sort : int_sort : 5 4 3 2 1
#   demo: float_sort : 5.1 4.1 3.1 2.1 1.1 -99.0
#
def int_sort(domain,A,B):
    if all([b.atom() for b in B]):
        ns = ints(B)
        ns.sort()
        return data(*[co(str(n)) for n in ns])
def int_sort0(domain,A,B):
    if B.empty(): return data()
CONTEXT.define('int_sort',int_sort,int_sort0)

def float_sort(domain,A,B):
    if all([b.atom() for b in B]):
        flts = floats(B)
        flts.sort()
        return data(*[co(str(fl)) for fl in flts])
def float_sort0(domain,A,B):
    if B.empty(): return data()
CONTEXT.define('float_sort',float_sort,float_sort0)
#
#   Involutions
#
#   demo:int_inv : 1 2 -3 -4
#   demo:float_inv : 1.1 2.1 -3.1 -4.1
#
def int_inv(domain,A,B):
    B0,BR = B.split()
    if B0.atom():
        bs = ints(B0)
        if len(bs)>0:
            return da(str(-bs[0])) + data((domain+A)|BR)
        else:
            return data((domain+A)|BR)
def int_inv_0(domain,A,B):
    if B.empty(): return data()
CONTEXT.define('int_inv',int_inv,int_inv_0)

def float_inv(domain,A,B):
    B0,BR = B.split()
    if B0.atom():
        bf = floats(B0)
        if len(bf)>0:
            return da(str(-bf[0])) + data((domain+A)|BR)
        else:
            return data((domain+A)|BR)
def float_inv_0(domain,A,B):
    if B.empty(): return data()
CONTEXT.define('float_inv',float_inv,float_inv_0)
