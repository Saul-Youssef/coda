#
#    Logging system
#
from base import *

class Log(object):
    def __init__(self): self._status = {}  # name->On/Off
    def __repr__(self): return ', '.join(['/'.join([key,str(value)]) for key,value in self._status.items()])
    def register(self,name): self.off(name); return self
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
        import IO
        message = 'log>'+name+': '+' '.join(msgs)
        if name in self and self[name]: IO.OUT(message+'\n')
        return self
    def logs(self):
        for name in self._status.keys(): yield name

LOG = Log()

#CONTEXT.define('log')  # logging option

#def logs(domain,A,B):
#    def stat(l):
#        if l: return 'on'
#        else: return 'off'
#    L = [(co('log')+co(name))|da(stat(status)) for name,status in LOG]
#    return data(*L)
#CONTEXT.define('logs',logs)

def log_on(domain,A,B):
    if B.rigid():
        for b in B:
            if str(b) in LOG: LOG.on(str(b))
        return data()
def log_off(domain,A,B):
    if B.rigid():
        for b in B:
            if str(b) in LOG: LOG.off(str(b))
        return data()
#CONTEXT.define('log+',log_on)
#CONTEXT.define('log-',log_off)

if __name__=='__main__':
    LOG.register('test').on('test')
    LOG('test','message')
    LOG.off('test')
    LOG('test','message')
