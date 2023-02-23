#
#    o A data is a finite sequence of codas.
#    o A coda is a pair of data. 
#
#    ...fix me for new codas 
#
from base import * 
#
#   Return the universe all data with width and depth less than 
#   specified values. 
#
#def universe(width,depth):
#    U = [data()]; T = U[:]
#    for i in range(depth):
#        T = G(T,width)
#        U.extend(T)
#    return U
#
#def G(L,width):
#    L2 = []
#    from itertools import product
#    for w in range(1,width+1):
#        for p in product(L,repeat=w): L2.append(data(*p))
#    return L2
#

import itertools 

def alldata(depth,width):  # all data leq specified width and depth 
    datas = []
    if depth==0:
        datas.append(data())
    else:
        codas = [c for c in allcoda(depth,width)]
        for w in range(0,width+1):
            for T in itertools.product(codas,repeat=w): datas.append(data(*T))
    return datas

def allcoda(depth,width):
    codas = []
    if depth==0:
        return (coda(data(),data()),)
    else:
        datas = [d for d in alldata(depth-1,width)]
        for T in itertools.product(datas,repeat=2): codas.append(coda(T[0],T[1]))
    return codas 