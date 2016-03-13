# -*- coding: utf-8 -*- 
import urllib , requests , sys ,string ,time
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from time import gmtime, strftime

#nagomi
#fkey作者來源key.txt
#fcomiclist結果key_nagomi.text

#輸出格式：
#nagomi
#!作者
#!總筆數
#==類別_數量_中文敘述
#[同人團_作者群][原作][同人場cXX]同人作品
#參考網址

#頁顯示數量
pnum = 100
mlink = 'http://nagomi.ne.jp/web/top/'

fkey = open('key.txt', 'r')
key = fkey.readline()#key=作者
fkey.close()

#key=作者
key2 = urllib.quote(key.decode('utf8').encode('EUC_JP'))#當sjis輸出utf8的url
key3 = urllib.unquote(key2.decode('shift_jis').encode('utf8'))#utf8的url翻sjis

#檢查BOM
if '%EF%BB%BF' in urllib.quote(key):
    print 'fuck ms'

link='''http://nagomiweb.jp/cgi-bin/search_frame.cgi?\
rm=&user=et080948&kubun=&word='''+key2+'&p='+'0'+'''\
&stock=1&search_num=4&search_order=1&part=1'''

res = requests.get(link)
res.encoding='EUC_JP'#亂碼處理

soup = BeautifulSoup(res.text,"html.parser")#,  parse_only=only_a_tags)

def next(page = 2):
    link='''http://nagomiweb.jp/cgi-bin/search_frame.cgi?\
    rm=&user=et080948&kubun=&word='''+key2+'&p='+str(page)+'''\
    &stock=1&search_num=4&search_order=1&part=1'''
    
    res = requests.get(link)
    res.encoding =  res.apparent_encoding
    
    only_a_tags = SoupStrainer("body")#縮小處理範圍
    soup = BeautifulSoup(res.text,"html.parser",  parse_only=only_a_tags)
    
    return soup

#全轉半
def Q2B(ustring):
    fs=u'０１２３４５６７８９\
    ＱｑＷｗＥｅＲｒＴｔＹｙＵｕＩｉＯｏＰｐＡａＳｓＤｄＦｆＧｇＨｈＪｊＫｋＬｌＺｚＸｘＣｃＶｖＢｂＮｎＭｍ'
    hs=u'0123456789QqWwEeRrTtYyUuIiOoPpAaSsDdFfGgHhJjKkLlZzXxCcVvBbNnMm'
    rstr = ''
    for tm in ustring:
        if fs.find(tm)+1:
            tm = hs[fs.find(tm)]
        rstr = rstr + tm
    ustring = rstr
    ustring=ustring.lower()
    return ustring
#半轉全
def B2Q(ustring):
    fs=u'０１２３４５６７８９\
    ＱｑＷｗＥｅＲｒＴｔＹｙＵｕＩｉＯｏＰｐＡａＳｓＤｄＦｆＧｇＨｈＪｊＫｋＬｌＺｚＸｘＣｃＶｖＢｂＮｎＭｍ'
    hs=u'0123456789QqWwEeRrTtYyUuIiOoPpAaSsDdFfGgHhJjKkLlZzXxCcVvBbNnMm'
    rstr = ''
    ustring=ustring.lower()
    for tm in ustring:
        if hs.find(tm)+1:
            tm = fs[hs.find(tm)]
        rstr = rstr + tm
    ustring = rstr
    return ustring

#資料儲存
def save(sdict , check=0):
    for temp in listdata:
        if sdict.get(temp):
            fout.write(sdict[temp].encode('utf8')  + '\n')
    #return

