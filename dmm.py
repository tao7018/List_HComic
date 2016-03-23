# -*- coding: utf-8 -*- 
import urllib , requests , sys ,string ,time
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from time import gmtime, strftime

#dmm
#fkey作者來源key.txt
#fcomiclist結果key_dmm.text

#輸出格式：
#dmm
#!作者
#!總筆數
#==類別_數量_中文敘述
#[同人團_作者群][原作][同人場cXX]同人作品
#參考網址

#頁顯示數量
pnum = 30
mlink = 'http://book.dmm.co.jp/'

fkey = open('key.txt', 'r')
key = fkey.readline()#key=作者
fkey.close()

#key=作者
key2 = urllib.quote(key.decode('utf8').encode('shift_jis'))#當sjis輸出utf8的url
key3 = urllib.unquote(key2.decode('shift_jis').encode('utf8'))#utf8的url翻sjis
#網址用
key4 = urllib.quote(key)

#檢查BOM
if '%EF%BB%BF' in urllib.quote(key):
    print 'fuck ms'

'''
http://www.dmm.co.jp/search/=
/searchstr=%E5%A5%A5%E6%A3%AE%E3%83%9C%E3%82%A6%E3%82%A4#作者
/analyze=V1EBD1YFUAM_#可省略?
/limit=30#頁顯示數量
/n1=FgRCTw9VBA4GAFNXXF0_
/sort=date#排序
/view=text#檢視模式_有無
/page=2#頁_P1沒有
/#尾
'''
#page=1
link="http://www.dmm.co.jp/search/=/\
searchstr="+key4+"/limit=30/n1=FgRCTw9VBA4GAFNXXF0_/sort=date/"
#標題與話數_http://book.dmm.co.jp/detail/b333afjpc00714/

res = requests.get(link)
res.encoding =  res.apparent_encoding#亂碼處理
r= res.text
#r=r[r.find(u'<td id="mu">'):r.find(u'<!-- /mu --></td>')+len(u'<!-- /mu --></td>')]#+'</td>'#搜尋結果擷取
r=r[r.find(u'</div><![endif]-->')+len(u'</div><![endif]-->'):r.find(u'<div id="footer">')]#+'</td>'#搜尋結果擷取


#only_a_tags = SoupStrainer(id="mu")#縮小檢索範圍
soup = BeautifulSoup(r,"lxml")#,  parse_only=only_a_tags)

def next(page = 2):
    #page=int(page)
    #ps=page*pnum+1
    link="http://www.dmm.co.jp/search/=/\
    searchstr="+key4+"/limit=30/n1=FgRCTw9VBA4GAFNXXF0_/sort=date/"
    
    if page>1:
        link=link+'page='+str(page)+'/'
    
    res = requests.get(link)
    res.encoding =  res.apparent_encoding
    r= res.text
    r=r[r.find(u'</div><![endif]-->')+len(u'</div><![endif]-->'):r.find(u'<div id="footer">')]#+'</td>'#搜尋結果擷取
    
    #先html.parser解析與縮小範圍，再以字串給lxml
    #only_a_tags = SoupStrainer(id="mu")#縮小檢索範圍
    soup = BeautifulSoup(r,"lxml")#,  parse_only=only_a_tags)
    
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
#半轉全
def B2Q(ustring):
    fs=u'０１２３４５６７８９ＱｑＷｗＥｅＲｒＴｔＹｙＵｕＩｉＯｏＰｐＡａＳｓＤｄＦｆＧｇＨｈＪｊＫｋＬｌＺｚＸｘＣｃＶｖＢｂＮｎＭｍ'
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

#作品頁面
def finddata(dlink):
    res = requests.get(dlink)
    res.encoding =  res.apparent_encoding#亂碼處理
    r= res.text
    r=r[r.find(u'</div><![endif]-->')+len(u'</div><![endif]-->'):r.find(u'<div id="footer">')]
    
    sou=BeautifulSoup(r,"lxml")
    
    dname=u''
    dbook=u''
    dcheck=0
    for d in sou.select('.m-boxDetailProductInfoMainList__description__list')[0].select('a'):
        if d.text==key.decode('utf8'):
            dcheck=1
        dname=dname+'_'+d.text
    dname=dname.strip(u'_')
    dbook=sou.select('.m-boxDetailProductInfoMainList__description__list')[1].text.strip().strip(u'\n').strip(u'\t')
    if dcheck==1 :
        if key.decode('utf8') != dname:
            dcheck=3
    
    return dname,dbook,dcheck

