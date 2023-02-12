#
#   A foundational system for math and computing
#
#   This is the result of years of gradually simplifying previous personal computing systems, particularly 
#   "types", "ee", "egg" (with Margo Seltzer and David Parkes), an attempt to use Aldor for Category theory 
#   (Aldor is by Stephen Watt and collaborators), and "coda-classic".  This system and it's internal language
#   is called "coda". 
#
#   Saul Youssef, January 2023
#
#-----------------------------------------------------------------------------------------------------------
#
#   Pure data 
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
#   The two foundational binary operations.  Note that * is associative, but : and ** are not.
#
    def __add__(self,D): return data(*(self._data+D._data))  # concatenation of sequences - (A B)  in lang, A+B in python 
    def __or__ (self,D): return data(self)+D                 # colon of sequences         - (A:B)  in lang, A|B in python
    def __and__(self,D): return data(self)+data(D)           # pairing data.              -        in lang, A & B in python
#
#   Data display
#
    def __repr__(self): return '('+''.join([d.__repr__() for d in self])+')'
    def __str__(self):
        from Code import CODE # data->unicode map for display purposes 
        if self in CODE: return CODE[self]
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
    def flag(self): 
        if len(self)>0 and len(self[0])>0: return self[0][0]
        return data()
    def atom(self):
        return len(self)==1 and DEF.atomic(self)
#
#   Definitions is the global mapping from flags to a collection of operators 
#   which implement a partial function from data to data with domain defined 
#   by data flag. 
#
class Definitions(object):
    def __init__(self): self._definitions = {} 
    def __repr__(self): return ','.join([str(flag) for flag,pf in self])
    def __len__(self): return len(self._definitions) 
    def __iter__(self):
        for flag,pf in self._definitions.items(): yield flag,pf 

    def __contains__(self,flag): return flag in self._definitions 
    def add(self,pf): # add partial function 
        self._definitions[pf.flag()] = pf; return self 
    def get(self,flag): # get partial function associated with flag 
        return self._definitions[flag]

    def atomic(self,D): return D.flag() in self and self.get(D.flag()).identity()
#
#   Partial functions are defined by zero or more operators with 
#   pf:(flag,A)B -> pf_operator(A,B).  Zero such operators indicates 
#   the identity partial function.  
#
class PF(object):
    def __init__(self,flag,*ops):
        self._flag = flag
        self._ops  = ops 
    def flag(self): return self._flag
    def domain(self,D): return D.flag()==self.flag() 
    def __len__(self): return len(self._ops)
    def identity(self): return len(self)==0 
    def __repr__(self): return str(self.flag()) 
    def __iter__(self):
        for op in self._ops: yield op 
    def __call__(self,D):
        if len(self)==0: return D # identity partial function 
        if len(D)>0:
            flag,A = D[0].split()
            B = data(*D[1:])
            for op in self:
                R = op(A,B)
                if not R is None: return R
#
#   The global collection of definitions
#
DEF = Definitions()
DEF.add(PF(data(),[])) 
#
#   System exceptions
#
class error(Exception):
    def __init__(self,msg): self._msg = msg
    def __str__(self): return self._msg
#
#   Translating unicode text into corresponding data
#
def da(text): import Code; return Code.data(text) 
