#
#    Text colors and styles
#
ESC = '\x1b'
colors = {'default':'','red':'31','white':'37','green':'32','yellow':'33','blue':'34','magenta':'35','cyan':'36'}
styles = {'default':'','bold':';1','underline':';4','blink':';5','reversevideo':';7','concealed':';8'}

def decorate(txt,color='default',style='default'):
    return ESC+'['+colors[color]+styles[style]+'m'+txt+ESC+'[0m'

#from base import *
#import Code
if __name__=='__main__':
    t = '@@@'
    print(t)
    print(decorate(t,'red'))
    print(decorate(t,'blue','bold'))
