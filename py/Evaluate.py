#
#   Simple evaluation recursively using
#   definitions to a specified depth, 
#   quitting if there is no progress.
#
def depth(D,n):
    if n<=0:
        return D,n
    else:
        D2 = D.eval()
        if D==D2: return D2,n
        return depth(D2,n-1)
#
#   Resolve is the same as depth 
#   but returns None if the input 
#   data has not converged.
#
def resolve(D,n):
    D2,n = depth(D,n)
    if n>0: return D2
