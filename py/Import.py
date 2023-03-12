#
#     Tools for importing definition-rich data
#
from base import *
#
#   The home directory of the currently running software
#
#   demo: home:
#   demo: dir : home :
#
def home(domain,A,B):
    import inspect
    path = inspect.getabsfile(home)
    path = '/'.join(path.split('/')[:-2])
    return da(path)
CONTEXT.define('home',home)
#
#   The startup directory of the currently running software
#
#   Make a file coda.co in this directory to create startup
#   data for the interpreter
#
#   demo: start:
#   demo: dir : start :
#
def start(domain,A,B):
    import os
    path = os.path.expanduser('~')
    path = os.path.join(path,'.coda')
    return da(path)
CONTEXT.define('start',start)

def startcontext(domain,A,B):
    import Language
    src = 'codx : source : readpath : endswith </coda.co> : dir co : start : '
    return Language.lang(src,data(),data())
CONTEXT.define('startcontext',startcontext)

def homecontext(domain,A,B):
    import Language
#    src = 'coda : source : readpath : dir co : endswith </co> : dir : home :'
    src = 'codx : source : readpath : dir co : endswith </co> : dir : home :'
    return Language.lang(src,data(),data())
CONTEXT.define('homecontext',homecontext)
