#
#   A foundational system for math, computing and logic
#
#   Saul Youssef, January 2023
#====================================================================================
#
#   = A data is a finite sequence of codas =
#
class data(object):
    def __init__(self,*codas): self._sequence = codas
    def __repr__(self): return ''.join([repr(c) for c in self])
    def __hash__(self): return hash(tuple(self._sequence))
    def __str__(self): return UNICODE.data(self)
    def __eq__(self,A): return self._sequence==A._sequence
#
#   Sequence
#
    def __iter__(self):
        for c in self._sequence: yield c
    def __getitem__(self,i): return self._sequence[i]
    def __len__(self): return len(self._sequence)
    def split(self): return data(*self[:1]),data(*self[1:])
#
#   Context dependent properties
#
    def atomic(self,context): return all(c.atom(context) for c in self)
    def irred (self,context): return any(c.atom(context) for c in self)
    def atom  (self,context): return len(self)==1 and self.atomic(context)
    def rigid (self,context): return self.atomic(context) and all(c.left().rigid(context) and c.right().rigid(context) for c in self)
#
#   Algebra
#
    def __add__(self,A): return data(*(self[:]+A[:]))  # A B in the language
    def __or__ (self,A): return coda(self,A)           # A:B in the language
    def empty    (self): return len(self)==0
#
#   = A coda is a pair of data =
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
    def triplet(self): dom,A = self.left().split() ; return dom,A,self.right()
    def arg(self): return self.left().split()[-1]
    def domain(self):
        dom,A,B = self.triplet()
        if str(dom).startswith('{') and str(dom).endswith('}'): return da('language')
        return dom
#
#   Data creation from a pair of codas
#
    def __add__(self,c): return data(self,c)
#
#   Atom in context
#
    def atom(self,context): return self in context and len(context[self])==0
    def rigid(self,context): return data(self).rigid(context)

ATOM = data()|data()
BIT0 = data(ATOM)|data()
BIT1 = data(ATOM)|data(ATOM)
#
#   = A context is a function from coda to data =
#
class Context(object):
    def __init__(self,*doms): self._defs = {dom:[] for dom in doms}
    def __iter__(self):
        for domain,defs in self._defs.items(): yield domain,defs
    def __repr__(self): return ','.join([str(dom) for dom,defs in self])
    def copy(self):
        cont = Context()
        for key,value in self: cont._defs[key] = value
        return cont
    def has(self,dom): return dom in self._defs
    def add(self,domain,*Fs):
        if domain in self._defs: raise error(str(domain)+' is already defined')
        self._defs[domain] = Fs; return self
    def define(self,name,*Fs): return self.add(da(name),*Fs)

    def __contains__(self,c): return c.domain() in self._defs
    def __getitem__ (self,c): return self._defs[c.domain()]
    def __call__(self,c):  # total function from coda to data
            for F in self[c]:
                domain,A,B = c.triplet()
                D = F(self,domain,A,B)
                if not D is None: return D
            return data(c)
CONTEXT = Context(data(),data(ATOM),data(BIT0),data(BIT1))
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
        self.setatom(ATOM,atom)
        self.setatom(BIT0,bit0)
        self.setatom(BIT1,bit1)
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
            if   x=='0': B.append(BIT0)
            elif x=='1': B.append(BIT1)
        while len(B)<8: B = [BIT0] + B
        return data(BIT0)|data(*B)
    def co(self,text): return data(BIT1)|data(*[self.byte(c) for c in text])
    def da(self,text): return data(self.co(text))
    def data(self,D,sep=' '): return sep.join([self.coda(c) for c in D])
    def coda(self,c):
        if c in self: return self[c]
        if c.domain() in [data(ATOM),data(BIT0),data(BIT1)]: return self.data(c.right(),'')
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
