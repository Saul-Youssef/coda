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
def readpath_0(A,B):
    if B.empty(): return data()
def readpath_1(A,B):
    I,R = B.split()
    if I.atom():
        for i in I:
            try:
                Help.SOURCES.append(Help.SourceFile(i.decode()))
                bytes = open(i.decode(),'r').read()
                return data(bytes.encode())+one(b'readpath',A,R)
            except IOError:
                raise error('Error reading file ['+i.decode()+']')
DEF.add(data(b'readpath'),readpath_1,readpath_0)
#
#   dir selects paths from it's input.  The argument
#   filters for file extensions.
#
#   demo: dir : .
#   demo: dir co da : .
#   demo: read : dir da : .
#
def Dir(A,B):
    I,R = B.split()
    if A.decided() and I.atom() and is_code(I[0]):
        path = I[0].decode()
        import os
        try:
            paths = [os.path.join(path,f).encode() for f in os.listdir(path)]
            extensions = [a for a in A if is_code(a)]
            paths2 = []
            for path in paths:
                if any([path.endswith(b'.'+ext) for ext in extensions]): paths2.append(path)
            if len(extensions)==0:
                return data(*paths) + one(b'dir',A,R)
            else:
                return data(*paths2) + one(b'dir',A,R)
        except IOError:
            pass
def Dir_0(A,B):
    if B.empty(): return data()
DEF.add(data(b'dir'),Dir,Dir_0)

def pickle_out(A,B):
    A0,AR = A.split()
    A1,AR = AR.split()
    if A0.atom() and A1.atom():
        import Number
        if len(Number.ints(A0))>0:
            n = Number.ints(A0)[0]
            if is_code(A1[0]):
                path = A1[0]
                import pickle
                import Evaluate
                with open(path,'wb') as f:
                    D = Evaluate.generic(B,n)
                    f.write(pickle.dumps(D))
                    return data()
def pickle_out_0(A,B):
    if B.empty(): return data()
#DEF.add(data(b'pickle_out'),pickle_out,pickle_out_0)
def pickle_in(A,B):
    B0,BR = B.split()
    if B0.atom():
        if is_code(B0[0]):
            path = B0[0]
            with open(path,'rb') as f:
                import pickle
                D = pickle.loads(f.read())
                return D + one(b'pickle_in',A,BR)
def pickle_in_0(A,B):
    if B.empty(): return data()
#DEF.add(data(b'pickle_in'),pickle_in,pickle_in_0)
