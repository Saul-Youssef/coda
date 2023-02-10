#
#
#    Probability search
#
from base import *
import random

EXCLUDED = ['path','read','write','stat','help','error','home','start',\
   'startcontext','homecontext','eval','evaluate','let','def','store',\
   'defs','dump','demo','pickle_in','pickle_out','pickle','readpath',\
   'dir','sources','source']
EXCLUDED = [data(x.encode()) for x in EXCLUDED]

class DataSearch(object):
    def __init__(self,lengths,codes,flags,maxdepth=5):
        self._length,self._length_wt = [],[]
        for length,weight in lengths:
            self._length.append(length)
            self._length_wt.append(weight)
        self._codes,self._code_wt = [],[]
        for code,weight in codes:
            self._codes.append(code)
            self._code_wt.append(weight)
        self._flags,self._flag_wt = [],[]
        for flag,weight in flags:
            self._flags.append(flag)
            self._flag_wt.append(weight)
        self._maxdepth = maxdepth
        self._flagnext  = [0.9,0.1]
        self._codenext  = [0.5,0.5]
    def sample(self): return self.choose_data(0)
    def choose_data(self,depth):  # generate one data
        if depth>self._maxdepth: return data()
        L = []
        for i in range(self.choose_length()):
            if self.code_next(): L.append(self.choose_code ())
            else               : L.append(self.choose_colon(depth+1))
        return data(*L)
    def choose_colon(self,depth): # generate one colon
        if random.choices([True,False],self._flagnext)[0]:
            flag = self.choose_flag()
            return colon(flag+self.choose_data(depth),self.choose_data(depth))
        else:
            return colon(self.choose_data(depth),self.choose_data(depth))

    def code_next  (self): return random.choices([True,False],self._codenext)[0]
    def flag_next  (self): return random.choices([True,False],self._flagnext)[0]

    def choose_length(self): return random.choices(self._length,self._length_wt)[0]
    def choose_code  (self): return random.choices(self._codes, self._code_wt  )[0]
    def choose_flag  (self): return random.choices(self._flags, self._flag_wt  )[0]

if __name__=='__main__':
    import __init__
    lengths = [(0,1.),(1,1.),(2,0.5),(3,0.4),(4,0.3)]
    codes = [(b'x',1.),(b'y',1.),(b'0',1.),(b'1',1.),(b'2',1.)]
    flags = [(data(),1.),(data(b'rev'),1.)]
    for flag,defs in DEF.defs():
        if not flag in EXCLUDED: flags.append((flag,1.0))
    print('Number of flags=',len(flags))
    S = DataSearch(lengths,codes,flags,5)
#    for i in range(10):
#        print(S.choose_data(0))

    import Evaluate,Logic
    stat = {'e':0,'a':0,'u':0}
    for i in range(100000):
        D = S.sample()
        D = Evaluate.generic(D,10)
        z = Logic.zen(D)
        stat[z] = stat[z] + 1
    print(stat)
