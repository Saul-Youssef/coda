

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
    def __len__(self): return len([e for e in self]) 
    def __iter__(self):
        for e in self._endos: yield e
    def itempotent(self):
        for e in self:
            if e.idempotent(): yield e 
    def space(self):
        for e in self:
            if e.space(): yield e 
    def distributive(self):
        for e in self:
            if e.distributive(): yield e 
    def involution(self):
        for e in self:
            if e.involution(): yield e 
    def positive(self):
        for e in self:
            if e.positive(): yield e 
    def special(self):
        for e in self._special: yield e 
    def is_special(self,f):
        return any([f==s for s in self.special()]) 
    def commute_with_special(self,f):
        return any([f.commute(s) for s in self.special()]) 

class endo(object):
    def __init__(self,vals):
        self._values = [v for v in vals]
    def __hash__(self): return hash(tuple(self._values))
    def __len__(self): return len(self._values) 
    def __repr__(self): return ''.join([str(v) for v in self])
    def bound(self,i): return min(i,len(self._values)-1)
    def __iter__(self):
        for v in self._values: yield v 
    def range(self):
        S = set([])
        for i in range(len(self)): S.add(self(i))
        return S 
    def domain(self):
        for i in range(len(self)): yield i 
    def __call__(self,i): return self._values[self.bound(i)]
    def __eq__(self,e): return all([self(i)==e(i) for i in self.domain()]) 
    def __add__(self,e):
        vals = []
        for i in range(len(self._values)): vals.append(self.bound(self(i)+e(i)))
        f = endo(vals)
        return f 
    def __mul__(self,e):
        vals = []
        for i in range(len(self._values)): vals.append(self.bound(self(e(i)))) 
        f = endo(vals)
        return f 
    def idempotent(self): return all([self(i)==self(self(i)) for i in self.domain()]) 
    def identity(self): return all([self(i)==i for i in self.domain()]) 
    def positive(self): return all([self(i) >0 for i in self.domain()]) 
    def unit(self): # a morphism is a unit iff it is a permutation
        S = set([self(i) for i in self.domain()])
        return len(S)==len(self) 
    def space(self):
        r = self.idempotent()
        if r:
            for x,y in itertools.product(range(len(self)),repeat=2):
                r = self(x+y)==self(self(x)+self(y))
                if not r: return r 
        return r 
    def distributive(self):
        for x,y in itertools.product(range(len(self)),repeat=2):
#           print(x,y,self(x+y),self(x)+self(y),self(x+y)==self(x)+self(y))
            if not self(x+y)==self.bound(self(x)+self(y)): return False
        return True 
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
    def bound(self,i): return i%len(self._values)
    def __add__(self,e):
        vals = []
        for i in range(len(self._values)): vals.append(self.bound(self(i)+e(i)))
        f = endomod(vals)
        return f 
    def __mul__(self,e):
        vals = []
        for i in range(len(self._values)): vals.append(self.bound(self(e(i)))) 
        f = endomod(vals)
        return f 

      
        
    

        
    
        
    