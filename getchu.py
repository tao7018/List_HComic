# -*- coding: utf-8 -*- 
import urllib , requests , sys ,string ,time
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

#getchu
#fkey作者來源key.txt
#fcomiclist結果key_getchu.text

#輸出格式：
#getchu
#!作者
#!總筆數
#==類別_數量_中文敘述
#類別_品名
#網址

#頁顯示數量
pnum = 30
mlink = 'http://www.getchu.com/'

fkey = open('key.txt', 'r')
key = fkey.readline()#key=作者
fkey.close()

#key=作者
key2 = urllib.quote(key.decode('utf8').encode('euc_jp'))
key3 = urllib.unquote(key2.decode('euc_jp').encode('utf8'))
#網址用
key4 = urllib.quote(key)
#print key4, '\n' , urllib.quote(key.decode('sjis').encode('utf8')) 

#檢查BOM
if '%EF%BB%BF' in urllib.quote(key):
    print 'fuck ms'

'''網址樣本
http://www.getchu.com/php/search.phtml?search_keyword=&search_title=&search_brand=&
search_person=%BE%E5%C6%A3%C0%AF%BC%F9
&search_jan=&search_isbn=&genre=all&start_date=&end_date=&age=&list_count=30&sort=sales&sort2=down&list_type=list&search=1&
pageID=1
'''
link = "http://www.getchu.com/php/search.phtml?search_keyword=&search_title=&search_brand=&search_person=" + urllib.quote(key3) + "&search_jan=&search_isbn=&genre=all&start_date=&end_date=&age=&list_count=30&sort=sales&sort2=down&list_type=list&search=1&pageID=1"

#head = {'User-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'}
res = requests.get(link)#, headers = head)

res.encoding =  res.apparent_encoding#亂碼處理
soup = BeautifulSoup(res.text,"html.parser")#超出lxml緩存，改其他存取

def next(page = 2):
    link = "http://www.getchu.com/php/search.phtml?search_keyword=&search_title=&search_brand=&search_person=" + urllib.quote(key3) + "&search_jan=&search_isbn=&genre=all&start_date=&end_date=&age=&list_count=30&sort=sales&sort2=down&list_type=list&search=1&pageID="+ str(page)
    
    res = requests.get(link)
    res.encoding =  res.apparent_encoding
    
    only_a_tags = SoupStrainer("ul", class_="display")#縮小處理範圍
    #先html.parser解析與縮小範圍，再以字串給lxml
    soup = BeautifulSoup(str(BeautifulSoup(res.text,"html.parser",  parse_only=only_a_tags)),"lxml")
    
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
    return ustring

#資料儲存
def save(sdict , check=0):
    #print listdata
    for temp in listdata:
        if sdict.get(temp):
            #fout.write(temp.encode('utf8') +sdict[temp].encode('utf8')  + '\n')
            fout.write(sdict[temp].encode('utf8')  + '\n')
    #return

#資料處理
def findbook(soup , page = 1):
    a =0
    check = 0
    for li in soup.select('li'):
        ctype = soup.select('.orangeb')[a].text
        cbook = soup.select('.blueb')[a].text
        cdata = soup.select('.orangeb')[a].next_sibling.next_sibling[5:]
        #print li
        #print ctype,cbook,cdata
        
        #類型
        if u'・' in ctype:
            stype = ctype.split(u'・')
            dtype = stype[0] + ']'
        else:
            dtype = ctype
        
        #品名
        book = cbook
        
        #日期處理
        #print cdata
        cdata = cdata.rstrip()
        if len(cdata) < 8:#無日期
            cdata = '0000/00/00'#填入日期
            check = 4#新作
        data = cdata
        while listdata.count(data):#重複日期判斷
            data = data[:8] + str(int(data[8:]) + 1).rjust(2,'0')#日期+1_十位數填0
        listdata.append(data)
            
        '''
        typea = ['[BOOKS]','[雑誌]','[同人]']
        typeb = ['[アニメ]']
        typec = ['[PCゲーム]','[DVD-PG]']
        #其他
        グッズ
        アダルトグッズ
        音楽CD
        グラビア
        実写
        '''
        #網址
        blink = ''
        blink = soup.select('.blueb')[a].get('href')
        blink = mlink + blink[3:]
        #print blink
        
        #寫入dict
        book = dtype + '_' + book + '_' + '\n!' + blink#類形+書名+網址
        if check == 4:
            dict4.setdefault(data,book)
        elif dtype in [u'[BOOKS]',u'[雑誌]',u'[同人]'] :
            dict1.setdefault(data,book)
        elif dtype in[u'[アニメ]']:
            dict2.setdefault(data,book)
        elif dtype in [u'[PCゲーム]',u'[DVD-PG]']:
            dict3.setdefault(data,book)
        else:
            dict5.setdefault(data,book)
        
        a = a + 1
        #print key ,  sname[0]
        #print a
    #print listdata[:]
    #print '========'
    #return

########

pn = soup.select('.s_condition')[0].select('b')[0].text#資料筆數
#資料筆數_是否數字
if pn.isdigit():
    #print soup.find_all('b')
    if int(pn) > pnum:
        print 'BIG'
    
    fout = open(key.decode('utf8') + '_getchu.txt', 'w')#寫入模式開檔
    fout.write('getchu\n')#getchu
    print key.decode('utf8') , pn , 'num\n========'
    time.sleep(1)
    fout.write('!' + key + '\n!總筆數' + pn.encode('utf8') + '\n')
    
    p = 0#頁
    #建空輸出用字典與陣列
    dict1={}#BOOKS,雑誌,同人
    dict2={}#アニメ
    dict3={}#PCゲーム,DVD-PG
    dict4={}#新
    dict5={}#其他
    listdata = []
    
    #資料處理
    while (int(pn) - p * pnum) > 0:
        p = p + 1
        print 'page:' + str(p)
        soup = next(p)#頁
        
        findbook(soup)#資料處理
        time.sleep(1)
    #print 'ook\n',listdata
    
    #日期排序
    listdata.sort()
    
    temp = ''
    #dict1_BOOKS,雑誌,同人輸出
    fout.write('==book_' + str(len(dict1)) +'_BOOKS,雑誌,同人\n')
    save(dict1)
    
    #dict2_アニメ輸出
    fout.write('==anime_' + str(len(dict2)) +'_アニメ\n')
    save(dict2)
    
    #dict3_PCゲーム,DVD-PG輸出
    fout.write('==game_' + str(len(dict3)) +'_PCゲーム,DVD-PG\n')
    save(dict3)
    
    #dict4_新輸出
    fout.write('==new_' + str(len(dict4)) +'_新\n')
    save(dict4)
    
    #dict5_其他輸出
    fout.write('==other_' + str(len(dict5)) +'_其他\n')
    save(dict5)
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
print 'end'
