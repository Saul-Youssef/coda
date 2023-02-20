#
#     Substitute for specified colons recursively
#
from base import *

class Substitute(object):
    def __init__(self):
        self._substitute = {}
    def add(self,col,substitute_data):
        self._substitute[col] = substitute_data
        return self 
    def var(self,name,substitute_data):
        col = colon(data(b'?'),data(name.encode()))
        self.add(col,substitute_data)
        return self
    def __call__(self,D):
        L = []
        for d in D:
            if d in self._substitute:
                for dd in self.substitute_data(d): L.append(dd)
            elif is_code(d):
                L.append(d)
            else:
                dd = colon(self(d.left()),self(d.right()))
                L.append(dd)
        return data(*L)
    def substitute_data(self,d): return self._substitute[d]

if __name__=='__main__':
    D = data(colon(data(b'?'),data(b'x')))
    S = data(b'1',b'2',b'3',b'4')
    print(D)
    Sub = Substitute()
    Sub.add(colon(data(b'?'),data(b'x')),S)
    D2 = D+D
    print(Sub(D2))
