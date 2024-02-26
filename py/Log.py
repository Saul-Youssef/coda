#
#    Logging system
#
from base import *

class Log(object):
    def __init__(self):
        self._status = {}      # name -> On/Off
        self._description = {} # name -> description
    def __repr__(self): return ', '.join(['/'.join([key,str(value)]) for key,value in self._status.items()])
    def register(self,name,description):
        self._description[name] = description
        self.off(name); return self
    def names(self):
        for name,status in self: yield name
    def on(self,*names):
        for name in names: self._status[name] = True
        return self
    def off(self,*names):
        for name in names: self._status[name] = False
        return self
    def __contains__(self,name): return name in self._status
    def __getitem__(self,name): return self._status[name]
    def __iter__(self):
        for name,status in self._status.items(): yield name,status
    def __call__(self,name,*msgs):
        if name in self and self[name]: message(name,', '.join(msgs))
        return self
    def logging(self,*names):
        return all(name in self and self[name] for name in names)
    def logs(self):
        names = [name for name in self._status.keys()]
        names.sort()
        return names
#        for name in self._status.keys(): yield name

LOG = Log()

def message(name,msg):
    import IO
    IO.OUT(name+'> '+msg+'\n')

def logs(context,domain,A,B):
    message('logs available',' '.join(LOG.names()))
    return data()
def logging(context,domain,A,B):
    message('logging',' '.join([name for name,status in LOG if status]))
    return data()
CONTEXT.define('logging',logging)
CONTEXT.define('logs',logs)

def log_(context,domain,A,B):
    if B.empty(): return data()
    if A.rigid(context) and len(A)<=1 and B.rigid(context):
        logs = [str(b) for b in B]
        if len(A)==1 and str(A[0])=='off':
            for l in logs:
                if l in LOG: LOG.off(l)
        else:
            for l in logs:
                if l in LOG: LOG.on(l)
        return data()
CONTEXT.define('log',log_)

if __name__=='__main__':
    LOG.register('test').on('test')
    LOG('test','message')
    LOG.off('test')
    LOG('test','message')
