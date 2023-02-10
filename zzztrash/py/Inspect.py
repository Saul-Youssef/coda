#
#    Data inspection operations
#
from base import *
from Text import decorate
#
#   Get statistics about data
#
#   The optional argument specifies the number of generic evaluations
#   done before collecting statistics.
#
#   demo: stat : stat : sum n : first 100 : nat : 0
#   demo: stat 100 : sum n : first 100 : nat : 0
#   demo: stat 1000 : sum n : first 100 : nat : 0
#
def Stat(A,B):
    import Evaluate,Number
    As = Evaluate.generic(A,100)
    A0,Ar = As.split()
    n = 0
    if len(Number.ints(A0))>0: n = Number.ints(A0)[0]
    stat = statistic()
    stat = update_stat(Evaluate.generic(B,n),stat,0)
    stat.display()
    return data()
DEF.add(data(b'stat'),Stat)

class statistic(object):
    def __init__(self):
        self.nitems    = 0
        self.ncodes    = 0
        self.ncolons   = 0
        self.nlanguage = 0
        self.nflags    = 0
        self.flags     = {}
        self.codes     = {}
        self.language  = {}
        self.width     = 0
        self.depth     = 0
        self.variables = set([])
    def display(self):
        self.display_line('stats',self.stat_line())
        self.display_line('shape',self.shape_line())
        self.display_line('flags',self.flag_line())
        self.display_line('variables',self.variable_line())
        self.display_line('codes',self.code_line())
        self.display_line('language',self.language_line())
    def display_line(self,header,line):
        while len(header)<10: header = ' '+header
        print(decorate(header+':','default','bold'),line)
    def variable_line(self):
        L = [str(v[0].right()) for v in self.variables]
        return ', '.join([decorate(l,'blue','reversevideo') for l in L])
    def flag_line(self):
        L = []
        for flag,n in self.flags.items(): L.append((str(flag),n,))
        L.sort()
        L2 = []
        fields = []
        for fl,n in L:
            field = decorate(fl,'magenta','bold')+'/'+str(n)
            fields.append(field)
        return ', '.join(fields)
    def stat_line(self):
        fields = []
        fields.append(decorate('items','default','reversevideo')+'/'+str(self.nitems))
        fields.append(decorate('language','default','reversevideo')+'/'+str(self.nlanguage))
        fields.append(decorate('colons','default','reversevideo')+'/'+str(self.ncolons))
        fields.append(decorate('codes','default','reversevideo')+'/'+str(self.ncodes))
        return ', '.join(fields)
    def shape_line(self):
        fields = []
        fields.append('width/'+str(self.width))
        fields.append('depth/'+str(self.depth))
        return ', '.join(fields)
    def code_line(self):
        L = []
        for key,value in self.codes.items(): L.append((key,value,))
        L.sort(); L.reverse()
        M = []
        while not len(L)==0:
            key,value = L.pop()
            M.append(decorate(key.decode(),'blue','bold')+'/'+str(value))
        return ', '.join(M)
    def language_line(self):
        L = []
        for key,value in self.language.items(): L.append((key,value,))
        L.sort(); L.reverse()
        M = []
        while not len(L)==0:
            key,value = L.pop()
            M.append(decorate(key.decode(),'green','underline')+'/'+str(value))
        return ', '.join(M)

def update_stat(D,stat,depth):
    if len(D)>stat.width: stat.width = len(D)
    if depth>stat.depth: stat.depth = depth
    for d in D:
        if is_code(d): stat.ncodes += 1
        else         : stat.ncolons += 1
        stat.nitems += 1
        if is_code(d):
            if d.startswith(b'{'):
                if not d in stat.language: stat.language[d] = 0
                stat.language[d] += 1
                stat.nlanguage += 1
            else:
                if not d in stat.codes: stat.codes[d] = 0
                stat.codes[d] += 1
        for flag in data(d).flag():
            if not '{' in str(flag):
                stat.nflags += 1
                if not flag in stat.flags: stat.flags[flag] = 0
                stat.flags[flag] += 1
    for d in D:
        if is_colon(d):
            update_stat(d.left(),stat,depth+1)
            update_stat(d.right(),stat,depth+1)
            if d.left()==data(b'?'): stat.variables.add(data(d))
    return stat
