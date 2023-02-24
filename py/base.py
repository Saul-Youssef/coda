#
#   A foundational system for math and computing
#
#   This is the result of years of gradually simplifying previous personal computing systems, particularly
#   "types", "ee", "egg" (with Margo Seltzer and David Parkes), an attempt to use Aldor for Category theory
#   (Aldor is by Stephen Watt and collaborators), and "coda-classic".  This system and it's internal language
#   is also called "coda".
#
#   Saul Youssef, January 2023
#====================================================================================
#
#   A coda is a pair of data
#
class coda(object):
    def __init__(self,left,right): self._left,self._right = left,right
    def __hash__(self): return hash((self._left,self._right,))
    def __repr__(self): return '('+repr(self.left())+':'+repr(self.right())+')'
    def __str__(self): import Code; return Code.codastr(self)
    def __eq__(self,c): return self.left()==c.left() and self.right()==c.right()
    def    left (self): return self._left
    def   right (self): return self._right
    def   depth (self): return max(self._left.depth(),self._right.depth())
    def  domain (self): return self.left().split()[0] # domain is data and may be empty
    def __add__ (self,c): return data(self,c)
#    def atom(self): return self in CONTEXT and CONTEXT[self].identity()
    def atom(self): return self in CONTEXT and len(CONTEXT[self])==0
    def eval(self): # self -> data, evaluating recursively
        c = self.left().eval()|self.right().eval()
        if c in CONTEXT: return CONTEXT[c](c)
        return data(c)
#
#   ...and data is a finite sequence of codas
#
class data(object):
    def __init__(self,*cs):
        for c in cs:
            if not type(c)==TCODA: raise error('data error: '+str(c)+' is not a coda')
        self._coda = cs
    def __hash__(self): return hash(self._coda)
    def __repr__(self): return ''.join([repr(c) for c in self])     # display as pure data
    def __str__ (self): return ''.join([ str(c) for c in self])     # display using Code mappings
    def __eq__  (self,d): return self._coda==d._coda
    def __add__ (self,d): return data(*(self[:]+d[:]))  # A B in language
    def __or__  (self,d): return coda(self,d)           # A:B in language
    def __len__ (self): return len(self._coda)
    def __iter__(self):
        for c in self._coda: yield c
    def __getitem__(self,i): return self._coda[i]
    def depth(self): return max([0]+[1+c.depth() for c in self])
    def split(self): return data(*self[:1]),data(*self[1:])
    def empty(self): return len(self)==0
    def atom(self): return len(self)==1 and self[0].atom()
    def eval(self): # self -> data, evaluating recursively
        R = []
        for c in self:
            for d in c.eval(): R.append(d)
        return data(*R)
#
#   A definition is a partial function from coda to data
#
class DEF(object):
    def __init__(self,domain,*pfs): self._domain,self._pfs = domain,pfs
    def domain(self): return self._domain
    def __len__(self): return len(self._pfs)
    def __contains__(self,c): return c.domain()==self.domain()
#    def identity(self): return len(self._pfs)==0
    def __call__(self,c):  # apply coda->data operation
        domain,A = c.left().split(); B = c.right()
        for pf in self._pfs:  # may be zero or more pfs
            R = pf(domain,A,B)
            if not R is None: return R
        return data(c)
#
#   Global collection of definitions with disjoint domains
#
class Definitions(object):
    def __init__(self): self._definitions = {data():DEF(data())}
    def __repr__(self): return '['+', '.join([str(domain) for domain,definition in self])+']'
    def __len__(self): return len(self._definitions)
    def __iter__(self):
        for domain,definition in self._definitions.items(): yield domain,definition
    def __contains__(self,c): return c.domain() in self._definitions
    def __getitem__(self,c): return self._definitions[c.domain()]
    def add(self,definition):
        if definition.domain() in self._definitions: raise error(str(definition)+' is already defined.')
        self._definitions[definition.domain()] = definition
#
#   coda type for a validation check in the data __init__
#
TCODA = type(coda(data(),data())) # used only for a validation check in __init__ of data
#
#   The global context contains all activated definitions
#
CONTEXT = Definitions()
#
#   System exceptions
#
class error(Exception):
    def __init__(self,msg): self._msg = msg
    def __str__(self): return self._msg
#
#   Text to data utilites
#
def co(text): import Code; return data()|data(*[Code.byte(c) for c in text])
def da(text): import Code; return data(co(text))
#
#   Import builtin definitions from other source files
#
import builtin
