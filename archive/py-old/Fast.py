#
#    General function accelerator
#
class Function(object):
    def __init__(self,F):
        self._function = F
        self._cache = {}
    def __call__(self,*X):
        if X in self._cache:
            return self._cache[X]
        else:
            FX = self._function(*X)
            self._cache[X] = FX
            return FX

if __name__=='__main__':
    def F(x,y): return x+y
    FF = FastFunction(F)
    print(FF(2,5))
