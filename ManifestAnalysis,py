# -*- coding: utf_8 -*-
import os
from xml.dom import minidom
import subprocess
import optparse
import time
def ReadManifest(manifest):
    with open(manifest,'r') as f:
            dat=f.read()
    return dat
def GetManifest(Dir):
    mfest=''
    dat=ReadManifest(Dir).replace("\n","")
    try:
        print "Get AndroidManifest.xml"
        mfest=minidom.parseString(dat)
    except Exception as e:
        print 'hehe'
    return mfest
def ManifestAnalysis(mfest):
    print "Started"
    mfxml=mfest
    manifest = mfxml.getElementsByTagName("manifest")
    services = mfxml.getElementsByTagName("service")
    activities = mfxml.getElementsByTagName("activity")
    applications = mfxml.getElementsByTagName("application")
    datas = mfxml.getElementsByTagName("data")
    intents = mfxml.getElementsByTagName("intent-filter")
    actions = mfxml.getElementsByTagName("action")
    granturipermissions = mfxml.getElementsByTagName("grant-uri-permission")
    mainact=''
    for activity in activities:
        if len(mainact)<1:
            for sitem in activity.getElementsByTagName("action"):
                val = sitem.getAttribute("android:name")
                if val == "android.intent.action.MAIN" :
                    mainact=activity.getAttribute("android:name")
            if mainact=='':
                for sitem in activity.getElementsByTagName("category") :
                    val = sitem.getAttribute( "android:name" )
                    if val == "android.intent.category.LAUNCHER" :
                        mainact=activity.getAttribute("android:name")
    for node in manifest:
        package = node.getAttribute("package")
        print 'packagename is:'+'  '+package
    RET=''
    EXPORTED=[]
    for service in services:
        if service.getAttribute("android:exported") == 'true':
            perm = ''
            if service.getAttribute("android:permission"):
                perm =' (permission '+service.getAttribute("android:permission")+' exists.) '
            servicename = service.getAttribute("android:name")
            print perm+'\n'+servicename+".........."+'expoted=true'+'\n'
    for application in applications:

        if application.getAttribute("android:debuggable") == "true":
            print 'debug detect  '
        if application.getAttribute("android:allowBackup") == "true":
            print '允许任意备份...allowBackup'
        elif application.getAttribute("android:allowBackup") == "false":
            pass
        else:
            print 'something wrong'
        if application.getAttribute("android:testOnly")== "true":
            print 'test modle'
        for node in application.childNodes:

            if node.nodeName == 'activity':
                itmname= 'Activity'

            elif node.nodeName == 'activity-alias':
                itmname ='Activity-Alias'

            elif node.nodeName == 'provider':
                itmname = 'Content Provider'
            elif node.nodeName == 'receiver':
                itmname = 'Broadcast Receiver'
            elif node.nodeName == 'service':
                itmname = 'Service'
            else:
                itmname = 'NIL'
            item=''
            if ((itmname =='Activity' or itmname=='Activity-Alias') and (node.getAttribute("android:taskAffinity"))):
                item=node.getAttribute("android:name")
                print'taskaffinity         ' +item#这样设置可能让别的应用读取intent，导致信息泄露
            if ((itmname =='Activity' or itmname=='Activity-Alias') and ((node.getAttribute("android:launchMode")=='singleInstance') or (node.getAttribute("android:launchMode")=='singleTask'))):
                item=node.getAttribute("android:name")
                print 'launchmode   '+item#可能会被别的应用读取正在调用的intent的内容
            item=''
            isExp=False
            if ('NIL' != itmname) and (node.getAttribute("android:exported") == 'true'):
                isExp=True
                perm=''
                item=node.getAttribute("android:name")
                if node.getAttribute("android:permission"):
                    perm = ' (permission '+node.getAttribute("android:permission")+' exists.) '
                if item!=mainact:
                    if (itmname =='Activity' or itmname=='Activity-Alias'):
                        EXPORTED.append(item)
                    print 'dangeous  '+ perm
            else:
                isExp=False
            impE=False
            if ('NIL' != itmname) and (node.getAttribute("android:exported") == 'false'):
                impE=True
            else:
                impE=False
            if (isExp==False and impE==False):
                isInf=False
                intentfilters = node.childNodes
                for i in intentfilters:
                    inf=i.nodeName
                    if inf=="intent-filter":
                        isInf=True
                if isInf:
                    item=node.getAttribute("android:name")
                    if item!=mainact:
                        if (itmname =='Activity' or itmname=='Activity-Alias'):
                            EXPORTED.append(item)
                            print 'exported     '+item

    for granturi in granturipermissions:
        if granturi.getAttribute("android:pathPrefix") == '/':
            print 'high level'
        elif granturi.getAttribute("android:path") == '/':
            print ' high level'
        elif granturi.getAttribute("android:pathPattern") == '*':
            print 'high level'


    for data in datas:#敏感信息
        if data.getAttribute("android:scheme") == "android_secret_code":
            xmlhost = data.getAttribute("android:host")
            print xmlhost+'info'
        elif data.getAttribute("android:port"):#
            print 'data disclosure'


    for intent in intents:#权限过高导致“覆盖”
        if intent.getAttribute("android:priority").isdigit():
            value = intent.getAttribute("android:priority")
            if int(value) > 100:
                print 'intent priority high enough？'

    for action in actions:
        if action.getAttribute("android:priority").isdigit():
            value = action.getAttribute("android:priority")
            if int(value) > 100:
                print 'action priority是不是有点高'
    if len(RET)< 2:
        print 'down'
def ReadApk(path,apkname):
    if path:
        try:
            os.system('unzip '+str(path)+str(apkname)+' -d'+str(apkname).replace('.apk',' '))
        except Exception as e:
            print str(e)
def BinaryParseXML(path,apkName):
    if path:
        try:#这里有个不智能的地方是默认了AXMLPrinter所在的目录，智能应当能指定。
            #其实这里可以转换文件后删除原来的AndroidManifest文件，然后重命名新生成的文件为原文件名，这样就好很多了。
            os.system("java -jar "+str(path)+"AXMLPrinter2.jar "+str(path)+str(apkName).replace(".apk",'')+"/"+"AndroidManifest.xml"+'>'+str(path)+str(apkName).replace(".apk",'')+"/"+"AndroidManifest1.xml")
        except Exception as e:
            print e
    else:
        time.sleep(10)
        return
if __name__=='__main__':
    parse = optparse.OptionParser('Usage:%prog [] path ')
    parse.add_option('-d','--dirPath',dest='name_file',default='/',help='path of apk',type='string')
    parse.add_option('-q','--akname',dest='apkname',default=None,type='string',help='input apk name')
    (options,args)=parse.parse_args()
    ReadApk(options.name_file,options.apkname)
    #time.sleep(10)
    BinaryParseXML(options.name_file,str(options.apkname).replace('.apk',''))
    #mn='AndroidManifest.xml'
    if options.apkname==None:
            print 'are you kidding me?'
            #break 合法性判断
#这样读出来的文件是不对的，还要用二进制转到string的xml文件
    try:
            t=GetManifest(options.name_file+'/'+str(options.apkname).replace('.apk','')+'/'+'AndroidManifest1.xml')
            ManifestAnalysis(t)
    except Exception  as e:
        print str(e)
