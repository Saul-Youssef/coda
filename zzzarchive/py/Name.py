#
#   The ascii code in pure data 
#
from base import * 
import string 

NAME = {}
z = data() 
b0 = z|z
b1 = z|(z|z)
NAME[z] = "0"
NAME[b0] = "\N{MATHEMATICAL BOLD DIGIT ZERO}"
NAME[b1] = "\N{MATHEMATICAL BOLD DIGIT ONE}"
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
    return data(*B)

for c in string.printable: NAME[byte(c)] = c