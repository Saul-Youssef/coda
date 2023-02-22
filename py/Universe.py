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
def universe(width,depth):
    U = [data()]; T = U[:]
    for i in range(depth):
        T = G(T,width)
        U.extend(T)
    return U

def G(L,width):
    L2 = []
    from itertools import product
    for w in range(1,width+1):
        for p in product(L,repeat=w): L2.append(data(*p))
    return L2

def data_depth(n):  # data with depth <= n
    if n==0: 
        return [data()]
    else:
        
        
    