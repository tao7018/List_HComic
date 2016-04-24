# -*- coding: utf-8 -*- 
import urllib , requests , sys , string   ,time , os
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from time import gmtime , strftime

'''
daito-i

daito_i.txt
#無書目例#http://www.daito-i.com/top/comics/detail.php?code=9784344805408
#有圖http://www.daito-i.com/top/comics/detail.php?code=9784799206096
'''

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

#資料儲存
def save(fout , listdata , sdict , check=0):
    for tep in listdata:
        if sdict.get(tep):
            fout.write(sdict[tep]  + '\n')
    #return

#單行本
def find_b(blink, key, bdict2):
    res = requests.get(blink)
    res.encoding =  res.apparent_encoding
    only_a_tags = SoupStrainer(class_="goodTxt")
    soup = BeautifulSoup(res.text ,"lxml",  parse_only=only_a_tags)
    
    bdata = ''
    nnum= 0
    nnum = str(soup).count('<br/>')#<br/>次數
    for tm in soup.select('p'):
        if (str(tm).count('<br/>') > 5):
            bdata = bdata + '(' + str(str(tm).count('<br/>')) + ')-'#換行次數當單行本話數
            bdict2 = bdict2 + tm.get_text('_') + '_'#比對用疊加
            bdata = bdata + tm.get_text('\n-') + '%\n'
        bdata = bdata.strip('\n')
    return bdata,nnum,bdict2
#雜誌類
def find_m(blink, key, listdict3):
    res = requests.get(blink)
    res.encoding =  res.apparent_encoding
    only_a_tags = SoupStrainer(class_="goodTxt")
    soup = BeautifulSoup(res.text ,"lxml",  parse_only=only_a_tags)
    
    bdata = ''
    nnum=0
    nnum = Q2B(soup.text).encode('utf8').count(key)#作者出現次數
    for tm in soup.select('p'):
        if (str(tm).count('】') > 4):#特徵
            tt=Q2B(tm.text).strip().strip('\n').replace('\t','').split(u'】')
            for t in tt:
                if key.decode('utf8') in t[t.find(u'【')+1:]:
                    listdict3.append(t[:t.find(u'【')])#比對用疊加
                    bdata= bdata+ t[:t.find(u'【')]
                    if key.decode('utf8') != t[t.find(u'【')+1:]:
                        bdata= bdata+ '['+ t[t.find(u'【')+1:]+ ']'
                    bdata= bdata+ '_'
            bdata=bdata.strip('_')
    return bdata,nnum,listdict3

#資料處理
def findbook(dictB, listdata, listdict3, receive):
    link, key, p, pn, pnn, olddate, bdict2=receive
    mlink = 'http://www.daito-i.com/top/'
    if len(link)<5:
        return dictB, listdata, listdict3, pnn, olddate, bdict2
    
    res = requests.get(link)
    res.encoding =  res.apparent_encoding
    r= res.text
    r=r[r.find(u'<!-- ▼mainContents -->'):r.find(u'<!-- ▲mainContents -->')+len(u'<!-- ▲mainContents -->')]
    soup = BeautifulSoup(r ,"lxml")#,  parse_only=only_a_tags)
    
    bn=len(soup.select('.itmBox'))-len(soup.find_all(src="images/dummy.jpg"))
    
    a =0
    for tm in soup.select('.itmBox')[:bn]:
        if pnn==0:
            return dictB, listdata, listdict3, pnn, olddate, bdict2
        pnn=pnn-1
        a=a+1
        print '\r',pnn,
        
        check=0
        cdata=''
        ctype= tm.div.next_sibling.strip(' \n')
        cname = Q2B(tm.select('a')[2].text)
        
        if ctype== u'予約商品':
            check= 1
        elif ctype== u'コミックス' and key.decode('utf8') in cname:
            check= 2
        elif (ctype== u'雑誌') or (ctype== u'コミックス' and cname == u'アンソロジー'):
            check= 3
        elif ctype in [u'ノベルズ', u'文庫']:
            check= 4
        else:
            continue
        
        cbook = tm.select('a')[1].text
        clink = tm.select('a')[0].get('href')
        blink = mlink + clink
        
        if check== 2:
            cdata, nnum, bdict2= find_b(blink, key, bdict2)#book
            if len(cdata) < 10:
                cdata = 'lost'
        elif check== 3:
            cdata, nnum, listdict3= find_m(blink, key, listdict3)#magazine
        
        listdata.append(pnn)
        
        cbook = cbook.encode('utf8')
        ctype = ctype.encode('utf8')
        cname = cname.encode('utf8')
        cdata = cdata.encode('utf8')
        
        if check==1:#新刊
            book = cname + '_' + cbook + '_\n!' + blink
            dictB["dict1"].setdefault(pnn,book)
        elif check==2:#單行本
            if key.decode('utf8') != cname:#多作者
                cbook= cbook+'['+ cname+ ']'
            book = cbook + '_\n' + cdata + '\n!' + blink
            dictB["dict2"].setdefault(pnn,book)
        elif check==3:#雜誌
            book = cbook + '[' + cname + ']_' + cdata + '_\n!' + str(nnum) + '!' + blink
            dictB["dict3"].setdefault(pnn,book)
        elif check==4:#其他
            book = ctype + '_' + cname + '_' + cbook + '_\n!' + blink
            dictB["dict4"].setdefault(pnn,book)
        
        if a==(bn):
            break
        #continue
    print '.'
    #print '========'
    return dictB, listdata, listdict3, pnn, olddate, bdict2

