
#
#   remember use : def might happen during execution
#
from base import *
import Number
import time
from Log import LOG

SECONDS = 2.0
MEMORY  = 5.0 # GB
MULTI_SECONDS = 1000.0
MULTI_MEMORY = 2.0

LOG.register('cache.miss','Cache miss')
LOG.register('cache.hit','Cache hit')
LOG.register('cache','New cach creation')
LOG.register('cache','Reset cache')

LOG.register('multi','Multiprocessing operations')

LOG.register('eval','Default time and memory')
LOG.register('eval.step','Evaluation step')

CONTEXT.define('defaultTime')
CONTEXT.define('cache.reset')
CONTEXT.define('cache.clear')

class Cache(object):
    def __init__(self):
        LOG('cache','Create new cache')
        self._cache = {}
        self._done = set([])  # done data
    def __repr__(self): return str(len(self))+'/'+str(len(self._done))
    def __len__(self): return len(self._cache)
    def reset(self,context):
        LOG('cache','before cache reset: '+str(len(self._cache)))
        keys = [key for key in self._cache.keys()]
        for key in keys:
            if not self._cache[key].rigid(context): del self._cache[key]
        self._done = set([])
        LOG('cache','after cache reset: '+str(len(self._cache)))
        return self
    def clear(self):
        self._cache = {}
        self._done = set([])
        return self
    def set(self,c,D):
        if LOG.logging('cache.miss'): LOG('cache.miss',str(c),'->',str(D),str(len(self)))
        self._cache[c] = D
        return self
    def setdone(self,D): self._done.add(D); return self
    def done(self,D): return D in self._done
    def __contains__(self,c): return c in self._cache
    def __call__(self,c):
        if LOG.logging('cache.hit'): LOG('cache.hit',str(c),'->',str(self._cache[c]))
        return self._cache[c]

class Evaluate(object):
    def __init__(self,context,seconds,GB):
        self.context   = context
        self.seconds   = seconds
        self.bytes     = GB*1000000000
        self.max_time  = None
        self.max_bytes = None
        self.step = 0
        import psutil
        self.process = psutil.Process()
        self.cache = Cache()
        LOG('eval','creation','max seconds:'+str(seconds),'max GB:'+str(GB))
    def settings(self,D):
        for d in D:
            if d.domain()==da('defaultTime'):
                fs = Number.floats(d.right())
                if len(fs)==1: self.setTimeLimit(fs[0])
            if d.domain()==da('cache.reset'):
                self.cache.reset(self.context)
            if d.domain()==da('cache.clear'):
                self.cache.clear()
        return self
    def setTimeLimit(self,tlimit):
        self.seconds = tlimit
        return self
    def __call__(self,D):  # saturate definitions if necessary
        self.max_time  = time.time()+self.seconds
        self.max_bytes = self.bytes
        self.step = 0
        ndefinitions = len(self.context)

        D2 = data(*[d for d in D])
        while True:
            D2 = self.evaluate(D2)
            if not self.time() or not self.memory(): break
            if ndefinitions==len(self.context):
                break
            else:
                ndefinitions = len(self.context)
                self.cache.reset(self.context)
        self.log()
        return D2
    def evaluate(self,D):
        DE = data_evaluator(self.context,self.cache,D)
        while not DE.done() and self.time() and self.memory():
            DE.step()
            self.step += 1
        return DE.value()
    def time(self): return time.time()<self.max_time
    def memory(self):
        return True
        return self.rss()<self.max_bytes
    def rss(self): return self.process.memory_info().rss
    def log(self):
        if LOG.logging('eval.step'):
            LOG('eval.step','step '+str(self.step),
                'time:'+'{:.2f}'.format(self.seconds - (self.max_time-time.time()))+'/'+
                         '{:.2f}'.format(self.seconds),
                'GB:'+'{:.2f}'.format(float(self.rss())/1000000000)+'/'+
                        '{:.2f}'.format(float(self.max_bytes)/1000000000),
                'context:'+str(len(self.context)),
                'cache:'+str(self.cache))

def pr(L): return '['+','.join([str(l.value()) for l in L])+']'

class data_evaluator(object):
    def __init__(self,context,cache,D):
        self.cache = cache
        if cache.done(D):
            if LOG.logging('cache.hit'): LOG('cache.hit','data',str(D))
            self._obj = data_done(D)
        else:
            if LOG.logging('cache.miss'): LOG('cache.miss','data',str(D))
            self._obj = data_evaluator_(context,cache,D)
    def step(self):
        self._obj.step()
        return self
    def done(self): return self._obj.done()
    def value(self): return self._obj.value()

class data_evaluator_(object):
    def __init__(self,context,cache,D):
        self.cache = cache
        self._work = [coda_evaluator(context,cache,d) for d in D]
        self._done = []
        while len(self._work)>0 and self._work[0].done(): self._done.append(self._work.pop(0))
    def step(self):
        self._work = [d.step() for d in self._work]
        while len(self._work)>0 and self._work[0].done(): self._done.append(self._work.pop(0))
        return self
    def done(self): return self._work==[]
    def value(self):
        L = []
        for d in self._done+self._work:
            for dd in d.value(): L.append(dd)
        D = data(*L)
        if self._work==[]: self.cache.setdone(D)
        return D

