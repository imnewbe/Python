#! /usr/bin/env python
__author__ = 'yoyoyo'
import requests
import sys
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf8')
url='http://www.tianyatool.com/cgi-bin/bbs.pl?url=http://bbs.tianya.cn/post-16-1019242-{0}.shtml'
table = []
for i in xrange(1,99):
	table.append(url.format(i))
for x in table:
	r=requests.get(x)
	bu=BeautifulSoup(r.content)
	detail = bu.findAll('div',{"class":"bbs-content"})
	with open('novle.txt','a+') as f:
		f.write(str(detail)+"\n")