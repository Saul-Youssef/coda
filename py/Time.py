#
#    Pause waits an argument-specified amount of time
#    for each input.
#
#    demo: pause : a b c
#    demo: pause 3 : a b c
#    demo: pause 0.1 : a b c 
#
from base import *

def pause(context,domain,A,B):
    if A.rigid(context):
        BL,BR = B.split()
        if BL.atom(context):
            import time
            import Number
            t = Number.floatdef(0.1,A)
            if t>0.0: time.sleep(t)
            return BL+data((domain+A)|BR)
def pause_0(context,domain,A,B):
    if B.empty(): return data()
CONTEXT.define('pause',pause,pause_0)
