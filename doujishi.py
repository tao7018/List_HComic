# -*- coding: utf-8 -*- 
import urllib , requests , sys ,string ,time
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from time import gmtime, strftime

'''doujinshi
作者來源key.txt

#處理類別
同人CG_同人ノベル_同人誌
漫画_雑誌_商業ノベル_商業本その他
#不處理類別
商業アートブック_商業CG_商業その他_商業ソフト_漫画 (抜粋)
海賊版_カレンダー_ムック_ポストカード_ポスター_下敷き_テレホンカード_不詳
同人グッズ_同人映像作品_同人音楽作品_同人その他_同人ソフト

#流程
1詳細搜尋頁_最高作品數作者
2作者頁_別名
3作品頁_作者+同人場次
4輸出

#結果key_doujinshi.text
#輸出格式：
doujinshi
!作者_doujishiID
!總筆數_開始時間->結束時間
!商業刊出道時間_[別名]
==djs_數量_同人(同人CG_同人ノベル_同人誌)
[原作][同人場cXX]作品名
==ndjs_數量_同人合本
[同人團][作者][原作][同人場cXX]作品名
!作者數!作品網址
==book_數量_單行本(漫画)
作品名
==magazine_數量_雜誌(雑誌)
[作者]作品名
!作者數!作品網址
==other_數量_其他商業作品(商業ノベル_商業本その他)
[類型][作者]作品名
!作者數!作品網址
==ondjs_數量_別名同人
[同人團][作者][原作][同人場cXX]作品名
!作者數!作品網址
==onbook_數量_別名商業作品
[類別][作者]同人作品
!作者數!作品網址
'''

#頁顯示數量
pnum = 50
mlink = 'http://www.doujinshi.org/'

fkey = open('key.txt', 'r')
nkey=list(fkey)
#key = fkey.readline()#key=作者
fkey.close()

key = nkey[0]
if '(' in key:
    key=key[key.find('(')+1:key.find(')')]
key=key.strip('\n').strip('').lower()

#key=作者
key2 = urllib.quote(key.decode('utf8').encode('shift_jis'))#當sjis輸出utf8的url
key3 = urllib.unquote(key2.decode('shift_jis').encode('utf8'))#utf8的url翻sjis
#網址用
key4 = urllib.quote(key)

#檢查BOM
if '%EF%BB%BF' in urllib.quote(key):
    print 'fuck ms'

'''搜尋網址
http://www.doujinshi.org/search/item/?order=objects&T=author&flow=DESC&sn=%E7%8A%AC&Q=s&match=3&page=1
http://www.doujinshi.org/browse/author/42893/Hisasi/?order=title&page=1
http://www.doujinshi.org/search/item/
?Q=s&
T=author&#搜尋項目
sn=%E7%8A%AC&#關鍵字
match=3&#搜尋模式_0模糊1前2後3精確4聲似
order=objects&#排序
flow=DESC#升降_ASC升 DESC降
'''

link="http://www.doujinshi.org/search/item/\
?order=objects&T=author&flow=DESC&sn="+key4+"&Q=s&match=3&page=1"
#搜尋例_東山翔_犬_inu#資料缺少例_方言#馬甲例_大友卓二

#cookis_語言預設英文，透過cookie設定。
cookies = {'PHPSESSID':'qlac2h749s2fpjtgqlnmqbvlo4',
           ' AGE':'18',
           '__utmt':'1',
           '__utma':'221679373.1195927157.1458231980.1458231980.1458231980.1',
           '__utmb':'221679373.6.10.1458231980',
           '__utmc':'221679373',
           '__utmz':'221679373.1458231980.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
           'LANG':'2'
}

res = requests.get(link,cookies=cookies)
res.encoding =  res.apparent_encoding#亂碼處理
soup = BeautifulSoup(res.text,"html.parser")

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
def save(sdict , check=0):
    for tep in listdata:
        if sdict.get(tep):
            #fout.write(sdict[tep].encode('utf8')  + '\n')
            fout.write(sdict[tep]  + '\n')
    #return

