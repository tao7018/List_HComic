# -*- coding: utf-8 -*- 
import urllib , requests , sys ,string ,time
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from time import gmtime, strftime

#頁顯示數量
pnum = 30
mlink = 'http://www.dlsite.com/books/'

fnkey = open('nkey.txt', 'r')
#nkey = fnkey.readline()#key=作者

###檔案化作列表
nkey=list(fnkey)
fnkey.close()

def Q2B(ustring):
    fs=u'０１２３４５６７８９ＱｑＷｗＥｅＲｒＴｔＹｙＵｕＩｉＯｏＰｐＡａＳｓＤｄＦｆＧｇＨｈＪｊＫｋＬｌＺｚＸｘＣｃＶｖＢｂＮｎＭｍ'
    hs=u'0123456789QqWwEeRrTtYyUuIiOoPpAaSsDdFfGgHhJjKkLlZzXxCcVvBbNnMm'
    rstr = ''
    for tm in ustring:
        if fs.find(tm)+1:
            tm = hs[fs.find(tm)]
        rstr = rstr + tm
    ustring = rstr
    ustring=ustring.lower()
    return ustring


####取出作者
print nkey[1][:-1]
key=nkey[1].decode('utf8')#[nkey[1].find(u'('):nkey[1].find(u')')]
gkey=key[:key.find(u'(')]
key=key[key.find(u'(')+1:key.find(u')')]
#print gkey,key,type(key)

print '\\','/'

fout = open('output/'+key + '_comiclistv1.txt', 'w')#寫入模式開檔
#fout = open('/output/'+key.decode('utf-8') + '_comiclistv1.txt', 'w')#寫入模式開檔
#fout = open(u'/out/'+key + u'_comiclistv1.txt', 'w')#寫入模式開檔
fout.write('comiclist\n')#comiclist
fout.close()

###逐字檢查，'unicode' type的b2
b2=u'喔asdらくじん児島未生'*1
print 'b2:',type(b2)
for j in b2:
    print type(j)
    #j2 = urllib.quote(j.decode('utf8'))#.encode('utf8'))
    j2 = urllib.quote(j.encode('utf8'))
    j3 = urllib.unquote(j2.decode('sjis').encode('utf8'))
    print b2.find(j),'[[',j2,']][[',j3,']][[',j,']]'
    time.sleep(.5)
    #print '\r',
'''
#當sjis輸出utf8的url
key2 = urllib.quote(key.decode('utf8').encode('sjis'))
#utf8的url翻sjis
key3 = urllib.unquote(key2.decode('sjis').encode('utf8'))
#'''
###結尾
raw_input("\nPress Any Key To Exit")

'''
##時間
print time.localtime(time.time())
print  time.asctime( time.localtime(time.time()) )
#print time.strptime("30 Nov 00", "%d %b %y")   
print gmtime()
print strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
#print time.localtime(time.time())
print strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime(time.time()))
print strftime("%a, %d %b %Y %H:%M:%S +0000")
print strftime("%Y/%m/%d,%H:%M")
print strftime("%H:%M")
#'''