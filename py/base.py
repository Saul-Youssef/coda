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
#=========================================================
#
#   Pure data 
#
class data(object):
    def __init__   (self,*D): self._data = D
    def __hash__      (self): return hash(self._data)
    def __len__       (self): return len(self._data)
    def depth(self): 
        if len(self)==0: return 0
        else           : return max([d.depth()+1 for d in self]) 
    def __eq__      (self,d): return self._data==d._data 
    def empty         (self): return len(self._data)==0
    def __iter__      (self):
        for d in self._data: yield d
    def __getitem__ (self,i): return self._data[i]
#
#   The foundational binary operations
#
    def __add__(self,D): return data(*(self._data+D._data))  # concatenation of sequences - (A B)  in lang, A+B in python 
    def __or__ (self,D): return data(self)+D                 # colon of sequences         - (A:B)  in lang, A|B in python
#
#   Data display
#
    def __repr__(self): return '('+''.join([d.__repr__() for d in self])+')'  # native display 
    def __str__(self):
        from Code import CODE # data->unicode map for display purposes 
        if self in CODE: return CODE[self]
        else           : return '('+''.join([d.__str__() for d in self])+')'
#
#   Split is available if len(data)>0
#
    def split_left (self): return data(*self[: 1]),data(*self[ 1:])
    def split_right(self): return data(*self[:-1]),data(*self[-1:])
    def split(self): return self.split_left()
#
#   Each data has a type which determines an applicable definition  
#
    def type(self):
        if len(self)>0 and len(self[0])>0: return self[0][0]
        return data()
    def atom(self): return self in DEF and len(DEF[self])==0
#
#   Definitions   
#
class Definitions(object):
    def __init__(self): self._definitions = {} 
    def __repr__(self): return ','.join([str(type) for type,pf in self])
    def __len__(self): return len(self._definitions) 
    def __iter__(self):
        for type,pf in self._definitions.items(): yield type,pf 
    def __contains__(self,D): return D.type() in self._definitions 
    def add(self,pf): self._definitions[pf.type()] = pf; return self 
    def __getitem__(self,D): return self._definitions[D.type()]
#
#   Partial function 
#
class PF(object):
    def __init__(self,type,*ops): self._type,self._ops = type,ops 
    def type(self): return self._type
    def domain(self,D): return D.type()==self.type() 
    def __len__(self): return len(self._ops)
    def __repr__(self): return str(self.type()) 
    def __iter__(self):
        for op in self._ops: yield op 
    def __call__(self,D):
        if len(D)>0:
            type,A = D[0].split()
            B = data(*D[1:])
            for op in self:
                R = op(A,B)
                if not R is None: return R
        return D 
#
#   The global collection of definitions
#
DEF = Definitions()
DEF.add(PF(data()))  # empty typed data is atomic 
#
#   Translating unicode text into corresponding data
#
def co(text): import Code; return Code.data(text) 
#
#   System exceptions
#
class error(Exception):
    def __init__(self,msg): self._msg = msg
    def __str__(self): return self._msg