#作品頁面
def finddata(dlink,check):
    global oname
    res = requests.get(dlink,cookies=cookies)
    res.encoding =  res.apparent_encoding
    rr= res.text
    rtn=rr[rr.find(u'<tr><td><B>イベント:'):rr.find(u'<tr><td><B>シリーズ:')]#同人場段落
    rr=rr[rr.find(u'<tr><td colspan=3><br><div class="list">著者:'):]
    rr=rr[:rr.find(u'<tr><td colspan=3><br><div class="list">',1)]
    
    #同人作品檢查
    if check==1:
        rr=rtn+'\n'+rr
    so=BeautifulSoup(rr,"lxml")
    
    dcheck=0
    s=0
    dcxx=''
    dname=''
    doname=''
    n=0
    #book_club_raw
    
    #cxx
    if check==1:
        dcxx=so.a.text
        s=2
    
    #作者
    for b in so.select('td')[1+s::3]:#日文_英文_空
        if Q2B(b.text).strip().strip('\n').replace('\t','').replace('\n','')==key.decode('utf8'):
            dcheck=1
        elif (len(oname)>0) and (Q2B(b.text).strip().strip('\n').replace('\t','').replace('\n','') in oname):
            doname=Q2B(b.text).strip().strip('\n').replace('\t','').replace('\n','')#抓出別名
        dname=dname+Q2B(b.text).strip().strip('\n').replace('\t','').replace('\n','')+'_'
        n=n+1
    dname=dname.strip('_')
    
    #類型
    if (n>1) and (check == 1):#同人的多作者
        check=2
    elif (n>1) and (check != 4):#非雜誌的多作者
            check=5
    if (dcheck==0) and (check==2 or check==1):#馬甲+同人
        check=6
    elif dcheck==0:#馬甲
        check=7
    
    return dname,dcxx,check,doname,n

#資料處理
def findbook(page = 1, link = 'www'):
    global mindate,oname
    
    if len(link)<5:
        return 0
    
    link=link+'?order=title&page='+str(page)
    res = requests.get(link,cookies=cookies)#日文介面
    res.encoding =  res.apparent_encoding
    r= res.text
    r1=r[r.find(u'<div class="rounded_box">'):r.find(u'<!--rounded_box-->')+len(u'<!--rounded_box-->')]#含別名內容
    rt='<table border=0 width=\"100%\" class=\'tablefixing\'>'
    r2=r[r.rfind(rt)+len(rt):r.rfind('</table>')]#主內容
    
    #別名
    if (page==1) and (u'別名' in r1):
        #so = BeautifulSoup(r1,"lxml")
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
    doc.pop()
    
    a =0
    for tm in doc[:]:
        sou = BeautifulSoup(tm,"lxml")
        
        cbook=sou.select('.tab.LPEXACT1')[0].text
        cclub=sou.select('.tab.LPEXACT1')[2].text
        craw=sou.select('.tab.LPEXACT1')[4].text
        ctype=sou.select('.tab.LPEXACT1')[5].text
        clink=sou.a.get('href')
        
        cdata=clink[6:]
        cdata=cdata[:cdata.find('/')]
        cdate=sou.select('.tab.L33')[1].text
        cdate=cdate[cdate.find(u'発行日:')+len(u'発行日:'):cdate.find(u'-')].strip().strip('\n')
        blink=mlink+clink[1:]
        
        a=a+1
        print '\r',a,
        
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
        
        #作者與場次
        cname,ccxx,check,coname,n=finddata(blink,check)#連結_判斷類型
        
        #商業作品出道年
        if ((check==4) or (check==3)) and (int(cdate) > 1000) and (mindate - int(cdate) > 0):
            mindate=int(cdate)
        
        #data處理
        if len(cdata) < 3:#無data
            cdata = '0000/00/00'#填入data
            check = 4#
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
        #print cdata,cbook,cclub,craw,ctype,cdate,coname,n,clink,'\ncheck:',check,
        #print type(craw),type(cclub),type(ccxx),type(coname),type(cdata),type(cdate),type(blink),type(cname),
        
        #寫入dict
        if n>5 :#太多作者
            cname=key
            if check > 5:#馬甲
                cname=coname
        
        if check==1:#同人
            book='['+craw+']['+ccxx+']'+cbook
            dict1.setdefault(data,book)
        elif check==2:#同人合本
            book='['+cclub+']['+cname+']['+craw+']['+ccxx+']'+cbook+'\n!'+str(n)+'!'+blink
            dict2.setdefault(data,book)
        elif check==3:#單行本
            book=cbook
            dict3.setdefault(data,book)
        elif check==4:#雜誌
            book='['+cname+']'+cbook+'\n!'+str(n)+'!'+blink
            dict4.setdefault(data,book)
        elif check==5:#其他商業作品
            book='['+ctype+']'+'['+cname+']'+cbook+'\n!'+str(n)+'!'+blink
            dict5.setdefault(data,book)
        elif check==6:#別名同人
            book='['+cclub+']['+cname+']'+'['+craw+']['+ccxx+']'+cbook+'\n!'+str(n)+'!'+blink
            dict6.setdefault(data,book)
        else:#別名商業作品
            book='['+ctype+']'+'['+cname+']'+cbook+'\n!'+str(n)+'!'+blink
            dict7.setdefault(data,book)
        
        #if a>4:
        if a==(bn):
            break
        continue
    print '.'
    #print '========'
    #return