########
def main(key='',ucheck=0,pn=0,nlink=''):
    #ucheck_0建檔_1更新_2直讀
    
    pnum = 30#頁顯示數量
    mlink = 'http://www.daito-i.com/top/'#前綴網址
    
    olddate=''
    if ucheck != 2:
        #key=作者
        key=key.lower()
        key2 = urllib.quote(key.decode('utf8').encode('shift_jis'))#當sjis輸出utf8的url
        key3 = urllib.unquote(key2.decode('shift_jis').encode('utf8'))#utf8的url翻sjis
        #網址用
        key4 = urllib.quote(key)

        #檢查BOM
        if '%EF%BB%BF' in urllib.quote(key):
            print 'BOM！'

        link="http://www.daito-i.com/top/show_unit.php\
?mode=search&category=&subcategory=&search_cat=&keyword="+key4+"&sort=&page_num=0"
        
        res = requests.get(link)
        res.encoding =  res.apparent_encoding#亂碼處理
        r= res.text
        r=r[r.find(u'<!-- ▼mainContents -->'):r.find(u'<!-- ▲mainContents -->')+len(u'<!-- ▲mainContents -->')]
        soup = BeautifulSoup(r ,"lxml")#,  parse_only=only_a_tags)
        
        pn=0
        pn = int(soup.select('tr')[1].select('td')[1].text[:soup.select('tr')[1].select('td')[1].text.find(u'件')])
        
        #updata
        if (ucheck == 1) and (os.path.isfile('output/' + key.decode('utf8') + '_doujishiv1.txt')):#更新與欲輸入檔案存在
            fupdata = open('output/'+key.decode('utf8') + '_doujishiv1.txt', 'r+')
            rf=list(fupdata)
            kc=rf[1]
            if kc[1:len(key)+1] == key:
                oldn=int(rf[2][10:rf[2].find('_')])#建檔時筆數
                olddate=rf[2][rf[2].find('_')+1:rf[2].find('_')+11]
                olddate=olddate+str(9999)

                #更新筆數疊加
                for temp in range(rf.count('%\n')-1):#多一項
                    ub=rf.index('%\n')+2#位移
                    rf[rf.index('%\n')]=''#首項處理
                    oldnn=int(rf[ub][7:rf[ub].find('_')])
                    oldn=oldn+oldnn
                    olddate=rf[ub][rf[ub].find('_')+1:rf[ub].find('_')+11]
                    
                olddate=olddate.replace('/','')
                pn=pn-oldn
                print '更新筆數'+str(pn)

            if pn==0:#需要更新數為0跳出
                fupdata.seek(0, 2)
                fupdata.write('!updata\n!筆數' + str(pn).encode('utf8') +'_'+ strftime("%Y/%m/%d")+'\n%\n')
                fupdata.close()
                return 

    #資料筆數_是否數字
    if pn > 0:
        pnn=pn
        if int(pn) > pnum:
            print 'BIG'

        if ucheck == 1:
            fupdata.seek(0, 2)
            fupdata.write('!updata\n!筆數' + str(pn).encode('utf8') +'_'+ strftime("%Y/%m/%d,%H:%M")+'->')
        else:
            fout = open('output/'+key.decode('utf8') + '_daito-iv1.txt', 'w')#寫入模式開檔
            fout.write('daito-i\n')
            fout.write('!' + key + '_!'+link+'\n')
            fout.write('!總筆數' + str(pn).encode('utf8') +'_'+ strftime("%Y/%m/%d,%H:%M")+'->')
        
        print '==daito-i' , pn, '筆'
        time.sleep(1)
        p = 0#頁
        #建空輸出用字典與陣列
        dict1={}#新刊
        dict2={}#單行本
        dict3={}#雜誌
        dict4={}#其他#作畫擔任
        #dict5={}#其他
        dictB={
            'dict1':dict1,'dict2':dict2,'dict3':dict3,'dict4':dict4
        }
        listdict3=[]#雜誌單篇
        bdict2 = ''#單行本書目
        listdata = []

        #資料處理
        while (int(pn) - p * pnum) > 0:
            print 'page:' + str(p)
            
            nlink = link[:link.rfind('=')+1]+str(p)
            send=[nlink, key, p, pn, pnn, olddate, bdict2]
            dictB, listdata, listdict3, pnn, olddate, bdict2 = findbook(dictB, listdata, listdict3, send)#資料處理
            p = p + 1
            time.sleep(1)

        #日期排序
        #listdata.sort()

        listw=['==new_' + str(len(dictB["dict1"])) +'_新刊\n',
               '==book_' + str(len(dictB["dict2"])) +'_單行本\n',
               '==magazine_' + str(len(dictB["dict3"])) +'_雜誌\n',
               '==other_' + str(len(dictB["dict4"])) +'_他項\n'
              ]
        
        #紀錄筆數
        nb=0
        for w in range(len(listw)):
            nb= nb+ len(dictB["dict"+str(w+1)])
        
        #輸出
        if ucheck == 1:
            fupdata.write(strftime("%H:%M")+'_'+str(nb)+'\n')
            if len(olddate[8:]) > 0:#日期與資料不吻合，可能含舊資料
                fupdata.write('!舊資料'+olddate[8:]+'\n')
            for w in range(len(listw)):
                if len(dictB["dict"+str(w+1)]) > 0:
                    fupdata.write(listw[w])
                    save(fupdata , listdata , dictB["dict"+str(w+1)],w+1)
            fupdata.write('%\n')
            fupdata.close()
            
        else:
            fout.write(strftime("%H:%M")+'_'+str(nb)+'\n')
            for w in range(len(listw)):
                fout.write(listw[w])
                save(fout , listdata , dictB["dict"+str(w+1)],w+1)
            #單行本與雜誌比對#listdict3_bdict2
            out32 = ''
            for tmp in listdict3:
                if tmp in bdict2:
                    tmp='-'+tmp
                out32=out32+tmp+'\n'
            
            #比對輸出
            fout.write('==fd32_' + str(len(listdict3)) +'_比對結果\n')
            fout.write(out32.encode('utf8'))
            
            fout.write('%\n')
            fout.close()
        #sys.exit()################
        print 'ok'
    elif p:
        print '同人'
    #
    return

def log():
    '''
    log年份
    新增模式_動作 筆數 網站 時間 作者 
    #'''
    return

#main(key='八色',ucheck=0)
#ほりとも
#龍牙翔

#已知作者頁面，給定參數建檔。(跳過特殊符號用)
#main(key='木星在住',ucheck=2,pn=78,nlink='http://www.doujinshi.org/browse/author/36341/Mokusei-Zaijuu/')
