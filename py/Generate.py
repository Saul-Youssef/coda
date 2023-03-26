#
#    Generate spaces in various ways
#
from base import *
from Space import Space
import Help

LANGFRAC = 0.01

numbers = [co(str(i)) for i in range(4)]
letters = [co('a'),co('b'),co('A'),co('B')]

excluded_modules = ['Text','Compile','Define','Evaluate','Help','Import',
                    'IO','Language','Path','Space','Number']

defines = []
for dom,de in CONTEXT:
    H = Help.Help(str(dom))
    if not H.module() in excluded_modules and len(dom)>0: defines.append(dom[0])

langs = [co('{$}')]
#while len(langs)/len(defines) < LANGFRAC: langs.append(co('{$}'))

import random,itertools
codas = defines+numbers+letters+langs

class Gen(object):
    def __init__(self,codas,width):
        self._codas = codas
        self._width = width
        self._space0 = []
        for i in [1,2]:
            for p in itertools.permutations(self._codas,i):
                if any([pp==co('B') for pp in p]) and not any([pp==co('{$}') for pp in p]): self._space0.append(data(*p))
    def __len__(self):
        return len(self._space0)
    def space(self):
        ps = []
        for i in range(self._width):
            for p in itertools.product(self._codas,repeat=i):
                if self.nlang(p)<=1: ps.append(p)

        pout = []
        for p in ps:
            if self.nlang(p)==0:
                pout.append(p)
            elif self.nlang(p)==1:
                for d in self._space0:
                    p2 = self.replace(p,co('{'+str(d)+'}'))
                    pout.append(p2)
        random.shuffle(pout)
        return Space(*[data(*p) for p in pout])
    def nlang(self,p):
        n = 0
        for pp in p:
            if pp==co('{$}'): n += 1
        return n
    def replace(self,p,c):
        p2 = []
        for pp in p:
            if pp==co('{$}'): p2.append(c)
            else: p2.append(pp)
        return p2

def alldata(width,depth):  # all data leq specified width and depth
    datas = []
    if depth==0:
        datas.append(data())
    else:
        codas = [c for c in allcoda(width,depth)]
        for w in range(0,width+1):
            for T in itertools.product(codas,repeat=w): datas.append(data(*T))
    return datas

def allcoda(width,depth):
    codas = []
    if depth==0:
        return (coda(data(),data()),)
    else:
        datas = [d for d in alldata(width,depth-1)]
        for T in itertools.product(datas,repeat=2): codas.append(coda(T[0],T[1]))
    return codas

def Window(width,depth):
    return Space(*[d for d in alldata(width,depth)])

def EvenAtoms(n):
    at = data()|data()
    atoms = [data()]
    while len(atoms)<n: atoms.append(atoms[-1]+data(at,at))
    return Space(*atoms)
def OddAtoms(n):
    at = data()|data()
    atoms = [data(at)]
    while len(atoms)<n: atoms.append(atoms[-1]+data(at,at))
    return Space(*atoms)
