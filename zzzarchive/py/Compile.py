#
#    Compile
#
from base import *
#
#    coda compiles input code using the language.
#
#    coda : x y z -> (x:) (y:) (z:).. etc.
#
#    demo: coda : <rev : a b c>
#    demo: coda : <defs:>
#
count = 0

def coda_0(A,B):
    BL,BR = B.split()

def coda_1(A,B):
    global count
    I,R = B.split()
    if I.atom():
        source = I[0]
        count += 1
        if is_code(source): return one(b'{'+source+b'}',data(),data()) + one(b'coda',A,R)
def coda_0(A,B):
    if B.empty(): return data()
DEF.add(data(b'coda'),coda_1,coda_0)

#
#   compile source code block from a file
#   after removing comments and using
#   indentation for continuation.
#
def coda(txt):
    import Help,Language
    for t in Help.blocks(Help.comments(txt)): yield Language.lang(t,data(),data())
