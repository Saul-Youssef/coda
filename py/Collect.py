#
#    Collect and equivalence classes
#
from base import *
#
#   Collect inputs b with the same value of (A:b).
#
#   1. Equivalence classes of input codes.
#   2. Same as 1 with collected value (bin V:...)
#   3. Codes with the same length as byte sequences.
#   4. Same as 3 with the length (bin L:..codes with length L..)
#
#   demo: equiv : a b a b a a a x
#   demo: collect : a b a b a a a x
#   demo: get ((:):(:)) : a b aa bb aaa cccc zz xxx xxx
#   demo: equiv {count:get ((:):(:)):B} : a b aa bb aaa cccc zz xxx xxx
#   demo: collect {count:get ((:):(:)):B} : a b aa bb aaa cccc zz xxx xxx
#   demo: counts {count:get ((:):(:)):B} : a b aa bb aaa cccc zz xxx xxx
#
def equiv(domain,A,B):
    if all([b.atom() for b in B]):
        classes = {}
        if A.empty(): A = da('pass')
        for b in B:
            equiv = data(A|data(b))
            import Evaluate
            equiv = Evaluate.resolve(equiv,500)
            if not equiv in classes: classes[equiv] = []
            classes[equiv] = classes[equiv] + [b]
        if not None in classes:
            L = []
            for equiv,cls in classes.items(): L.append(da('bin')|data(*cls))
            return data(*L)
def equiv_0(domain,A,B):
    if B.empty(): return data()
#CONTEXT.define('equiv',equiv,equiv_0)
def collect(domain,A,B):
    if all([b.atom() for b in B]):
        classes = {}
        if A.empty(): A = da('pass')
        for b in B:
            equiv = data(A|data(b))
            import Evaluate
            equiv = Evaluate.resolve(equiv,500)
            if not equiv in classes: classes[equiv] = []
            classes[equiv] = classes[equiv] + [b]
        if not None in classes:
            L = []
            for equiv,cls in classes.items(): L.append((da('bin')+equiv)|data(*cls))
            return data(*L)
def collect_0(domain,A,B):
    if B.empty(): return data()
#CONTEXT.define('collect',collect,collect_0)
def counts(domain,A,B):
    if all([b.atom() for b in B]):
        classes = {}
        if A.empty(): A = da('pass')
        for b in B:
            equiv = data(A|data(b))
            import Evaluate
            equiv = Evaluate.resolve(equiv,500)
            if not equiv in classes: classes[equiv] = []
            classes[equiv] = classes[equiv] + [b]
        if not None in classes:
            L = []
            for equiv,cls in classes.items(): L.append((da('bin')+da(str(len(cls))))|data(*cls))
            return data(*L)
def counts_0(domain,A,B):
    if B.empty(): return data()
#CONTEXT.define('counts',counts,counts_0)
