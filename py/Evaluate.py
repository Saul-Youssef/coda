
from base import *
import Number

DEFAULT = 100

def multi_split(n,B):
    Bs = [b for b in B]
    out = []
    T = []
    while not Bs==[]:
        T.append(Bs.pop(0))
        if len(T)>=n:
            out.append(data(*T))
            T = []
    if len(T)>0: out.append(data(*T))
    return out

MULTI_DEFAULT = 500
def EVAL(D): return CONTEXT.evaluate(MULTI_DEFAULT,D)

def multiEval(context,domain,A,B):
    if A.rigid(context) and B.atomic(context):
        nproc = 8
        n = len(B)//nproc
        Bs = multi_split(n,B)
        from multiprocessing.pool import Pool
        pool = Pool(nproc)
        results = []
        for result in pool.imap_unordered(EVAL,Bs):
            results.append(result)
        L = []
        for result in results:
            for c in result: L.append(c)
        return data(*L)
CONTEXT.define('multi',multiEval)
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
#   demo: eval : with (def first3 : {first 3:B}) : first3 : a b c d e f g
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
def eval_0(context,domain,A,B):
    if A.rigid(context) and B.atom(context):
        n = Number.intdef(DEFAULT,A); b = B[0]
        if not b.domain()==da('with'): return context.evaluate(n,B)
CONTEXT.define('eval1',eval_0,eval_with)
CONTEXT.define('with')
#
#     step evaluation step-by-step evaluation of it's input
#
#     demo: step 10 : nat : 0
#     demo: step : {first A : B} 2 : a b c d e
#
def stepEval(context,domain,A,B):
    if A.rigid(context):
        import Number
        depth = Number.intdef(DEFAULT,A)
        step = [B]
        B2 = context.evaluate(1,B)
        while not step[-1]==B2 and len(step)<=depth:
            step.append(B2)
            B2 = context.evaluate(1,B2)
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
