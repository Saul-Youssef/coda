#
#    Text colors and styles
#
ESC = '\x1b'
colors = {'default':'','red':'31','white':'37','green':'32','yellow':'33','blue':'34','magenta':'35','cyan':'36'}
styles = {'default':'','bold':';1','underline':';4','blink':';5','reversevideo':';7','concealed':';8'}

def decorate(txt,color='default',style='default'):
    return ESC+'['+colors[color]+styles[style]+'m'+txt+ESC+'[0m'

from base import *
import string
#
#   Get all codes up to argument specified length
#   with input alphabet.
#
#   demo: codes 3 : a b c
#
def codes(context,domain,A,B):
    if all([a.atom(context) for a in A]+[b.atom(context) for b in B]):
        import Number
        maxs = Number.ints(A)
        if len(maxs)==1:
            alpha = [str(b) for b in B]
            txts = [w for w in _alphawords(maxs[0],'',alpha)]
            return data(*[co(txt) for txt in txts])
def codes_0(context,domain,A,B):
    if B.empty(): return data()
CONTEXT.define('codes',codes,codes_0)

def _alphawords(max,base,alphabet):
    if len(base)<max:
        for c in alphabet:
            yield base+c
            for w in _alphawords(max,base+c,alphabet): yield w
#
#   Standard text-related data.
#
#   demo: alphabet:
#   demo: letters:
#   demo: digits:
#   demo: printable:
#
def    digits(context,domain,A,B): return data(*[co(s) for s in string.digits.split('\t')[0]])
def   letters(context,domain,A,B): return data(*[co(s) for s in string.ascii_letters.split('\t')[0]])
def printable(context,domain,A,B): return data(*[co(s) for s in string.printable.split('\t')[0]])
def  alphabet(context,domain,A,B): return data(*[co(s) for s in string.ascii_lowercase.split('\t')[0]])
CONTEXT.define('digits',digits)
CONTEXT.define('letters',letters)
CONTEXT.define('printable',printable)
CONTEXT.define('alphabet',alphabet)
#
#   A very non-practical data consisting of all codes with input alphabet
#   FIX ME
#   demo: step 5 : allcodes :
#
def allcodes(context,domain,A,B):
    import Number
    if (A.empty() or A.atom(context)) and len(Number.ints(A))<=1:
        n = 0
        if len(Number.ints(A))>0: n = Number.ints(A)[0]

        codes = da('codes'); N = da(str(n)); Np = da(str(n+1))
        return ((codes+N)|B) + ((domain+Np)|B)
def allcodes_0(context,domain,A,B):
    if B.empty(): return data()
CONTEXT.define('allcodes',allcodes,allcodes_0)
#
#   Display input in native "pure" form.
#
#   The argument replaces (:) with a supplied character for readability.
#
#   demo: pure : hello
#   demo: pure a : hello
#
def pure(context,domain,A,B):
    BL,BR = B.split()
    if BL.atom(context) and (A.empty() or A.atom(context)):
        if A.empty():
            return da(repr(BL)) + data((domain+A)|BR)
        else:
            atom = str(A[0])
            return da(str_atom_data(BL,atom)) + data((domain+A)|BR)
def pure_0(context,domain,A,B):
    if B.empty(): return data()
CONTEXT.define('pure',pure,pure_0)

def str_atom_coda(c,ch):
    if c.left().empty() and c.right().empty():
        return ch
    else:
        return '('+str_atom_data(c.left(),ch)+':'+str_atom_data(c.right(),ch)+')'
def str_atom_data(d,ch): return ''.join([str_atom_coda(c,ch) for c in d])
#
#   Wrap code with a one character prefix and postfix.
#
#   demo: wrap [] : xxx
#   demo: wrap | : xxx
#   demo: wrap <()> : xxx
#   demo: wrap <{}> : xxx
#   demo: wrap <<>> : xxx
#
def wrap(context,domain,A,B):
    A0,AR = A.split()
    B0,BR = B.split()
    if A0.atom(context) and B0.atom(context):
        w = str(A0); txt = str(B0)
        if w=='':
            l,r = '',''
        else:
            l,r = w[0],w[-1]
        return da(l+txt+r) + data((domain+A)|BR)
def wrap_0(context,domain,A,B):
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
def startswith(context,domain,A,B):
    if all([a.atom(context) for a in A]):
        BL,BR = B.split()
        if BL.atom(context):
            pre = [str(data(a)) for a in A]
            txt = str(BL)
            if any([txt.startswith(p) for p in pre]):
                return BL + data((domain+A)|BR)
            else:
                return      data((domain+A)|BR)
def startswith_0(context,domain,A,B):
    if B.empty(): return data()
CONTEXT.define('startswith',startswith,startswith_0)

def endswith(context,domain,A,B):
    if all([a.atom(context) for a in A]):
        BL,BR = B.split()
        if BL.atom(context):
            pre = [str(data(a)) for a in A]
            txt = str(BL)
            if any([txt.endswith(p) for p in pre]):
                return BL + data((domain+A)|BR)
            else:
                return      data((domain+A)|BR)
def endswith_0(context,domain,A,B):
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
def join(context,domain,A,B):
    if all([a.atom(context) for a in A]+[b.atom(context) for b in B]):
        sep = ''.join([str(a) for a in A])
        return da(sep.join([str(b) for b in B]))
CONTEXT.define('join',join)
def split(context,domain,A,B):
    if all([a.atom(context) for a in A]+[b.atom(context) for b in B]):
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

def strmax(txt,n):
    if len(txt)<=n: return txt
    return txt[:n]+'...'
def table(context,domain,A,B0):
    if not A.rigid(context): return
    if not B0.stable(context): return
    n = 1000
    import Number
    ns = Number.ints(A)
    if len(ns)>0 and ns[0]>0: n = ns[0]
    B = B0
#    B = context.evaluate(n,B0)
#    if B.stable(context):
    if True:
        left,right = [],[]
        for b in B:
            left.append(str(b.arg()))
            right.append(str(b.right()))
        lmax = 0
        if len(left)>0:
            lmax = max(len(l) for l in left)
        left2 = []
        for l in left:
            while len(l)<lmax: l = ' '+l
            left2.append(l)
        txts = []
        while len(left2)>0:
            l = left2.pop(0)
            r = right.pop(0)
            txts.append(l+' '+r)
        return da('\n'.join(txts))
CONTEXT.define('table',table)

if __name__=='__main__':
    t = '@@@'
    print(t)
    print(decorate(t,'red'))
    print(decorate(t,'blue','bold'))
