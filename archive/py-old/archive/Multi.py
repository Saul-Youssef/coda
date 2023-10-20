
from base import *
from Log import LOG
import multiprocessing

def eval_split(B,nproc):
    n = len(B)//nproc
    Bs = [b for b in B]
    L = []
    while len(Bs)>0:
        M = []
        while len(Bs)>0 and len(M)<n: M.append(Bs.pop(0))
        if len(M)>0: L.append(data(*M))
    return L
#
#   demo: aaa
#
def eval_1(domain,A,B):
    if A.rigid():
        import Number
        ns = Number.ints(A)
        depth,nproc = 100,multiprocessing.cpu_count()-4
        while len(ns)>0: depth = ns.pop(0)
        while len(ns)>0: nproc = ns.pop(0)
        print('aaaaa',nproc)
        Bs = eval_split(B,nproc)
        print('aaaa',len(Bs),Bs[0],Bs[1])

        pool = Pool(nproc)
        LOG('multi','Number of processors',str(nproc))
        import Eval
        def Feval(D): return Eval.depth(D,depth)
        results = []
        for result in pool.imap_unordered(Feval,Bs):
            n += 1
            LOG('multi',str(n)+'...')
            results.append(result)
        L = []
        for result in results:
            for c in result: L.append(c)
        return data(*L)
def eval_0(domain,A,B):
    if B.empty(): return data()
CONTEXT.define('eval',eval_0,eval_1)