#資料處理
def findbook(soup , page = 1):
    #global bl
    a =0
    #check = 0
    for di in soup.select('.id'):
        if not di.select('div'):#id標籤內無div內容(商品編號)
            break
        if a%5 ==0:#nagomi一列五項成組，主要處理統一lxml
            sou = BeautifulSoup(str(soup.select('.goodslist')[a//5]),"lxml")
        
        check = 0
        craw=u''
        cclub=u''
        cname=u''
        cid=sou.select('.id')[a%5].select('div')[0].text.strip().strip(u'\n').replace('\n',' ').replace('\t','')
        cdata= sou.select('.comment')[a%5]
        ctit=soup.select('.name')[a].text.replace('\n',' ').replace('\t','').replace(u'(コピー誌）','').strip().strip(u'\n')
        
        #網址
        clink= 'http://nagomiweb.jp/cgi-bin/detail.cgi?user=et080948&id='+cid
        #clink=sou.select('.image')[a%5].select('a')[1].get('href')
        
        #同人CG#同人誌#CG集
        if not((u'同人CG'in cdata.text)or(u'同人誌'in cdata.text)or(u'CG集'in cdata.text)):
            a=a+1
            continue
        
        #中古委託販売_レンタルケース
        if (u'レンタルケース' in cdata.text) or (u'中古委託販売' in cdata.text):
            #print 'nocomment'
            if key.decode('utf8') in cdata.text:
                check=2
        elif key.decode('utf8') in Q2B(ctit):
            a=a+1
            continue
        else:
            cclub=cdata.select('a')[0].text
            cname=cdata.select('a')[1].text
            craw=cdata.select('a')[2].text
            ctit=ctit[ctit.rfind('[')+1:ctit.rfind(']')]
        #作者
        if key.decode('utf8') == Q2B(cname):
            check=1
        
        #id處理
        if len(cid) < 3:#無id
            cid = '0000/00/00'#填入id
        bid = cid
        while listdata.count(bid):#重複id判斷
            bid = bid[:-2] + str(int(bid[-2:]) + 1).rjust(2,'0')#id+1_十位數填0
        listdata.append(bid)
        
        raw=craw
        book=ctit
        name=cname
        club=cclub
        blink=clink
        
        #寫入dict
        #參考格式_[To Heart 2][c69]年末年始ドリームジャンボ★宝くじ
        #[原作][同人場cXX]同人作品
        if check==1:
            book=u'['+raw+u']'+u'[-]'+book
            dict1.setdefault(bid,book)
        elif check==2:
            book=book+'_!'+blink
            dict2.setdefault(bid,book)
        elif len(raw)>1:
            book=u'['+club+'_'+name+u']'+u'['+raw+u']'+u'[-]'+book+'_!'+blink
            dict3.setdefault(bid,book)
        else:
            book=u'委託'+book+'_!'+blink
            dict3.setdefault(bid,book)
        
        a=a+1
        print '\r',a,
        #continue
    print '.'
    #print '========'
    #return

########
'''
#同人CG
#同人誌
#CG集
#中古委託販売_レンタルケース

#被截斷的標題例_hisasi
#沒被截斷的標題例_コバヤシテツヤ
#'''

key=key.lower()
pn=0
#print soup.select('span')[1].text
pn=int(soup.select('span')[1].text)#資料筆數

#資料筆數_是否數字
if pn>0:
    print 'ok'
    #print soup.find_all('b')
    
    if pn > pnum:
        print 'BIG'
    
    fout = open('output/'+key.decode('utf8') + '_nagomiv1.txt', 'w')#寫入模式開檔
    fout.write('nagomi\n')#toranoana
    print key , pn , 'num\n========v1'
    time.sleep(1)
    fout.write('!' + key + '\n!總筆數' + str(pn).encode('utf8') +'_'+ strftime("%Y/%m/%d,%H:%M")+'->')
    
    p = 0#頁
    #建空輸出用字典與陣列
    dict1={}#目標作者
    dict2={}#委託
    dict3={}#非目標
    listdata = []
    
    #資料處理
    while (int(pn) - p * pnum) > 0:
        
        print 'page:' + str(p)
        soup = next(p)#頁
        
        findbook(soup)#資料處理
        time.sleep(1)
        p = p + 1
    
    #日期排序
    listdata.sort()
    fout.write(strftime("%H:%M")+'\n')
    temp = ''
    #dict1_目標作者
    fout.write('==tnbook_' + str(len(dict1)) +'_同人作品\n')
    save(dict1)
    #dict2_委託
    fout.write('==tnother_' + str(len(dict2)) +'_中古委託販売レンタルケース\n')
    save(dict2)
    #dict3_其他
    fout.write('==otn_' + str(len(dict3)) +'_其他\n')
    save(dict3)
    
    #sys.exit()################
    fout.close()
    print 'ok'
elif pn:
    print 'No Date'

#結束讀秒
x=3
while x!=0:
    print x,'..',
    x=x-1
    time.sleep(1)
raw_input("\nPress Any Key To Exit")