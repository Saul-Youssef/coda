

import itertools 

def front(n,x):
    if x>=n: return n 
    return x 

def subsets(S):
    subsets = [[]]
    for s in S:
        new_subsets = [subset + [s] for subset in subsets]
        subsets.extend(new_subsets)
    return subsets 
#    T = [i for i in range(n)]
#    S = []
#    return S

class End(object):
    def __init__(self,N):
        self._N = N
        self._endos = []
        for p in itertools.product(range(N),repeat=N): self._endos.append(endo(p))
        self._special = []
        for n in range(N):
            f = [front(n,i) for i in range(N)]
            self._special.append(endo(f))
    def __repr__(self): return str(self._N) 
    def __len__(self): return len(self._endos)
    def __iter__(self):
        for e in self._endos: yield e
    def itempotent(self):
        for e in self:
            if e.idempotent(): yield e 
    def space(self):
        for e in self:
            if e.space(): yield e 
    def involution(self):
        for e in self:
            if e.involution(): yield e 
    def special(self):
        for e in self._special: yield e 
    def is_special(self,f):
        return any([f==s for s in self.special()]) 
    def commute_with_special(self,f):
        return any([f.commute(s) for s in self.special()]) 

class endo(object):
    def __init__(self,vals):
        self._values = [v for v in vals]
    def __len__(self): return len(self._values) 
    def __repr__(self): return ''.join([str(v) for v in self])
    def __iter__(self):
        for v in self._values: yield v 
    def domain(self):
        S = set([])
        for i in range(len(self)): S.add(self(i))
        return S 
    def __call__(self,i): return self._values[min(i,len(self._values)-1)] 
    def idempotent(self): return all([self(i)==self(self(i)) for i in self.domain()]) 
    def identity(self): return all([self(x)==x for x in self.domain()]) 
    def space(self):
        r = self.idempotent()
        if r:
            for x,y in itertools.product(range(len(self)),repeat=2):
                r = self(x+y)==self(self(x)+self(y))
                if not r: return r 
        return r 
    def involution(self): return all([self(self(i))==i for i in self.domain()]) 
    def commute(self,f):
        return all(f(self(i))==self(f(i)) for i in range(len(self._values))) 

class EndMod(End):
    def __init__(self,N):
        self._N = N
        self._endos = []
        for p in itertools.product(range(N),repeat=N):
            self._endos.append(endomod(p))
        self._special = [endomod([i for i in range(N)])] 
        for n in range(1,N):
            f = [i%n for i in range(N)]
            self._special.append(endomod(f))

class endomod(endo):
    def __call__(self,i): return self._values[i%len(self._values)] 
      
        
    

        
    
        
    