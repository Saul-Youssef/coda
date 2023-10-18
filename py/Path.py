#
#
#
from base import *
import os
#
#    Go up/down one level in a file system
#
def up_1(context,domain,A,B):
    BL,BR = B.split()
    if BL.atom(context): return ((domain+A)|BL) + ((domain+A)|BR)
def up_2(context,domain,A,B):
    if B.atom(context):
        p = str(B[0])
#        import os
#        path = os.path.abspath(os.path.expanduser(p))
        path = p
        return da('/'.join(path.split('/')[:-1]))
def up_3(context,domain,A,B):
    if B.empty(): return data()
CONTEXT.define('up1',up_2,up_3,up_1)

def down_1(context,domain,A,B):
    BL,BR = B.split()
    if BL.atom(context): return ((domain+A)|BL) + ((domain+A)|BR)
def down_2(context,domain,A,B):
    if A.atom(context) and B.atom(context):
#        dirpath = os.path.abspath(os.path.expanduser(str(B[0])))
        dirpath = str(B[0])
        if not dirpath.endswith('/'): dirpath = dirpath+'/'
        fn = str(A[0]).split('/')[-1]
        return da(dirpath+fn)
def down_3(context,domain,A,B):
    if B.empty(): return data()
CONTEXT.define('down1',down_2,down_3,down_1)
