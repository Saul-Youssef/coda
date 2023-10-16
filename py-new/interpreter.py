#!/usr/bin/env python3
#
#   Coda Interpreter
#
#   Command line setup
#
import rlcompleter
import readline
readline.parse_and_bind("tab: complete")
#
#    System
#
from start import *
import Text,Language

EXIT = ['exit','quit']
UNICODE.setatoms('(:)','0','1') # non-unicode for CLI 
try:
    while True:
        try:
            line = input(Text.decorate('@','blue','reversevideo')+' ')
            if line in EXIT: break

            D = Language.lang(line,data(),data())
            D = Evaluate.evaluate(100,CONTEXT,D)

            if not D.empty(): sys.stdout.write(str(D)+'\n')
        except KeyboardInterrupt:
            print('')
except EOFError:
    pass
