#!/usr/bin/env python3
#
#   Data evaluator
#
#   Command line setup
#
import rlcompleter
import readline
readline.parse_and_bind("tab: complete")
#
#    System
#
import __init__
from base import *
import sys
sys.setrecursionlimit(10000)
import Evaluate,Text
#
#    Standard context
#
Evaluate.generic(data(colon(data(b'{coda:homecontext:}'),data())),1000)
Evaluate.generic(data(colon(data(b'{coda:startcontext:}'),data())),1000)
#
#    Interpreter loop
#
N = 100
EXIT = [b'exit',b'quit']
line = input(Text.decorate('@<- ','blue','bold')).encode()
D = data(colon(data(b'{'+line+b'}'),data()))
try:
    while True:
        try:
            if not D.empty(): sys.stdout.flush(); sys.stdout.write(str(D)+'\n')
            import Inspect
            stat = Inspect.statistic()
            stat = Inspect.update_stat(D,stat,0)
            stat.display()
            line = input(Text.decorate('@E ','blue','bold'))
            try:
                if line.strip()=='': line = '1'
                N = int(line)
                D2 = Evaluate.generic(D,N)
                if D==D2: sys.stdout.flush(); sys.stdout.write(str(D)+'\n')
                D = D2
            except ValueError:
                if line.startswith('<-'):
                    line = line.encode()
                    D = data(colon(data(b'{'+line[2:]+b'}'),data()))
                else:
                    D = data(colon(data(b'{'+line.encode()+b'}'),D))
        except KeyboardInterrupt:
            print('')
except EOFError:
    pass
