#
#    Compiler
#
from base import *
#
#    The coda language compiler
#
special_characters = ' :(){}<>=*+/'
#
#   lang takes unicode string code and data A,B and makes it into
#   the corresponding data for the compiler.
#
def lang(code,A,B): return data((da('{'+code+'}')+A)|B)

def src(domain):
    s = str(domain)
    if s.startswith('{') and s.endswith('}'): return s[1:-1]
    return ''
    raise error('Unexpected language input ['+s+']')

def escape(s):
    if len(s)==2 and s[0]=='\\' and s[1]=='n': return '\n'
    return s

def language(context,domain,A,B):
    s = src(domain)
    if s.startswith(' '): return lang(s[1:  ],A,B)
    if s.endswith  (' '): return lang(s[ :-1],A,B)
    if s== '': return data()
    if s=='A': return A
    if s=='B': return B
#
#   The essential operations are concatenation and colon.  The rest is syntactic sugar.
#
    Colon = parse(':',s,'left')
    if Colon():
        front,back = Colon.parts()
        return data(lang(front,A,B)|lang(back,A,B))
#
#   A=B -> (= A:B)
#
    Equal = parse('=',s,'left')
    if Equal():
        front,back = Equal.parts()
        return data((da('equal')+lang(front,A,B))|lang(back,A,B))
#
#   A+B -> (+ A:B)
#
    Sum = parse('+',s,'left')
    if Sum():
        front,back = Sum.parts()
        return data((da('plus')+lang(front,A,B))|lang(back,A,B))
#
#   A+B -> (+ A:B)
#
    Star = parse('*',s,'left')
    if Star():
        front,back = Star.parts()
        return data((da('star')+lang(front,A,B))|lang(back,A,B))
#
#   A B -> A B
#
    Space = parse(' ',s,'left')
    if Space():
        front,back = Space.parts()
        return lang(front,A,B)+lang(back,A,B)
#
#   A/B -> (/ A:B)
#
    Slash = parse('/',s,'right')
    if Slash():
        front,back = Slash.parts()
        return data((da('slash')+lang(front,A,B))|lang(back,A,B))
#
#   Operations are grouped with parenthesis.  Text within curly brackets is source code.
#   Text between angle brackets are byte strings.
#
    if s.startswith('(') and s.endswith(')'): return lang(s[1:-1],A,B)
    if s.startswith('{') and s.endswith('}') and balanced(s[1:-1]): return da(s)
    if s.startswith('<') and s.endswith('>'): return da(escape(s[1:-1]))
#
#   A bit of syntactic sugar to make x? -> (?:x) etc.
#
    if s.endswith('?') and len(s)>1: return data(da(s[:-1])|data())
#
#   There are no syntax errors.  All byte strings are valid source code.
#
    return da(s)
CONTEXT.define('language',language)
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
    for c in code:
        if   c=='(' and ncurly==0: npar +=  1
        elif c==')' and ncurly==0: npar += -1
        elif c=='{': ncurly +=  1
        elif c=='}': ncurly += -1
        if npar<0 or ncurly<0: break
    nangle = 0
    for c in code:
        if   c=='<': nangle +=  1
        elif c=='>': nangle += -1
    return npar==0 and ncurly==0 and nangle==0
