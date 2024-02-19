#!/usr/bin/env python3
#
#   Coda Interpreter
#
#   Command line setup
#
import rlcompleter
import readline,sys
readline.parse_and_bind("tab: complete")
sys.setrecursionlimit(10000)
#
#    System
#
from base import *
import Text,Language
import Evaluation

EXIT = ['exit','quit']
UNICODE.setatoms('(:)','0','1') # non-unicode for CLI
#
#   import local definitions from .../coda/co
#
KI = '--' in sys.argv
TR = '-'  in sys.argv
args = []
for a in sys.argv:
    try    : args.append(float(a))
    except : pass
SECONDS = 2.0
if len(args)>0: SECONDS = args.pop(0)
GB = 2.0
if len(args)>0: GB = args.pop(0)

if not KI:
    Local = Language.lang('ap use1 : localdef:',data(),data())
    D = Evaluation.Evaluate(CONTEXT,60,2)(Local)
    if not D.empty(): raise error('Local definition error '+str(D))

try:
    EV = Evaluation.Evaluate(CONTEXT,SECONDS,GB)
    while True:
        try:
            line = input(Text.decorate('@','blue','reversevideo')+' ')
            if line in EXIT: break
            D = Language.lang(line,data(),data())
            D = EV(D)

            if len(D)==1 and D[0].domain()==da('defaultTime'):
                try:
                    t = float(str(D[0].right()))
                    EV.setTimeLimit(t)
                except ValueError:
                    pass
            if not D.empty(): sys.stdout.write(str(D)+'\n')
        except KeyboardInterrupt:
            import traceback
            if TR: print(traceback.format_exc())
            sys.stdout.write('\n')
except EOFError:
    pass
