#
#    Import start to set up all of the definitions coming from the source
#    code in the core of the system.
#
from base import *
import Language,Evaluate
import sys

#sys.setrecursionlimit(10000)
#
#    Standard context
#
Evaluate.resolve(Language.lang('homecontext:', data(),data()),1000)
Evaluate.resolve(Language.lang('startcontext:',data(),data()),1000)
