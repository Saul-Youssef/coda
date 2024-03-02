#
#   I/O function
#
from base import *
import Help
from Log import LOG

LOG.register('pickle','Python pickle operation')

class Stdout(object):
    def __init__(self):
        self._mode = 'default'
        self._out = ''
    def kernel(self):
        self._mode = 'kernel' # kernel mode accumulates stdout
        return self
    def __call__(self,txt):
        if self._mode=='default':
            import sys
            sys.stdout.write(txt)
        else:
            self._out += txt
    def flush(self):
        out = self._out[:]
        self._out = ''
        return out
OUT = Stdout()
#
#   Basic local read of all the bytes from a local files
#
#   readpath : path B -> <bytes in path> (readpath : B)
#
#def readpath_0(context,domain,A,B):
#    if B.empty(): return data()
#
def readpath_1(context,domain,A,B):
    if B.empty(): return data()
    BL,BR = B.split()
    if BL.atom(context):
        try:
            path = str(BL)
            Help.SOURCES.append(Help.SourceFile(path))
            bytes = open(path,'r').read()
            return da(bytes) + data((domain+A)|BR)
        except IOError:
            return
            raise error('Error reading file ['+path+']')
CONTEXT.define('readpath',readpath_1)
#
#   dir selects paths from it's input.  The argument
#   filters for file extensions.
#
#   demo: dir : .
#   demo: dir co da py : .
#
def Dir(context,domain,A,B):
    BL,BR = B.split()
    if BL.atom(context) and all([a.atom(context) for a in A]):
        p = str(BL)
        import os
        try:
            p = os.path.abspath(os.path.expanduser(p))
            paths = [os.path.join(p,f) for f in os.listdir(p)]
            extensions = [str(data(a)) for a in A]
            paths2 = []
            if len(extensions)>0:
                for path in paths:
                    if any([path.endswith('.'+ext) for ext in extensions]): paths2.append(path)
            else:
                paths2 = paths
            return data(*[co(path) for path in paths2]) + data((da('dir')+A)|BR)
        except IOError:
            return
            raise
def Dir_0(context,domain,A,B):
    if B.empty(): return data()
CONTEXT.define('dir',Dir,Dir_0)
#
#   Write input to argument specified file
#
#   out file1 : a b c
#   in : file1
#   out file2 : nat : 0
#   in : file1 file2
#
def Out(context,domain,A,B):
    if A.rigid(context) and len(A)>=1:
        As = [str(a) for a in A]
        path = As.pop(0)
        import Evaluation
        seconds = Evaluation.SECONDS
        memory  = Evaluation.MEMORY
        if len(As)>0:
            try:
                seconds = float(As.pop(0))
            except ValueError:
                pass
        if len(As)>0:
            try:
                memory = float(As.pop(0))
            except ValueError:
                pass
        EV = Evaluation.Evaluate(context,seconds,memory)
        BE = EV(B)
        import Define
        if Define._Outfriendly(context,BE):
            import os,pickle
            try:
                with open(path,'wb') as f:
                    f.write(pickle.dumps(BE))
                    return data()
            except Exception as e:
                return
CONTEXT.define('out',Out)

class stat(object):
    def __init__(self,context):
        self._context = context
        self._stat = {}
    def update(self,D):
        for d in D: self.update_coda(d)
        return self
    def update_coda(self,d):
        if not d.domain() in self._stat: self._stat[d.domain()] = 0
        self._stat[d.domain()] += 1
        self.update(d.left()).update(d.right())
        return self
    def data(self):
        L = []
        for key,value in self._stat.items(): L.append([str(key),key,value])
        L.sort()
        return data(*[((da('bin')+da(str(n)))|dom) for s,dom,n in L])

def Stat(context,domain,A,B):
    if A.rigid(context) and B.rigid(context):
        import os,pickle
        try:
            L = []
            S = stat(context)
            for b in B:
                path = str(b)
                with open(path,'rb') as f:
                    LOG('pickle','start',path)
                    D = pickle.loads(f.read())
                    LOG('pickle','end',path)
                    S.update(D)
            return S.data()
        except Exception as e:
            LOG('error',str(e))
CONTEXT.define('stat',Stat)

def word(text,A): return text in [str(a) for a in A]
def IN(context,domain,A,B):
    if A.rigid(context) and B.rigid(context):
        import os,pickle
        try:
            R = []
            for b in B:
                path = str(b)
                with open(path,'rb') as f:
                    D = pickle.loads(f.read())
                    i = 0
                    for d in D:
                        i += 1
                    if word('with',A):
                        for d in D: R.append(da('with')|data(d))
                    elif word('atomic',A):
                        for d in D:
                            if d.atom(context): R.append(d)
                    elif word('stable',A):
                        for d in D:
                            if d.stable(context): R.append(d)
                    elif word('rigid',A):
                        for d in D:
                            if d.rigid(context): R.append(d)
                    else:
                        for d in D: R.append(d)
            return data(*R)
        except Exception as e:
            return
CONTEXT.define('in',IN)