#資料處理
def findbook(soup , page = 1):
    global bl
    a =0
    check = 0
    for n in soup.select('.m-boxListBookProduct__item'):
        cbook=n.select('.m-boxListBookProductTmb__ttl')[0].text
        ctype=n.select('.m-boxListGenreIco.m-boxListGenreIco--large')[0].text
        cbn=''#卷
        cname=Q2B(n.select('.m-boxListBookProductTmb__linkAuthor')[0].text.strip().strip(u'\n'))
        #網址
        clink=n.select('.m-boxListBookProductTmb')[0].select('a')[0].get('href')
        
        a=a+1
        print '\r',a,
        
        #類別
        #if (u'' == ctype):
        if u'単行本' == ctype:
            check=1#單行本
        elif u'単話' ==ctype:
            check=2#單話
        else:
            continue#目標外
        
        #作品頁_1標題2作者3系列
        if (u'...' in cbook)or(key.decode('utf8') !=cname):#or():
            cname,cbook,dcheck=finddata(clink)
            if dcheck>2:
                check=3#多作者
            elif dcheck==0:
                continue#非作者
        
        #作品名
        cbook=cbook[:cbook.rfind(u'（単話）')]
        cbook=cbook[:cbook.rfind(u'【フルカラー】')]
        
        #卷
        if n.select('.m-boxListBookProductTmbSub.m-boxListBookTmbSubInfo--series'):
            cbn=n.select('.m-boxListBookProductTmbSub.m-boxListBookTmbSubInfo--series')[0].text
            cbn=cbn[2:cbn.find(u'卷')]    
        
        cdata=clink[len(u'http://book.dmm.co.jp/detail/'):-1]#網址當排序依據
        #print ctype,cbook,cname,len(cbn),'_',cbn,cdata#,clink
        
        #data處理
        if len(cdata) < 3:#無data
            cdata = '0000/00/00'#填入data
            check = 4#
        data = cdata
        while listdata.count(data):#重複data判斷
            data = data[:-2] + str(int(data[-2:]) + 1).rjust(2,'0')#尾數+1_十位數填0
        listdata.append(data)
        
        book=cbook
        btype=ctype
        name=cname
        bn=cbn
        blink=clink
        
        #寫入dict
        if (len(bn)>0) or (check==3) or (u'【セット】' in book):
            if len(bn)>0:
                book=book+u'['+bn+u']'
            book=book+'_!'+blink
        
        if check==1:#單行本
            dict1.setdefault(data,book)
        elif check==2:#單話
            dict2.setdefault(data,book)
        else:#多作者
            book=u'['+name+u']['+btype+u']_'+book
            dict3.setdefault(data,book)
        
        #club=cclub.strip().strip(u'\n').replace('\n','')
        continue
    print '.'
    #print '========'
    #return

########

key=key.lower()
pn=0

tmp=soup.select('.m-boxPagenation__txt')[0].text
pn=tmp[tmp.find(u'全')+1:-1]#資料筆數
print pn

'''
アダルトコミック___単行本_単話_コミック雑誌
美少女ノベル・官能小説
アダルト写真集・雑誌
#美少女ノベル_コミック雑誌

#小說與寫真無法區分，皆不記錄。
含小說_ぽるのいぶき
含寫真_奥森ボウイ

#標題切斷範例_奥森ボウイ
#多作者_LINDA
#【セット】【フルカラー】（単話）
#'''

#資料筆數_是否數字
if pn>0:
    if pn > pnum:
        print 'BIG'
    
    fout = open('output/'+key.decode('utf8') + '_dmmv1.txt', 'w')#寫入模式開檔
    fout.write('dmm\n')#toranoana
    print key , pn , 'num\n========v1'
    time.sleep(1)
    fout.write('!' + key + '\n!總筆數' + str(pn).encode('utf8') +'_'+ strftime("%Y/%m/%d,%H:%M")+'->')
    
    p = 0#頁
    #建空輸出用字典與陣列
    dict1={}#單行本
    dict2={}#單話
    dict3={}#多作者
    listdata = []
    
    #資料處理
    while (int(pn) - p * pnum) > 0:
        p = p + 1
        print 'page:' + str(p)
        soup = next(p)#頁
        #print soup.select('.TBLdtil')[2]
        findbook(soup)#資料處理
        time.sleep(1)
    
    #日期排序
    listdata.sort()
    
    fout.write(strftime("%H:%M")+'\n')
    temp = ''
    #dict1_單行本
    fout.write('==book_' + str(len(dict1)) +'_單行本\n')
    save(dict1)
    #dict2_單話
    fout.write('==sbook_' + str(len(dict2)) +'_單話\n')
    save(dict2)
    #dict3_多作者
    fout.write('==other_' + str(len(dict3)) +'_多作者\n')
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