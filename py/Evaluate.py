
from base import *
import Number

DEFAULT = 20
STEPS = 100
EVALS = 10000000
#
#    Evaluation of data to a maximum of steps and evals in the supplied context
#
class Eval(object):
    def __init__(self,steps,evals,context):
        self.max_steps = steps
        self.max_evals = evals
        self.context = context
        self._cache = {}
    def evaluate(self,D): return self(D)
    def __call__(self,D):
        if D in self._cache: return self._cache[D]
        D2 = self.evaluate(D)
        if D2.defined(self.context): self._cache[D] = D2
        return D2
    def evaluate(self,D):
        self.steps = self.max_steps
        self.evals = self.max_evals
        Done = [] # stable leading data does not need evaluation
        Ds = [d for d in D]
        while self.steps>0:
            self.steps -= 1
            while len(Ds)>0 and Ds[0].stable(self.context): Done.append(Ds.pop(0))
            D1 = data(*Ds)
            D2 = self.step(D1)
            if D1==D2: break
            Ds = [d for d in D2]
        return data(*(Done+Ds))
    def step(self,D):
        Ds = []
        for d in D:
            if d.domain()==da('with'):
                Ds.append(self.evaluate(d.left())|d.right())
            elif d in self.context and self.evals>0:
                self.evals -= 1
                R = self.context(d)
                if R==data(d):
                    Ds.append(self.step(d.left())|self.step(d.right()))
                else:
                    for r in R: Ds.append(r)
            else:
                Ds.append(self.step(d.left())|self.step(d.right()))
        return data(*Ds)

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

#def EVAL(D): return CONTEXT.evaluate(100,D)
#def APP_100  (D): return CONTEXT.evaluate(  100,D)
#def APP_500  (D): return CONTEXT.evaluate(  500,D)
#def APP_1000 (D): return CONTEXT.evaluate( 1000,D)
#def APP_5000 (D): return CONTEXT.evaluate( 5000,D)
#def APP_10000(D): return CONTEXT.evaluate(10000,D)
#
#def multiarg(A):
#    args = [a for a in A]
#    n = 500
#    if len(args)>0:
#        try:
#            n = int(str(args[0]))
#            args.pop(0)
#        except ValueError:
#            pass
#    return n,data(*args)
#
#   map A : B is the same as ap A : B except
#     1. Each application is done in a separate process for speed.
#     2. If the first atom in A is an integer, it is interpreted
#     3. As the maximum depth of the application.
#
#   demo: map {int_sum:first 500:get:B} : (:nat:0) (:nat:0) (:nat:0)
#   demo: map 1000 {int_sum:first 500:get:B} : (:nat:0) (:nat:0) (:nat:0)
#   demo: ap pause 10 : 0 1 2 3 4 5 6 7 8 9
#   demo: map pause 11 : 0 1 2 3 4 5 6 7 8 9
#
#def Map(context,domain,A,B):
#    if A.atomic(context) and B.atomic(context):
#        import multiprocessing
#        nproc = min(len(B),multiprocessing.cpu_count()-4)
#        n = len(B)//nproc
#        depth,ARG = multiarg(A)
#
#        B2 = data(*[ARG|data(b) for b in B])
#        Bsplit = _split(n,B2)
#
#        from multiprocessing.pool import Pool
#        pool = Pool(len(Bsplit))
#
#        ap = APP_500
#        if depth> 500: ap = APP_1000
#        if depth>1000: ap = APP_5000
#        if depth>5000: ap = APP_10000
#
#        results = []
#        for result in pool.imap_unordered(ap,Bsplit): results.append(result)
#        def f(s,t): return s+t
#        from functools import reduce
#        return reduce(f,results)
#CONTEXT.define('map',Map)
#
#def Evaluate(context,n,D): return context.evaluate(500,D)
#

def MULTI_TEST(P):
    context = P[0]
    D = P[1]
    return context.evaluate(500,D)
#    context = CONTEXT.copy()
#    return context.evaluate(500,D)
#    return D
#    E = context.__getattribute__('evaluate')
#    return E(500,D)
#    return context.copy().evaluate(500,D)
#return Evaluate(P[0],500,P[1])
#    return P[0].evaluate(500,P[1])
#    return CONTEXT.copy().evaluate(500,D)

def Multi(context,domain,A,B):
    if A.rigid(context) and B.atomic(context):
        import multiprocessing
        nproc = min(len(B)+1,multiprocessing.cpu_count()-4)
        n = len(B)//nproc

#        B2 = [(CONTEXT.copy(),data(b)) for b in B]

#        B2 = data(*[(da('eval')+A)|data(b) for b in B])
        Bsplit = _split(n,B)
        Bs2 = [[CONTEXT.copy(),D] for D in Bsplit]

        from multiprocessing.pool import Pool
        pool = Pool(nproc)
        results = []
        for result in pool.imap_unordered(MULTI_TEST,Bs2): results.append(result)
        def f(s,t): return s+t
        from functools import reduce
        return reduce(f,results)
CONTEXT.define('multi',Multi)
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
#   demo: nat : 0
#   demo: with : nat : 0
#   demo: eval 10 : with : nat : 0
#   demo: eval 100 : with : nat : 0
#
def eval_(context,domain,A,B):
    if B.empty():
        return data()
    elif A.rigid(context) and B.atom(context):
        b = B[0]
        ns = Number.ints(A)
        steps,evals = STEPS,EVALS
        if len(ns)>0: steps = ns.pop(0)
        if len(ns)>0: evals = ns.pop(0)

        if b.domain()==da('with'):
            ARGS = Eval(STEPS,EVALS,context)(b.arg())
            args = [da('use1')|data(arg) for arg in ARGS if arg.domain()==da('def')]
            new = context.copy()
            DA = Eval(STEPS,EVALS,new)(data(*args))
            if DA.empty():
                R = Eval(steps,evals,new)(b.right())
                return data((b.domain()+ARGS)|R)
        else:
            return Eval(n,EVALS,context)(B)
CONTEXT.define('eval1',eval_)
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
        steps = STEPS
        evals = EVALS
        ns = Number.ints(A)
        if len(ns)>0: steps = ns.pop(0)
        if len(ns)>0: evals = ns.pop(0)

        E = Eval(2*steps,evals,context)
        B2 = B
        outs = []
        n = 0
        while steps>0:
            s = str(B2)
            outs.append('['+str(n)+'] '+s); n += 1
            Bnew = E.step(B2)
            if B2==Bnew: break
            B2 = Bnew
            steps -= 1
        return da('\n'.join(outs))
def stepEval_0(context,domain,A,B):
    if B.empty(): return data()
CONTEXT.define('step',stepEval,stepEval_0)
