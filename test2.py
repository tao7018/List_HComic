# -*- coding: utf-8 -*- 
import urllib , requests , sys ,string ,time
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

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

#key.encoding =  key.apparent_encoding
print sys.getdefaultencoding()
print '1一:',key
#print u'2二:',key.decode('utf8')
key=key.decode('utf8')
print '2二:',key.encode('utf8')
#.decode('utf8')

#raw_input("\nPress Any Key To Exit")