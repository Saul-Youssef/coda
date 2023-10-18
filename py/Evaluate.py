
from base import *
import Number

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
    if c in context: return context(evaluate_data(context,c.left())|evaluate_data(context,c.right()))
    else           : return data(evaluate_data(context,c.left())|c.right())

def evaluate(n,context,D):
    D2 = evaluate_data(context,D)
    if n<=0 or D==D2: return D2
    else            : return evaluate(n-1,context,D2)
#
#   evaluation of data and new contexts with 'with'
#
#   eval : evaluates to specified depth
#   use  : uses input definitions in the current context
#   with : create a new 'scope' including argument specified definitions
#
#   demo: eval 100 : {a b c}:
#   demo: eval : {a b c}:
#   demo: eval 10 : with : nat : 0
#   demo: eval 10 : with (let x:5) : x?
#   demo: x?
#   demo: get with : eval 100 : with (let x:5) (let y:6) : int_sum : x? y?
#   demo: x? y?
#   demo: use : (let x:5) (let y:6)
#   demo: int_sum : x? y?
#   demo: x? y?
#   demo: first3 : a b c d 
#
def eval_with(context,domain,A,B):
    if A.atom(context) and B.atom(context):
        n = Number.intdef(1,A); b = B[0]
        if b.domain()==da('with') and b.arg().rigid(context):
            defs  = [c for c in b.arg() if c.domain()==da('def')]
            uses  = [da('use1')|data(de) for de in defs]
            new = context.copy()
            D = evaluate(100,new,data(*uses))
            if D.empty():
                n = Number.intdef(1,A)
                return data((b.domain()+b.arg())|evaluate(n,new,b.right()))
def eval_0(context,domain,A,B):
    if A.rigid(context) and B.atom(context):
        n = Number.intdef(1,A); b = B[0]
        if not b.domain()==da('with'): return evaluate(n,context,B)
CONTEXT.define('eval1',eval_0,eval_with)
CONTEXT.define('with')
