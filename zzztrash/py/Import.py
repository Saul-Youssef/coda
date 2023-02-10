#
#     Tools for importing definition-rich data
#
from base import *
#
#   The home directory of the currently running software
#
#   demo: home:
#   demo: dirpath : home :
#
def home(A,B):
    import inspect
    path = inspect.getabsfile(home)
    path = '/'.join(path.split('/')[:-2])
    return data(path.encode())
DEF.add(data(b'home'),home)
#
#   The startup directory of the currently running software
#
#   Make a file coda.co in this directory to create startup
#   data for the interpreter
#
#   demo: start:
#   demo: dirpath : start :
#
def start(A,B):
    import os
    path = os.path.expanduser('~')
    path = os.path.join(path,'.coda')
    return data(path.encode())
DEF.add(data(b'start'),start)

def startcontext(A,B):
    src = b'coda : source : readpath : endswith </coda.co> : dir co : start : '
    return data(src)
DEF.add(data(b'startcontext'),startcontext)

def homecontext(A,B):
    src = b'coda : source : readpath : dir co : endswith </co> : dir : home :'
    return data(src)
DEF.add(data(b'homecontext'),homecontext)
