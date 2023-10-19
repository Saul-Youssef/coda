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
D = CONTEXT.evaluate(100,Language.lang('ap use1 : localdef:',data(),data()))
#D = Evaluate.evaluate(100,CONTEXT,Language.lang('ap use1 : localdef:',data(),data()))
if not D.empty(): raise error('Local definition error '+str(D))

try:
    while True:
        try:
            line = input(Text.decorate('@','blue','reversevideo')+' ')
            if line in EXIT: break

            D = Language.lang(line,data(),data())
            D = CONTEXT.evaluate(100,D)
#            D = Evaluate.evaluate(100,CONTEXT,D)

            if not D.empty(): sys.stdout.write(str(D)+'\n')
        except KeyboardInterrupt:
            raise
            print('')
except EOFError:
    pass
