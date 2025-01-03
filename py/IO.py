#
#   I/O function
#
from base import *
import Help
from Log import LOG

#LOG.register('pickle','Python pickle operation')
LOG.register('turbo','Function acceleration')
LOG.register('io','I/O operations')
#
#   These have to be removed as they are not functions
#
def _data2str(context,domain,A,B):
    if B.atomic(context):
        txt = bytes(data2str(B),'utf-8')
        import zlib
        txtc = zlib.compress(txt)
        txt2 = zlib.decompress(txtc)
        return da(data2str(B))
CONTEXT.define('d2s',_data2str)
def _str2data(context,domain,A,B):
    if B.atom(context): return str2data(str(B[0]))
CONTEXT.define('s2d',_str2data)

def block(ts):
    L = []
    for t in ts: L.append(str(len(t))+' '+t)
    return ''.join(L)
def split(t):
    i = 0
    while i<len(t) and not t[i]==' ': i+=1
    n = int(t[:i])
    front = t[i+1:i+1+n]
    back  = t[i+1+n:]
    return n,front,back

def _block(ts):
    L = []
    for t in ts: L.append(bytes(str(len(t)),'utf-8')+b' '+t)
    return b''.join(L)
def _split(t):
    i = 0
    while i<len(t) and not t[i]==32: i+=1
    if not t[i]==32: raise error('File format error')
    n = int(t[:i])
    front = t[i+1:i+1+n]
    back  = t[i+1+n:]
    return n,front,back

def data2bytes(D): return _block([coda2bytes(d) for d in D])
def coda2bytes(d): return _block([data2bytes(d.left()),data2bytes(d.right())])

def data2str(D): return block([coda2str(d) for d in D])
def coda2str(d): return block([data2str(d.left()),data2str(d.right())])

import Cache
B2D = Cache.Turbo('bytes->data',1000000000)
B2C = Cache.Turbo('bytes->coda',1000000000)

def bytes2data(t):
    L = []
    while len(t)>0:
        n,front,t = _split(t)
        L.append(B2C(bytes2coda,front))
    return data(*L)
def bytes2coda(t):
    n,front,t = _split(t)
    m,back,t  = _split(t)
    if not len(t)==0: raise error('corrupted data')
    return B2D(bytes2data,front)|B2D(bytes2data,back)

def str2data(t):
    L = []
    while len(t)>0:
        n,front,t = split(t)
        L.append(str2coda(front))
    return data(*L)
def str2coda(t):
    n,front,t = split(t)
    m,back,t  = split(t)
    if not t=='': raise error('corrupted data')
    return str2data(front)|str2data(back)

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
#def Out(context,domain,A,B):
#    if A.rigid(context) and len(A)>=1:
#        As = [str(a) for a in A]
#        path = As.pop(0)
#        import Evaluation
#        seconds = Evaluation.SECONDS
#        memory  = Evaluation.MEMORY
#        if len(As)>0:
#            try:
#                seconds = float(As.pop(0))
#            except ValueError:
#                pass
#        if len(As)>0:
#            try:
#                memory = float(As.pop(0))
#            except ValueError:
#                pass
#        EV = Evaluation.Evaluate(context,seconds,memory)
#        BE = EV(B)
#        import Define
#        if True or Define._Outfriendly(context,BE):
#            import os,pickle
#            if os.path.exists(path): return # never overwrite anything
#            try:
#                with open(path,'wb') as f:
#                    f.write(pickle.dumps(BE))
#                    return data()
#            except Exception as e:
#                LOG('error','error writing to pickle file',str(e))
#CONTEXT.define('out',Out)

def word(text,A): return text in [str(a) for a in A]
#def IN(context,domain,A,B):
#    if A.rigid(context) and B.rigid(context):
#        import os,pickle
#        try:
#            R = []
#            for b in B:
#                path = str(b)
#                with open(path,'rb') as f:
#                    D = pickle.loads(f.read())
#                    i = 0
#                    for d in D:
#                        i += 1
#                    if word('with',A):
#                        for d in D: R.append(da('with')|data(d))
#                    elif word('atomic',A):
#                        for d in D:
#                            if d.atom(context): R.append(d)
#                    elif word('stable',A) or word('invariant',A):
#                        for d in D:
#                            if d.stable(context): R.append(d)
#                    elif word('rigid',A):
#                        for d in D:
#                            if d.rigid(context): R.append(d)
#                    else:
#                        for d in D: R.append(d)
#            return data(*R)
#        except Exception as e:
#            LOG('error','Error reading from pickle file',str(e))
#CONTEXT.define('in',IN)

#
#   Write input to argument specified file
#
#   write file1 : a b c
#   read : file1
#   write file2 : nat : 0
#   read : file1 file2
#
def _Out(context,domain,A,B):
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

        import os
        if os.path.exists(path): return # never overwrite anything
        try:
            with open(path,'wb') as f:
                import zlib
                LOG('io','Start reading '+path+'...')
                f.write(zlib.compress(data2bytes(BE)))
                LOG('io','Finished reading '+path)
                return data()
        except Exception as e:
            LOG('error','error writing to file',str(e))
            return
#CONTEXT.define('write',_Out)

