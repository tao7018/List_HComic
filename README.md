# List_HComic
===============
###
爬蟲

###爬蟲目標
wnacg
hdm2011
nhentai

簡稱	網址
cl	http://comiclist.jp/index.php				單行本		成人非成人向，2009前單行本
di	http://www.daito-i.com/top/index.php		單篇_單行本	單行本書目，2010以前沒有
dmm	http://www.dmm.co.jp/dc/book/			電子雜誌	電子單篇
dls	http://www.dlsite.com/books/			電子雜誌_其他	擔任原畫
gc	http://www.getchu.com/				其他
djs	http://www.doujinshi.org/				同人_單行本	出道年份
tn	http://www.toranoana.jp/cgi-bin/R2/d_search.cgi	同人
ngm	http://nagomi.ne.jp/web/top/			同人

####檔案
key.txt
半形，沒有符號、空格。

####最終的成品
畫品!作者	同_商_單-同-商-單	出道年_同人最新_商刊最新	-tag_備註_(它tag)
單行本_^檢驗過單行本_
單行本加註[集數]
同人
單篇

####成品可以爬取的元素
單行本
1comic
雜誌單篇(單行本單篇)
2magazine
同人(同人合本)
3doujin
一般向青年向作品
4generalcomic
被動畫作品
5anime
擔任插畫(特指小說類)
6art
擔任原畫(特指電子產品)
7cg
其它插畫
8other

####各網站爬取的資料分類_定義_
cl
新單行本
newcomic
成人向單行本
adultcomic
cl成人向單行本多卷
cladultcomicnum
一般向青年向單行本
nomalcomic
它項單行本
othercomic
不明單行本
unknowcomic

gc
gc新
gcnew
gc漫畫(BOOKS,雑誌,同人)
gcbook
動畫
anime
遊戲
game
其它
other

dls
dls新
dlsnew
dls單作者作品
dlsbook
dls多作者作品
dlsbooknum
dls同人作品
dlsdj
dls其它

dls提及作者漫畫

dls提及作者其它

==new_0_新
==book_9_漫單
==numbook_10_漫多
==dbook_0_漫同人
==other_0_它
==obook_2_漫
==oother_0_它
di
==new_0_新刊
==book_1_單行本
==adult_16_雜誌
==art_0_作畫擔任
==other_0_其他
==fd32_15_比對結果


comiclist
==adult_1_成人向
==adultnum_0_成人向多卷
==new_0_新
==nomal_0_一般向青年向
==unknow_0_不明
==other_0_它項
getchu
==book_1_BOOKS,雑誌,同人
==anime_0_アニメ
==game_0_PCゲーム,DVD-PG
==new_0_新
==other_0_其他
dlsite
==new_0_新
==book_9_漫單
==numbook_10_漫多
==dbook_0_漫同人
==other_0_它
==obook_2_漫
==oother_0_它
daito-i
==new_0_新刊
==book_1_單行本
==adult_16_雜誌
==art_0_作畫擔任
==other_0_其他
==fd32_15_比對結果
dmm
djs
tn
ngm