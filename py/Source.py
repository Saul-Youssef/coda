#
#    Home directory of the installation, source code compilation into data.
#
from base import *

def localdef(context,domain,A,B):
#    code = 'coda : source : readpath : dir co : endswith </co> : dir : home : '
    code = 'coda : source : readpath : dir co : down1 co : home : '
    import Language
    return Language.lang(code,data(),data())
CONTEXT.define('localdef',localdef)
#
#   Compile input text source code into data.
#
#   demo: wrap [] : source : readpath : first 2 : dir co : endswith </co> : dir : home :
#   demo: coda : source : readpath : first 2 : dir co : endswith </co> : dir : home :
#   demo: wrap [] : source : readpath : first 2 : dir co : down1 co : home:
#
def coda(context,domain,A,B):
    BL,BR = B.split()
    if BL.atom(context) and BL[0].domain()==data(BIT1):
        import Language
        D = Language.lang(str(BL[0]),data(),data())
        return Language.lang(str(BL[0]),data(),data()) + data((domain+A)|BR)
def coda_0(context,domain,A,B):
    if B.empty(): return data()
CONTEXT.define('coda',coda,coda_0)
#
#   Get source code blocks with indentation and removing comments
#
#   demo: source : readpath : first 2 : dir co : endswith </co> : dir : home :
#   demo: wrap [] : source : readpath : first 2 : dir co : endswith </co> : dir : home :
#
def source(context,domain,A,B):
    BL,BR = B.split()
    if BL.atom(context):
        txt = str(BL)
        import Help
        return data(*([co(t) for t in Help.blocks(Help.comments(txt))] + [(domain+A)|BR]))
def source_0(context,domain,A,B):
    if B.empty(): return data()
CONTEXT.define('source',source,source_0)
#
#   The startup directory of the currently running software
#
#   Make a file coda.co in this directory to create startup
#   data for the interpreter
#
#   demo: start:
#   demo: dir : start :
#

#
#   The home directory of the currently running software
#
#   demo: home:
#   demo: dir : home :
#   demo: dir co : endswith </co> : dir : home:
#
def home(context,domain,A,B):
    import inspect
    path = inspect.getabsfile(home)
    path = '/'.join(path.split('/')[:-2])
    return da(path)
CONTEXT.define('home',home)
