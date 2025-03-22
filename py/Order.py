#
#
#
from base import *

#
#   less/more
#
#   demo: less a b : c d e f
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
#
#   Order operations based on the number of atoms
#   demo: le a b c : a b c d e
#   demo: le a b c : a
#   demo: ge a b c : a
#   demo: ge a b c : a b c d e
#   demo: lt a b c : a b c d
#   demo: gt a b c : a
#   demo: srt : e d c b a 
#
def lt(context,domain,A,B):
    if A.atomic(context) and B.atomic(context):
        if len(A)<len(B): return data()
        return data(data()|data())
def gt(context,domain,A,B):
    if A.atomic(context) and B.atomic(context):
        if len(A)>len(B): return data()
        return data(data()|data())
def le(context,domain,A,B):
    if A.atomic(context) and B.atomic(context):
        if len(A)<=len(B): return data()
        return data(data()|data())
def ge(context,domain,A,B):
    if A.atomic(context) and B.atomic(context):
        if len(A)>=len(B): return data()
        return data(data()|data())
CONTEXT.define('le',le)
CONTEXT.define('ge',ge)
CONTEXT.define('lt',lt)
CONTEXT.define('gt',gt)

def text_sort(context,domain,A,B):
    if B.atomic(context):
        txts = [str(b) for b in B]
        txts.sort()
        return data(*[co(txt) for txt in txts])
CONTEXT.define('srt',text_sort)
