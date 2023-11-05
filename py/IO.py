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
