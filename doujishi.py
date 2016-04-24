# -*- coding: utf-8 -*- 
import urllib , requests , sys , string   ,time , os
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from time import gmtime , strftime

'''
doujishi

doujishi.txt
'''

#全轉半_unicode輸入
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
def save(fout , listdata , sdict , check=0):
    for tep in listdata:
        if sdict.get(tep):
            fout.write(sdict[tep]  + '\n')
    #return

#作品頁面
def finddata(key , dlink,check,oname,cook):
    res = requests.get(dlink,cookies=cook)
    res.encoding =  res.apparent_encoding
    rr= res.text
    rr=rr[rr.rfind('<table'):rr.rfind('<!--round_middle-->')+len('<!--round_middle-->')]
    so=BeautifulSoup(rr,"lxml")
    
    dcxx=''
    dname=''
    dbook=''
    dclub=''
    draw=''
    dcheck=0
    n=0
    doname='!!!!'
    
    #同人
    if check==1:
        dcxx=so.find_all('td',text='イベント:')[0].next_sibling.text.strip(' \n')

        #club
        s= so.find_all('div').index(so.find_all('div',text='サークル:')[0])#div位置
        a= so.find_all('td').index(so.find_all('div')[s].parent)#td開始位置
        b= so.find_all('td').index(so.find_all('div')[s+1].parent)#td結束位置
        for temp in so.find_all('td')[a+1:b:3]:
            dclub= dclub+temp.text.strip(' \n')+'_'
        dclub= dclub.strip('_')
        
        #raw
        s= so.find_all('div').index(so.find_all('div',text='原作:')[0])#div位置
        a= so.find_all('td').index(so.find_all('div')[s].parent)#td開始位置
        b= so.find_all('td').index(so.find_all('div')[s+1].parent)#td結束位置
        for temp in so.find_all('td')[a+1:b:3]:
            draw= draw+temp.text.strip(' \n')+'_'
        if draw.count('_') > 1:
            draw= 'mix'
        draw= draw.strip('_')
    
    #標題
    dbook=so.find_all('td',text='原題:')[0].next_sibling.text.strip(' \n')
    
    #name作者
    s= so.find_all('div').index(so.find_all('div',text='著者:')[0])#div位置
    a= so.find_all('td').index(so.find_all('div')[s].parent)#td開始位置
    b= so.find_all('td').index(so.find_all('div')[s+1].parent)#td結束位置
    for temp in so.find_all('td')[a+1:b:3]:#日文_英文_空
        if Q2B(temp.text).strip(' \n') == key.decode('utf8'):
            dcheck=1
        elif (len(oname) > 0) and (Q2B(temp.text).strip(' \n') in oname):
            doname=Q2B(temp.text).strip(' \n')#抓出別名
        dname=dname+Q2B(temp.text).strip(' \n')+'_'
    n=dname.count('_')
    dname= dname.strip('_')
    
    #類型
    if (n>1) and (check == 1):#同人的多作者
        check=2
    elif (n>1) and (check != 4):#非雜誌的多作者
            check=5
    if (dcheck==0) and (check==2 or check==1):#馬甲+同人
        check=6
    elif dcheck==0:#馬甲
        check=7
    #
    return dname, dcxx, dbook, dclub, draw, check, doname, n

