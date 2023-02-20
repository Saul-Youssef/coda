#
#    System
#
import __init__
from base import *
import sys
sys.setrecursionlimit(10000)
import Evaluate,Text
#
#    Standard context
#
Evaluate.generic(data(colon(data(b'{coda:homecontext:}'),data())),1000)
Evaluate.generic(data(colon(data(b'{coda:startcontext:}'),data())),1000)
#
#    Interpreter loop
#
import sys
try:
    N = abs(int(sys.argv[1]))
except (ValueError,IndexError):
    N = 500

def co(text): return data(colon(data(b'{'+text.encode()+b'}'),data()))
def ev(D,n): return Evaluate.depth(D,n)[0]
def st(D):
    import Inspect
    stat = Inspect.statistic()
    stat = Inspect.update_stat(D,stat,0)
    stat.display()
