# -*- coding: utf-8 -*- 
import urllib , requests , sys ,string ,time
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from time import gmtime, strftime
#dlsite
#fkey作者來源key.txt
#fcomiclist結果key_dlsite.text

#輸出格式：
#dlsite
#!作者
#!總筆數
#==類別_數量_中文敘述
#類別_品名
#網址

#頁顯示數量
pnum = 30
mlink = 'http://www.dlsite.com/books/'

fkey = open('key.txt', 'r')
key = fkey.readline()#key=作者
fkey.close()

#檢查BOM
if '%EF%BB%BF' in urllib.quote(key):
    print 'fuck ms'

'''網址樣本
http://www.dlsite.com/maniax/fsr/=/language/jp/sex_category%5B0%5D/male/keyword/
urllib.quote(key)
/ana_flg/all/order%5B0%5D/release_d/genre_and_or/or/options_and_or/or/per_page/30/show_type/n/page/
1
'''
link = "http://www.dlsite.com/maniax/fsr/=/language/jp/sex_category%5B0%5D/male/keyword/"+urllib.quote(key)+"/ana_flg/all/order%5B0%5D/release_d/genre_and_or/or/options_and_or/or/per_page/30/show_type/n/page/1"

#head = {'User-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'}
res = requests.get(link)#, headers = head)

res.encoding =  res.apparent_encoding#亂碼處理
soup = BeautifulSoup(res.text,"html.parser")#超出lxml緩存，改其他存取

def next(page = 2):
    link = "http://www.dlsite.com/maniax/fsr/=/language/jp/sex_category%5B0%5D/male/keyword/"+urllib.quote(key)+"/ana_flg/all/order%5B0%5D/release_d/genre_and_or/or/options_and_or/or/per_page/30/show_type/n/page/"+str(page)

    res = requests.get(link)
    res.encoding =  res.apparent_encoding
    
    only_a_tags = SoupStrainer(id="search_result_list")#縮小處理範圍
    soup = BeautifulSoup(res.text,"html.parser",  parse_only=only_a_tags)
    
    return soup

#全轉半_含轉小寫
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
#半轉全_含轉小寫
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
    #print listdata
    for temp in listdata:
        if sdict.get(temp):
            #fout.write(temp.encode('utf8') +sdict[temp].encode('utf8')  + '\n')
            fout.write(sdict[temp].encode('utf8')  + '\n')
    #return

#作品頁面
def bfind(blink='http://www.dlsite.com/books/'):
    res = requests.get(blink)
    res.encoding =  res.apparent_encoding
    ssoup_1 = SoupStrainer(id="work_right")#資訊欄位
    ssoup_2 = SoupStrainer(class_="work_article work_story")#內容欄位
    
    soup1 = BeautifulSoup(res.text,"lxml",  parse_only=ssoup_1)#資訊欄位
    soup2=BeautifulSoup(res.text,"lxml",  parse_only=ssoup_2)#內容欄位
    
    nnum1=''#作者出現次數
    nnum2=''#作者出現次數
    bdate1=''#含作者資料
    bdate2=''#含作者資料
    check=0
    cname=''
    
    nnum1 = Q2B(soup1.text).encode('utf8').count(key)#作者出現次數
    nnum2=Q2B(soup2.text).encode('utf8').count(key)
    
    #資訊欄位
    for tm in soup1.select('tr'):
        #日期
        if u'予告開始日' in tm.text:
            check=1
            cdata=tm.td.text
        elif u'販売日' in tm.text:
            cdata=tm.td.text
        #類型
        if u'作品形式'in tm.text:
            ctype='['+tm.td.text+']'
        #作者
        ##作者不一定有<a>，棄用的方法。
        #tmm=tm.select('a')#.get_text('//')
        tmm=tm.td
        tm=Q2B(tm.text).replace('\n','')
        if key.decode('utf8') in tm:
            ##棄用的方法。
            #for tmmm in tmm:
                #cname=cname+tmmm.text+u'/'
            #print tmm,len(tmm)
            cname=Q2B(tmm.text).replace('\n','')
            bdate1=bdate1+tm+'_'
    bdate1=bdate1[:-1]
    
    #內容欄位
    x=0
    if nnum2 > 0:
        tm=Q2B(soup2.text)
        while tm.find(key.decode('utf8'))>-1:
            #以\n為界的key資料，疊加
            ##\r處理
            bdate2=bdate2+'-'+tm[tm.rfind(u'\n',0,tm.find(key.decode('utf8'))) : tm.find(u'\n',tm.find(key.decode('utf8')))].strip(u'\n').strip(u'\r')+u'\n'
            tm=tm[tm.find(key.decode('utf8'))+1:]
            x=x+1
            if x>10:
                break
    #\n佔用兩格?
    bdate2=bdate2.rstrip('\n')
    #'''
    
    #類型判斷
    if int(nnum1) > 0:
        check=5
        if u'マンガ' in ctype:
            check=2
            if u'同人' in ctype:
                check=4
            elif key.decode('utf8') != cname:
                check=3
                
    elif nnum2>0:
        if u'マンガ' in ctype:
            check=6
        else:
            check=7
    
    '''
    1新
    2漫單
    3漫多
    4漫同人
    5它
    6漫
    7它
    1>4>3>2
    #'''
    
    #print 'bfind'
    #類型_nnum1_bdate1_nnum2_bdate2_check
    return ctype,nnum1,bdate1,nnum2,bdate2,check

