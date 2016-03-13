# -*- coding: utf-8 -*- 
import urllib , requests , sys ,string ,time
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from time import gmtime, strftime

#toranoana
#fkey作者來源key.txt
#fcomiclist結果key_toranoana.text

#輸出格式：
#toranoana
#!作者
#!總筆數
#==類別_數量_中文敘述
#[同人團_作者群][原作][同人場cXX]同人作品
#參考網址

#頁顯示數量
pnum = 30
mlink = 'http://www.toranoana.jp/'

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
#res = requests.post("http://www.toranoana.jp/cgi-bin/R2/d_search.cgi", data = adict)

網址樣本
http://www.toranoana.jp/cgi-bin/R2/d_search.cgi
?item_kind=0401
&stk=1
&obj=0
&nam=
&mak=
&act=%82%cd%82%e9%82%e9%82%f1#作者
&adl=0
&img=0#圖顯示0不顯示，1顯示
&dys=
&dms=01
&dye=
&dme=01
&bl_fg=0
&ps=1#頁數控制，31 61
&itc=
&ikb=
&gnr=
&mch=
&com=

'''

link = "http://www.toranoana.jp/cgi-bin/R2/d_search.cgi?item_kind=0401&stk=1&obj=0&nam=&mak=&act=" + key2 + "&adl=0&img=0&dys=&dms=01&dye=&dme=01&ps=1&bl_fg=0&itc=&ikb=&gnr=&mch=&com="
cookies = {'_tcuid':'201602230349005234',
               '_tcuid_updated_at':'1456170540395',
               '_tcsid':'201602230349001329',
               '_tcsid_updated_at':'1456170540395',
               '_ga':'GA1.2.1089385032.1456170540',
               'afg':'0'
}#作品頁面年齡驗證

res = requests.get(link)
res.encoding =  res.apparent_encoding#亂碼處理
r= res.text
r=r[r.find(u'<!-- MAIN AREA -->'):r.find(u'<!-- /MAIN AREA -->')+len(u'<!-- /MAIN AREA -->')]#搜尋結果擷取
#r=r[r.find(u'<!-- MAIN AREA -->'):r.rfind(u'</table>')+len(u'</table>')]#搜尋結果擷取
#print r

only_a_tags = SoupStrainer("table",class_="f_tbl_9cf",cellspacing="1")#縮小檢索範圍
soup = BeautifulSoup(r,"html.parser",  parse_only=only_a_tags)

def next(page = 2):
    #page=int(page)
    ps=page*pnum+1
    link = "http://www.toranoana.jp/cgi-bin/R2/d_search.cgi?item_kind=0401&stk=1&obj=0&nam=&mak=&act=" + key2 +     "&adl=0&img=0&dys=&dms=01&dye=&dme=01&ps="+str(ps)+"&bl_fg=0&itc=&ikb=&gnr=&mch=&com="
    
    res = requests.get(link)
    res.encoding =  res.apparent_encoding
    r= res.text
    r=r[r.find(u'<!-- MAIN AREA -->'):r.find(u'<!-- /MAIN AREA -->')+len(u'<!-- /MAIN AREA -->')]#搜尋結果擷取
    
    only_a_tags = SoupStrainer("tr", class_="TBLdtil")#縮小處理範圍
    #先html.parser解析與縮小範圍，再以字串給lxml
    #soup = BeautifulSoup(str(BeautifulSoup(res.text,"html.parser",  parse_only=only_a_tags)),"lxml")
    soup = BeautifulSoup(r,"lxml",  parse_only=only_a_tags)
    
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
    res = requests.get(dlink,cookies=cookies)
    res.encoding =  res.apparent_encoding#亂碼處理
    r= res.text
    r=r[r.find(u'<td class=\"Main\">'):r.find(u'<!--フッターここまで-->')+len(u'<!--フッターここまで-->')]+u'\n</td>'#搜尋結果擷取
    
    only_a_tags = SoupStrainer("table", summary="Details")#縮小檢索範圍
    sou=BeautifulSoup(r,"lxml",  parse_only=only_a_tags)
    
    dname=sou.select('.DetailData_L')[2].text#作者
    draw=sou.select('.DetailData_L')[3].text#同人原作
    dtype=sou.select('.DetailData_R')[0].text#類型
    ddate=sou.select('.DetailData_R')[1].text#日期
    
    dname=Q2B(dname.strip().strip(u'\n').replace('\n',' ').replace('\t',''))
    draw=draw.strip().strip(u'\n').replace('\n','').replace('\t','')
    #print dname,draw,dtype,ddate
    return dname,draw,dtype,ddate

#資料處理
def findbook(soup , page = 1):
    global bl
    a =0
    check = 0
    for tb in soup.select('.TBLdtil'):
        a=a+1
        print '\r',a,
        '''
        if a>5:
            break
        #'''
        clink= tb.select('a')[0].get('href')[1:]#連結
        cbook=tb.select('.noi_c2')[0].text#作品名
        cbl=tb.select('.noi_c5')[0].text#作品取向_判斷BL作
        cclub=tb.select('.noi_c3')[0].text#社團
        #print clink,cname,cbl
        #print a,#cclub,
        
        #網址
        blink = ''
        blink=mlink+clink
        
        if (u'株式会社虎の穴' in cclub) or (u'【とらのあな' in cbook):
            continue#跳過虎穴出品
        else:
            cname,craw,ctype,cdate=finddata(blink)
            if (key.decode('utf8') in cname) and ((u'同人誌' in ctype) or (u'同人CG集' in ctype)):
                if key.decode('utf8') ==cname:
                    check=1#單作者
                else:
                    check=2#多作者
            else:
                continue#跳過非目標作者
        
        #日期處理
        #無日期sample_http://www.toranoana.jp/mailorder/article/04/0000/01/66/040000016646.html
        if len(cdate) < 3:#無日期
            cdate = '0000/00/00'#填入日期
            check = 4#新作
        date = cdate
        while listdata.count(date):#重複日期判斷
            date = date[:8] + str(int(date[8:]) + 1).rjust(2,'0')#日期+1_十位數填0
        listdata.append(date)
        
        #bl
        if u'女性向' in cbl:
            bl=bl+1
        
        book=cbook.strip().strip(u'\n')
        club=cclub.strip().strip(u'\n').replace('\n','')
        name=cname
        raw=craw
        dtype=ctype
        #print key,book,name,club,raw,date,dtype,bl
        
        #寫入dict
        #單作者參考格式_[To Heart 2][c69]年末年始ドリームジャンボ★宝くじ
        #多作者參考格式_[PINK+Petite*Cerisier][To Heart 2][c69]年末年始ドリームジャンボ★宝くじ
        book=u'['+raw+u']'+u'[-]'+book#[原作][同人場cXX]同人作品
        if check==1:
            book=club+'_'+book
            dict1.setdefault(date,book)
        else:
            book=u'['+club+'_'+name+u']'+book+'\n!'+blink
            dict2.setdefault(date,book)
        
        #continue
    print '.'
    #print '========'
    #return

