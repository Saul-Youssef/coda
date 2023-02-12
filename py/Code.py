#
#   Pure data can have associated unicode names  
#
import base 
import string 

DATA = {} # Unicode name to corresponding pure data 
CODE = {} # Pure data to corresponding unicode name 

z = base.data() 
b0 = z|z
b1 = z|(z|z)
CODE[z] = "\u2205"
CODE[b0] = "\N{MATHEMATICAL SANS-SERIF BOLD DIGIT ZERO}"
CODE[b1] = "\N{MATHEMATICAL SANS-SERIF BOLD DIGIT ONE}"

base.DEF.add(base.PF(b0)) # bit-0 flagged data is atomic 
base.DEF.add(base.PF(b1)) # bit-1 flagged data is atomic 
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
    return base.data(*B)

for c in string.printable: 
    CODE[byte(c)] = c
    DATA[c] = byte(c)
#
#    Translate a unicode string into pure data 
#
def data(text): return base.data(*[byte(c) for c in text])  
