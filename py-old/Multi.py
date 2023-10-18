
from base import *
from Log import LOG
import Evaluate
import multiprocessing

def EVAL(D):
    D2,n = Evaluate.depth(D,500)
    return D2

def eval_split(B,nproc):
    n = max(1,len(B)//nproc)
    Bs = [b for b in B]
    split = []
    while len(Bs)>0:
        M = []
        while len(Bs)>0 and len(M)<n: M.append(Bs.pop(0))
        if len(M)>0: split.append(data(*M))
    return split
#
#   multi evaluates its input in parallel
#
#   demo: aaaa
#
def multi_1(domain,A,B):
    if A.rigid():
        import multiprocessing
        import Number
        ns = Number.ints(A)
        depth,nproc = 100,multiprocessing.cpu_count()-4
        while len(ns)>0: depth = ns.pop(0)
        while len(ns)>0: nproc = ns.pop(0)
        depth = max(1,depth)
        nproc = max(1,nproc)
# Evaluate until the language is done
        B2 = Evaluate.language(B,100)
# Evaluate until the length is at least nproc
        B3 = B2
        ntry = 0
        while True:
            B3 = B3.eval()
            ntry += 1
            if ntry>100 or len(B3)>nproc or B3==B3.eval(): break
        split = eval_split(B3,nproc)
#        print('aaaaa split',len(split))
#        for s in split: print('aaaaa s',type(s),s)
        LOG('multi','Number of processors',str(nproc))

#        for s in split: print('aaa s',s)

        from multiprocessing.pool import Pool
        pool = Pool(nproc)
#        import Eval
#        def Feval(D): return Eval.depth(D,500)
        results = []
#        print('aaaaaaa',len(split))
#        results.append(EVAL(B3))
#        for D in split:
#            results.append(EVAL(D))
        n = 0
        for result in pool.imap_unordered(EVAL,split):
            n += 1
            LOG('multi',str(n)+'...')
            results.append(result)
        L = []
        for result in results:
            for c in result: L.append(c)
        return data(*L)
def multi_0(domain,A,B):
    if B.empty(): return data()
CONTEXT.define('multi',multi_0,multi_1)
