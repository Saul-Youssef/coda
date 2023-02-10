#
#   Some data displays
#
from base import *

SPA = '.'
IND = 2

def ddisplay(D,indent=0):
    for d in D:
        if is_code(d):
            yield (indent*SPA)+d.decode()+'\n'
        else:
            for t in cdisplay(d,indent): yield t

def cdisplay(d,indent):
    yield (indent*SPA)+'('+'\n'
    for t in ddisplay(d.left(),indent+IND): yield t
    yield (indent*SPA)+':'+'\n'
    for t in ddisplay(d.right(),indent+IND): yield t
    yield (indent*SPA)+')'+'\n'
