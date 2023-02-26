#
#    Text colors and styles
#
ESC = '\x1b'
colors = {'default':'','red':'31','white':'37','green':'32','yellow':'33','blue':'34','magenta':'35','cyan':'36'}
styles = {'default':'','bold':';1','underline':';4','blink':';5','reversevideo':';7','concealed':';8'}

def decorate(txt,color='default',style='default'):
    return ESC+'['+colors[color]+styles[style]+'m'+txt+ESC+'[0m'

from base import * 
import Code 
#
#   Wrap code with a one character prefix and postfix.
#
#   demo: wrap [] : xxx
#   demo: wrap | : xxx
#   demo: wrap <()> : xxx
#   demo: wrap <{}> : xxx
#   demo: wrap <<>> : xxx
#
def wrap(domain,A,B):
    A0,AR = A.split()
    B0,BR = B.split()
    if A0.atom() and B0.atom():
        w = Code.pretty(A0); txt = Code.pretty(B0)
        if w=='':
            l,r = '',''
        else:
            l,r = w[0],w[-1]
        return da(l+txt+r) + data((domain+A)|BR) 
def wrap_0(A,B):
    if B.empty(): return data()
CONTEXT.define('wrap',wrap,wrap_0)
#
#   Selects codes that start/end with argument specified pre or post code
#
#   demo: startswith xy : xyaaa xbbbx yzzz xycccx
#   demo: startswith x y : xyaaa xbbbx yzzz xycccx
#   demo: startswith <x y> : <x yaaa> <x ybbb> xxx
#   demo: endswith x : xyaaa xbbbx xycccx
#
def startswith(domain,A,B):
    if all([a.atom() for a in A]):
        BL,BR = B.split()
        if BL.atom():
            print('aaaaaa',A)
            pre = [Code.pretty(data(a)) for a in A]
            print('aaaaa',len(pre),pre)
            txt = Code.pretty(BL)
            if any([txt.startswith(p) for p in pre]):
                return BL + data((domain+A)|BR)
            else:
                return      data((domain+A)|BR) 
def startswith_0(domain,A,B):
    if B.empty(): return data()
CONTEXT.define('startswith',startswith,startswith_0) 

#def endswith(A,B):
#    AL,AR = A.split()
#    BL,BR = B.split()
#    if AL.atom() and BL.atom():
#        pre = codes(AL)
#        if len(pre)==1:
#            txt = pre.pop()
#            ts = codes(BL)
#            if len(ts)==1:
#                if ts[0].endswith(txt): return BL + one(b'endswith',AL,BR)
#                else                  : return      one(b'endswith',AL,BR)
#def endswith_0(A,B):
#    if B.empty(): return data()
#DEF.add(data(b'endswith'),endswith,endswith_0)


if __name__=='__main__':
    t = '@@@'
    print(t)
    print(decorate(t,'red'))
    print(decorate(t,'blue','bold'))
