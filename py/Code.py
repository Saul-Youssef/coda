#
#   Pure data can have associated unicode names
#
import base
import string

CODA = {} # Unicode to corresponding coda
CODE = {} # Coda to corresponding unicode name

z = base.data()
b0 = z|z
b1 = z|(z|z)
#CODE[z] = "\u2205"
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
        else: raise error('Error converting byte')
    while len(B)<8:
        B = [b0]+B
    return base.coda(base.data(),base.data(*B))

for c in string.printable:
    CODE[byte(c)] = c
    CODA[c] = byte(c)
