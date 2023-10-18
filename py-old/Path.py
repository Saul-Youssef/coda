#
#
#
from base import *
#
#    Go up/down one level in a file system
#
def up_1(domain,A,B):
    BL,BR = B.split()
    if BL.atom(): return ((domain+A)|BL) + ((domain+A)|BR)
def up_2(domain,A,B):
    if B.atom():
        p = str(B[0])
        import os
        path = os.path.abspath(os.path.expanduser(p))
        return da('/'.join(path.split('/')[:-1]))
def up_3(domain,A,B):
    if B.empty(): return data()
CONTEXT.define('up',up_2,up_3,up_1)

def down_1(domain,A,B):
    BL,BR = B.split()
    if BL.atom(): return ((domain+A)|BL) + ((domain+A)|BR)
def down_2(domain,A,B):
    if A.atom() and B.atom():
        dirpath = os.path.abspath(os.path.expanduser(str(A[0])))
        if not dirpath.endswith('/'): dirpath = dirpath+'/'
        fn = str(B[0]).split('/')[-1]
        return da(dirpath+fn)
def down_3(domain,A,B):
    if B.empty(): return data()
CONTEXT.define('down',down_2,down_3,down_1)
