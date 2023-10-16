#
#    Definition
#
from base import *

def define(context,domain,D,V):
    if context.atom(D) and context.rigid(D) and context.rigid(V):
        if V.empty(): context.add(D)
        else: context.add(D,lambda cont,dom,A,B: data((V+A)|B))
        return data()
CONTEXT.define('def',define)
