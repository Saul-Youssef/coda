

import itertools

class morph(object):
    def __init__(self,*F): self._values = F
    def __str__(self):
        return str(self._values)
    def dis(self):
        t = [str(self)]
        t.append(str(self.fixed()))
        t.append(self.property())
        return ' '.join(t)
    def __len__(self): return len(self._values)
    def __iter__(self):
        for i in range(len(self)): yield i
    def __call__(self,i): return self._values[i]

    def idempotent(self): return all(self(self(i))==self(i) for i in self)
    def nonincreasing(self):
        return all(self(i)<=i for i in self)
    def nondecreasing(self):
        return all(self(i)>=i for i in self)
    def increasing(self):
        return any(self(i)>i for i in self)
    def decreasing(self):
        return any(self(i)<i for i in self)
    def fixed(self): return len([i for i in self if self(i)==i])
    def property(self):
        ps = []
        if self.identity(): ps.append('identity')
        if self.constant(): ps.append('constant')
        if self.minramp(): ps.append('minramp')
        return '/'.join(ps)
    def identity(self): return all(self(i)==i for i in self)
    def constant(self): return all(self(i)==self(0) for i in self)
    def minramp(self):
        if self.identity():
            return True
        else:
            for i in self:
                if not i==self(i): non_fixed = i; break
            if non_fixed>0 and self(non_fixed)==non_fixed-1:
                ramp = True
                for i in self:
                    if i>=non_fixed and not(self(i)==self(non_fixed-1)):
                        ramp = False
                return ramp
            else:
                return False
    def space(self):
        for i in range(len(self._values)):
            for j in range(len(self._values)):
                if (i+j)<len(self) and (self(i)+self(j))<len(self):
                    SP = self(i+j)==self(self(i)+self(j))
                    if not SP: return False
        return True

def Morph(n):
    for P in itertools.product(range(n),repeat=n): yield morph(*P)

def search(n):
    total = 0
    spaces = 0
    for m in Morph(n):
        total += 1
        if m.idempotent() and m.space():
            spaces += 1
            print(m.dis())
#            print(str(m),m.increasing() and m.decreasing(),m.fixed(),m.property())
    print(spaces,total)

def bsearch(n):
    total = 0
    spaces = 0
    for m in Morph(n):
        total += 1
        if m.idempotent() and m.space(): spaces += 1
    print(n,spaces,total,float(spaces)/float(total))
