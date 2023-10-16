
from base import *

def intdef(ndef,A):
    n = ndef
    try: n = int(str(A))
    except: pass
    return n

def evaluate_data(context,D):
    L = []
    for d in D:
        for c in evaluate_coda(context,d): L.append(c)
    return data(*L)

def evaluate_coda(context,c):
    if c in context: return context(c.left()|evaluate_data(context,c.right()))
    else           : return data(evaluate(context,c.left())|B)

def evaluate(n,context,D):
    D2 = evaluate_data(context,D)
    if n<=0 or D==D2: return D2
    else            : return evaluate(n-1,context,D2)
#
#   evaluate data
#
#   demo: eval 100 : {a b c}:
#   demo: eval : {a b c}:
#   demo: eval 100 : with : nat : 0
#   demo: eval 100 : with (Let x:5) : x?
#   demo: x?
#
def eval_with(context,domain,A,B):
    if context.atom(A) and context.atom(B):
        n = intdef(A); b = B[0]
        if b.domain()==da('with') and context.rigid(b.arg()) and context.joinable(b.arg()):
            new = context.join(b.arg())
            return data((b.domain()+b.arg())|evaluate(n,new,b.right()))
def eval_0(context,domain,A,B):
    if context.rigid(A) and context.atom(B):
        n = intdef(A); b = B[0]
        if not b.domain()==da('with'): return evaluate(n,context,B)
CONTEXT.define('eval',eval_0,eval_with)
CONTEXT.define('with')
