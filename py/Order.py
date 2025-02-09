#
#
#
from base import *

#
#   less/more
#
#   demo: less | | : | | |
#   demo: less | | | : |
#   demo: more | | : | | |
#   demo: more | | | : |
# 
def less(context,domain,A,B):
    if A.atomic(context) and B.atomic(context):
        if len(A)<len(B): return A
        return B
def more(context,domain,A,B):
    if A.atomic(context) and B.atomic(context):
        if len(A)>len(B): return A
        return B
CONTEXT.define('less',less)
CONTEXT.define('more',more)