class data_done(object):
    def __init__(self,D): self._data = D
    def step(self): return self
    def done(self): return True
    def value(self): return self._data

class coda_evaluator(object):
    def __init__(self,context,cache,c):
        self.context   = context
        self.cache     = cache
        if c in cache:
            self.cached    = True
            self.data      = cache(c)
            if LOG.logging('cache.hit'): LOG('cache.hit','coda',str(c))
        else:
            self.cached    = False
            self.origin    = c
            self.left      = data_evaluator(context,cache,c.left())
            self.right     = data_evaluator(context,cache,c.right())
            self.data_eval = None
            self.data      = None
            if LOG.logging('cache.miss'): LOG('cache.miss','coda',str(c))
    def done(self): return not self.data is None
    def step(self):
        if self.done():
            pass
        elif self.data_eval is None:
            self.step_coda()
        else:
            self.data_eval.step()
            if self.data_eval.done(): self.data = self.data_eval.value()
        return self
    def step_coda(self):
        c = self.left.step().value()|self.right.value()
        D = self.context(c)
        if data(c)==D:
            if self.left.done() and self.right.done():
                self.data = D
            elif c.domain()==da('with'):
                self.left.step()
                if self.left.done():
                    self.data = data(self.left.value()|self.right.value())
            else:
                self.left.step()
                self.right.step()
        else:
            if    len(D)==0:
                self.data = D
            elif  len(D) >1:
                self.data_eval = data_evaluator(self.context,self.cache,D)
            else:
                self.left  = data_evaluator(self.context,self.cache,D[0].left ())
                self.right = data_evaluator(self.context,self.cache,D[0].right())
        return self
    def value(self):
        if self.data is None:
            if self.data_eval is None:
                return data(self.left.value()|self.right.value())
            else:
                return self.data_eval.value()
        if not self.cached: self.cache.set(self.origin,self.data)
        return self.data

def MULTI(W):
    context,A,D = W
    MD = data((da('do')+A)|D)
    EV = Evaluate(context,MULTI_SECONDS,available_GB()/4.0)
    return EV(MD)

def limits(A):
    import Number
    seconds,GB = SECONDS,available_GB()/4.0
    fs = Number.floats(A)
    if len(fs)>0: seconds = fs.pop(0)
    if len(fs)>0: memory  = fs.pop(0)
    return seconds,GB

def Multi(context,domain,A,B):
    if A.rigid(context) and B.atomic(context) and all(b.domain()==da('with') for b in B):
        import multiprocessing
        nproc = min(len(B)+1,multiprocessing.cpu_count()-4) # always leave at least 4 procs for other tasks
        LOG('multi','Using '+str(nproc)+' processors for '+str(len(B))+' inputs')

        from multiprocessing.pool import Pool
        pool = Pool(nproc)
        IN = []
        for b in B: IN.append((context,A,data(b),))
        results = []
        for result in pool.imap(MULTI,IN): results.append(result)
        def f(s,t): return s+t
        from functools import reduce
        LOG('multi','Collecting results')
        return reduce(f,results)
CONTEXT.define('multi',Multi)
CONTEXT.define('domulti',Multi)
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
def available_GB():
    import psutil
    mem = psutil.virtual_memory().available
    return mem/1000000000.0

def eval_(context,domain,A,B):
    if B.empty():
        return data()
    elif A.rigid(context) and B.atom(context):
        b = B[0]
        ns = Number.floats(A)
        steps,seconds = 2,available_GB()/2.0
        if len(ns)>0: steps   = ns.pop(0)
        if len(ns)>0: seconds = ns.pop(0)

        if b.domain()==da('with'):
            ARGS = Evaluate(context,100,2)(b.arg())
            args = [da('use1')|data(arg) for arg in ARGS if arg.domain()==da('def')]
            new = context.copy()
            DA = Evaluate(new,steps,seconds)(data(*args))
            if DA.empty():
                R = Evaluate(new,steps,seconds)(b.right())
                return data((b.domain()+ARGS)|R)
CONTEXT.define('do1',eval_)
CONTEXT.define('with')

def more(context,domain,A,B):
    if B.empty(): return data()
    if A.rigid(context):
        ns = Number.floats(A)
        seconds,memory = SECONDS,MEMORY
        if len(ns)>0: seconds = ns.pop(0)
        if len(ns)>0: memory = ns.pop(0)
        return Evaluate(context,seconds,memory)(B)
CONTEXT.define('eval',more)
#
#     step evaluation step-by-step evaluation of it's input
#
#     demo: step 10 : nat : 0
#     demo: step : {first A : B} 2 : a b c d e
#
def stepEval(context,domain,A,B):
    if A.rigid(context):
        import Number
        steps = 20
        ns = Number.nats(A)
        if len(ns)>0: steps = ns.pop(0)

        E = data_evaluator(context,Cache(),B)
        outs = []
        n = 0
        while not E.done() and n<=steps:
            n += 1
            outs.append('['+str(n)+'] '+str(E.step().value()))
        return da('\n'.join(outs))
CONTEXT.define('step',stepEval)
