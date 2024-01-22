#
#   I/O function
#
from base import *
import Help

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
def readpath_0(context,domain,A,B):
    if B.empty(): return data()
def readpath_1(context,domain,A,B):
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
CONTEXT.define('readpath',readpath_1,readpath_0)
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
#   Serialize input after evaluating to argument specified depth
#
#   out file1 : a b c
#   in : file1
#   out file2 : (defs:) nat : 0
#   in : file1 file2
#
def Out(context,domain,A,B):
    if A.rigid(context) and len(A)==1:
        path = str(A[0])
        import os,pickle
        try:
            with open(path,'wb') as f:
                f.write(pickle.dumps(B))
                return data()
        except Exception as e:
            return
CONTEXT.define('out',Out)

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
                    print(word('with',A),word('atomic',A),word('stable',A),'aaaaa')
                    if True or word('with',A):
                        for d in D: R.append(da('with')|data(d))
                    elif word('atomic',A):
                        for d in D:
                            if d.atom(context): R.append(d)
                    elif word('stable',A):
                        for d in D:
                            if d.stable(context): R.append(d)
                    else:
                        for d in D: R.append(d)
            return data(*R)
        except Exception as e:
            return
CONTEXT.define('in',IN)
