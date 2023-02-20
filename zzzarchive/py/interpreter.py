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

EXIT = [b'exit',b'quit']
try:
    while True:
        try:
            line = input(Text.decorate('@','blue','reversevideo')+' ').encode()
            if line in EXIT: break
            D = data(colon(data(b'{'+line+b'}'),data()))
#            D = Evaluate.generic(D,N)
            D,n = Evaluate.depth(D,N)
            if not D.empty(): sys.stdout.write(str(D)+'\n')
#            if not D.empty(): sys.stdout.write(str(D)+'............['+str(N-n)+']\n')
        except KeyboardInterrupt:
            print('')
except EOFError:
    pass
