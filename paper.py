#! /usr/bin/env python
__author__ = 'yoyoyo'
import threading
import re
import random
import requests
import Queue
def GetUrl(host,pattern,queue):
    proxy = {"http": "http://127.0.0.1:8087", "https": "https://127.0.0.1:8087"}
    response = requests.get("http://arxiv.org/list/cs.CR/recent", proxies=proxy, verify=False)
    url = re.findall(pattern, response.text)
    hostList = []
    threads = []
    for r in url:
        downPdfUrl = host+r
        hostList.append(downPdfUrl)
    for k in hostList:
            queue.put(k[:])
    for x in xrange(5) :
            thread  = myThread(host,pattern,queue)
            threads.append(thread)
    for h in threads:
            h.start()
    for i in threads:
            i.join()


       # return hostList
       # for hosts in hostList:
       #     queue.put(hosts)
       # Uri=queue.get()
       # r = requests.get(Uri)
       # with open(str(random.randint(1, 100))+'.pdf', 'wb') as code:
       #     code.write(r.content)
       # queue.task_done()
class myThread (threading.Thread):
    def __init__(self, url, pattern,queue):
        threading.Thread.__init__(self)
        self.pattern = pattern
        self.queue=queue
    def run(self):
        while 1:
            if not self.queue.empty():
                Uri=self.queue.get()
                r = requests.get(Uri)
                with open(str(random.randint(1, 100))+'.pdf', 'wb') as code:
                    code.write(r.content)
            else:
                break
               # queue.task_done()
           # GetUrl(self.pattern)
if __name__ == '__main__':

    host = 'http://arxiv.org'
    pattern = r'\/pdf\/\d{4}\.\d{5}'
    queue=Queue.Queue()
    #downhost = list[GetUrl(pattern)]
    #for j in downhost:
    #    queue.put(j)
   # queue.join()
    GetUrl(host,pattern,queue)



















