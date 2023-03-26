#
#   This is some hacky code for getting comments, demos etc.
#   from python and/or coda source code files.
#
from base import *
import IO

#
#   Help system
#
#   demo: help : n
#   demo: help : <=>
#   demo: help : <|>
#   demo: demo n : 2
#   demo: help : Sequence
#
def help(domain,A,B):
    I,R = B.split()
    if I.atom():
        if I[0] in CONTEXT:
            import Code
#            H = Help(Code.coda2str(I[0]))
            H = Help(str(I[0]))
            H.display()
            return data()
    else:
        return data(domain|da('help'))
CONTEXT.define('help',help)

#
#
def sources(A,B):
    for S in SOURCES: print(S)
    return data()
#DEF.add(data(b'sources'),sources)
#
#    classes to hold coda source code sections, i.e. either comment blocks
#    or multi-line source code blocks (which are really one line).  The
#    reason do to it like this is to associate each source code block with
#    the first comment block above it in the file.
#
class Block(object):
    def __init__(self,lines):
        self._lines = lines
    def __iter__(self):
        for line in self._lines: yield line
    def body(self):
        bdy = []
        for line in self:
            while line.startswith('#'): line = line[1:]
#            line = line.strip()
            if not line=='' and not 'demo:' in line: bdy.append(line)
        return bdy[:]
    def display(self):
        IO.OUT('==============================================='+'\n')
#        print('===============================================')
#        print(str(self))
        IO.OUT(str(self)+'\n')
class Comment(Block):
    def __str__(self): return 'COMMENT:'+'\n'+'\n'.join(self._lines)
    def display(self):
#        print('===============================================')
#        print('COMMENT TITLE:',self.title()); n = 1
        IO.OUT('==============================================='+'\n')
        IO.OUT('COMMENT TITLE:',self.title()+'\n'); n = 1
        for demo in self.demos():
#            print(n,'....',demo)
            IO.OUT(str(n)+'....'+' '+str(demo)+'\n')
            n += 1
    def body(self):
        bdy = []
        for line in self:
            while line.startswith('#'): line = line[1:]
            line = line.strip()
            if not line=='' and not 'demo:' in line \
                            and not 'flag:' in line : bdy.append(line)
        return bdy[1:]
    def title(self):
        for line in self:
            while line.startswith('#'): line = line[1:]
            if not line.strip()=='': return line.strip()
    def flags(self):
        flgs = []
        for line in self:
            if 'flag:' in line:
                Fs = line.split('flag:')[-1].strip().split(' ')
                Fs = [f for f in Fs if not f=='']; flgs.extend(Fs)
        return flgs
    def demos(self):
        demos = []
        for line in self._lines:
            if 'demo:' in line: demos.append(line.split('demo:')[-1].strip())
        return demos
class Coda(Block):
        def __str__(self): return 'CODA:'+'\n'+'\n'.join(self._lines)
        def display(self):
#            print(str(self))
#            print('Flags:',','.join(self.flags()))
            IO.OUT(str(self)+'\n')
            IO.OUT('Flags:'+' '+','.join(self.flags())+'\n')
        def flags(self):
            F = []
            for line in self:
                if line.startswith('def '):
                    flag = line.split('def ')[-1].split(':')[0].strip()
                    F.append(flag)
                elif line.startswith('var '):
                    line = line.split('var ')[-1].strip()
                    if line.startswith('('):
                        flag = line[1:].split(')')[0].replace(' ','').strip()
                        F.append('('+flag+')')
                    else:
                        flag = line.split(' ')[0]
            return F

class Python(Block):
        def __str__(self): return 'PYTHON:'+'\n'+'\n'.join(self._lines)
        def display(self):
#            print(str(self))
#            print('Flags:',','.join(self.flags()))
            IO.OUT(str(self)+'\n')
            IO.OUT('Flags:'+' '+','.join(self.flags())+'\n')
        def flags(self):
            F = []
            for line in self:
                if line.startswith('CONTEXT.define') and "define('" in line:
                    flag = line.split("define('")[-1].split("'")[0]
                    F.append(flag)
            return F

