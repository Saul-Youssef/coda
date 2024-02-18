
from base import *
import Number
import time,os,psutil
from Log import LOG

#DEFAULT = 20
STEPS = 500
#EVALS = 10000000
SECONDS = 36000
#
#    Evaluation of data to a maximum of steps and evals in the supplied context
#
class Evaluate(object):
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
