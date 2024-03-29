#
#   A foundational system for math and computing
#
#   This is the result of years of gradually simplifying previous personal computing systems, particularly
#   "types", "ee", "egg" (with Margo Seltzer and David Parkes), an attempt to use Aldor for Category theory
#   (Aldor is by Stephen Watt and collaborators), and "coda-classic".  This system, and it's
#   internal language are also called "coda"
#
#   Saul Youssef, January 2023
#====================================================================================
#
#   == A data is a finite sequence of codas ==
#
class data(object):
    def __init__(self,*codas): self._sequence = codas
    def __repr__(self): return ''.join([repr(c) for c in self])
    def __hash__(self): return hash(tuple(self._sequence))
    def __str__(self): return UNICODE.data(self)
    def __eq__(self,A): return self._sequence==A._sequence
#
#   Basic sequence operations
#
    def __iter__(self):
        for c in self._sequence: yield c
    def __getitem__(self,i): return self._sequence[i]
    def __len__(self): return len(self._sequence)
    def split(self): return data(*self[:1]),data(*self[1:])
#
#   Algebra
#
    def __add__(self,A): return data(*(self[:]+A[:]))  # A B in the coda language
    def __or__ (self,A): return coda(self,A)           # A:B in the coda language
#
#   Logic
#
    def empty    (self): return len(self)==0
#
#   == A coda is a pair of data ==
#
class coda(object):
    def __init__(self,left,right): self._left,self._right = left,right
    def __repr__(self): return '('+repr(self.left())+':'+repr(self.right())+')'
    def __hash__(self): return hash((self._left,self._right,))
    def __str__ (self): return UNICODE.coda(self)
    def __eq__(self,c): return self.left()==c.left() and self.right()==c.right()
#
#   Components
#
    def left (self): return self._left
    def right(self): return self._right
    def triplet(self):
        dom,A = self.left().split()
        return dom,A,self.right()
    def domain(self):
        dom,A,B = self.triplet()
        if str(dom).startswith('{') and str(dom).endswith('}'): return da('language')
        return dom
#
#   Data creation from a pair of codas
#
    def __add__(self,c): return data(self,c)
#
#   == A Context is a collection of definitions with disjoint domains ==
#
class Context(object):
    def __init__(self):
        self._definitions = {} # domain -> definition
        self._cache       = {} # cached results
    def __repr__(self): return  str(len(self._definitions))+' '+','.join([str(domain) for domain,definition in self._definitions.items()])
    def domain(self,c): return c.domain()
    def __contains__(self,c): return self.domain(c) in self._definitions
    def __getitem__(self,c): return self._definitions[self.domain(c)]
    def __iter__(self):
        for domain,definition in self._definitions.items(): yield domain,definition
    def invariant(self,c): return c in self and len(self[c])==0
#
#   Partial function, extended to coda -> data with identity
#
    def subcontext(self,A):
        context = Context()
        context._definitions[data()] = self._definitions[data()]
        for a in A:
            if data(a) in self._definitions: context._definitions[data(a)] = self._definitions[data(a)]
        return context
    def copy(self):
        context = Context()
        for key,value in self._definitions.items(): context._definitions[key] = value
        return context
    def add_variables(self,V):
        context = self.copy()
        for v in V:
            if v.domain()==da('='):
                L0,L1 = v.left().split()
                if len(L1)==1 and L1[0].right()==data():
                    variable = L1[0].left()
                    if variable in context._definitions:
                        raise error('...')
                    else:
                        context._definitions[variable] = Definition(variable,lambda dom2,A2,B2:v.right())
        return context
    def __call__(self,c):
        if c in self:
            if False and c in self._cache:
                return self._cache[c]
            else:
                d = self[c](c.left()|c.right().evaluate(self))
                if c.left().rigid() : self._cache[c] = d
#                if c.left().rigid() and c.right().rigid() and d.rigid(): self._cache[c] = d
                self.update(d)
                return d
        return data(c)
    def update(self,D):
        for d in D:
            if d.domain()==da('definition'):
                dom,A = d.left().split()
                B = d.right()
                definition = Definition(A,lambda domain,A2,B2:data((B+A2)|B2))
                if not A in self._definitions: self._definitions[A] = definition
#
#   Adding a definition to this context
#
    def define(self,name,*pfs): return self.add(Definition(da(name),*pfs))
    def add(self,definition):
        if definition.domain() in self._definitions: raise error('['+str(definition.domain())+']'+' is already defined')
        self._definitions[definition.domain()] = definition
        return self
#
#   Global context
#
CONTEXT = Context()
#
class Atoms(object):
    def __init__(self):
        self.atom = data()|data()
        self.bit0 = data(self.atom)|data()
        self.bit1 = data(self.atom)|data(self.atom)
    def domains(self):
        for domain in [data(),data(self.atom),data(self.bit0),data(self.bit1)]: yield domain
#
#   Standard atoms
#
ATOMS = Atoms()
for domain in ATOMS.domains(): CONTEXT.add(Definition(domain))
#
#   Unicode <-> data
#
class Unicode(object):
    def __init__(self):
        import string
        self._map = {}
        self.setatoms("\u25CE",u"\U0001D7EC",u"\U0001D75E")
        for c in string.printable: self._map[self.byte(c)] = c
    def setatom(self,co,unicode):
        self._map[co] = unicode
        return self
    def setatoms(self,atom,bit0,bit1):
        self.setatom(ATOMS.atom,atom)
        self.setatom(ATOMS.bit0,bit0)
        self.setatom(ATOMS.bit1,bit1)
        return self
    def __repr__(self): return ','.join([value for key,value in self._map.items()])
    def __add__(self,coda,s):
        self._map[coda] = s
        return self
    def __contains__(self,c): return c in self._map
    def __getitem__(self,c): return self._map[c]
    def byte(self,c):
        if type(c)==type(1): s = str(bin(c))
        else               : s = str(bin(ord(c)))
        s = s.split('0b')[-1]
        B = []
        for x in s:
            if   x=='0': B.append(ATOMS.bit0)
            elif x=='1': B.append(ATOMS.bit1)
        while len(B)<8: B = [ATOMS.bit0] + B
        return data(ATOMS.bit0)|data(*B)
    def co(self,text): return data(ATOMS.bit1)|data(*[self.byte(c) for c in text])
    def da(self,text): return data(self.co(text))
    def data(self,D,sep=' '): return sep.join([self.coda(c) for c in D])
    def coda(self,c):
        if c in self: return self[c]
        if c.domain() in [data(ATOMS.atom),data(ATOMS.bit0),data(ATOMS.bit1)]: return self.data(c.right(),'')
        return '('+self.data(c.left())+':'+self.data(c.right())+')'
UNICODE = Unicode()
#
#   Coda error class
#
class error(Exception):
    def __init__(self,msg): self._msg = msg
    def __str__(self): return self._msg
#
#   Text to data utilites
#
def co(text): return UNICODE.co(text)
def da(text): return UNICODE.da(text)
#
#   Import builtin definitions from other source files
#
import builtin

if __name__=='__main__':
    print(UNICODE)
    print(CONTEXT)
    print(da('hello'))
    print(repr(da('hello')))
