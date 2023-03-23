#
#    These are some classes for data searching and classification
#
from base import *
#
#    The classifier class attempts to find data D in Sample which
#    separates Space A from Space B in the sense that D:a and D:b
#    have disjoint logical values for a in A, b in B.
#
class Classifier(object):
    def __init__(self,A,B,Sample,ndef,width,maxiter,nthread):
        self._A = A               # space to classify
        self._B = B               # space to separate from A
        self._sample = Sample     # search space for D separating A and B
        self._width = width       # search width
        self._ndef = ndef         # number of definitions to try adding at a time
        self._maxiter = maxiter   # maximum number of tries with specified width
        self._distance = 0.0      # separation metric. The distance from D:A to D:B is maximized.
        self._classifier = data() # = D, the best classifier found from Sample
        self._context = Context() # The context in which D classifies
        self._nthread = nthread   # Number of parallel threads
    def choose_new_context(self):
        cos = []
        for co in self._sample.codas():
            if not co in CONTEXT: cos.append(co)
        import random
        random.shuffle(cos)
        newcontext = Context()
        while (len(newcontext)<self._ndef) and len(cos)>0:
            co = cos.pop()
            da = self._sample.data_sample(1)[0]
            newcontext.add(co,da)
        return newcontext
    def iterate(self):
        attempts = []
        for w in range(self._width):
            newcontext = self.choose_new_context()
            distance,best_classifier = self.attempt(newcontext+self._context)
            attempts.append((distance,best_classifier,newcontext,))
#        attempts.sort()
        attempts = sorted(attempts,key=lambda t:t[0])
        return attempts[-1]
    def attempt(self,context):
        context.install()
        tries = []
        for s in self._sample:
            sA = self._A.leftap(s).eval(100,self._nthread)
            sB = self._B.leftap(s).eval(100,self._nthread)
            distance = sA.distance(sB)
            tries.append([distance,s,])
        nc = 0
        for t in tries:
            print('aaaaa',t); nc+= 1
            if nc>10: break
#        tries.sort()
        tries = sorted(tries,key=lambda p:p[0])
        return tries[-1]
    def search(self):
        iter = 0
        while iter<self._maxiter and self._distance<1.0:
            iter += 1
            distance,best_classifier,newcontext = self.iterate()
            if distance>self._distance:
                self._distance = distance
                self._classifier = best_classifier
                self._context.update(newcontext)
        return self._distance,self._classifier
    def distance(self): return self._distance
    def classifier(self): return self._classifier
    def context(self): return self._context

class Context(object):
    def __init__(self):
        self._context = {}
    def __len__(self): return len(self._context)
    def __repr__(self):
        return ', '.join(['->'.join([str(co),str(da)]) for co,da in self])
    def __iter__(self):
        for co,da in self._context.items(): yield co,da
    def __add__(self,C):
        S = Context()
        for co,da in self: S.add(co,da)
        for co,da in    C: S.add(co,da)
        return S
    def add(self,co,da):
        self._context[co] = da
        return self
    def update(self,C):
        for co,da in C: self._context[co] = da
        return self
    def install(self):  # install context in the real context
        CONTEXT.clear()
        CONTEXT.dom(data(),Definition(data()))
        for co,da in self: CONTEXT.val(co,da)
