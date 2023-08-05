#
#   Pure data can have associated unicode names
#
#import base
from base import *
import string
#
#    Coda to unicode for display purposes
#
#Unicode = {}  # coda to unicode
#
#z = data()
#atom = (z|z)
#bit0 = (data(atom)|data())
#bit1 = (data(atom)|data(atom))
#Unicode[atom] = "\u220E"
#Unicode[atom] = "\u229B"
#Unicode[atom] = "\u23FA"
#Unicode[atom] = "\u25C9"
#Unicode[atom] = "\u25CE"
#Unicode[atom] = '*'
#Unicode[atom] = "\u25D1"
#Unicode[atom] = "\u2B24"
#Unicode[bit0] = "0"
#Unicode[bit1] = "1"

#bit0 = z|z
#bit1 = z|data(bit0)
#Unicode[bit1] = "1"
#Unicode[bit0] = "0"
#Unicode[bit0] = "\u2299"
#Unicode[bit1] = '\u25A1'
#Unicode[bit0] = '\u25A0'
#Unicode[bit1] = u"\U0001D7D9"
#Unicode[bit0] = u"\U0001D7D8"
#Unicode[bit1] = u"\U0001D75E"
#Unicode[bit0] = u"\U0001D7EC"
#Unicode[bit1] = '1'
#Unicode[bit0] = '0'

#  Display atom, 0-bit and 1-bit in ascii instead of fancy unicode characters
#def ascii_bits():
#    Unicode[atom] = '*'
#    Unicode[bit0] = '0'
#    Unicode[bit1] = '1'
#
#   bits, bytes and byte sequences are atomic
#
#CONTEXT.add(Definition(data(    ))) # the domain of the "Hydrogen atom"
#CONTEXT.add(Definition(data(atom))) # the domain of 0-bit, 1-bit, other bits if hypothetically added
#CONTEXT.add(Definition(data(bit0))) # the domain of bit sequences
#CONTEXT.add(Definition(data(bit1))) # the domain of sequences of bit sequences, e.g. byte sequences
#
#   create a coda byte from a single character as an 8 bit bit string with domain bit0
#
#def byte2coda(c):
#    if type(c)==type(1): s = str(bin(c))      # ...integers
#    else               : s = str(bin(ord(c))) # ...single character strings
##    s = str(bin(ord(c)))
#    s = s.split('0b')[-1]
#    B = []
#    for x in s:
#        if   x=='0': B.append(bit0)
#        elif x=='1': B.append(bit1)
#        else: raise error('Error converting byte')
#    while len(B)<8:
#        B = [bit0]+B
#    return (data(bit0)|data(*B))
#
#def text2coda(text): return (data(bit1)|data(*[byte2coda(c) for c in text]))
#
#for c in string.printable: Unicode[byte2coda(c)] = c
#
#def data2unicode(D,sep=' '):
#    return sep.join([coda2unicode(c) for c in D])
#def coda2unicode(c):
#    if c in Unicode: return Unicode[c]
#    if c.domain() in [data(atom),data(bit1),data(bit0)]: return data2unicode(c.right(),'')
#    return '('+data2unicode(c.left(),' ')+':'+data2unicode(c.right(),' ')+')'

def unicode(domain,A,B):
    if A.atom() and not B.empty() and B.invariant():
        UNICODE.setatom(A[0],str(B))
        return data()
CONTEXT.define('unicode',unicode)
#
#   Wrap code with a one character prefix and postfix.
#
#   demo: wrap [] : xxx
#   demo: wrap | : xxx
#   demo: wrap <()> : xxx
#   demo: wrap <{}> : xxx
#   demo: wrap <<>> : xxx
#
def wrap(domain,A,B):
    A0,AR = A.split()
    B0,BR = B.split()
    if A0.atom() and B0.atom():
        w = str(A0); txt = str(B0)
        if w=='':
            l,r = '',''
        else:
            l,r = w[0],w[-1]
        return da(l+txt+r) + data((domain+A)|BR)
def wrap_0(domain,A,B):
    if B.empty(): return data()
CONTEXT.define('wrap',wrap,wrap_0)
#
#   Selects codes that start/end with argument specified pre or post code
#
#   demo: startswith xy : xya xbbbx yzzz xycccx
#   demo: startswith x y : x y <> xx yy zz
#   demo: startswith <x y> : <x yaaa> <x ybbb> xxx
#   demo: endswith a : xa xb xc ya yb yc
#   demo: endswith a b : xa xb xc ya yb yc
#
def startswith(domain,A,B):
    if all([a.atom() for a in A]):
        BL,BR = B.split()
        if BL.atom():
            pre = [str(data(a)) for a in A]
            txt = str(BL)
            if any([txt.startswith(p) for p in pre]):
                return BL + data((domain+A)|BR)
            else:
                return      data((domain+A)|BR)
def startswith_0(domain,A,B):
    if B.empty(): return data()
CONTEXT.define('startswith',startswith,startswith_0)

def endswith(domain,A,B):
    if all([a.atom() for a in A]):
        BL,BR = B.split()
        if BL.atom():
            pre = [str(data(a)) for a in A]
            txt = str(BL)
            if any([txt.endswith(p) for p in pre]):
                return BL + data((domain+A)|BR)
            else:
                return      data((domain+A)|BR)
def endswith_0(domain,A,B):
    if B.empty(): return data()
CONTEXT.define('endswith',endswith,endswith_0)
#
#   Join codes with argument provided separator.
#
#   demo: join , : a b c
#   demo: join <-> : a b c
#   demo: count : join < > : a b c
#   demo: join <> : a b c
#   demo: join : a b c
#   demo: split . : a.b.c.d
#   demo: join . : split . : a.b.c.d
#   demo: split % <=> : <aaa%bbb=ccc>
#
def join(domain,A,B):
    if all([a.atom() for a in A]+[b.atom() for b in B]):
        sep = ''.join([str(a) for a in A])
        return da(sep.join([str(b) for b in B]))
CONTEXT.define('join',join)
def split(domain,A,B):
    if all([a.atom() for a in A]+[b.atom() for b in B]):
        splits = [str(a) for a in A if not str(a)=='']
        Bs = [str(b) for b in B]
        if len(splits)==0:
            T = []
            for b in Bs:
                for t in b: T.append(t)
        while len(splits)>0:
            sep = splits.pop()
            T = []
            for b in Bs:
                for x in b.split(sep): T.append(x)
            Bs = T
        return data(*[co(t) for t in T])
CONTEXT.define('split',split)
