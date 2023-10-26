
from base import *
import Number

DEFAULT = 100

def _split(n,B):
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

def EVAL(D): return CONTEXT.evaluate(100,D)
def APP_100  (D): return CONTEXT.evaluate(  100,D)
def APP_500  (D): return CONTEXT.evaluate(  500,D)
def APP_1000 (D): return CONTEXT.evaluate( 1000,D)
def APP_5000 (D): return CONTEXT.evaluate( 5000,D)
def APP_10000(D): return CONTEXT.evaluate(10000,D)

def multiarg(A):
    args = []
    n = 500
    for a in A:
        try:
            n = int(str(a))
        except ValueError:
            args.append(a)
    return n,data(*args)

def multi(context,domain,A,B):
    if A.atomic(context) and B.atomic(context):
        import multiprocessing
        nproc = min(len(B),multiprocessing.cpu_count()-4)
        n = len(B)//nproc
        depth,ARG = multiarg(A)

        B2 = data(*[ARG|data(b) for b in B])
        Bsplit = _split(n,B2)

        from multiprocessing.pool import Pool
        pool = Pool(len(Bsplit))

        ap = APP_500
        if depth>500: ap = APP_1000
        if depth>1000: ap = APP_5000
        if depth>5000: ap = APP_10000

        results = []
        for result in pool.imap_unordered(ap,Bsplit): results.append(result)
        def f(s,t): return s+t
        from functools import reduce
        return reduce(f,results)
CONTEXT.define('multi',multi)

#def multiEval(context,domain,A,B):
##    if A.rigid(context) and B.atomic(context):
#    if A.rigid(context):
#        import multiprocessing
#        nproc = max(1,multiprocessing.cpu_count()-4)
#        nproc = Number.intdef(nproc,A)
#        Bs = context.atom_data(nproc,B)
#        n = len(Bs)//nproc
#        Bsplit = _split(n,B)
#
#        from multiprocessing.pool import Pool
##        pool = Pool(nproc)
#        pool = Pool(len(Bsplit))
#        results = []
#        for result in pool.imap_unordered(EVAL,Bsplit): results.append(result)
#        def f(s,t): return s+t
#        from functools import reduce
#        return reduce(f,results)
#CONTEXT.define('multi',multiEval)
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

def atoms(context,domain,A,B):
    if A.rigid(context):
        import Number
        n = Number.intdef(DEFAULT,A)
        return context.atom_data(n,B)
CONTEXT.define('atoms',atoms)
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