########START
'''
1單同_同人CG_同人ノベル_同人誌
2多同

3單漫_漫画
4雑誌
5多漫_商業ノベル_商業本その他

6別名同
7別商
#'''

pn=0
nname=0
a=0
c=0

if len(soup.select('.next'))>0:#存在下一頁
    mp=len(soup.select('.header')[0].text)-2
    fplink=link[:-1]+str(mp)
    print 'Big~'

for temp in soup.find_all(title='More Info'):
    tmp=str(temp)
    tmp=tmp[:tmp.rfind('<br>')]
    tmp=tmp[tmp.find('"More Info">')+len('"More Info">'):tmp.rfind('(')].strip('\t\n ').lower()
    if key == tmp:
        nname=nname+1
        #print tmp,len(tmp)
        if c==0:
            c=1
            nlink=temp.get('href')
            nid=nlink[15:]
            nid=nid[:nid.find('/')]
            nlink=mlink+nlink[1:]#作者網址
            print nlink,nid,type(nid)
            
            pt=soup.find_all(title='More Info')[a].parent.parent.td.a.text
            pn=int(pt[:pt.find(u'作品')])#資料筆數
    a=a+1

print '符合筆數'+str(nname)+'_作品筆數'+str(pn)

#資料筆數_是否數字
if pn>0:
    if pn > pnum:
        print 'BIG'
    
    fout = open('output/'+key.decode('utf8') + '_doujishiv1.txt', 'w')#寫入模式開檔
    fout.write('doujishi\n')#doujishi
    print key , pn , 'num\n========v1'
    time.sleep(1)
    fout.write('!' + key + '_' + nid.encode('utf8') + '\n!總筆數' + str(pn).encode('utf8') +'_'+ strftime("%Y/%m/%d,%H:%M")+'->')
    
    p = 0#頁
    #建空輸出用字典與陣列
    dict1={}#同人目標作者
    dict2={}#同人多作者
    dict3={}#漫畫
    dict4={}#雜誌
    dict5={}#其他商業
    dict6={}#馬甲同人
    dict7={}#馬甲商業
    listdata = []
    mindate=9999#出道年
    oname=[]#別名
    
    #資料處理
    while (int(pn) - p * pnum) > 0:
        p = p + 1
        print 'page:' + str(p)
        #soup = next(p, nlink)#頁
        
        #print soup.select('.TBLdtil')[2]
        #findbook(soup)#資料處理
        findbook(p, nlink)#資料處理
        time.sleep(1)
        
    #日期排序
    #listdata.sort()
    
    fout.write(strftime("%H:%M")+'\n!'+str(mindate)+'_')#出道年
    if len(oname) > 0:
        fout.write('[')
        for tm in oname:#別名
            fout.write(tm.encode('utf8')+'_')
        fout.write(']')
    fout.write('\n')
    
    #dict1_同人
    fout.write('==djs_' + str(len(dict1)) +'_同人\n')
    save(dict1)
    #dict2_同人合本
    fout.write('==ndjs_' + str(len(dict2)) +'_同人合本\n')
    save(dict2)
    #dict3_單行本
    fout.write('==obook_' + str(len(dict3)) +'_單行本\n')
    save(dict3)
    #dict4_雜誌
    fout.write('==magazine_' + str(len(dict4)) +'_雜誌\n')
    save(dict4)
    #dict5_其他商業作品
    fout.write('==other_' + str(len(dict5)) +'_其他商業作品\n')
    save(dict5)
    #dict6_別名同人
    fout.write('==ondjs_' + str(len(dict6)) +'_別名同人\n')
    save(dict6)
    #dict7_別名商業作品
    fout.write('==onbook_' + str(len(dict7)) +'_別名商業作品\n')
    save(dict7)
    
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