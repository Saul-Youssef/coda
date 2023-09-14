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
#   Standard text-related data.
#
#   demo: alphabet:
#   demo: letters:
#   demo: digits:
#   demo: printable:
#
def    digits(domain,A,B): return data(*[co(s) for s in string.digits.split('\t')[0]])
def   letters(domain,A,B): return data(*[co(s) for s in string.ascii_letters.split('\t')[0]])
def printable(domain,A,B): return data(*[co(s) for s in string.printable.split('\t')[0]])
def  alphabet(domain,A,B): return data(*[co(s) for s in string.ascii_lowercase.split('\t')[0]])
CONTEXT.define('digits',digits)
CONTEXT.define('letters',letters)
CONTEXT.define('printable',printable)
CONTEXT.define('alphabet',alphabet)
#
#   A very non-practical data consisting of all codes with input alphabet
#
#   demo: step 5 : allcodes :
#
def allcodes(domain,A,B):
    import Number
    if (A.empty() or A.atom()) and len(Number.ints(A))<=1:
        n = 0
        if len(Number.ints(A))>0: n = Number.ints(A)[0]

        codes = da('codes'); N = da(str(n)); Np = da(str(n+1))
        return ((codes+N)|B) + ((domain+Np)|B)
def allcodes_0(domain,A,B):
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

#def dis_1(domain,A,B):
#    if all([b.atom() for b in B]):
#        lines = []
#        for line in data_display(B,'__'): lines.append(line[2:])
#        return da('\n'.join(lines))
#def dis_0(domain,A,B):
#    if B.empty(): return data()
#CONTEXT.define('purev',dis_1,dis_0)
#
def data_display(D,margin):
    for c in D:
        for line in coda_display(c,margin): yield line

def coda_display(c,margin):
    if False and c in Unicode:
        yield margin+Unicode[c]
    elif len(margin)+len(repr(c))<80 and len(repr(c))<20:
        yield margin+repr(c)
    else:
        yield margin+'('
        for line in data_display(c.left(),margin+margin): yield line
        yield margin+':'
        for line in data_display(c.right(),margin+margin): yield line
        yield margin+')'

if __name__=='__main__':
    t = '@@@'
    print(t)
    print(decorate(t,'red'))
    print(decorate(t,'blue','bold'))
