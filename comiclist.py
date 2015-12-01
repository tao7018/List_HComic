# -*- coding: utf-8 -*- 
import urllib , requests , sys ,string ,time
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from time import gmtime, strftime

#comiclist
#fkey作者來源key.txt
#fcomiclist結果key_comiclist.text

#輸出格式：
#comiclist
#!作者
#!總筆數
#==類別_數量_中文敘述
#條目

#comiclist常數
pnum = 30#頁顯示數量
mlink = 'http://comiclist.jp/'#前綴網址

fkey = open('key.txt', 'r')
key = fkey.readline()#key=作者
fkey.close()

#檢查BOM
if '%EF%BB%BF' in urllib.quote(key):
    print 'fuck ms'

link = "http://comiclist.jp/index.php?p=s&mode=ss&keyword=" + urllib.quote(key) + "&type=title"
res = requests.get(link)

res.encoding =  res.apparent_encoding#亂碼處理
only_a_tags = SoupStrainer(id='listArea')#縮小檢索範圍
soup = BeautifulSoup(res.text ,"lxml",  parse_only=only_a_tags)#.prettify()#prettify_縮進顯示html

#換頁
def next(page = 2):
    #http://comiclist.jp/index.php?p=s&mode=ss&type=title&keyword=%E4%B8%8A%E8%97%A4%E6%94%BF%E6%A8%B9&andor=and&maxline=30&pgn=3&pgn=1
    #&andor=and&maxline=無影響&pgn=無影響&pgn=頁
    link = "http://comiclist.jp/index.php?p=s&mode=ss&type=title&keyword=" + urllib.quote(key) + "&andor=and&maxline=30&pgn=1&pgn=" + str(page)
    res = requests.get(link)
    res.encoding =  res.apparent_encoding
    only_a_tags = SoupStrainer(id='listArea')
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

#資料處理
def findbook(soup , page = 1):
    a =0
    check=0
    for strong in soup.select('strong'):
        cname = soup.select('.list-name')[a].text
        cbook = soup.select('strong')[a].text
        #print soup.select('strong')[a]
        cdata = soup.select('.list-day')[a].text
        
        #作者處理
        '''舊
        check = 0#非目標作者
        cname = cname.replace(u'　','')#移除全形空格
        cname = Q2B(cname)
        if u'］' not in cname:
            cname = cname + u'］'
        sname = cname.split(u'］')#切拆作者
        '''
        s_name = []
        for temp in soup.select('.list-name')[a].select('a'):
            temp = temp.text
            temp = temp.replace(u'　','')#移除全形空格
            temp = Q2B(temp)
            s_name.append(temp)
        s_name.append('')#避while錯誤
        
        b = 0
        name = ''
        while len(s_name[b]) > 0:
            ##while對split切不出不視為陣列？
            if u'［' not in s_name[b]:
                s_name[b] = s_name[b] + u'［'
            ssname = s_name[b].split(u'［')#切拆作者後綴
            #print ssname
            tname = ssname[0]
            if key == tname.encode('utf8'):#符合作者
                #print 'ok'
                check = 1#目標作者
                if (u'画' in ssname[1] )or (u'著' in ssname[1] ):#符合後綴
                    check = 2#符合後綴
            name = name + ssname[0] + u'、'#作者串接 
            b = b + 1
        name = name.rstrip(u'、')#多餘分號處理
        
        #書名處理
        book = cbook
        if (u'（成）' in cbook) and (check == 2):#去前綴
            check = 3
            book = cbook.replace(u'（成）','')
        
        #日期處理
        cdata = cdata.rstrip()
        if len(cdata) < 8:#無日期
            cdata = '0000/00/00'#填入日期
            if check > 0:
                check = 4#新作
        data = cdata[:10]
        while listdata.count(data):#重複日期判斷
            data = data[:8] + str(int(data[8:]) + 1).rjust(2,'0')#日期+1_十位數填0
        listdata.append(data)
        
        #多卷處理
        if (u'巻' in cdata) and (int(cdata[10:-1]) > 1):
            bnum = cdata[10:-1]#冊數
            book = book + '[' + bnum + ']'
            
        #書名連結
        blink = ''
        blink = soup.select('.list-book')[a].select('a')[0].get('href')
            
        #字典新增
        if len(str(check)):
        #if check > 0:
            if check == 1:
                book = book + '_' + name + '\n' + mlink +blink#書名+作者+網址
                dict1.setdefault(data,book)
            elif check ==2:
                dict2.setdefault(data,book)
            elif check ==3:
                dict3.setdefault(data,book)
            elif check ==4:
                dict4.setdefault(data,book)
            else:
                book = book + '_' + name + '\n' + mlink +blink#書名+作者+網址
                dict5.setdefault(data,book)
        a = a + 1
        print '\r',a,
    print '.'
    #print '========'