#資料處理
def findbook(soup , page = 1):
    a =0
    check = 0
    for work_thumb in soup.select('.work_thumb'):
        tr = soup.select('tr')[3*a]#資料欄位，間隔3
        sou = BeautifulSoup(str(tr),"lxml")
        
        ctype = sou.select('.work_genre')[0].text
        cbook = sou.select('.work_name')[0].text
        cdata = sou.select('.sales_date')[0].text
        #print ctype,cbook,cdata
        
        #網址
        blink = ''
        blink = sou.select('.work_name')[0].select('a')[0].get('href')
        
        #作品處理
        #日期_品名
        #類型_nnum1_bdate1_nnum2_bdate2
        cfind=bfind(blink)
        #print '########catch:',len(cfind)#,cfind[:]
        ctype=cfind[0]
        cnum1=str(cfind[1]).decode('utf8')
        cdate1=cfind[2]
        cnum2=str(cfind[3]).decode('utf8')
        cdate2=cfind[4]
        check=cfind[5]
        
        #品名
        book = cbook.replace('\n','')
        
        #類型
        dtype=ctype
        
        #日期處理
        #予告開始日 : 	2015年04月24日
        #販売日: 2015年08月21日
        if u'予告開始日' in cdata:
            cdata=cdata[7:].replace(u'年','').replace(u'月','').replace(u'日','')
            check=1
        else:
            cdata=cdata[5:].replace(u'年','').replace(u'月','').replace(u'日','')
        
        #cdata = cdata.rstrip()
        if len(cdata) < 4:#無日期
            cdata = u'0000/00/00'#填入日期
        data = cdata
        while listdata.count(data):#重複日期判斷
            data = data[:6] + str(int(data[6:]) + 1).rjust(2,'0')#日期+1_十位數填0
        listdata.append(data)
        #'''
        
        '''
        1新
        2漫單
        3漫多
        4漫同人
        5它
        6漫
        7它
        #'''
        
        #寫入dict
        #參考1參考2，無筆數則不紀錄。
        if check == 1:#新
            #日期_類型_品名_
            #!參考1!連結
            book=data+'_'+dtype+'_'+book+'_\n!'+cnum1+'!'+blink
            dict1.setdefault(data,book)
        elif check == 2:#漫單
            #類型_品名_作者資料1_
            book=dtype+'_'+book+'_'+cdate1+'_'
            dict2.setdefault(data,book)
        elif check == 3:#漫多
            #類型_品名_作者資料1_
            book=dtype+'_'+book+'_'+cdate1+'_'
            dict3.setdefault(data,book)
        elif check == 4:#漫同人
            #類型_品名_作者資料1_
            book=dtype+'_'+book+'_'+cdate1+'_'
            dict4.setdefault(data,book)
        elif check == 5:#它
            #類型_品名_作者資料1_
            #!參考1!參考2!連結
            book=dtype+'_'+book+'_'+cdate1+'_\n!'+cnum1+'!'+cnum2+'!'+blink
            dict5.setdefault(data,book)
        elif check == 6:#漫
            #類型_品名_
            #作者資料2_
            #!參考1!參考2!連結
            book=dtype+'_'+book+'_\n'+cdate2+'_\n!'+cnum1+'!'+cnum2+'!'+blink
            dict6.setdefault(data,book)
        elif check==7:#它
            #類型_品名_
            #作者資料2_
            #!參考1!參考2!連結
            book=dtype+'_'+book+'_\n'+cdate2+'_\n!'+cnum1+'!'+cnum2+'!'+blink
            dict7.setdefault(data,book)
        #print check,'_',book
        #'''
        a = a + 1
        print '\r',a,
        #sys.exit()################
    print '.'
    #print '========'
    #return

########
key=key.lower()

pn=''
if len(soup.select('strong'))>0:
    pn = soup.select('strong')[0].text#資料筆數

#資料筆數_是否數字
if pn.isdigit():
    if int(pn) > pnum:
        print 'BIG'
    
    fout = open(key.decode('utf8') + '_dlsite.txt', 'w')#寫入模式開檔
    fout.write('dlsite\n')#getchu
    print key.decode('utf8') , pn , 'num\n========v1'
    time.sleep(1)
    #fout.write('!' + key + '\n!總筆數' + pn.encode('utf8') + '\n')
    fout.write('!' + key + '\n!總筆數' + pn.encode('utf8') +'_'+ strftime("%Y/%m/%d,%H:%M")+'->')
    
    p = 0#頁
    #建空輸出用字典與陣列
    dict1={}#新
    dict2={}#漫單
    dict3={}#漫多
    dict4={}#漫同人
    dict5={}#它
    dict7={}#漫
    dict6={}#它
    listdata = []
    check=0
    
    #資料處理
    while (int(pn) - p * pnum) > 0:
        p = p + 1
        print 'page:' + str(p)
        soup = next(p)#頁
        
        findbook(soup)#資料處理
        time.sleep(1)
    
    #日期排序
    listdata.sort()
    
    fout.write(strftime("%H:%M")+'\n')
    temp = ''
    #dict1_新輸出
    fout.write('==new_' + str(len(dict1)) +'_新\n')
    save(dict1)
    #dict2_漫單輸出
    fout.write('==book_' + str(len(dict2)) +'_漫單\n')
    save(dict2)
    #dict3_漫多輸出
    fout.write('==numbook_' + str(len(dict3)) +'_漫多\n')
    save(dict3)
    #dict4_漫同人輸出
    fout.write('==dbook_' + str(len(dict4)) +'_漫同人\n')
    save(dict4)
    #dict5_它輸出
    fout.write('==other_' + str(len(dict5)) +'_它\n')
    save(dict5)
    #dict6_漫輸出
    fout.write('==obook_' + str(len(dict6)) +'_漫\n')
    save(dict6)
    #dict7_它輸出
    fout.write('==oother_' + str(len(dict7)) +'_它\n')
    save(dict7)
    
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