
from base import *
import Number
import time
from Log import LOG

LOG.register('step','Evaluation step')

#DEFAULT = 20
STEPS = 100
#EVALS = 10000000
SECONDS = 36000
#
#    Evaluation of data to a maximum of steps and evals in the supplied context
#
class Eval(object):
    def __init__(self,steps,seconds,context):
        self.max_steps = steps
        self.steps     = 0
        self.max_seconds = seconds
        self.seconds   = 0.0
        self.context = context
        self._cache = {}
        self.cache_on = True
    def __call__(self,D):
        if not self.cache_on: return self.evaluate(D)
        if D in self._cache: return self._cache[D]
        D2 = self.evaluate(D)
        return D2
    def evaluate(self,D):
        self.steps   = self.max_steps
        self.seconds = self.max_seconds
        Done = [] # stable leading data does not need evaluation
        Ds = [d for d in D]
        while self.steps>0 and self.seconds>0:
            self.steps -= 1
            while len(Ds)>0 and Ds[0].stable(self.context): Done.append(Ds.pop(0))
            D1 = data(*Ds)
            t = time.time()
            D2 = self.step(D1)
            self.seconds -= time.time()-t
            if D1==D2: break
            Ds = [d for d in D2]
        if LOG.logging('step'):
            LOG('step','saturated: '+str(D1==D2),
                'steps used: '+str(self.max_steps-self.steps)+'/'+str(self.max_steps),
                'time used: '+'{:.3f}'.format(self.max_seconds-self.seconds)+'/'+'{:.3f}'.format(self.max_seconds),
                'context: '+str(len(self.context)),
                'cache: '+str(len(self._cache)))
        return data(*(Done+Ds))
    def step(self,D):
        Ds = []
        for d in D:
            if d.domain()==da('with'):
                Ds.append(self.evaluate(d.left())|d.right())
            elif d in self.context:
                R = self.context(d)
                if R==data(d):
                    Ds.append(self.step(d.left())|self.step(d.right()))
                else:
                    for r in R: Ds.append(r)
            else:
                Ds.append(self.step(d.left())|self.step(d.right()))
        return data(*Ds)

def MULTI(W):
    context,A,D = W
    MD = data((da('eval')+A)|D)
    EV = Eval(STEPS,SECONDS,context)
    return EV(MD)

def Multi(context,domain,A,B):
    if A.rigid(context) and B.atomic(context) and all(b.domain()==da('with') for b in B):
        import multiprocessing
        nproc = min(len(B)+1,multiprocessing.cpu_count()-4) # always leave at least 4 procs for other tasks

        from multiprocessing.pool import Pool
        pool = Pool(nproc)
        IN = []
        for b in B: IN.append((context,A,data(b),))
        results = []
        for result in pool.imap(MULTI,IN): results.append(result)
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
        ns = Number.floats(A)
        steps,seconds = STEPS,SECONDS
        if len(ns)>0: steps   = ns.pop(0).__floor__()
        if len(ns)>0: seconds = ns.pop(0)

        if b.domain()==da('with'):
            ARGS = Eval(STEPS,SECONDS,context)(b.arg())
            args = [da('use1')|data(arg) for arg in ARGS if arg.domain()==da('def')]
            new = context.copy()
            DA = Eval(STEPS,SECONDS,new)(data(*args))
            if DA.empty():
                R = Eval(steps,seconds,new)(b.right())
                return data((b.domain()+ARGS)|R)
        else:
            return Eval(steps,seconds,context)(B)
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
        ns = Number.ints(A)
        if len(ns)>0: steps = ns.pop(0)

        E = Eval(STEPS,SECONDS,context)
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
