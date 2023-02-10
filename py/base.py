#
#   A foundational system for math and computing
#
#   This is the result of years of gradually simplifying previous personal computing systems, particularly 
#   types, egg (with Margo Seltzer and David Parkes), a serious attempt to use Aldor for Category theory 
#   (Aldor by Stephen Watt and collaborators), and coda (a simplified descendent of egg).  This system 
#   is also named coda.  
#
#   Saul Youssef, 2023
#
class data(object):
    def __init__   (self,*D): self._data = D
    def __hash__      (self): return hash(self._data)
    def __len__       (self): return len(self._data)
    def __eq__      (self,d): return self._data==d._data 
    def empty         (self): return len(self._data)==0
    def __iter__      (self):
        for d in self._data: yield d
    def __getitem__ (self,i): return self._data[i]
#
#   The two foundational binary operations
#
    def __add__(self,D): return data(*(self._data+D._data))  # concatenation of sequences - (A B) in lang, A+B in python 
    def __or__ (self,D): return data(self)+D                 # colon of sequences         - (A:B) in lang, A|B in python
#
#   Data display
#
    def __repr__(self): return '('+''.join([d.__repr__() for d in self])+')'
    def __str__(self):
        from Name import NAME # data->unicode map for display purposes 
        if self in NAME: return NAME[self]
        else           : return '('+''.join([d.__str__() for d in self])+')'
#
#   Splits
#
    def split_left (self): return data(*self[: 1]),data(*self[ 1:])
    def split_right(self): return data(*self[:-1]),data(*self[-1:])
    def split(self): return self.split_left()
#
#   The "flag" of a data determines which partial function (if any) applies
#
    def flag(self): return self.split()[0].split()[0]
    
class Definitions(object):
    def __init__(self):
        self._definitions = {} # mapping from flags to sequences of partial functions from data to data 
    def add(self,flag,*pfs):
        self._definitions[flag] = pfs
    def contains(self,flag):
        return flag in self._definitions 
    def pfs(self,flag):
        return self._definitions[flag]
#
#   System exceptions
#
class error(Exception):
    def __init__(self,msg): self._msg = msg
    def __str__(self): return self._msg

