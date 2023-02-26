#
#    Compile
#
from base import *
import Code,Language
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
    if BL.atom(): return Language.lang(Code.pretty(BL),data(),data()) + data((domain+A)|BR)
def coda_0(domain,A,B):
    if B.empty(): return data()
CONTEXT.define('coda',coda_1,coda_0)


