#
#   A foundational system for math and computing
#
#   This is the result of years of gradually simplifying previous personal computing systems, particularly 
#   "types", "ee", "egg" (with Margo Seltzer and David Parkes), an attempt to use Aldor for Category theory 
#   (Aldor is by Stephen Watt and collaborators), and "coda-classic".  This system and it's internal language
#   is also called "coda". 
#
#   Saul Youssef, January 2023
#
#============================================
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
    def __add__(self,D): return data(*(self._data+D._data))  # concatenation sequences  
    def __or__ (self,D): return data(self)+D                 # colon of sequences 
#    def __and__(self,D): return data(self)+data(D)           # concatenate colons 
#
#   Data display
#
    def __repr__(self): return '('+''.join([d.__repr__() for d in self])+')'  # native display 
    def __str__(self):
        from Code import CODE # data->unicode map for display purposes 
        if self in CODE: return CODE[self]
        else           : return '('+''.join([d.__str__() for d in self])+')'
#
#   Each data has a type which determines an applicable definition  
#
    def type(self): 
        if len(self)>0 and len(self[0])>0: return self[0][0]
        return data()
    def atom(self): return self in CONTEXT and len(CONTEXT[self])==0
    def atomic(self): return len(self)==1 and self[0].atom()
#
#   Definitions   
#
class Definitions(object):
    def __init__(self): self._definitions = {data():PF(data())}  # empty data
    def __repr__(self): return ','.join([str(type) for type,pf in self])
    def __len__(self): return len(self._definitions) 
    def __iter__(self):
        for type,pf in self._definitions.items(): yield type,pf 
    def __contains__(self,D): return D.type() in self._definitions 
    def add(self,pf): 
        if not pf.type().atom(): raise error('Partial function type ['+str(pf)+'] must be an atom')
        self._definitions[pf.type()] = pf; return self 
    def __getitem__(self,D): return self._definitions[D.type()]
    def __call__(self,D):
        L = []
        for d in D:
            if d in self:
                for dd in self[d](d): L.append(dd)
            else:
                L.append(d)
        return data(*L)
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
        A = data(*D[0][1:])
        B = data(*D[1:])
        for op in self:
            R = op(A,B)
            if not R is None: return R
        return data(D)
#
#   System exceptions
#
class error(Exception):
    def __init__(self,msg): self._msg = msg
    def __str__(self): return self._msg
#
#   The global collection of definitions
#
CONTEXT = Definitions() 
#
#   Unicode utilities
#
def co ( text): import Code; return Code.data(text) 
def col(*args): return data( data(*[co(t) for t in args[:-1]]) | data(*args[-1]) )
