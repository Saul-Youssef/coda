#
#
#
from base import *
import os
#
#    Go up/down in a file system
#
#    demo: home:
#    demo: up : home:
#    demo: down xxx : home: 
#
def up_1(context,domain,A,B):
    BL,BR = B.split()
    if BL.atom(context): return ((domain+A)|BL) + ((domain+A)|BR)
def up_2(context,domain,A,B):
    if B.atom(context):
        p = str(B[0])
        path = os.path.realpath(p)
        return da('/'.join(path.split('/')[:-1]))
def up_3(context,domain,A,B):
    if B.empty(): return data()
CONTEXT.define('up1',up_2,up_3,up_1)

def down_1(context,domain,A,B):
    BL,BR = B.split()
    if BL.atom(context): return ((domain+A)|BL) + ((domain+A)|BR)
def down_2(context,domain,A,B):
    if A.atom(context) and B.atom(context):
        dirpath = str(B[0])
        if not dirpath.endswith('/'): dirpath = dirpath+'/'
        fn = str(A[0]).split('/')[-1]
        return da(dirpath+fn)
def down_3(context,domain,A,B):
    if B.empty(): return data()
CONTEXT.define('down1',down_2,down_3,down_1)
