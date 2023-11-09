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
