# -*- coding: utf-8 -*- 
import urllib , requests , sys ,string
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

#爬comiclist
#測試用：源五郎
#fkey作者來源key.txt
#fcomiclist結果key_comiclist.text

fkey = open('key.txt', 'r')
key = fkey.readline()
fkey.close()

#檢查BOM
if '%EF%BB%BF' in urllib.quote(key):
    print 'fuck ms'

#key=作者
#key = '源五郎'
#key2 = urllib.quote(key.decode('utf8').encode('sjis'))
#key3 = urllib.unquote(key2.decode('sjis').encode('utf8'))
#網址用
#key4 = urllib.quote(key)
#print key4

#http://comiclist.jp/index.php?p=s&mode=ss&type=title&keyword=%E4%B8%8A%E8%97%A4%E6%94%BF%E6%A8%B9&andor=and&maxline=30&pgn=3&pgn=1
#&andor=and&maxline=無影響&pgn=無影響&pgn=頁
#link = "http://comiclist.jp/index.php?p=s&mode=ss&type=title&keyword= + urllib.quote(key) + "&andor=and&maxline=30&pgn=1&pgn=" + page
link = "http://comiclist.jp/index.php?p=s&mode=ss&keyword=" + urllib.quote(key) + "&type=title"
res = requests.get(link)

#亂碼處理
res.encoding =  res.apparent_encoding
#縮小檢索範圍
only_a_tags = SoupStrainer(id='listArea')

soup = BeautifulSoup(res.text ,"lxml",  parse_only=only_a_tags)#.prettify()

def next(page = 2):
    link = "http://comiclist.jp/index.php?p=s&mode=ss&type=title&keyword=" + urllib.quote(key) + "&andor=and&maxline=30&pgn=1&pgn=" + str(page)
    res = requests.get(link)
    res.encoding =  res.apparent_encoding
    only_a_tags = SoupStrainer(id='listArea')
    soup = BeautifulSoup(res.text ,"lxml",  parse_only=only_a_tags)#.prettify()
    return soup
    

#資料處理
def findbook(soup , page = 1):
    a =0
    #for soup.select('strong')[a]:
    for strong in soup.select('strong'):
            #print soup.select('strong')[a].text
            cname = soup.select('.list-name')[a].text
            cbook = soup.select('strong')[a].text
            cdata = soup.select('.list-day')[a].text
            
            #作者處理
            #画_著_無後綴
            check = 0
            cname = cname.replace(u'　','')
            #while對split切不出不視為陣列？
            if u'］' not in cname:
                cname = cname + u'］'
            sname = cname.split(u'］')
            b = 0
            #print sname[b]
            name = ''
            
            #'''
            while len(sname[b]) > 0:
            #while sname[b]:
            #for sname[b]:
                #s_name = sname[b]
                ssname = sname[b].split(u'［')
                
                temp = ssname[0]
                #print len(key) , key , len(temp.encode('utf8')) , temp.encode('utf8')
                
                #if key == ssname[0]:
                #符合作者
                if key == temp.encode('utf8'):
                    check = 1
                    #符合後綴
                    if (u'画' in ssname[1] )or (u'著' in ssname[1] ):
                        check = 2
                        #print 'ok'
                        
                b = b + 1
                #ssname[0] =  u'、' + ssname[0]
                #作者疊加
                name = name + ssname[0] + u'、'
                #print ssname[0]
            #'''
            #多於分號處理
            name = name.rstrip(u'、')
            #print name
            
            #單作者檢查
            '''
            if soup.select('.list-name')[a].br:
                #print '多作者處理'
            '''            
            
            #書名
            book = cbook
            if (u'（成）' in cbook) and (check == 2):
                check = 3
                book = cbook.replace(u'（成）','')
                #print 'adult' 
            #print cbook
            
            #日期
            #print soup.select('.list-day')[a]
            #print cdata
            cdata = cdata.rstrip()
            if len(cdata) < 8:
                cdata = '0000/00/00'
                check = 4
            #print cbook + 'check' + str(check) +'\n' + cdata
            
            #重複日期判斷
            data = cdata[:10]
            while listdata.count(data):
            #for data in listdata:
                data = data[:8] + str(int(data[8:]) + 1)
            listdata.append(data)
            
            if (u'巻' in cdata) :#and (check > 0):
            #if soup.select('.list-day')[a].br:
                #print '卷處理' + str(cdata[10:-1])
                #冊數
                bn = cdata[10:-1]
            #print name.encode('utf8') , urllib.quote(key)
            #print urllib.quote(name.encode('utf8'))
            
            #存檔處理
            #if key == name.encode('utf8'):
            if check > 0:
                #print key ,  sname[0]
                #print soup.select('.list-day')[a].text , soup.select('.list-name')[a].text
                #fout.write(soup.select('.list-day')[a].text.encode('utf8') + cbook.encode('utf8')  + '\n')
                
                #fout.write(cdata.encode('utf8') + cbook.encode('utf8')  + '\n')
                #字典新增
                #dict1.setdefault('b',2)
                if check == 1:
                    dict1.setdefault(data,book)
                elif check ==2:
                    dict2.setdefault(data,book)
                elif check ==3:
                    dict3.setdefault(data,book)
                elif check ==4:
                    dict4.setdefault(data,book)
            #print key ,  sname[0]
            
            
            
            #fout.write(soup.select('strong')[a].text.encode('utf8') + '\n')
            
            a = a + 1
            #print a
    #print listdata[:]
    #print '========'
            

