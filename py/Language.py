#
#    Compiler
#
from base import *
import Code

def wrap(txt): return '{'+txt+'}'

def split(A):
    chars = []
    As = [a for a in A]
    done = False
    while len(As)>0:
        a = As.pop(0)
        if a==Code.byte('}'):
            done = True; break
        else:
            chars.append(a)
    code = ''.join([str(a) for a in chars])
    return code,data(*As)

def fuse(code,A): return Code.code2data(wrap(code))+A
def new(code,A,B): return data((fuse(code)+A)|B)

def language(domain,A0,B):
    s,A = split(A0) # extract source code from A0

    if s.startswith(' '): return new(s[1:  ],A,B)
    if s.endswith  (' '): return new(s[ :-1],A,B)
    if s== '': return data()
    if s=='A': return A
    if s=='B': return B
#
#   A=B -> (= A:B)
#
    Equal = parse('=',s,'left')
    if Equal():
        front,back = Equal.parts()
        return new('=',new(front,A,B),new(back,A,B))
#
#   The essential operations are concatenation and colon.  The rest is syntactic sugar.
#
    Colon = parse(':',s,'left')
    if Colon():
        front,back = Colon.parts()
        return data(new(front,A,B)|new(back,A,B))
#
#       A*B : X is defined to be A:B:X
#
#    Star  = parse(b'*',x,b'left')
#    if Star():
#        front,back = Star.parts()
#        return data(b'*')+one(b'*',one(wrap(front),A,B),one(wrap(back),A,B))
#
#   A*B:X is defined to be A:B:X
#
    Space = parse(' ',s,'left')
    if Space():
        front,back = Space.parts()
        return new(front,A,B)+new(back,A,B)
#
#   Operations are grouped with parenthesis.  Text within curly brackets is source code.
#   Text between angle brackets are byte strings.
#
    if s.startswith('(') and s.endswith(')'): return new(s[1:-1],A,B)
    if s.startswith('{') and s.endswith('}') and balanced(x[1:-1]): return da(x)
    if s.startswith('<') and s.endswith('>'): return da(x[1:-1])
#
#   There are no syntax errors.  All text is valid source code.
#
    return da(x)
CONTEXT.add(DEF(Code.byte('{'),language))....?
#CONTEXT.add(DEF(da('{'),language))
#
#   The kernel for the language definition is defined by a sequence of rules
#   where the first rule that applies defines the language.
#
#   To compile code x, do {x}: in the language.
#
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
            if self._direction=='left':
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
        b = ''
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
