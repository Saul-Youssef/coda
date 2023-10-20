
from base import *
import Number

DEFAULT = 100

#def intdef(ndef,A):
#    n = ndef
#    try: n = int(str(A))
#    except: pass
#    return n
#
#def evaluate_data(context,D):
#    L = []
#    for d in D:
#        for c in evaluate_coda(context,d): L.append(c)
#    return data(*L)
#
#def evaluate_coda(context,c):
#    if c in context: return context(evaluate_data(context,c.left())|evaluate_data(context,c.right()))
#    else           : return data(evaluate_data(context,c.left())|c.right())
#
#def evaluate(n,context,D):
#    D2 = evaluate_data(context,D)
#    if n<=0 or D==D2: return D2
#    else            : return evaluate(n-1,context,D2)

#
#   evaluation of data and new contexts with 'with'
#
#   eval : evaluates to specified depth
#   use  : uses input definitions in the current context
#   with : create a new 'scope' including argument specified definitions
#
#   demo: eval : a b c
#   demo: eval :
#   demo: eval : with (let x:5) (let y:6) : int_sum : x? y?
#   demo: x? y?
#   demo: eval : eval : with (def first3 : {first 3:B}) : first3 : a b c d e f g
#   demo: get with : eval : with (def first3 : {first 3:B}) : first3 : a b c d e f g
#   demo: first3 : a b c d e f g
#   demo: eval : with (let x:a) (let y:b) : (x? y?) = (y? x?)
#   demo: eval 100 : with (let x:a) (let y:a) : (x? y?) = (y? x?)
#
def eval_with(context,domain,A,B):
    if A.rigid(context) and B.atom(context):
        b = B[0]
        if b.domain()==da('with') and b.arg().rigid(context):
            defs  = [c for c in b.arg() if c.domain()==da('def')]
            uses  = [da('use1')|data(de) for de in defs]
            new = context.copy()
            D = new.evaluate(DEFAULT,data(*uses))
            if D.empty(): # evaluate right side of with in new context.
                n = Number.intdef(DEFAULT,A)
                return data((b.domain()+b.arg())|new.evaluate(n,b.right()))
#                return data((b.domain()+b.arg())|evaluate(n,new,b.right()))
def eval_0(context,domain,A,B):
    if A.rigid(context) and B.atom(context):
        n = Number.intdef(DEFAULT,A); b = B[0]
        if not b.domain()==da('with'): return context.evaluate(n,B)
#        if not b.domain()==da('with'): return evaluate(n,context,B)
CONTEXT.define('eval1',eval_0,eval_with)
CONTEXT.define('with')
#
#     step evaluation step-by-step evaluation of it's input
#
#     demo: step 10 : nat : 0
#     demo: step 100 : sum n : 1 1
#
def stepEval(context,domain,A,B):
#    if A.atom() or A.empty():
    if A.rigid(context):
        import Number
        ns = Number.ints(A)
        if len(ns)==1 and ns[0]>=0: depth = ns[0]
        else                      : depth = DEPTH
        step = [B]
#        B2 = B.eval()
        B2 = context.edata(B)
        while not step[-1]==B2 and len(step)<=depth:
            step.append(B2)
#            B2 = B2.eval()
            B2 = context.edata(B)
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