########
key=key.lower()
pn=soup.find_all('b')[1].text

#資料筆數_是否數字
if pn.isdigit():
    if int(pn) > pnum:
        print 'BIG'
    
    fout = open(key.decode('utf-8') + '_comiclistv1.txt', 'w')#寫入模式開檔
    fout.write('comiclist\n')#comiclist
    print key.decode('utf-8') , pn , 'num\n========v1'
    time.sleep(1)
    #fout.write('!' + key + '\n!總筆數' + soup.find_all('b')[1].text.encode('utf8') + '\n')
    fout.write('!' + key + '\n!總筆數' + pn.encode('utf8') +'_'+ strftime("%Y/%m/%d,%H:%M")+'->')
    
    p = 0#頁
    #建空輸出用字典與陣列
    dict1={}#作者無後綴
    dict2={}#作者一般向青年向
    dict3={}#作者成人向
    dict4={}#作者成人向新刊
    dict5={}#它項
    listbnum=[]
    bnum = ''#卷
    listdata = []
    
    #資料處理
    while (int(soup.find_all('b')[1].text) - p * pnum) > 0:
        p = p + 1
        print 'page:' + str(p)
        soup = next(p)#頁
        findbook(soup)#資料處理
        time.sleep(1)
    
    #日期排序
    listdata.sort()
    
    fout.write(strftime("%H:%M")+'\n')
    temp = ''
    #dict3_成人向輸出
    fout.write('==adult_' + str(len(dict3)) +'_成人向\n')
    for temp in listdata:
        if dict3.get(temp):
            fout.write(dict3[temp].encode('utf8')  + '\n')
            if dict3[temp].count(u']',-2):
                listbnum.append(dict3[temp])
    
    #輸出多卷
    fout.write('==adultnum_' + str(len(listbnum)) +'_成人向多卷\n')
    for temp in listbnum:
        fout.write(temp.encode('utf8') + '\n')
    
    #dict4_新刊輸出
    fout.write('==new_' + str(len(dict4)) +'_新\n')
    for temp in listdata:
        if dict4.get(temp):
            fout.write(temp.encode('utf8') +dict4[temp].encode('utf8')  + '\n')
    
    #dict2_一般向青年向
    fout.write('==nomal_' + str(len(dict2)) +'_一般向青年向\n')
    for temp in listdata:
        if dict2.get(temp):
            fout.write(dict2[temp].encode('utf8')  + '\n')
    
    #dict1_其他輸出
    fout.write('==unknow_' + str(len(dict1)) +'_不明\n')
    for temp in listdata:
        if dict1.get(temp):
            fout.write(temp.encode('utf8') +dict1[temp].encode('utf8')  + '\n')
    
    #dict5_它項輸出
    fout.write('==other_' + str(len(dict5)) +'_它項\n')
    for temp in listdata:
        if dict5.get(temp):
            fout.write(temp.encode('utf8') +dict5[temp].encode('utf8')  + '\n')
    
    fout.close()
    print 'ok'
elif soup.find_all('b')[1].text:
    print '同人'

#結束讀秒
x=3
while x!=0:
    print x,'..',
    x=x-1
    time.sleep(1)
raw_input("\nPress Any Key To Exit")