class SourceFile(object):
    def __str__(self): return self._path+':'+', '.join(self.flags())
    def __init__(self,path):
        self._path = path
        self._ext  = path.split('.')[-1]
        f = open(path,'r')
        self._text = f.read()
        f.close()
        self._seps = separate(self._text)
        self._blocks = []
        for sep in self._seps:
            if len(sep.strip())>0:
                lines = sep.split('\n')
                if ''.join(lines).strip().startswith('#'):
                    self._blocks.append(Comment(lines))
                elif self._ext=='py':
                    self._blocks.append(Python(lines))
                elif self._ext=='co':
                    self._blocks.append(Coda(lines))
                else:
                    raise error('Unexpected file type ['+self._ext+']')
        self._flag2block   = {}  # text flag -> corresponding block
        self._flag2comment = {}  # text flag -> corresponding comment block
        self.init_db()
    def __contains__(self,flag):
        return flag in self._flag2block
    def __iter__(self):
        for block in self._blocks: yield block
    def init_db(self):
        blocks = self._blocks[:]
        last_comment = None
        for block in blocks:
            if type(block)==type(Python([])) or type(block)==type(Coda([])):
                for flag in block.flags():
                    self._flag2block[flag] = block
                    if not last_comment is None:
                        self._flag2comment[flag] = last_comment
            elif type(block)==type(Comment([])):
                for flag in block.flags():
                    self._flag2block[flag] = block
                    if not last_comment is None:
                        self._flag2comment[flag] = block
                last_comment = block
    def comment(self,flag):
        if flag in self._flag2comment : return self._flag2comment[flag]
    def block(self,flag):
        if flag in self._flag2block : return self._flag2block[flag]
    def flags(self):
        for flag in self._flag2block.keys(): yield flag
    def path(self): return self._path
#
#    separate code and comments for either coda or python source files
#
def separate(filetext):
    lines = filetext.split('\n')
    lines2 = []
    lastline = '#'
    while len(lines)>0:
        if       lastline.startswith('#') and not lines[0].startswith('#'):
            lines2.append('$$SEPARATOR$$')
        elif not lastline.startswith('#') and     lines[0].startswith('#'):
            lines2.append('$$SEPARATOR$$')
        lastline = lines.pop(0)
        lines2.append(lastline)
    return ('\n'.join(lines2)).split('$$SEPARATOR$$')

def source(domain,A,B):
    BL,BR = B.split()
    if BL.atom():
        txt = str(BL)
        return data(*([co(t) for t in blocks(comments(txt))] + [(domain+A)|BR]))
#    I,R = B.split()
#    if I.atom():
#        if is_code(I[0]):
#            txt = I[0]
#            return data(*[t for t in blocks(comments(txt))]) + one(b'source',A,R)
#        else:
#            raise error('Unexpected coda source file input')
def source_0(domain,A,B):
    if B.empty(): return data()
CONTEXT.define('source',source,source_0)

def comments(text):
    # remove comments from coda source code text
    L = text.split('\n')
    lines = []
    for l in L:
        if not l.startswith('#'):
            lines.append(l.replace('\t','    '))
    return lines

def blocks(lines):
    block = []
    for line in lines:
        if line.startswith(' '):
            block.append(line.strip())
        else:
            if len(block)>0:
                txt = ' '.join(block)
                if not txt.strip()=='': yield txt
            block = [line]
    if len(block)>0:
        txt = ' '.join(block)
        if not txt.strip()=='': yield txt

SOURCES = []

import inspect,os
path = inspect.getabsfile(sources)
pydir = '/'.join(path.split('/')[:-1])
paths = [os.path.join(pydir,f) for f in os.listdir(pydir) if f.endswith('.py')]
for path in paths: SOURCES.append(SourceFile(path))

#
#   Demos are an easy way to learn the definitions.
#
#   demo: help : n
#   demo: demo 1 : n
#   demo: demo 7 : n
#
def demo(domain,A,B):
    AL,AR = A.split()
    BL,BR = B.split()
    if (AL.atom() or AL.empty()) and BL.atom():
        H = Help(str(BL))
#        H = Help(Code.pretty(BL))
        import Number
        if not H is None and not H.comment() is None and not H.comment()=='' and len(Number.ints(AL))>0:
            ns = Number.ints(AL)
            n = ns[0]
            if n>0 and n<=len(H.comment().demos()):
                demcode = H.comment().demos()[n-1]
                import Language
                return Language.lang(demcode.strip(),data(),data())
