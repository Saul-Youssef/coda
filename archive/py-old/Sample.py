#
#    Generate spaces in various ways
#
from base import *
#from Space import Space
import Set
import Help

LANGFRAC = 0.01

numbers = [co(str(i)) for i in range(4)]
letters = [co('a'),co('b'),co('A'),co('B')]

excluded_modules = ['Text','Compile','Define','Evaluate','Help','Import','Variable',
                    'IO','Theorem','Language','Path','Sample','Generate','Set','Code']
excluded_strings = ['float','code_']

defines = []
for dom,de in CONTEXT:
    H = Help.Help(str(dom))
    if not H.module() in excluded_modules and len(dom)>0:
        if not any([ex in str(dom[0]) for ex in excluded_strings]):
            defines.append(dom[0])

langs = [co('{$}')]
#while len(langs)/len(defines) < LANGFRAC: langs.append(co('{$}'))

vars = [da(v)|data() for v in ['X','Y','Z','W']]

#vars = [da('?')|da('X'),da('?')|da('Y'),da('?')|da('Z'),da('?')|da('W')]

import random,itertools
codas = defines+numbers+letters+vars+vars+langs

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
    def set(self):
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
                    t = '{'+str(d)+'}'
                    p2 = self.replace(p,co(t))
                    pout.append(p2)
                    if ' ' in t:
                        p2 = self.replace(p,co(t.replace(' ',' : ')))
                        pout.append(p2)
        random.shuffle(pout)
        return Set.Set(*[data(*p) for p in pout])
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

def pure(width,depth): return Set.Set(*[d for d in alldata(width,depth)])

def evenAtoms(n):
    at = data()|data()
    atoms = [data()]
    while len(atoms)<n: atoms.append(atoms[-1]+data(at,at))
    return Set.Set(*atoms)
def oddAtoms(n):
    at = data()|data()
    atoms = [data(at)]
    while len(atoms)<n: atoms.append(atoms[-1]+data(at,at))
    return Set.Set(*atoms)
def Atoms(n):
    at = data()|data()
    atoms = [data()]
    while len(atoms)<n: atoms.append(atoms[-1]+data(at))
    print('aaaaaa',len(atoms))
    return data(*[data()|a for a in atoms])
#
#   Simple searching
#
#   If D=Domain(codas) with a specified list of codas
#
#   D.window(w,d) is defined to be the set of data with width<=w and depth<=d
#
#   Thus...
#
#   win(1,1) = () plus (c) for supplied codas c
#   win(w,d) = all pairs win(w-1,d) win(1,d)  if w>1 and d>1
#   win(w,d) = win(1,d-1) + all colons win(w,d-1):win(w,d-1) elif d>1
#
class Domain(object):
    def __init__(self,*codas):
        self._codas = codas
    def __repr__(self): return str(len(self._codas))
    def __iter__(self):
        for c in self._codas: yield c
    def window(self,width,depth):
        if width==1 and depth==1:
            return [data()]+[data(c) for c in self._codas]
        elif width>1:
            return self.concat(self.window(width-1,depth),self.window(1,depth))
        elif depth>1:
            return self.window(1,depth-1) + self.colon(self.window(width,depth-1),self.window(width,depth-1))
    def concat(self,As,Bs):
        S = []
        for A in As:
            for B in Bs: S.append(A+B)
        return S
    def colon(self,As,Bs):
        S = []
        for A in As:
            for B in Bs: S.append(data(A|B))
        return S
#
#   Get a sample of even and odd atoms.
#
#   demo: sample.even : 5
#   demo: sample.odd  : 5
#   demo: sample.atom : 5
#   demo: count : sample.atom : 10
#   demo: sample.pure : 2 2
#   demo: sample.data a : 5
#   demo: sample.data a b : 5
#   demo: sample.data <A> <B> <{$}> a : 3
#   demo: sample.data <A> <B> <{$}> (defs:Apply Basic Logic Number Sequence) : 2
#
def even_0(domain,A,B):
    if B.empty(): return data()
def even_1(domain,A,B):
    if B.invariant() and len(B)>0 and A.invariant():
        import Number
        ns = Number.ints(B)
        if len(ns)>0: return evenAtoms(ns[0]).bin()
CONTEXT.define('sample.even',even_0,even_1)
def odd_0(domain,A,B):
    if B.empty(): return data()
def odd_1(domain,A,B):
    if B.invariant() and len(B)>0 and A.invariant():
        import Number
        ns = Number.ints(B)
        if len(ns)>0: return oddAtoms(ns[0]).bin()
CONTEXT.define('sample.odd',odd_0,odd_1)
#def atom_0(domain,A,B):
#    if B.empty(): return data()
#def atom_1(domain,A,B):
#    if B.invariant() and len(B)>0 and A.invariant():
#        import Number
#        ns = Number.ints(B)
#        if len(ns)>0: return Atoms(ns[0])
#CONTEXT.define('sample.atom',odd_0,odd_1)

def purewindow_0(domain,A,B):
    if B.empty(): return data()
def purewindow_1(domain,A,B):
    if B.invariant() and len(B)>0 and A.invariant():
        import Number
        ns = Number.ints(B)
        if len(ns)==2:
            width,depth = ns[0],ns[1]
            return pure(width,depth).bin()
CONTEXT.define('sample.pure',purewindow_0,purewindow_1)

def samplewindow_0(domain,A,B):
    if B.empty(): return data()
def samplewindow_1(domain,A,B):
    if A.invariant() and B.invariant() and len(B)>0:
        import Number
        ns = Number.ints(B)
        if len(ns)==2:
            width,depth = ns[0],ns[1]
            return Set.Set(*Domain(*[a for a in A]).window(width,depth)).bin()
CONTEXT.define('sample.window',samplewindow_0,samplewindow_1)

def sampledata_0(domain,A,B):
    if B.empty(): return data()
def sampledata_1(domain,A,B):
    if A.eval()==A and B.rigid() and len(B)>0:
        import Number
        ns = Number.ints(B)
        n = 1
        if len(ns)>0: n = abs(ns[0])
        G = Gen([a for a in A],n)
        return G.set().bin()
CONTEXT.define('sample.data',sampledata_0,sampledata_1)
