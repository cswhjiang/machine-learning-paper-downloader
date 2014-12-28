# !/usr/bin/env python
import urllib2
import urllib
import lxml.html.soupparser as soupparser
import os,errno,sys

import Queue
import threading
import time


class NIPSPapersDowonloader(object):
    def __init__(self,thread_num=10):
        self.work_queue = Queue.Queue()
        self.threads = []
        self.__init_work_queue()
        self.__init_thread_pool(thread_num)

    def getFileName(self,url):
        s = url.split('/')
        s = s[-1].split('-')
        return s[0]
 
    def __init_thread_pool(self,thread_num):
        for i in range(thread_num):
            self.threads.append(Work(self.work_queue))

    def __init_work_queue(self):
        urlPrefix = 'http://papers.nips.cc/book/advances-in-neural-information-processing-systems'
        for i in range(27):
            nipsURL = urlPrefix +'-'+ str(i+1) +'-'+ str(1988+i)
            yearStr = 'NIPS' + str(1988+i)
            try:
                os.mkdir(yearStr)
            except OSError as exc: 
                if exc.errno == errno.EEXIST and os.path.isdir(yearStr):
                    pass
               
            paperPrefix = 'http://papers.nips.cc'
            content = urllib2.urlopen(nipsURL).read()   
            dom = soupparser.fromstring(content)  
            
            for ele in dom.iter(tag = 'li'):
                x = ele.getchildren()
                href = (x[0].attrib)['href']
                if len(href) <= 2:
                    continue
                
                if x[0].text != None:
                    print 'title: ' + x[0].text
                else:
                    print 'title: '
                
                for i in range(1,len(x)):
                    print "author: " + x[i].text
                    
                paperURL = paperPrefix + href
                fileName = self.getFileName(paperURL)
                fileName = yearStr + '/'+ yearStr + '_' + fileName
                args = [paperURL,fileName ]
                self.work_queue.put((do_job, args))



    def wait_allcomplete(self):
        for item in self.threads:
            if item.isAlive():item.join()

class Work(threading.Thread):
    def __init__(self, work_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self.start()

    def run(self):
        while True:
            try:
                do, args = self.work_queue.get(block=False)
                do(args)
                self.work_queue.task_done()
            except:
                break

def reporthook(a,b,c): 
    print "% 3.1f%% of %d bytes\r" % (min(100, float(a * b) / c * 100), c), sys.stdout.flush()

def do_job(args):
    paperURL = args[0]
    paperName = args[1]
    pdfURL = paperURL+ '.pdf'
    bibURL = paperURL + '/bibtex'
    pdfFileName = paperName + '.pdf'
    bibFileName = paperName + '.bib'
    print 'download: ' + pdfURL
    print 'to '+ pdfFileName
    
    urllib.urlretrieve(pdfURL, pdfFileName)
    urllib.urlretrieve(bibURL, bibFileName)


if __name__ == '__main__':
    start = time.time()
    work_manager =  NIPSPapersDowonloader(thread_num=20)
    work_manager.wait_allcomplete()
    end = time.time()
    print "cost all time: %s" % (end-start)