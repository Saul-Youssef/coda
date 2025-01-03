


def eval_0(context,domain,A,B):
    if context.rigid(A):
        import Number
        n = Number.intdef(1,A)

def eval_data(context,D):
    L = []
    for d in D:
        for c in eval_coda(context,d): L.append(c)
    return data(*L)

def eval_coda(context,d):
    if d.domain()==da('with'): ... 
    if d in context: return context(d.left()|eval_data(context,d.right()))
    return data(d)

def eval_iter(n,context,D):
    D2 = eval_data(context,D)
    if n<=0 or D==D2: return D2
    else            : return eval_iter(n-1,context,D2)

def eval_0(context,domain,A,B):
    if context.rigid(A) and


def eval_0(context,domain,A,B):
    if context.rigid(A) and context.rigid(B):
        import Number
        n = Number.intdef(1,A)
        if all(b.domain()==da('with') for b in B)          \
               and  all(b.left().rigid() for b in B)       \
               and  all(context.joinable(b.arg()) for b in B):
            L = []
            for b in B:
                newcontext = context.join(b.arg())
                D = eval_iter(n,newcontext,b.right())
                L.append(b.left()|eval_iter(n,newcontext,b.right()))
            return data(*L)
CONTEXT.define('eval',eval_0)

CONTEXT.define('with')
