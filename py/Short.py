#
#   Shortened named codas
#
from base import *
import Sample

SH = []
for D in Sample.pure(2,2): SH.append(data(ATOM)|D)

n = 0
SH.pop(0)
SH.pop(0)
for D in SH:
    n += 1
    print(n,repr(D))

#UNICODE.setatom(SH[2],'bool')
#UNICODE.setatom(SH[3],'=')
#UNICODE.setatom(SH[4],'not')

#import Define
#CONTEXT.add(SH[2],Define.PartialFunction(da('bool')))

#import Sample
#
#SAMPLE = Sample.pure(2,2)
#n = 0
#Shorts = []
#for s in SAMPLE:
#    S = data(ATOM)|s
#    n += 1
##    print(n,repr(S))
#    if n>2:
#        print(n-2,repr(S))
#        Shorts.append(S)
#    if n>20: break
#
#n = 0
#for D in SHORTS:
#    n += 1
#    print(n,repr(D))

#UNICODE.setatom(data(ATOM)|data(*[ATOM,ATOM]),'bool')
#UNICODE.setatom(data(ATOM)|data(*[ATOM,ATOM]),'bool')
