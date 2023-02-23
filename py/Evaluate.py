#
#   Simple evaluation recursively using
#   definitions to a specified depth
#
def depth(D,n):
    if n<=0:
        return D,n
    else:
        D2 = D.eval()
        if D==D2: return D2,n
        return depth(D2,n-1)
