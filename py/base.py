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
    def atomic   (self): return any([c.atom() for c in self])
    def invariant(self): return all([c.atom() for c in self])
    def atom     (self): return len(self)==1 and self.atomic()
#
#   Evaluation
#
    def eval(self):
        result = []
        for c in self:
            for d in c.eval(): result.append(d)
        return data(*result)
#
#   == A coda is a pair of data ==
#
class coda(object):
    def __init__(self,left,right): self._left,self._right = left,right
    def __repr__(self): return '('+repr(self.left())+':'+repr(self.right())+')'
    def __hash__(self): return hash((self._left,self._right,))
    def __str__(self): return UNICODE.coda(self)
    def __eq__(self,c): return self.left()==c.left() and self.right()==c.right()
#
#   Components
#
    def left (self): return self._left
    def right(self): return self._right
    def domain(self): return self.left().split()[0]
#
#   Data creation from a pair of codas
#
    def __add__(self,c): return data(self,c)
#
#   Logic
#
    def atom(self): return CONTEXT.invariant(self)
#
#   Evaluation
#
    def eval(self):
        c = self.left().eval() | self.right().eval()
        if c in CONTEXT: return CONTEXT[c](c)
        else           : return data(c)
#
#   == A definition is a partial function from codas with
#   a specified domain to data ==
#
class Definition(object):
    def __init__(self,domain,*pfs): self._domain,self._pfs = domain,pfs
    def __repr__(self): return str(self._domain)
    def __contains__(self,c): return c.domain()==self._domain
    def domain(self): return self._domain
    def __len__(self): return len(self._pfs)
#
#   Partial function extended to coda -> data with identity
#
    def __call__(self,c):
        domain,A = c.left().split(); B = c.right()
        for pf in self._pfs:
            R = pf(domain,A,B)
            if not R is None: return R
        return data(c)
#
#   == A Context is a collection of definitions with disjoint domains ==
#
class Context(object):
    def __init__(self): self._definitions = {} # domain -> definition
    def __repr__(self): return ','.join([str(domain) for domain,definition in self._definitions.items()])
    def domain(self,c): # handles the {...} -> language convention
        d = c.domain(); s = str(d)
        if s.startswith('{') and s.endswith('}'): d = da('language')
        return d
    def __contains__(self,c): return self.domain(c) in self._definitions
    def __getitem__(self,c): return self._definitions[self.domain(c)]
    def __iter__(self):
        for domain,definition in self._definitions.items(): yield domain,definition
    def invariant(self,c): return c in self and len(self[c])==0
#
#   Partial function, extended to coda -> data with identity
#
    def __call__(self,c):
        if c in self: return self[c](c)
        return data(c)
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
#   Three standard atoms for the domain of bits, bit sequences and byte sequences
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
#        self._map[ATOMS.atom] = '*'
#        self._map[ATOMS.bit0] = '0'
#        self._map[ATOMS.bit1] = '1'
#        self._map[ATOMS.atom] = "\u25CE"
#        self._map[ATOMS.bit0] = u"\U0001D7EC"
#        self._map[ATOMS.bit1] = u"\U0001D75E"
        self.setatoms("\u25CE",u"\U0001D7EC",u"\U0001D75E")
        for c in string.printable: self._map[self.byte(c)] = c
    def setatoms(self,atom,bit0,bit1):
        self._map[ATOMS.atom] = atom
        self._map[ATOMS.bit0] = bit0
        self._map[ATOMS.bit1] = bit1
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
