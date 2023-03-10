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
    def __str__(self): import Code; return Code.coda2unicode(self)
    def __eq__(self,c): return self.left()==c.left() and self.right()==c.right()
    def    left (self): return self._left
    def   right (self): return self._right
    def   depth (self): return max(self._left.depth(),self._right.depth())
    def  domain (self): # domain determines the corresponding definition
        dom = self.left().split()[0]
        if str(dom).startswith('{') and str(dom).endswith('}'): return da('language')
        return dom
    def __add__ (self,c): return data(self,c)
    def atom(self): return CONTEXT.identity(self)
#        print('aaaaa',self)
#        print('aaaaa',self in CONTEXT,type(CONTEXT[self]))
#        return self in CONTEXT and len(CONTEXT[self])==0
    def eval(self): # self -> data, evaluating recursively
        c = self.left().eval()|self.right().eval()
        if c in CONTEXT: return CONTEXT[c](c)
        return data(c)
#
#   Data is a finite sequence of codas
#
class data(object):
    def __init__(self,*cs):
        for c in cs:
            if not type(c)==TCODA: raise error('data error: '+str(c)+' is not a coda')
        self._coda = cs
    def __hash__(self): return hash(self._coda)
    def __repr__(self): return ''.join([repr(c) for c in self])     # display as pure data
    def __str__(self): import Code; return Code.data2unicode(self)
    def __eq__  (self,d): return self._coda==d._coda
    def __add__ (self,d): return data(*(self[:]+d[:]))  # A B in the coda language
    def __or__  (self,d): return coda(self,d)           # A:B in the coda language
    def __len__ (self): return len(self._coda)
    def __iter__(self):
        for c in self._coda: yield c
    def __getitem__(self,i): return self._coda[i]
    def depth(self): return max([0]+[1+c.depth() for c in self])
    def split(self): return data(*self[:1]),data(*self[1:])
    def empty(self): return len(self)==0
    def atom(self): return len(self)==1 and self[0].atom()
    def atomic(self): return len(self)>0 and any([c.atom() for c in self])
    def eval(self): # self -> data, evaluating recursively
        R = []
        for c in self:
            for d in c.eval(): R.append(d)
        return data(*R)
#
#   A definition is a partial function from coda to data
#
class Definition(object):
    def __init__(self,domain,*pfs): self._domain,self._pfs = domain,pfs
    def __repr__(self): return str(self._domain)
    def domain(self): return self._domain
    def __len__(self): return len(self._pfs)
    def __contains__(self,c): return c.domain()==self.domain()
    def __call__(self,c):  # apply coda->data operation
        domain,A = c.left().split(); B = c.right()
        for pf in self._pfs:    # may be zero or more pfs
            R = pf(domain,A,B)  # <- apply definition
            if not R is None: return R
        return data(c)
#
#   Global collection of definitions with disjoint domains
#
class Definitions(object):
    def __init__(self):
        self._domain = {}      # definitions with an invariant domain
        self._value  = {}      # definitions with invariant value
        self._used   = set([]) # domains used by value definitions
    def dom(self,domain,pf):
        if domain in self._domain or domain in self._used: raise error(str(domain)+' is already defined.')
        self._domain[domain] = pf
    def val(self,co,da):
        if co.domain() in self._domain or co in self._domain: raise error(str(co)+' is already defined')
        self._value[co] = da
    def __contains__(self,co): return co in self._value or co.domain() in self._domain
    def identity(self,co): return co.domain() in self._domain and len(self._domain[co.domain()])==0
    def __getitem__(self,co):
        if co in self._value: return lambda c : self._value[c]
        if co.domain() in self._domain: return self._domain[co.domain()]

    def define(self,name,*pfs):
        defin = Definition(da(name),*pfs)
        if defin.domain() in self._domain: raise error(str(defin.domain())+' is already defined.')
        return self.dom(defin.domain(),defin)
    def __iter__(self):
        for domain,definition in self._domain.items(): yield domain,definition
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
def co(text): import Code; return Code.text2coda(text)
def da(text): return data(co(text))
#
#   Import builtin definitions from other source files
#
import builtin
