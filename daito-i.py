# -*- coding: utf-8 -*- 
import urllib , requests , sys ,string ,time
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

#daito-i
#fkey作者來源key.txt
#fcomiclist結果key_daito-i.text

#輸出格式：
#daito-i
#!作者
#!總筆數
#==類別_數量_中文敘述
#條目
#!網址

#comiclist常數
pnum = 30#頁顯示數量
mlink = 'http://www.daito-i.com/top/'#前綴網址

fkey = open('key.txt', 'r')
key = fkey.readline()#key=作者
fkey.close()

#檢查BOM
if '%EF%BB%BF' in urllib.quote(key):
    print 'fuck ms'

'''
link = "http://comiclist.jp/index.php?p=s&mode=ss&keyword=" + urllib.quote(key) + "&type=title"
res = requests.get(link)
'''


#print key2
#print key3
adict = { 
'mode':'search',
'page_num':'0',
'search_cat':'',
'keyword':key
}
res = requests.post("http://www.daito-i.com/top/show_unit.php", data = adict)

res.encoding =  res.apparent_encoding#亂碼處理
only_a_tags = SoupStrainer(id='contents')#縮小檢索範圍
soup = BeautifulSoup(res.text ,"lxml",  parse_only=only_a_tags)#.prettify()#prettify_縮進顯示html

#換頁
def next(page = 2):
    #http://comiclist.jp/index.php?p=s&mode=ss&type=title&keyword=%E4%B8%8A%E8%97%A4%E6%94%BF%E6%A8%B9&andor=and&maxline=30&pgn=3&pgn=1
    #&andor=and&maxline=無影響&pgn=無影響&pgn=頁
    #link = "http://comiclist.jp/index.php?p=s&mode=ss&type=title&keyword=" + urllib.quote(key) + "&andor=and&maxline=30&pgn=1&pgn=" + str(page)
    adict = { 
        'mode':'search',
        'category':'',
        'subcategory':'',
        'search_cat':'',
        'keyword':key,
        'sort':'',
        'page_num':str(page)
    }
    res = requests.post("http://www.daito-i.com/top/show_unit.php", data = adict)
    res.encoding =  res.apparent_encoding
    only_a_tags = SoupStrainer(id='contents')
    soup = BeautifulSoup(res.text ,"lxml",  parse_only=only_a_tags)#.prettify()
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
    #print listdata
    for temp in listdata:
        if sdict.get(temp):
            #fout.write(temp.encode('utf8') +sdict[temp].encode('utf8')  + '\n')
            fout.write(sdict[temp].encode('utf8')  + '\n')
    #return

#新刊
def find_1():
    #收網址
    #網址get
    #找出目錄_找出篇名
    #回報目錄篇名
    print 'find1'
    return 'a'
#單行本
def find_2(blink='http://www.daito-i.com/top/'):
    global bdict2
    bdate = ''
    res = requests.get(blink)
    res.encoding =  res.apparent_encoding
    only_a_tags = SoupStrainer(class_="rec")
    soup = BeautifulSoup(res.text ,"lxml",  parse_only=only_a_tags)
    print soup.select('strong')[0].text,soup.select('strong')[1].text#書名_作者
    #print len(soup.select('.goodTxt')),soup.select('.goodTxt')[0]#主內容
    
    nnum = str(soup.select('.goodTxt')[0]).count('<br/>')#<br/>次數
    for tm in soup.select('.goodTxt')[0].select('p'):
        if (str(tm).count('<br/>') > 5):# and str(tm).count(key):
            #print tm.text,type(tm.text)
            bdate = bdate + '(' + str(str(tm).count('<br/>')) + ')-'#單行本話數
            bdict2 = bdict2 + tm.get_text('_') + '_'#比對用疊加
            tm = tm.get_text('\n-')
            bdate = bdate + tm + '%\n'
    #print 'find2'
    bdate = bdate[:bdate.find(u'%')+1]#去多餘
    return bdate,nnum
#雜誌類
def find_3(blink='http://www.daito-i.com/top/'):
    bdate = ''
    res = requests.get(blink)
    res.encoding =  res.apparent_encoding
    only_a_tags = SoupStrainer(class_="rec")
    soup = BeautifulSoup(res.text ,"lxml",  parse_only=only_a_tags)
    #print soup.select('strong')[0].text,soup.select('strong')[1].text#雜誌名_期號
    #print len(soup.select('.goodTxt')),soup.select('.goodTxt')[0]#主內容
    
    nnum = Q2B(soup.select('.goodTxt')[0].text).encode('utf8').count(key)#作者出現次數
    for tm in soup.select('.goodTxt')[0].select('p'):
        if (str(tm).count('】') > 3):# and str(tm).count(key):#特徵與作者
            #print tm.text,type(tm.text)
            tm=tm.text
            tm=Q2B(tm)
            while tm.find(u'【') > 0:#特徵存在
                if key.decode('utf8') in tm[tm.find(u'【')+1:tm.find(u'】')]:#符合作者
                    listdict3.append(tm[:tm.find(u'【')])#比對用疊加
                    bdate = bdate + tm[:tm.find(u'【')] + '_'#疊加
                    if key != tm[tm.find(u'【')+1:tm.find(u'】')]:#作者不唯一
                        bdate = bdate + tm[tm.find(u'【'):tm.find(u'】')+1] + '_'#疊加
                tm=tm[tm.find(u'】')+1:]
    #print 'find3'
    return bdate,nnum

