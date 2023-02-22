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
import Text,Evaluate,Language,Code

DEPTH = 100 # maximum evaluation depth
EXIT = ['exit','quit']
try:
    while True:
        try:
            line = input(Text.decorate('@','blue','reversevideo')+' ')
            if line in EXIT: break
            D,depth = Evaluate.depth(Language.lang(line,data(),data()),DEPTH)
            if not D.empty(): sys.stdout.write(Code.pretty(D)+'\n')
        except KeyboardInterrupt:
            print('')
except EOFError:
    pass
