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

def codx(domain,A,B):
    if all([b.atom() for b in B]):
        for b in B:
            txt = str(b)
            for d in coda(txt):
                import Evaluate
                r = Evaluate.resolve(d,100)
                if r is None: raise error("Did not fully resolve ["+txt+"]")
        return data()
def codx_0(domain,A,B):
    if B.empty(): return ()
CONTEXT.define('codx',codx,codx_0)
