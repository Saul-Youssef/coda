#
#    Code operations
#
from base import *

def codes(D): return [d for d in D if is_code(d)]
def allcode(D): return all([is_code(d) for d in D])
#
#   Wrap code with a one character prefix and postfix.
#
#   demo: wrap [] : xxx
#   demo: wrap | : xxx
#   demo: wrap <()> : xxx
#   demo: wrap <{}> : xxx
#   demo: wrap <<>> : xxx
#
def wrap(A,B):
    A0,AR = A.split()
    B0,BR = B.split()
    if A0.atom() and B0.atom():
        if is_code(A0[0]) and is_code(B0[0]):
            w = A0[0]; txt = B0[0]
            if w==b'':
                l,r = b'',b''
            else:
                l,r = (w.decode()[0]).encode(),(w.decode()[-1]).encode()
            return data(l+B0[0]+r) + one(b'wrap',A0,BR)
def wrap_0(A,B):
    if B.empty(): return data()
DEF.add(data(b'wrap'),wrap,wrap_0)
#
#   Selects codes that start/end with argument specified pre or post code
#
#   demo: startswith xy : xyaaa xbbbx xycccx
#   demo: startswith <x y> : <x yaaa> <x ybbb> xxx
#   demo: endswith x : xyaaa xbbbx xycccx
#
def startswith(A,B):
    AL,AR = A.split()
    BL,BR = B.split()
    if AL.atom() and BL.atom():
        pre = codes(AL)
        if len(pre)==1:
            txt = pre.pop()
            ts = codes(BL)
            if len(ts)==1:
                if ts[0].startswith(txt): return BL + one(b'startswith',AL,BR)
                else                    : return      one(b'startswith',AL,BR)
def startswith_0(A,B):
    if B.empty(): return data()
DEF.add(data(b'startswith'),startswith,startswith_0)

def endswith(A,B):
    AL,AR = A.split()
    BL,BR = B.split()
    if AL.atom() and BL.atom():
        pre = codes(AL)
        if len(pre)==1:
            txt = pre.pop()
            ts = codes(BL)
            if len(ts)==1:
                if ts[0].endswith(txt): return BL + one(b'endswith',AL,BR)
                else                  : return      one(b'endswith',AL,BR)
def endswith_0(A,B):
    if B.empty(): return data()
DEF.add(data(b'endswith'),endswith,endswith_0)
#
#   Join codes with a separator.
#
#   demo: join , : a b c
#   demo: join <,> : a b c
#   demo: join < > : a b c
#   demo: join <> : a b c
#   demo: join : a b c
#
def join(A,B):
    if allcode(A) and allcode(B):
        sep = b''.join(A)
        return data(sep.join(B))
DEF.add(data(b'join'),join)
#
#   Prefix and postfix argument specified codes to inputs.
#
#   demo: prefix x : 1 2 3 4
#   demo: postfix x : 1 2 3 4
#
def prefix(A,B):
    if allcode(A):
        pre = b''.join(A)
        B0,BR = B.split()
        if B0.atom() and is_code(B0[0]):
            return data(pre+B0[0]) + one(b'prefix',data(pre),BR)
def prefix_0(A,B):
    if B.empty(): return data()
DEF.add(data(b'prefix'),prefix,prefix_0)
def postfix(A,B):
    if allcode(A):
        post = b''.join(A)
        B0,BR = B.split()
        if B0.atom() and is_code(B0[0]):
            return data(B0[0]+post) + one(b'postfix',data(post),BR)
def postfix_0(A,B):
    if B.empty(): return data()
DEF.add(data(b'postfix'),postfix,postfix_0)
#
#    Contains as substring
#
#    demo: contains x : aaa bbb ccxcc dddd xxx
#    demo: contains x y : ab ax ay axyb
#
def contains(A,B):
    if allcode(A):
        B0,BR = B.split()
        if B0.atom() and is_code(B0[0]):
            x = B0[0]
            if any([a in x for a in A]):
                return B0 + one(b'contains',A,BR)
            else:
                return one(b'contains',A,BR)
def contains_0(A,B):
    if B.empty(): return data()
DEF.add(data(b'contains'),contains,contains_0)
def notcontains(A,B):
    if allcode(A):
        B0,BR = B.split()
        if B0.atom() and is_code(B0[0]):
            x = B0[0]
            if not any([a in x for a in A]):
                return B0 + one(b'notcontains',A,BR)
            else:
                return one(b'notcontains',A,BR)
def notcontains_0(A,B):
    if B.empty(): return data()
DEF.add(data(b'notcontains'),notcontains,notcontains_0)

def _alphawords(max,base,alphabet):
    if len(base)<max:
        for c in alphabet:
            yield base+c
            for w in _alphawords(max,base+c,alphabet): yield w
#
#   Argument specified number of combinations of input characters
#
#   demo: alphacodes 2 : abcd
#
def alphacodes(A,B):
    import Number
    maxs = Number.ints(A)
    if len(maxs)==1 and allcode(B):
        chars = set([])
        for b in B:
            for i in range(len(b)): chars.add(b[i:i+1])
        codes = [w for w in _alphawords(maxs[0],b'',chars)]
        return data(*codes)
DEF.add(data(b'alphacodes'),alphacodes)

if __name__=='__main__':
    for x in _alphawords(3,b'',[b'a',b'b',b'c']): print(x)
