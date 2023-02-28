#
#    Compile
#
from base import *
import Language
#
#    coda compiles input code using the language.
#
#    coda : x y z -> (x:) (y:) (z:).. etc.
#
#    demo: coda : <rev : a b c>
#    demo: coda : <defs:>
#
def coda_1(domain,A,B):
    BL,BR = B.split()
    if BL.atom():
        L = []
        for d in coda(str(BL)):
            for c in d: L.append(c)
        return data(*L) + data((domain+A)|BR)
def coda_0(domain,A,B):
    if B.empty(): return data()
CONTEXT.define('coda',coda_1,coda_0)
#        return Language.lang(str(BL),data(),data()) + data((domain+A)|BR)
#
#   compile source code block from a file
#   after removing comments and using
#   indentation for continuation.
#
def coda(txt):
    import Help,Language
    for t in Help.blocks(Help.comments(txt)): yield Language.lang(t,data(),data())