#資料處理
def findbook(dictB , listdata , oname , cook , receive):
    link, mindate, key, pn, pnn, olddate=receive
    mlink = 'http://www.doujinshi.org/'    
    if len(link)<5:
        return dictB,listdata,oname,mindate,pnn,olddate
    
    res = requests.get(link,cookies=cook)#日文介面
    res.encoding =  res.apparent_encoding
    r= res.text
    r1=r[r.find(u'<div class="rounded_box">'):r.find(u'<!--rounded_box-->')+len(u'<!--rounded_box-->')]#含別名內容
    rt='<table border=0 width=\"100%\" class=\'tablefixing\'>'
    r2=r[r.rfind(rt)+len(rt):r.rfind('</table>')]#主內容
    
    #別名
    if (int(link[-1:])) and (u'別名' in r1):#別從存在，則加入主要作者名。搜尋名不一定是主名
        rt=r1[r1.find(u'日本名:</B>')+len(u'日本名:</B>'):r1.find(u'<B>名前')]#作者主名
        rt=rt.replace('<br>','').strip().strip('\n').replace('\t','')
        r1=r1[r1.find(u'別名:</B><br>')+len(u'別名:</B><br>'):r1.find(u'<br><B>所属')]#別名內容
        r1=r1.replace('</A><br>','')
        oname=r1.strip().strip('\n').replace('\t','').split('\n')
        
        tt=0
        for ttemp in oname:
            oname[tt]=ttemp.strip().strip('\n')
            tt=tt+1
        oname.append(rt)
    
    bn=r2.count('\"thumbnail\"')#頁作品數
    doc=r2.split('<!--round_middle-->')
    doc.pop()#多餘項
    
    a =0
    for tm in doc[:]:
        if pnn==0:
            return dictB,listdata,oname,mindate,pnn,olddate
        pnn=pnn-1
        a=a+1
        print '\r',pnn,
        
        sou = BeautifulSoup(tm,"lxml")
        
        ctype=sou.select('.tab.LPEXACT1')[5].text
        clink=sou.a.get('href')
        check=0
        
        #類型
        if (u'同人CG' in ctype) or (u'同人ノベル' in ctype) or (u'同人誌' in ctype):
            check=1
        elif u'漫画' in ctype:
            check=3
        elif u'雑誌' in ctype:
            check=4
        elif (u'商業ノベル' in ctype) or (u'商業本その他' in ctype):
            check=5
        else:
            continue
        
        cdata=clink[6:]
        cdata=cdata[:cdata.find('/')]
        cdate=sou.select('.tab.L33')[1].text
        cdate=cdate[cdate.find(u'発行日:')+len(u'発行日:'):].strip().strip('\n').replace('-','')
        blink=mlink+clink[1:]
        #18_はい_いいえ
        cadult=sou.select('.tab.L66')[0].text
        cadult=cadult[cadult.find(u'18+:')+len(u'18+:'):].strip().strip('\n')
        
        #作者與場次
        cname, ccxx, cbook, cclub, craw, check, coname, n=finddata(key, blink, check, oname, cook)#連結_判斷類型
        
        #商業作品出道年
        if ((check==4) or (check==3)) and (int(cdate) > 10000000) and (int(mindate[:8]) - int(cdate) > 0):
            mindate=cdate+'!'+blink
        if (len(olddate) > 0) and (int(cdate) < int(olddate[:8])):
            olddate = olddate + '_' + str(pn-pnn)
        
        #data處理
        if len(cdata) < 3:#無data
            cdata = '00000000'#填入data
            #check = 4#
        data = cdata
        while listdata.count(data):#重複data判斷
            data = data[:-2] + str(int(data[-2:]) + 1).rjust(2,'0')#尾數+1_十位數填0
        listdata.append(data)
        
        ctype=ctype.encode('utf8')
        cbook=cbook.encode('utf8')
        craw=craw.encode('utf8')
        cclub=cclub.encode('utf8')
        coname=coname.encode('utf8')
        cdate=cdate.encode('utf8')
        cname=cname.encode('utf8')
        ccxx=ccxx.encode('utf8')
        
        if n>5 :#太多作者
            cname=key
            if check > 5:#馬甲
                cname=coname
        if (cadult==u'いいえ') and ((check==3 or check==4) or check==5):#一般向商業作品
            check=8
        
        #寫入dict
        if check==1:#同人
            book='['+craw+']['+ccxx+']'+cbook
            dictB["dict1"].setdefault(data,book)
        elif check==2:#同人合本
            book='['+cclub+']['+cname+']['+craw+']['+ccxx+']'+cbook+'\n!'+str(n)+'!'+blink
            dictB["dict2"].setdefault(data,book)
        elif check==3:#單行本
            book=cbook
            dictB["dict3"].setdefault(data,book)
        elif check==4:#雜誌
            book='['+cname+']'+cbook+'\n!'+str(n)+'!'+blink
            dictB["dict4"].setdefault(data,book)
        elif check==5:#其他商業作品
            book='['+ctype+']'+'['+cname+']'+cbook+'\n!'+str(n)+'!'+blink
            dictB["dict5"].setdefault(data,book)
        elif check==6:#別名同人
            book='['+cclub+']['+cname+']'+'['+craw+']['+ccxx+']'+cbook+'\n!'+str(n)+'!'+blink
            dictB["dict6"].setdefault(data,book)
        elif check==7:#別名商業作品
            book='['+ctype+']'+'['+cname+']'+cbook+'\n!'+str(n)+'!'+blink
            dictB["dict7"].setdefault(data,book)
        else:#一般向商業作品
            book='['+ctype+']'+'['+cname+']'+cbook+'\n!'+str(n)+'!'+blink
            dictB["dict8"].setdefault(data,book)
        
        if a==(bn):
            break
        #continue
    print '.'
    #print '========'
    return dictB,listdata,oname,mindate,pnn,olddate

