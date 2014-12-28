import urllib2
import urllib
import lxml.html.soupparser as soupparser
import os,errno,sys

def downloadAllNIPS():
    urlPrefix = 'http://papers.nips.cc/book/advances-in-neural-information-processing-systems'
    for i in range(26):
        print 
        print '============ ' + 'nips' + str(i+1) + '(' + str(1988+i)+')' ' ============='
        url = urlPrefix +'-'+ str(i+1) +'-'+ str(1988+i)
        print url
        handleNIPSURL(url, str(1988+i))
        

def reporthook(a,b,c): 
    print "% 3.1f%% of %d bytes\r" % (min(100, float(a * b) / c * 100), c),
    sys.stdout.flush()

def getFileName(url):
    s = url.split('/')
    s = s[-1].split('-')
    return s[0]


def handleNIPSURL(nipsURL, yearStr):
    yearStr = 'NIPS' + yearStr
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
        pdfURL = paperURL+ '.pdf'
        bibURL = paperURL + '/bibtex'
        fileName = getFileName(paperURL)
        fileName = yearStr + '_' + fileName
        print paperURL
        print fileName

        urllib.urlretrieve(pdfURL, yearStr+'/'+fileName + '.pdf',reporthook)
        urllib.urlretrieve(bibURL, yearStr+'/'+fileName + '.bib')
        print
        print
        
if __name__ == "__main__":
    url = 'http://papers.nips.cc/book/neural-information-processing-systems-1987'
    handleNIPSURL(url, '1987')
#     downloadAllNIPS() 




        
    
    
    
    
    