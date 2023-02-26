#
#   I/O function
#
from base import *
import Help
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
            p = os.path.abspath(p)
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
#def pickle_out(domain,A,B):
#    A0,AR = A.split()
#    A1,AR = AR.split()
#    if A0.atom() and A1.atom():
#        import Number
#        if len(Number.ints(A0))>0:
#            n = Number.ints(A0)[0]
#            if is_code(A1[0]):
#                path = A1[0]
#                import pickle
#                import Evaluate
#                with open(path,'wb') as f:
#                    D = Evaluate.generic(B,n)
#                    f.write(pickle.dumps(D))
#                    return data()
#def pickle_out_0(domain,A,B):
#    if B.empty(): return data()
#DEF.add(data(b'pickle_out'),pickle_out,pickle_out_0)
#def pickle_in(domain,A,B):
#    B0,BR = B.split()
#    if B0.atom():
#        if is_code(B0[0]):
#            path = B0[0]
#            with open(path,'rb') as f:
#                import pickle
#                D = pickle.loads(f.read())
#                return D + one(b'pickle_in',A,BR)
#def pickle_in_0(domain,A,B):
#    if B.empty(): return data()
#DEF.add(data(b'pickle_in'),pickle_in,pickle_in_0)
