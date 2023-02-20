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
#   A coda is a pair of data
#
class coda(object):
    def __init__(self,left,right): self._left,self._right = left,right
    def __repr__(self): return '('+repr(self.left())+':'+repr(self.right())+')'
    def __hash__(self): return hash((self._left,self._right,))
    def __str__(self):
        from Code import CODE
        if self in CODE: return CODE[self]
        else           : return str(self.right())
    def __eq__(self,c): return self.left()==c.left() and self.right()==c.right()
    def    left (self): return self._left
    def   right (self): return self._right
    def __iter__(self):
        for c in self._right: yield c 
    def   depth (self): return max(self._left.depth(),self._right.depth())
    def  domain (self): return self.left().split()[0]
    def __add__ (self,c): return data(self,c)
#
#   A data is a finite sequence of codas
#
class data(object):
    def __init__(self,*cs): self._coda = cs
    def __repr__(self): return ''.join([repr(c) for c in self])
    def __str__ (self): return ''.join([ str(c) for c in self])
    def __hash__(self): return hash(self._coda)
    def __eq__  (self,d): return self._coda==d._coda
    def __add__ (self,d): return data(*(self[:]+d[:]))
    def __or__  (self,d): return coda(self,d)
    def __len__ (self): return len(self._coda)
    def __iter__(self):
        for c in self._coda: yield c
    def empty(self): return len(self)==0
    def __getitem__(self,i): return self._coda[i]
    def depth(self): return max([0]+[1+c.depth() for c in self])
    def split(self): return self[:1],self[1:]
#
#   A definition is a partial function from coda to data
#
class DEF(object):
    def __init__(self,domain,*pfs): self._domain,self._pfs = domain,pfs
    def __contains__(self,c): return c.domain()==self._domain
    def domain(self): return self._domain
    def atomic(self): return len(self._pfs)==0
    def apply(self,c):
        domain,A,B = c.left().split()
        for pf in self._pfs:
            R = pf(domain,A,B)
            if not R is None: return R
        return data(c)
    def __call__(self,D):
        R = []
        for c in D:
            if c in self:
                for d in self.apply(c): R.append(d)
            else:
                R.append(c)
        return data(*R)
#
#   Global definitions
#
class Definitions(object):
    def __init__(self): self._definitions = {data():DEF(data())} 
    def __len__(self): return len(self._definitions)
    def __iter__(self):
        for domain,Def in self.items(): yield domain,Def
    def __contains__(self,c): return c.domain() in self._definitions 
    def __getitem__(self,c): return self._definitions[c.domain()]
    def add(self,Def): 
        if Def.domain in self._definitions: raise error(str(Def)+' is already defined.')
        self._definitions[Def.domain()] = Def
    def __call__(self,D):
        R = []
        for c in D:
            if c in self:
                for d in self[c](c): R.append(d)
            else:
                R.append(c)
        return data(*R)
#
#   Global definitions 
#
CONTEXT = Definitions()
#
#   System exceptions
#
class error(Exception):
    def __init__(self,msg): self._msg = msg
    def __str__(self): return self._msg
#
#   Text to data 
#
def da(text): import Code; return data(*[Code.byte(c) for c in text])
