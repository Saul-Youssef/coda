#
#    Compiler
#
from base import *

def coda(A,B):
    source = source[:-2]
    print('aaaaa',A,B,source)
CONTEXT.add(PF(co('{')[0],coda))

def wrap(txt): return b'{'+txt+b'}'
#
#   The kernel for the language definition is defined by a sequence of rules
#   where the first rule that applies defines the language.
#
#   To compile code x, do {x}: in the language.
#
def co(A0,B):
    S,A = A0.split() # the language acts if S contains code in curly braces {x}
    if len(S)==1 and is_code(S[0]) and S[0].startswith(b'{') and S[0].endswith(b'}'): x = S[0][1:-1]
    else: return

    if x.startswith(b' '): return one(wrap(x[1:  ]),A,B)
    if x.endswith  (b' '): return one(wrap(x[ :-1]),A,B)
    if x==b'': return data()
    if x==b'A': return A
    if x==b'B': return B
#
#       A=B -> (= A:B)
#
    Equal = parse(b'=',x,b'left')
    if Equal():
        front,back = Equal.parts()
        return one(b'=',one(wrap(front),A,B),one(wrap(back),A,B))
#
#       Data operations are concatenation and colon.  The rest is syntactic sugar.
#
    Colon = parse(b':',x,b'left')
    if Colon():
        front,back = Colon.parts()
        return data(colon(one(wrap(front),A,B),one(wrap(back),A,B)))
#
#       A*B : X is defined to be A:B:X
#
    Star  = parse(b'*',x,b'left')
    if Star():
        front,back = Star.parts()
        return data(b'*')+one(b'*',one(wrap(front),A,B),one(wrap(back),A,B))
#
#       Data operations are concatenation and colon.  The rest is syntactic sugar.
#
    Space = parse(b' ',x,b'left')
    if Space():
        front,back = Space.parts()
        return one(wrap(front),A,B) + one(wrap(back),A,B)
#
#       Operations are groups with paranthesis as usual.  Scope is controlled with {...}
#       and code literals are denotes with <...>
#
    if x.startswith(b'(') and x.endswith(b')'): return one(wrap(x[1:-1]),A,B)  # parenthesis
    if x.startswith(b'{') and x.endswith(b'}') and balanced(x[1:-1]): return data(x)  # scope
    if x.startswith(b'<') and x.endswith(b'>'): return data(x[1:-1])           # literal code possibly with special characters
#
#       Unlike most compilers, all code is valid in coda
#
    if x.endswith(b'?'): return data(colon(data(b'?'),data(x[:-1])))
    return data(x)
#DEF.add(data(b'co'),co)

class parse(object):
    def __init__(self,sep,code,direction):
        self._sep  = sep
        self._code = code
        self._parts = None
        self._direction = direction
    def __call__(self):
        got_one = self._sep in self._code
        if got_one:
            parts = self._code.split(self._sep)
            if self._direction==b'left':
                lefts = [parts.pop(0)]
                while not balanced(self._sep.join(lefts)) and len(parts)>0: lefts.append(parts.pop(0))
                left,right = self._sep.join(lefts),self._sep.join(parts)
                got_one = balanced(left) and len(parts)>0
                self._parts = left,right
            else:
                rights = [parts.pop()]
                while not balanced(self._sep.join(rights)) and len(parts)>0: rights.insert(0,parts.pop())
                left,right = self._sep.join(parts),self._sep.join(rights)
                got_one = balanced(right) and len(parts)>0
                self._parts = left,right
        return got_one
    def parts(self):
        if self._parts is None: raise error('error ['+self._code+']')
        return self._parts
    def backchar(self):
        if self._parts is None: raise error('error ['+self._code+']')
        b = b''
        front,back = self.parts()
        if len(back)>0: b = back[0:1]
        return b

def balanced(code):
    npar,ncurly = 0,0
    for c in code.decode():
        if   c=='(' and ncurly==0: npar +=  1
        elif c==')' and ncurly==0: npar += -1
        elif c=='{': ncurly +=  1
        elif c=='}': ncurly += -1
        if npar<0 or ncurly<0: break
    nangle = 0
    for c in code.decode():
        if   c=='<': nangle +=  1
        elif c=='>': nangle += -1
    return npar==0 and ncurly==0 and nangle==0