#資料處理
def findbook(soup , page = 1):
    global pnn
    a =0
    for itmBox in soup.select('.itmBox'):
        ctype = soup.select('.marks')[a].next_sibling[1:]
        cbook = soup.select('.itmBox')[a].select('a')[1].text
        cname = soup.select('.itmBox')[a].select('a')[2].text
        #print type(itmBox),itmBox
        #print pnn,ctype,cbook,cname
        
        #作品網址
        blink = ''
        blink = soup.select('.itmBox')[a].select('a')[0].get('href')
        blink = mlink + blink
        #print blink
        
        #書名
        
        #類型
        bdate = ''#次層頁面主資料
        #b = str(pnn).rjust(3,'0')#倒數的流水號
        
        #予約商品_新刊
        if ctype in u'予約商品':#予約商品_
            !bdate=find_1()
            book = cname + '_' + cbook + '_\n!' + blink
            dict1.setdefault(pnn,book)
        #コミックス_單行本
        elif ctype in u'コミックス':
            if key.decode('utf8') in Q2B(itmBox.text):
                cfind=find_2(blink)#目標作者的單行本
                print cfind[1]
                bdate = cfind[0]
                if len(bdate) < 10:
                    bdate = 'lost'
                book = cbook + '_\n' + bdate + '\n!' + blink
                dict2.setdefault(pnn,book)
            elif cname in u'アンソロジー ':
                cfind=find_3(blink)#非作者or合本_アンソロジー 
                print cfind[1],'num'
                bdate=cfind[0]
                book = cname + '_' + cbook + '_' + bdate + '_\n!' + str(cfind[1]) + '!' + blink
                dict2.setdefault(pnn,book)
            else:
                book = ctype + '_' + cname + '_' + cbook + '_\n!' + blink
                dict2.setdefault(pnn,book)
        #雑誌_雜誌單篇
        elif ctype in u'雑誌':
            cfind=find_3(blink)
            print cfind[1],'name_num'
            bdate=cfind[0]
            book = cbook + '[' + Q2B(cname) + ']_' + bdate + '_\n!' + str(cfind[1]) + '!' + blink
            dict3.setdefault(pnn,book)
        #ノベルズ_文庫_画集_書籍_
        elif ctype in [u'ノベルズ',u'文庫',u'画集',u'書籍']:
            book = ctype + '_' + cname + '_' + cbook + '_\n!' + blink
            dict4.setdefault(pnn,book)
        #ムック_同人誌_販促品_
        elif ctype in [u'ムック',u'同人誌',u'販促品']:
            book = ctype + '_' + cname + '_' + cbook + '_\n!' + blink
            dict5.setdefault(pnn,book)
        
        #
        listdata.append(pnn)
        '''
        1予約商品_
        2コミックス_
        3雑誌_
        4ノベルズ_文庫_画集_書籍_
        5ムック_同人誌_販促品_
        '''
        
        a = a + 1
        
        #特徵itmBox開滿每頁顯示才放資料，會跑出空值，以搜尋筆數跳出。
        pnn = pnn -1
        #print a,pnn,int(pnn)
        #if pnn <78:
        if pnn == 0:
            break
        
    print '========'

########
key=key.lower()
KEY = B2Q(key.decode('utf8'))
KEY= KEY.encode('utf8')

pn =''
pn = soup.select('tr')[1].select('td')[1].text
pn = pn[0:pn.find(u'件')]#筆數
print pn

#資料筆數_是否數字
if pn > 0:
    if int(pn) > pnum:
        print 'BIG'
    
    fout = open(key.decode('utf8') + '_daito-iv1.txt', 'w')#寫入模式開檔
    fout.write('daito-i\n')#comiclist
    print key.decode('utf8') , pn , 'num\n========v1'
    time.sleep(1)
    fout.write('!' + key + '\n!總筆數' + pn.encode('utf8') + '\n')
    
    p = 0#頁
    #建空輸出用字典與陣列
    dict1={}#新刊
    dict2={}#單行本
    dict3={}#雜誌
    dict4={}#作畫擔任
    dict5={}#其他
    listdict3=[]#雜誌單篇
    bdict2 = ''#單行本書目
    listdata = []
    #搜尋結果特徵碼部分有空值?計步避開
    pnn = int(pn)#計步
    
    #資料處理
    while (int(pn) - p * pnum) > 0:
        
        print 'page:' + str(p)
        soup = next(p)#頁
        findbook(soup)#資料處理
        p = p + 1
        time.sleep(1)
    
    #日期排序
    listdata.sort()
    #print '======'
    
    #sys.exit()################
    temp = ''
    #dict1_雜誌輸出
    fout.write('==new_' + str(len(dict1)) +'_新刊\n')
    save(dict1)
    #dict2_單行本輸出
    fout.write('==book_' + str(len(dict2)) +'_單行本\n')
    save(dict2)
    #dict3_雜誌輸出
    fout.write('==adult_' + str(len(dict3)) +'_雜誌\n')
    save(dict3)
    #dict4_作畫擔任輸出
    fout.write('==art_' + str(len(dict4)) +'_作畫擔任\n')
    save(dict4)
    #dict5_其他輸出
    fout.write('==other_' + str(len(dict5)) +'_其他\n')
    save(dict5)
    
    #單行本與雜誌比對
    fout.write('==fd32_' + str(len(listdict3)) +'_比對結果\n')
    tmp = ''
    out32 = ''
    #listdict3_bdict2
    for tmp in listdict3:
        #print type(tmp),type(bdict2)
        if tmp in bdict2:
            #print 'catch'
            tmp='-'+tmp
        out32=out32+tmp+'\n'
    fout.write(out32.encode('utf8'))
    
    fout.close()
    print 'ok'
elif p:
    print '同人'

#結束讀秒
x=3
while x!=0:
    print x,'..',
    x=x-1
    time.sleep(1)
print 'end'
