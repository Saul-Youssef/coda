#
#   General function accelerator if the domain of F
#   has a length.
#
import sys

class Turbo(object):
    def __init__(self,name,maxbytes):
        self._name = name
        self._domain   = {}
        self._maxbytes = maxbytes
        self._bytes    = sys.getsizeof(self._domain)
        self._hit      = 0
        self._miss     = 0
    def __str__(self):
        d = {'name':self._name,'hit':self._hit,'miss':self._miss,'size':self._bytes,'limit':self._maxbytes}
        return ', '.join([key+':'+str(value) for key,value in d.items()])
    def __call__(self,F,X):
        if X in self._domain:
            self._hit += 1
            return self._domain[X]
        else:
            self._miss += 1
            Y = F(X)
            if self._bytes<self._maxbytes:
                self._domain[X] = Y
                self._bytes += sys.getsizeof(X)+sys.getsizeof(Y)
            return Y
#
#   Simple cache used in contexts.
#
#   A definition is a partial function from coda to data.
#   A context extends this to a total function from coda to data (ecoda)
#   This in
#
class Cache(object):
    def __init__(self):
        self._ndata = {}
        self._edata = {}
        self._ecoda = {}
    def copy(self):
        c = Cache()
        for key,value in self._ndata.items(): c._ndata[key] = value
        for key,value in self._edata.items(): c._edata[key] = value
        for key,value in self._ecoda.items(): c._ecoda[key] = value
        return c
    def evaluate(self,context,n,D):
        if (n,D) in self._ndata:
            return self._ndata[(n,D)]
        else:
            D2 = context._evaluate(n,D)
            self._ndata[(n,D)] = D2
            return D2
    def edata(self,context,D):
        if D in self._edata:
            return self._edata[D]
        else:
            D2 = context._edata(D)
            self._edata[D] = D2
            return D2
    def ecoda(self,context,c):
        if c in self._ecoda:
            return self._ecoda[c]
        else:
            D = context._ecoda(c)
            self._ecoda[c] = D
            return D

if __name__=='__main__':
    def f(x): return x*x
    T = Turbo('test',1000)
    print(T(f,2))
    print(T)
