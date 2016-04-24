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

#資料處理
def findbook(dictB, listdata, receive):
    link, key, p, pn, pnn, olddate=receive
    mlink = 'http://comiclist.jp/'
    if len(link)<5:
        return dictB, listdata, pnn, olddate
    
    res = requests.get(link)
    res.encoding =  res.apparent_encoding
    only_a_tags = SoupStrainer(id="listBOX-search")#id='listArea'
    soup = BeautifulSoup(res.text ,"lxml",  parse_only=only_a_tags)#.prettify()
    
    bn=len(soup.select('tr'))-1
    
    a =0
    for tm in soup.select('tr')[1:]:
        if pnn==0:
            return dictB, listdata, pnn, olddate
        pnn=pnn-1
        a=a+1
        print '\r',pnn,
        
        check=0
        cname = tm.select('.list-name')[0].select('a')
        
        #作者
        c=0
        bname=''
        for t in cname:
            t=t.text
            nname=''
            if u'　他' in t:#多作者特徵
                nname=u'_他'
                t=t.replace(u'　他','')
            t=Q2B(t.replace(u'　',''))
            if key.decode('utf8') == t[:t.find(u'［')]:
                c=1
                tt=t[-2:-1]
                if (u'画' == tt) or (u'著' == tt):#畫者作者
                    check=1
                else:#無後綴_非畫者作者
                    check=5
            bname=bname+t+'_'
        if c==0:
            continue
        bname=bname.strip('_')+nname
        if len(nname) >0:#多人
            check=4
        
        cbook = tm.strong.text
        cdate = tm.select('.list-day')[0].text
        clink= tm.select('.list-book')[0].a.get('href')
        blink=mlink+clink
        
        #書名_18
        if (u'（成）' not in cbook) and (check == 1):#去前綴
            check = 3
        elif check==1:
            cbook = cbook.replace(u'（成）','')
        
        #多卷
        if (u'巻' in cdate) and (int(cdate[10:-1]) > 1):
            cbook = cbook + '[' + cdate[10:-1] + ']'#冊數
            cdate=cdate[:10].replace(u'/','')
        
        #data處理
        cdate = cdate.rstrip()
        if len(cdate) < 8:#無日期
            cdate = '00000000'#填入日期
            check = 2#新作
        data = cdate
        while listdata.count(data):#重複日期判斷
            data = data[:-2] + str(int(data[-2:]) + 1).rjust(2,'0')#尾數+1_十位數填0
        listdata.append(data)
        
        #olddate
        if (len(olddate) > 0) and (int(cdate) < int(olddate[:8])):
            olddate = olddate + '_' + str(pn-pnn)
        
        bname = bname.encode('utf8')
        cbook = cbook.encode('utf8')
        cdate = cdate.encode('utf8')
        
        #字典新增
        book = cbook
        if check == 1:#成人向
            dictB["dict1"].setdefault(data,book)
        elif check ==2:#新
            book = book + '_[' + bname + ']\n!' + blink
            dictB["dict2"].setdefault(data,book)
        elif check ==3:#一般向青年向
            dictB["dict3"].setdefault(data,book)
        elif check ==4:#多人
            book = book + '_[' + bname + ']\n!' + blink
            dictB["dict4"].setdefault(data,book)
        else:#他項
            book = book + '_[' + bname + ']\n!' + blink
            dictB["dict5"].setdefault(data,book)
        
        if a==(bn):
            break
        #continue
    print '.'
    #print '========'
    return dictB, listdata, pnn, olddate

########
def main(key='',ucheck=0,pn=0,nlink=''):
    #ucheck_0建檔_1更新_2直讀
    
    pnum = 30#頁顯示數量
    mlink = 'http://comiclist.jp/'#前綴網址
    
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

        link = "http://comiclist.jp/index.php?p=s&mode=ss&keyword=" + urllib.quote(key) + "&type=title"
        res = requests.get(link)

        res.encoding =  res.apparent_encoding#亂碼處理
        only_a_tags = SoupStrainer(id='listArea')#縮小檢索範圍
        soup = BeautifulSoup(res.text ,"lxml",  parse_only=only_a_tags)
        
        #搜尋作者
        pn=0
        nname=0
        a=0
        c=0
        pn=int(soup.find_all('b')[1].text)

        #updata
        if (ucheck == 1) and (os.path.isfile('output/' + key.decode('utf8') + '_comiclistv1.txt')):#更新與欲輸入檔案存在
            fupdata = open('output/'+key.decode('utf8') + '_comiclistv1.txt', 'r+')
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
    if pn>0:
        pnn=pn
        if int(pn) > pnum:
            print 'BIG'

        if ucheck == 1:
            fupdata.seek(0, 2)
            fupdata.write('!updata\n!筆數' + str(pn).encode('utf8') +'_'+ strftime("%Y/%m/%d,%H:%M")+'->')
        else:
            fout = open('output/'+key.decode('utf8') + '_comiclistv1.txt', 'w')#寫入模式開檔
            fout.write('comiclist\n')
            fout.write('!' + key + '_!'+link+'\n')
            fout.write('!總筆數' + str(pn).encode('utf8') +'_'+ strftime("%Y/%m/%d,%H:%M")+'->')
        
        print '==comiclist' , pn, '筆'
        time.sleep(1)
        p = 0#頁
        #建空輸出用字典與陣列
        dict1={}#作者成人向
        dict2={}#作者成人向新刊
        dict3={}#作者一般向青年向
        dict4={}#多人
        dict5={}#它項_作者無後綴
        dictB={
            'dict1':dict1,'dict2':dict2,'dict3':dict3,'dict4':dict4,
            'dict5':dict5
        }
        bnum = ''#卷
        listdata = []
        
        #資料處理
        while (int(pn) - p * pnum) > 0:
            p = p + 1
            print 'page:' + str(p)
            
            nlink = "http://comiclist.jp/index.php?\
            p=s&mode=ss&type=title&keyword=" + urllib.quote(key) + "&andor=and&maxline=30&pgn=1&pgn=" + str(p)
            send=[nlink, key, p, pn, pnn, olddate]#pn
            dictB, listdata, pnn, olddate = findbook(dictB, listdata, send)#資料處理
            time.sleep(1)

        #日期排序
        #listdata.sort()
        
        listw=['==book_' + str(len(dictB["dict1"])) +'_成人向\n',
               '==new_' + str(len(dictB["dict2"])) +'_新\n',
               '==generalbook_' + str(len(dictB["dict3"])) +'_一般向青年向\n',
               '==magazine_' + str(len(dictB["dict4"])) +'_多人\n',
               '==other_' + str(len(dictB["dict5"])) +'_他項\n'
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
            fout.write('%\n')
            fout.close()
        #sys.exit()################
        print 'ok'
    elif soup.find_all('b')[1].text:
        print '同人'
    #
    return

#main(key='木星在住',ucheck=0)
#main(key='hisasi',ucheck=0)

#已知作者頁面，給定參數建檔。(跳過特殊符號用)
#main(key='木星在住',ucheck=2,pn=78,nlink='http://www.doujinshi.org/browse/author/36341/Mokusei-Zaijuu/')