#
#   Pure data can have associated unicode names
#
import base
import string

CODA = {} # Unicode to corresponding coda
CODE = {} # Coda to corresponding unicode name

z = base.data()
#b0 = z|z
#b1 = z|base.data(z|z)
#  data(z|z) is the empty string 
b0 = z|base.data(z|z)     
b1 = z|base.data(z|z,z|z)
CODE[b0] = "\N{MATHEMATICAL SANS-SERIF BOLD DIGIT ZERO}"
CODE[b1] = "\N{MATHEMATICAL SANS-SERIF BOLD DIGIT ONE}"
#
#   Get 8 bits of pure data from ascii characters.
#
def byte(c):
    s = str(bin(ord(c)))
    s = s.split('0b')[-1]
    B = []
    for x in s:
        if   x=='0': B.append(b0)
        elif x=='1': B.append(b1)
        else: raise base.error('Error converting byte')
    while len(B)<8:
        B = [b0]+B
    return base.coda(base.data(),base.data(*B))

for c in string.printable:
    CODE[byte(c)] = c
    CODA[c] = byte(c)

def coda2str(c): return ''.join([str(cc) for cc in c.right()])
def code2data(text): return base.data(*[byte(c) for c in text])
#
#   pretty display
#
def pretty(D):
    sep = ' '
    if D.depth()<=3: sep = ''
    return sep.join([prettycoda(c) for c in D])
def prettycoda(c):
    if          c in CODE: return CODE[c]
    elif c.left().empty(): return pretty(c.right())
    else: return '('+pretty(c.left())+':'+pretty(c.right())+')'

def codastr(c):
    if c in CODE: return CODE[c]
    else        : return '('+str(c.left())+':'+str(c.right())+')'

def datastr(d): return ' '.join([codastr(c) for c in d])

def _str_coda(c):
    if c in CODE: return CODE[c]
    elif c.left().empty(): return _str_data(c.right())
    else: return '('+_str_data(c.left())+':'+_str_data(c.right())+')'
def _str_data(d):
    sep = ' '
    if d.depth()==3: sep = ''
    return sep.join([_str_coda(c) for c in d])
