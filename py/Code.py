#
#   Pure data can have associated unicode names
#
#import base
from base import *
import string
#
#    Coda to unicode for display purposes
#
Unicode = {}  # coda to unicode

z = data()
bit0 = z|z
bit1 = z|data(bit0)
Unicode[bit1] = "1"
Unicode[bit0] = "0"
#Unicode[bit1] = '\u25A1'
#Unicode[bit0] = '\u25A0'
#Unicode[bit1] = u"\U0001D7D9"
#Unicode[bit0] = u"\U0001D7D8"
#
#   bits, bytes and byte sequences are atomic with
#   domain z=().
#
CONTEXT.dom(data(),Definition(data()))
CONTEXT.dom(data(bit1),Definition(data(bit1)))
CONTEXT.dom(data(bit0),Definition(data(bit0)))
#CONTEXT.add(Definition(z))
#
#   create a coda byte from a single character as an 8 bit bit string with domain bit0
#
def byte2coda(c):
    if type(c)==type(1): s = str(bin(c))      # to handle both single chars
    else               : s = str(bin(ord(c))) # ...and single integer bytes
#    s = str(bin(ord(c)))
    s = s.split('0b')[-1]
    B = []
    for x in s:
        if   x=='0': B.append(bit0)
        elif x=='1': B.append(bit1)
        else: raise error('Error converting byte')
    while len(B)<8:
        B = [bit0]+B
    return data(bit0)|data(*B)

for c in string.printable: Unicode[byte2coda(c)] = c

#def text2coda(text): return data(bit1)|data(*[byte2coda(c) for c in text])
def text2coda(text): return data(bit1)|data(*[byte2coda(c) for c in text])

def data2unicode(D,sep=' '): return sep.join([coda2unicode(c) for c in D])
def coda2unicode(c):
    if c in Unicode: return Unicode[c]
    if c.domain() in [data(),data(bit1),data(bit0)]:
        return data2unicode(c.right(),'')
    return '('+data2unicode(c.left(),' ')+':'+data2unicode(c.right(),' ')+')'
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
        splits = [str(a) for a in A]
        Bs = [str(b) for b in B]
        while len(splits)>0:
            sep = splits.pop()
            T = []
            for b in Bs:
                for x in b.split(sep): T.append(x)
            Bs = T
        return data(*[co(t) for t in T])
CONTEXT.define('split',split)
#
#   Get all codes up to argument specified length
#   with input alphabet.
#
#   demo: codes 3 : a b c
#
def codes(domain,A,B):
    if all([a.atom() for a in A]+[b.atom() for b in B]):
        import Number
        maxs = Number.ints(A)
        if len(maxs)==1:
            alpha = [str(b) for b in B]
            txts = [w for w in _alphawords(maxs[0],'',alpha)]
            return data(*[co(txt) for txt in txts])
def codes_0(domain,A,B):
    if B.empty(): return data()
CONTEXT.define('codes',codes,codes_0)

def _alphawords(max,base,alphabet):
    if len(base)<max:
        for c in alphabet:
            yield base+c
            for w in _alphawords(max,base+c,alphabet): yield w
#
#   Display input in native "pure" form.
#
#   The argument replaces (:) with a supplied character for readability.
#
#   demo: pure : hello
#   demo: pure a : hello
#
def pure(domain,A,B):
    BL,BR = B.split()
    if BL.atom() and (A.empty() or A.atom()):
        if A.empty():
            return da(repr(BL)) + data((domain+A)|BR)
        else:
            atom = str(A[0])
            return da(str_atom_data(BL,atom)) + data((domain+A)|BR)
def pure_0(domain,A,B):
    if B.empty(): return data()
CONTEXT.define('pure',pure,pure_0)

def str_atom_coda(c,ch):
    if c.left().empty() and c.right().empty():
        return ch
    else:
        return '('+str_atom_data(c.left(),ch)+':'+str_atom_data(c.right(),ch)+')'
def str_atom_data(d,ch): return ''.join([str_atom_coda(c,ch) for c in d])

def dis_1(domain,A,B):
    if all([b.atom() for b in B]):
        lines = []
        for line in data_display(B,'__'): lines.append(line[2:])
        return da('\n'.join(lines))
def dis_0(domain,A,B):
    if B.empty(): return data()
CONTEXT.define('purev',dis_1,dis_0)
#
def data_display(D,margin):
    for c in D:
        for line in coda_display(c,margin): yield line

def coda_display(c,margin):
    if False and c in Unicode:
        yield margin+Unicode[c]
#    elif len(margin)+len(str(c))<80 and len(str(c))<20:
#        yield margin+str(c)
    elif len(margin)+len(repr(c))<80 and len(repr(c))<20:
        yield margin+repr(c)
    else:
        yield margin+'('
        for line in data_display(c.left(),margin+margin): yield line
        yield margin+':'
        for line in data_display(c.right(),margin+margin): yield line
        yield margin+')'
