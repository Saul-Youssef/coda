#!/usr/bin/env python3
#
#   Coda Interpreter
#
#   Command line setup
#
import rlcompleter
import readline,sys
readline.parse_and_bind("tab: complete")
#
#    System
#
from base import *
import Text,Language,Evaluate

EXIT = ['exit','quit']
UNICODE.setatoms('(:)','0','1') # non-unicode for CLI
#
#   import local definitions from .../coda/co
#
Local = Language.lang('ap use1 : localdef:',data(),data())
D = Evaluate.Eval(10*Evaluate.STEPS,10*Evaluate.EVALS,CONTEXT).evaluate(Local)
if not D.empty(): raise error('Local definition error '+str(D))

KI = False
if len(sys.argv)>1:
    if sys.argv[1]=='-': KI = True
    try:
        n = int(sys.argv[1])
        if n>1:
            Evaluate.DEFAULT = n
            Evaluate.STEPS = n
    except ValueError:
        pass
if len(sys.argv)>2:
    try:
        e = int(sys.argv[2])
        if e>1:
            Evaluate.EVALS = e
    except ValueError:
        pass

try:
    EV = Evaluate.Eval(Evaluate.STEPS,Evaluate.EVALS,CONTEXT)
    while True:
        try:
            line = input(Text.decorate('@','blue','reversevideo')+' ')
            if line in EXIT: break

            D = Language.lang(line,data(),data())
            D = EV(D)

            if not D.empty(): sys.stdout.write(str(D)+'\n')
        except KeyboardInterrupt:
            if KI: raise
            print('')
except EOFError:
    pass
