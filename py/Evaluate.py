
from base import *

def langstep(A):
    result = []
    for a in A:
        if a.domain()==da('language'):
            for aa in a.eval(): result.append(aa)
        else:
            result.append(langstep(a.left())|langstep(a.right()))
    return data(*result)
def langeval(A,n=100):
    import Language
    ntry = 0
    while Language.hasLanguage(A) and ntry<n:
        ntry += 1
        A = langstep(A)
    return A,ntry 
#
#   Simple evaluation recursively using
#   definitions to a specified depth,
#   quitting if there is no progress.
#
def depth(D,n):
    if n<=0:
        return D,n
    else:
        D2 = D.eval()
        if D==D2: return D2,n
        return depth(D2,n-1)
#
#   Resolve is the same as depth
#   but returns None if the input
#   data has not converged.
#
def resolve(D,n):
    D2,n = depth(D,n)
    if n>0: return D2

DEPTH = 100

def default(D): return depth(D,DEPTH)[0]
#
#    Show and set the default evaluation depth
#
#    demo: getDefaultDepth :
#    demo: nat : 0
#    demo: setDefaultDepth : 20
#    demo: getDefaultDepth :
#    demo: nat : 0
#
def setDefaultDepth(domain,A,B):
    if B.atom():
        import Number
        global DEPTH
        ns = Number.ints(B)
        if len(ns)==1 and ns[0]>=0: DEPTH = ns[0]
        return da(str(DEPTH))
    elif B.empty():
        return data()
CONTEXT.define('setDefaultDepth',setDefaultDepth)
CONTEXT.define('getDefaultDepth',lambda domain,A,B: da(str(DEPTH)))
#
#     step displays step-by-step evaluation of it's input
#
#     demo: step 10 : nat : 0
#     demo: step 100 : sum n : 1 1
#
def stepEval(domain,A,B):
    if A.atom() or A.empty():
        import Number
        ns = Number.ints(A)
        if len(ns)==1 and ns[0]>=0: depth = ns[0]
        else                      : depth = DEPTH
        step = [B]
        B2 = B.eval()
        while not step[-1]==B2 and len(step)<=depth:
            step.append(B2)
            B2 = B2.eval()
        outs = []
        n = 0
        width = len(str(len(step)))
        for s in step:
            num = str(n)
            while len(num)<width: num = ' '+num
            outs.append('['+num+']'+' '+str(s)); n += 1
        return da('\n'.join(outs))
def stepEval_0(domain,A,B):
    if B.empty(): return data()
CONTEXT.define('step',stepEval,stepEval_0)
#
#     evaluate an argument specified number of times
#
def eval(domain,A,B):
    if A.atom() or A.empty():
        import Number
        ns = Number.ints(A)
        n = 1
        if len(ns)==1: n = ns[0]
        return depth(B,n)[0]
CONTEXT.define('eval',eval)