#資料筆數
if soup.find_all('b')[1].text.isdigit():
#if soup.find_all('b')[1].text > 0:
    #print key , soup.find_all('b')[1].text , '筆資料\n========'
    #print soup.find_all('b')
    if soup.find_all('b')[1].text > 30:
        print 'BIG'
    fout = open(key.decode('utf8') + '_comiclist.txt', 'w')
    fout.write('out\n')
    #findbook()
    p = 0
    #建空字典陣列
    dict1={}#作者無後綴
    dict2={}#作者一般向
    dict3={}#作者成人向
    dict4={}#作者成人向新刊
    listdata = []
    #num = soup.find_all('b')[1].text
    while (int(soup.find_all('b')[1].text) - p * 30) > 0:
        #ggg(p)
        p = p + 1
        soup = next(p)
        findbook(soup)
    
    #日期排序
    listdata.sort()
    
    temp = ''
    #成人向輸出dict3
    for temp in listdata:
    #for temp in dict3.itervalues():
        if dict3.get(temp):
            fout.write(temp.encode('utf8') +dict3[temp].encode('utf8')  + '\n')
            #print temp , dict3[temp]
    
    #新刊輸出dict4
    fout.write('==新\n')
    for temp in listdata:
    #for temp in dict3.itervalues():
        if dict4.get(temp):
            fout.write(temp.encode('utf8') +dict4[temp].encode('utf8')  + '\n')
            #print temp , dict3[temp]
    
    #一般向dict2
    fout.write('==一般\n')
    for temp in listdata:
    #for temp in dict3.itervalues():
        if dict2.get(temp):
            fout.write(temp.encode('utf8') +dict2[temp].encode('utf8')  + '\n')
            #print temp , dict3[temp]
    
    #其他輸出dict1
    fout.write('==不明\n')
    for temp in listdata:
    #for temp in dict3.itervalues():
        if dict1.get(temp):
            fout.write(temp.encode('utf8') +dict1[temp].encode('utf8')  + '\n')
            #print temp , dict3[temp]
    
    
    fout.close()
#print soup.select('.search_page_link_info')[1].text
#print soup.select('.search_page_link_info')[1]

#爬蟲重點內容
#print soup.select('#listBOX-search')[0].text

#print soup.select('td[class^="list-line"]')
#print res.text