def Write(context,domain,A,B):
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

        path_undecided = path+'.undecided'
        import os
        if os.path.exists(path): return # never overwrite anything
        if os.path.exists(path_undecided): return

        EV = Evaluation.Evaluate(context,seconds,memory)
        BE = EV(B)

        DECIDED   = []
        UNDECIDED = []
        for b in BE:
            if b.rigid(context): DECIDED.append(b)
            else               : UNDECIDED.append(b)

        try:
            with open(path,'wb') as f:
                import zlib
                LOG('io','Start writing '+path+'...')
                f.write(zlib.compress(data2bytes(data(*DECIDED))))
                LOG('io','Finished writing '+path)
#                return data()
        except Exception as e:
            LOG('error','error writing to file ',str(e))
            return
        try:
            with open(path_undecided,'wb') as f:
                import zlib
                LOG('io','Start writing '+path_undecided+'...')
                f.write(zlib.compress(data2bytes(data(*UNDECIDED))))
                LOG('io','Finished writing '+path_undecided)
                return data()
        except Exception as e:
            LOG('error','error writing to file ',str(e))
            return
CONTEXT.define('write',Write)

def _IN(context,domain,A,B):
    if A.rigid(context) and B.rigid(context):
        try:
            R = []
            for b in B:
                path = str(b)
                with open(path,'rb') as f:
                    import zlib
                    LOG('io','Start reading '+path+'...')
                    D = bytes2data(zlib.decompress(f.read()))
                    LOG('io','Finished reading '+path)
                    LOG('turbo',str(B2D))
                    LOG('turbo',str(B2C))
                    i = 0
                    for d in D:
                        i += 1
                    if word('with',A):
                        for d in D: R.append(da('with')|data(d))
                    elif word('atomic',A):
                        for d in D:
                            if d.atom(context): R.append(d)
                    elif word('stable',A) or word('invariant',A):
                        for d in D:
                            if d.stable(context): R.append(d)
                    elif word('rigid',A):
                        for d in D:
                            if d.rigid(context): R.append(d)
                    else:
                        for d in D: R.append(d)
            return data(*R)
        except Exception as e:
            LOG('error','Error reading from file',str(e))
CONTEXT.define('read',_IN)

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
        if not (d.domain()==co('a').domain()): self.update(d.left()).update(d.right())
        return self
    def data(self):
        L = []
        for key,value in self._stat.items(): L.append([str(key),key,value])
        def f(M): return M[0]
        L.sort(key=f)
        return data(*[((da('with')+da(str(n)))|dom) for s,dom,n in L])
    def __str__(self):
        L = []
        for key,value in self._stat.items(): L.append([str(key),key,value])
        def f(M): return M[0]
        L.sort(key=f)
        return ', '.join([str(dom)+'/'+str(n) for s,dom,n in L])
#
#class statNEW(object):
#    def __init__(self,context):
#        self._context = context
#        self._stat = {}
#    def context(self): return self._context
#    def update(self,D):
#        for d in D: self.update_coda(d)
#        return self
#    def update_coda(self,d):
#        if not d.domain() in self._stat: self._stat[d.domain()] = 0
#        self._stat[d.domain()] += 1
#        if not d.domain()==da('a').domain(): self.update(d.left()).update(d.right())
#        return self
#    def data(self):
#        L = []
#        for key,value in self._stat.items(): L.append([str(key),key,value])
#        def f(M): return M[0]
#        L.sort(key=f)
#        return data(*[((da('with')+da(str(n)))|dom) for s,dom,n in L])
#    def __str__(self):
#        L = []
#        for key,value in self._stat.items(): L.append([str(key),key,value])
#        def f(M): return M[0]
#        L.sort(key=f)
#        return ', '.join([str(dom)+'/'+str(n) for s,dom,n in L])

def countdata(dom,D): return sum([countcoda(dom,d) for d in D])
def countcoda(dom,d):
    n = 0
    if d.domain()==dom: n = 1
    LOG('stata',str(n))
    return n + countdata(dom,d.left()) + countdata(dom,d.right())

def Stata(context,domain,A,B):
    if A.rigid(context) and B.rigid(context):
        try:
            for b in B:
                path = str(b)
                with open(path,'rb') as f:
                    import zlib
                    LOG('io','Start reading '+path+'...')
                    D = bytes2data(zlib.decompress(f.read()))
                    LOG('io','Finished reading '+path)
                    return da(str(countdata(A,D)))
        except Exception as e:
            LOG('error','Error reading from file',str(e))
CONTEXT.define('stata',Stata)

def Stat(context,domain,A,B):
    if A.rigid(context) and B.rigid(context):
        try:
            L = []
            S = stat(context)
            for b in B:
                path = str(b)
                with open(path,'rb') as f:
                    import zlib
                    LOG('io','Start reading '+path+'...')
                    D = bytes2data(zlib.decompress(f.read()))
                    LOG('io','Finished reading '+path)
                    LOG('turbo',str(B2D))
                    LOG('turbo',str(B2C))
                    S.update(D)
            return S.data()
        except Exception as e:
            LOG('error','Error reading from file',str(e))
CONTEXT.define('stat',Stat)
