
#
#   remember use : def might happen during execution
#
from base import *
import time
from Log import LOG 

class evaluator(object):
    def __init__(self,context,seconds,bytes):
        self.seconds = seconds
        self.bytes   = bytes
        self.max_seconds = None
        self.max_bytes   = None
        import psutil
        self.process = psutil.Process()
        self.cache = {}
    def __call__(self,D):  # saturate definitions if necessary
        self.max_seconds = time.time()+self.seconds
        self.max_bytes   = self.bytes
        ndefinitions = len(self.context)

        D2 = self.evaluate(D)
        while (not ndefinitions==len(self.context)) and self.time() and self.memory():
            self.cache = {}  # can preserve some cache at some point this is a bit lazy
            D2 = self.evaluate(D2)
        return D2
    def evaluate(self,D):
        DE = eval_data(self.context,self.cache,D)
        while not DE.done() and self.time() and self.memory(): DE.step()
        return DE.value()
    def time(self):
        return time.time()<self.max_time
    def memory(self):
        return self.process.memory_info().rss<self.max_rss

class eval_data(object):
    def __init__(self,context,cache,D):
        self._sequence = [eval_coda(context,cache,d) for d in D]
    def step(self):
        self._sequence = [d.step() for d in self._sequence]
        return self
    def done(self):
        return all(d.done() for d in self._sequence)
    def value(self):
        L = []
        for d in self._sequence:
            for dd in d.value(): L.append(dd)
        return data(*L)

class eval_coda(object):
    def __init__(self,context,cache,c):
        self.context = context
        self.cache   = cache
        self.orig = c
        if c in cache:
            self.data = cache[c]
            self.done = True
        else:
            self.left  = eval_data(context,cache,c.left())
            self.right = eval_data(context,cache,c.right())
            self.data = None
            self.done = False
    def step(self):
        if self.data is None and not self.done:
            self.left = []
            self.left.step()
            self.right.step()
            c = self.left.value()|c.right.value()
            D = self.context(c)
            self.done = D==data(c)
            if not len(D)==1: self.data = eval_data(self.context,self.cache,D)
        else:
            self.data.step()
            self.done = all(d.done() for d in self.data)
        return self
    def done(self): return self.done
    def value(self):
        if self.data is None: D = data(self.left.value()|self.right.value())
        else                : D = self.data.value()
        self.cache[self.orig] = D
        return D
