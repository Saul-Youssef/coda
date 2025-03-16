#
#   This is a python implementation of L for speed
#

class Data(object):
    def __init__(self,L):
        self._data = tuple(l for l in L)
    def __iter__(self): 
        for l in self._data: yield l
    def __len__(self): return len(self._data)

class End(object):
    def __init__(self,n):
        