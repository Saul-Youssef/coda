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
if not D.empty(): raise error('Local definition error '+str(D))

KI = False
if len(sys.argv)>1:
    if sys.argv[1]=='-': KI = True
    try:
        n = int(sys.argv[1])
        if n>1: Evaluate.DEFAULT = n
    except ValueError:
        pass

try:
    CONTEXT = CONTEXT.xeval(da('with'))
    while True:
        try:
            line = input(Text.decorate('@','blue','reversevideo')+' ')
            if line in EXIT: break

#            D = Language.lang('eval:'+line,data(),data())
            D = Language.lang(line,data(),data())
            D = CONTEXT.evaluate(100,D)
#            D = CONTEXT.xeval(da('with')).evaluate(100,D)

            if not D.empty(): sys.stdout.write(str(D)+'\n')
        except KeyboardInterrupt:
            if KI: raise
            print('')
except EOFError:
    pass