########START
def main(key='',ucheck=0,pn=0,nlink=''):
    #ucheck_0建檔_1更新_2直讀
    
    pnum = 50#頁顯示數量
    mlink = 'http://www.doujinshi.org/'

    #cookis_語言預設英文，透過cookie設定。
    cook = {'PHPSESSID':'qlac2h749s2fpjtgqlnmqbvlo4',
               ' AGE':'18',
               '__utmt':'1',
               '__utma':'221679373.1195927157.1458231980.1458231980.1458231980.1',
               '__utmb':'221679373.6.10.1458231980',
               '__utmc':'221679373',
               '__utmz':'221679373.1458231980.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
               'LANG':'2'
    }
    
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

        link="http://www.doujinshi.org/search/item/\
        ?order=objects&T=author&flow=DESC&sn="+key4+"&Q=s&match=3&page=1"
        #搜尋例_東山翔_犬_inu#資料缺少例_方言#馬甲例_大友卓二

        res = requests.get(link,cookies=cook)
        res.encoding =  res.apparent_encoding#亂碼處理
        soup = BeautifulSoup(res.text,"html.parser")

        #搜尋作者
        pn=0
        nname=0
        a=0
        c=0
        if len(soup.select('.next'))>0:#太多同名_存在下一頁
            mp=len(soup.select('.header')[0].text)-2
            fplink=link[:-1]+str(mp)
            print 'Big~'
        for temp in soup.find_all(title='More Info'):
            tmp=str(temp)
            tmp=tmp[:tmp.rfind('<br>')]
            tmp=tmp[tmp.find('"More Info">')+len('"More Info">'):tmp.rfind('(')].strip('\t\n ').lower()#作者
            if key == tmp:
                nname=nname+1
                if c==0:#預設處理第一位(也是作品最多的)作者
                    c=1
                    nlink=temp.get('href')
                    nlink=mlink+nlink[1:]#作者網址

                    pt=soup.find_all(title='More Info')[a].parent.parent.td.a.text
                    pn=int(pt[:pt.find(u'作品')])#資料筆數
            a=a+1

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
        elif ucheck==0:
            print '符合筆數'+str(nname)+'_作品筆數'+str(pn)
    
    #資料筆數_是否數字
    if pn>0:
        pnn=pn
        nid=nlink[39:]
        nid=nid[:nid.find('/')]#網站作者流水號
        if pn > pnum:
            print 'BIG'
        
        if ucheck == 1:
            fupdata.seek(0, 2)
            fupdata.write('!updata\n!筆數' + str(pn).encode('utf8') +'_'+ strftime("%Y/%m/%d,%H:%M")+'->')
        else:
            fout = open('output/'+key.decode('utf8') + '_doujishiv1.txt', 'w')#寫入模式開檔
            fout.write('doujishi\n')
            fout.write('!' + key + '_' + nid.encode('utf8') + '_!'+link+'\n')
            fout.write('!總筆數' + str(pn).encode('utf8') +'_'+ strftime("%Y/%m/%d,%H:%M")+'->')
        
        print '==doujishi' , pn, '筆'
        time.sleep(1)
        p = 0#頁
        #建空輸出用字典與陣列
        dict1={}#同人目標作者
        dict2={}#同人多作者
        dict3={}#漫畫
        dict4={}#雜誌
        dict5={}#其他商業
        dict6={}#馬甲同人
        dict7={}#馬甲商業
        dict8={}#一般向商業
        dictB={
            'dict1':dict1,'dict2':dict2,'dict3':dict3,'dict4':dict4,
            'dict5':dict5,'dict6':dict6,'dict7':dict7,'dict8':dict8
        }
        listdata = []
        oname=[]#別名
        mindate='99999999'#出道年

        #資料處理
        while (int(pn) - p * pnum) > 0:
            p = p + 1
            print 'page:' + str(p)
            
            nlink=nlink+'?order=date&flow=DESC&page='+str(p)
            send=[nlink, mindate, key, pn, pnn, olddate]
            dictB, listdata, oname, mindate, pnn, olddate = findbook(dictB, listdata, oname, cook, send)#資料處理
            time.sleep(1)

        #日期排序
        #listdata.sort()
        
        listw=['==djs_' + str(len(dictB["dict1"])) +'_同人\n',
               '==ndjs_' + str(len(dictB["dict2"])) +'_同人合本\n',
               '==obook_' + str(len(dictB["dict3"])) +'_單行本\n',
               '==magazine_' + str(len(dictB["dict4"])) +'_雜誌\n',
               '==other_' + str(len(dictB["dict5"])) +'_其他商業作品\n',
               '==ondjs_' + str(len(dictB["dict6"])) +'_別名同人\n',
               '==onbook_' + str(len(dictB["dict7"])) +'_別名商業作品\n',
               '==nomal_' + str(len(dictB["dict8"])) +'_一般向商業作品\n'
              ]
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
            fout.write(strftime("%H:%M")+'_'+str(nb)+'\n!')
            if len(oname) > 0:
                fout.write('[')
                for tm in oname:#別名
                    fout.write(tm.encode('utf8')+'_')
                fout.write(']_')
            mindate=mindate[:4]+mindate[8:]
            fout.write(str(mindate[:])+'\n')#出道年
            for w in range(len(listw)):
                fout.write(listw[w])
                save(fout , listdata , dictB["dict"+str(w+1)],w+1)
            fout.write('%\n')
            fout.close()
        #sys.exit()################
        print 'ok'
    elif pn:
        print 'No Date'
    #
    return

#main(key='目目蓮',ucheck=0)

#已知作者頁面，給定參數建檔。(跳過特殊符號用)
#main(key='木星在住',ucheck=2,pn=78,nlink='http://www.doujinshi.org/browse/author/36341/Mokusei-Zaijuu/')