########

key=key.lower()
pn=0
if soup.select('span'):
    pn=int(soup.select('span')[2].text[:soup.select('span')[2].text.find(u'件')])#資料筆數

'''
成年向け同人誌 -
全年齢対象同人誌 -
同人CG
#sample_http://www.toranoana.jp/mailorder/article/04/0010/13/34/040010133499.html
- 同人ソフト -軟體
- 同人音楽作品 -CD
- 同人グッズ -周邊
#'''

#資料筆數_是否數字
if pn>0:
    print 'ok'
    #print soup.find_all('b')
    
    if pn > pnum:
        print 'BIG'
    
    fout = open('output/'+key.decode('utf8') + '_toranoanav1.txt', 'w')#寫入模式開檔
    fout.write('toranoana\n')#toranoana
    print key , pn , 'num\n========v1'
    time.sleep(1)
    fout.write('!' + key + '\n!總筆數' + str(pn).encode('utf8') +'_'+ strftime("%Y/%m/%d,%H:%M")+'->')
    
    p = 0#頁
    #建空輸出用字典與陣列
    dict1={}#單作者
    dict2={}#多作者
    listdata = []
    bl=0#bl作品數
    
    #資料處理
    while (int(pn) - p * pnum) > 0:
        
        print 'page:' + str(p)
        soup = next(p)#頁
        #print soup.select('.TBLdtil')[2]
        findbook(soup)#資料處理
        time.sleep(1)
        p = p + 1
    
    #日期排序
    listdata.sort()
    
    fout.write(strftime("%H:%M")+'\n')
    #fout.write('!BL數'+str(bl).encode('utf8')+'\n')
    if bl > 0:
        fout.write('!BL數'+str(bl).encode('utf8')+'\n')
    temp = ''
    #dict2_多作者
    fout.write('==anime_' + str(len(dict2)) +'_同人多作者\n')
    save(dict2)
    #dict1_單作者
    fout.write('==book_' + str(len(dict1)) +'_同人單作者\n')
    save(dict1)
    
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