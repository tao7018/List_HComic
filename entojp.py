# -*- coding: utf-8 -*- 
import urllib , requests , sys ,string ,time
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from time import gmtime, strftime

#entojp
#fkey作者來源entojp.txt
#fcomiclist結果key_comiclist.text

#輸出格式：
#comiclist
#!作者
#!總筆數
#==類別_數量_中文敘述
#條目

#comiclist常數
pnum = 25#頁顯示數量
mlink = 'http://nhentai.net/'#前綴網址

fnkey = open('entojp.txt', 'r')
nkey=list(fnkey)###檔案化作列表
fnkey.close()
print nkey

#檢查BOM
if '%EF%BB%BF' in urllib.quote(nkey[0]):
    print 'fuck ms'

#http://nhentai.net/search/?q=linda&page=1
'''
link = "http://nhentai.net/search/?q=" + urllib.quote(key) + "&page=1"
res = requests.get(link)

res.encoding =  res.apparent_encoding#亂碼處理
only_a_tags = SoupStrainer(id='listArea')#縮小檢索範圍
soup = BeautifulSoup(res.text ,"lxml",  parse_only=only_a_tags)#.prettify()#prettify_縮進顯示html
#'''
#換頁
def next(key,page = 1):
    #http://nhentai.net/search/?q=linda&page=1
    link = "http://nhentai.net/search/?q=" + urllib.quote(key) + "&page=" + str(page)
    res = requests.get(link)
    res.encoding =  res.apparent_encoding
    #only_a_tags = SoupStrainer(id='listArea')
    soup = BeautifulSoup(res.text ,"lxml")#,  parse_only=only_a_tags)#.prettify()
    return soup

#全轉半
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

#頁面處理
def findname(blink,key):
    res = requests.get(blink)
    res.encoding =  res.apparent_encoding
    soupfn = BeautifulSoup(res.text ,"lxml")
    
    if soupfn.select('#info h2'):#檢查日文檔名是否存在
        cn1=soupfn.select('#info h1')[0].text
        cn2=soupfn.select('#info h2')[0].text
        cn1=Q2B(cn1)
        cn2=Q2B(cn2)
        
        #(CT27) [Waffle Doumeiken (Tanaka Decilitre)] Sakusei Jouzu na Mai Senpai (Musaigen no Phantom World) 
        #(こみトレ27) [ワッフル同盟犬 (田中竕)]
        #print cn1[cn1.find(key)-1] , cn1[cn1.find(key)+len(key)]#()位置
        #print cn1.count(cn1[cn1.find(key)+len(key)],0,cn1.find(key))#)在(之前的數量
        
        tmp=u''
        tm=cn2
        tmp=cn1.count(cn1[cn1.find(key)+len(key)],0,cn1.find(key))
        while tmp> 0:#特徵存在
            tm=cn2[cn2.find(cn1[cn1.find(key)+len(key)])+1:]
            tmp=tmp-1
        #cn2處理過之tm，取出()之間的內容：)之前的(，與第一個)。
        print tm[tm.rfind(cn1[cn1.find(key)-1],0,tm.find(cn1[cn1.find(key)+len(key)]))+1:tm.find(cn1[cn1.find(key)+len(key)])].encode('utf8')
        
        #寫入字典
        data=key+'_'+cn2+'_'
        name='!'+tm[tm.rfind(cn1[cn1.find(key)-1],0,tm.find(cn1[cn1.find(key)+len(key)]))+1:tm.find(cn1[cn1.find(key)+len(key)])]
        del dict1[key]
        dict1.setdefault(name,data)
        
        return 1
    #return 

#資料處理
def findbook(soup,key , page = 1):
    a =0
    check=0
    for caption in soup.select('.caption'):
        #print "aa",type(key),len(key)
        caption=Q2B(caption)
        #print caption
        
        if ( (u'('+key+u')' in caption) or (u'['+key+u']') in caption ):
            clink = ''
            check=0
            clink = soup.select('.cover')[a].get('href')
            blink=mlink+clink
            
            check=findname(blink,key)
            #print blink#,len(clink)
            
            if check==1:
                return 1
            
        a = a + 1
        #print '\r',a,
    #print '.'
    #print '========'

########

a=0
dict1={}#
fout = open('output/'+ 'out_entojp.txt', 'w')#寫入模式開檔
fout.write('entojp\n'+strftime("%Y/%m/%d,%H:%M")+'->')#entojp
time.sleep(1)
for tmp in nkey:
    time.sleep(1)
    nkey[a]=nkey[a].rstrip().rstrip(u'\n')
    nkey[a]=Q2B(nkey[a])
    dict1.setdefault(nkey[a],u'Ｘ')
    print nkey[a].encode('utf8'), '=>' ,
    
    soup1 = next(nkey[a],1)
    soup2 = next(nkey[a],2)
    
    f1=findbook(soup1,nkey[a])
    if f1==1:
        a=a+1
        continue
    f2=findbook(soup2,nkey[a])
    if f2<>1:
        print ''
    a=a+1
    
fout.write(strftime("%H:%M")+'\n')
tmp=u''
for tmp in dict1.iterkeys():
    #print tmp,dict1[tmp]
    fout.write(dict1[tmp].encode('utf8')+'\n'+tmp.encode('utf8')+'\n')

fout.close()
print 'ok'
#sys.exit()################

#結束讀秒
x=3
while x!=0:
    print x,'..',
    x=x-1
    time.sleep(1)
raw_input("\nPress Any Key To Exit")