#                return data(colon(data(b'{'+demcode.encode()+b'}'),data()))
            else:
                return data()
def demo_0(domain,A,B):
    if B.empty(): return data()
CONTEXT.define('demo',demo,demo_0)
#
#    Help object for a single flag
#
class Help(object):
    def __init__(self,flag):
        self._flag    = flag
        self._comment = None
        self._block   = None
        self._path    = None
        self._fn      = None
        self._module  = None
        for SF in SOURCES:
            if flag in SF:
                self._block   = SF.block(flag)
                self._comment = SF.comment(flag)
                self._path    = SF.path()
                self._fn      = self._path.split('/')[-1]
                self._module  = self._fn.split('.')[0]
    def __str__(self): return str(self._block)+'\n'+str(self._comment)
    def comment(self):
        if self._module is None: return ''
        return self._comment
    def module(self):
        if self._module is None: return ''
        return self._module
    def flag(self): return self._flag
    def summary(self):
        if self._comment is None: return ''
        title = self._comment.title()
        if title is None: return ''
        return title
    def display(self):
        if not self._comment is None:
            S = []
            S.append(section('code',[self._flag]))
            S.append(section('module',[self._module]))
            S.append(section('summary',[self._comment.title()]))
            S.append(section('description',self._comment.body()))
            S.append(section('path',[self._path]))
            if not self._path.endswith('py'):
                S.append(section('source code',self._block.body()))
            S.append(section('demos',self._comment.demos()))
            for s in S: s.display()

class section(object):
    def __init__(self,title,lines):
        self.title = title
        self.lines = lines
        self.indent = 4
    def display(self):
        import Text
        txt = Text.decorate(self.title+':','default','bold')
#        print(txt)
        IO.OUT(txt+'\n')
        n = 1
        for line in self.lines:
            if   self.title=='demos':
#                print(self.indent*' '+str(n)+'. '+Text.decorate(line,'magenta','underline'))
                IO.OUT(self.indent*' '+str(n)+'. '+Text.decorate(line,'magenta','underline')+'\n')
            elif self.title=='code' :
#                print(self.indent*' '+Text.decorate(line,'blue','reversevideo'))
                IO.OUT(self.indent*' '+Text.decorate(line,'blue','reversevideo')+'\n')
            else                    :
#                print(self.indent*' '+line)
                IO.OUT(self.indent*' '+line+'\n')
            n += 1
#
#   defs makes a table of available definitions.
#
#   demo: defs:
#   demo: defs : Basic
#   demo: defs : Basic Number
#
def defs(domain,A,B):
    import Code
#    modules = [Code.coda2str(b) for b in B]
    modules = [str(b) for b in B]
    table = []
    for domain,definition in CONTEXT:
#        dom = Code.pretty(domain)
        dom = str(domain)
        H = Help(dom)
        if not dom.endswith('1') and not dom.endswith('_') and len(H.summary())>2:
            if len(modules)==0 or H.module() in modules:
                table.append([H.module(),dom,H.summary(),len(definition)])
    deftable(table)
    return data()
CONTEXT.define('defs',defs)

def deftable(table):
    max_module,max_flag,max_summary = 0,0,0
    for module,flag,summary,n in table:
        if len(module)>max_module  : max_module  = len(module)
        if len(flag)  >max_flag    : max_flag    = len(flag)
        if len(summary)>max_summary: max_summary = len(summary)
    T = sorted(table)
    MARGIN = 2;
    max_module += MARGIN
    max_flag   += MARGIN
    for module,flag,summary,n in T:
        import Text
        while len(module)<max_module: module = module+'.'
        while len(flag)  <max_flag  : flag   = flag + '.'
        flag = Text.decorate(flag,'blue','bold')
        summary = Text.decorate(summary,'magenta','underline')
#        print(flag+module+str(n)+'..'+summary)
        IO.OUT(flag+module+str(n)+'..'+summary+'\n')
    IO.OUT(str(CONTEXT))

if __name__=='__main__':
    f = open('/Users/youssef/coda/co/Number.co','r')
    txt = f.read()
    S = SourceFile('/Users/youssef/coda/co/Number.co')
    for b in S: b.display()
    T = SourceFile('/Users/youssef/coda/py/Basic.py')
    for b in T: b.display()
