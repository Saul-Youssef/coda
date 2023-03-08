#!/usr/bin/env python3
#
#   Coda Interpreter
#
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
import Text,Evaluate,Language

EXIT = ['exit','quit']
try:
    while True:
        try:
            line = input(Text.decorate('@','blue','reversevideo')+' ')
            if line in EXIT: break
            D = Evaluate.default(Language.lang(line,data(),data()))
            if not D.empty(): sys.stdout.write(str(D)+'\n')
        except KeyboardInterrupt:
            print('')
except EOFError:
    pass
