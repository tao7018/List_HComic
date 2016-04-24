# -*- coding: utf-8 -*- 
import urllib , requests , sys , string   ,time , os
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from time import gmtime , strftime


import doujishi
import comiclist
import daito-i
#key=''_ucheck=0

fkey = open('key.txt', 'r')
nkey=list(fkey)
#key = fkey.readline()#key=作者
fkey.close()


for key in nkey:
    #key = nkey[0]
    print key
    if '(' in key:
        key=key[key.find('(')+1:key.find(')')]
    key=key.strip('\n').strip('').lower()
    #doujishi.main(key)
    #comiclist.main(key)
    daito-i.main(key)