#
#    Import start to set up all of the definitions coming from the source 
#    code in the core of the system.
#
from base import * 
import Code,Language,Universe 
import sys

#sys.setrecursionlimit(10000)

#
#    Standard context
#
#Evaluate.generic(data(colon(data(b'{coda:homecontext:}'),data())),1000)
#Evaluate.generic(data(colon(data(b'{coda:startcontext:}'),data())),1000)
#
#    Interpreter loop
#
#import sys
#try:
#    N = abs(int(sys.argv[1]))
#except (ValueError,IndexError):
#    N = 500
