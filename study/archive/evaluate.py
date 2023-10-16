#
#    eval 100 : with (home:) : B
#
from base import *

def evaluate(context,D):
    if len(D)==1:
        c = D[0]; domain,A,B = c.triplet()
        if domain==da('with') and context.rigid(A) and context.joinable(A):
            return data((domain+A)|evaluate(context.join(A),B))
        if c in context:
            return context(c.left()|evaluate(context,c.right()))
        return data(evaluate(context,domain+A)|B)
    else:
        return data(*[evaluate(context,c) for d in D])

def def_0(context,domain,A,B):
    if len(A)==1 and context.rigid(A) and context.rigid(B):
        context.add(A[0],B); return data()
CONTEXT.define('def',def_0)

def eval_0(context,domain,A,B):
    if context.rigid(A):
        import Number
        n = Number.intdef(1,A)
        return eval_(n,context,B)
CONTEXT.define('eval',eval_0)

def eval_(n,context,D):
    D2 = evaluate(context,D)
    if n<=0 or D==D2: return D2
    else            : return eval_(n-1,context,D2)

def ap_0(context,domain,A,B):
    if B.empty(): return data()
def ap_1(context,domain,A,B):
    if context.atom(B): return data(A|B)
def ap_2(context,domain,A,B):
    BL,BR = B.split()
    if len(BL)>0: return ((domain+A)|BL) + ((domain+A)|BR)
CONTEXT.define('ap',ap_0,ap_1,ap_2)

def ap(context,domain,A,B):
    if len(B)==1:
        if context.atom(B): return data(A|B)
    else:
        return data(*[(domain+A)|data(b) for b in B])

class Context(object):
    def __init__(self): self._defs = {}
    def __iter__(self):
        for domain,defs in self._defs.items(): yield domain,defs
    def __repr__(self): return str(len(self._defs))

    def contains(self,A): return all(a in self._defs for a in A)
    def subcontext(self,A):
        context = Context()
        for a in A:
            if context._defs[a] = context.defs[a]
        return context

    def atomic(self,A): return any(a.domain() in self for a in A)
    def  rigid(self,A): return all(a.domain() in self for a in A)
    def   atom(self,A): return len(A)==1 and A[0] in self and len(self[A[0]])==0

    def __contains__(self,c): return self.domain(c) in self._defs
    def __getitem__ (self,c): return self._defs[c.domain()]
    def __call__(self,c):  # total function from coda to data
            for F in self[c]:
                domain,A,B = c.triplet()
                D = F(self,domain,A,B)
                if not D is None: return D
            return D

    def define(self,name,*Fs):
        domain = da(name)
        if domain in self._defs: raise error(name+' is already defined')
        self._defs[domain] = Fs
