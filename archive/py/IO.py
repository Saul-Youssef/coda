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
def readpath_0(domain,A,B):
    if B.empty(): return data()
def readpath_1(domain,A,B):
    BL,BR = B.split()
    if BL.atom():
        try:
            path = str(BL)
            Help.SOURCES.append(Help.SourceFile(path))
            bytes = open(path,'r').read()
            return da(bytes) + data((domain+A)|BR)
        except IOError:
            raise error('Error reading file ['+path+']')
CONTEXT.define('readpath',readpath_1,readpath_0)
#
#   dir selects paths from it's input.  The argument
#   filters for file extensions.
#
#   demo: dir : .
#   demo: dir co da py : .
#
def Dir(domain,A,B):
    BL,BR = B.split()
    if BL.atom() and all([a.atom() for a in A]):
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
            raise
def Dir_0(domain,A,B):
    if B.empty(): return data()
CONTEXT.define('dir',Dir,Dir_0)
#
#   Serialize input after evaluating to argument specified depth
#
#   demo: dir : .
#
def out(domain,A,B):
    if len(A)>0 and all([a.atom() for a in A]):
        path = str(A[0])
        import Number,Evaluate
        ns = Number.ints(A)
        depth = Evaluate.DEPTH
        if len(ns)==1 and ns[0]>0: depth = ns[0]
        try:
            import os
            dir = os.path.dirname(path)
            if os.path.exists(dir):
                with open(path,'wb') as f:
                    import pickle
                    f.write(pickle.dumps(Evaluate.depth(B,depth)[0]))
                    return data()
        except Exception as e:
            raise error("Error writing to ["+path+"]: ["+str(e)+"]")
CONTEXT.define('out',out)

def In_1(domain,A,B):
    BL,BR = B.split()
    if BL.atom(): return ((domain+A)|BL) + ((domain+A)|BR)
def In_2(domain,A,B):
    if B.atom():
        path = str(B[0])
        import os
        if os.path.exists(path):
            with open(path,'rb') as f:
                import pickle
                return pickle.loads(f.read())
def In_0(domain,A,B):
    if B.empty(): return data()
CONTEXT.define('in',In_2,In_0,In_1)
