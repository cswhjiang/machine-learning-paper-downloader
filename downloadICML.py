import urllib
from urllib import urlretrieve  
#import sys,os,string  
# from HTMLParser import HTMLParser
import HTMLParser,sys,os,string  
from htmlentitydefs import name2codepoint
import re,htmlentitydefs

import urllib2
import lxml.html.soupparser as soupparser
# import xml.etree.ElementTree as etree
import lxml.etree as etree
import codecs
import re



class Mybibtex():
    def __init__(self, key=' ',
                     author=' ',
                     title=' ',
                     journal=' ',
                     year=' ',
                     volume=' ',
                     pages=' ',
                     month=' ',
                     publisher=' ',
                     url=' ',
                     booktitle=' '):
        self.key = key
        self.author = author
        self.title = title
        self.journal = journal
        self.year = year
        self.volume = volume
        self.pages = pages
        self.month = month
        self.publisher = publisher
        self.url = url
        self.booktitle = booktitle
        
    def set_key(self,key):
        if key != None:
            self.key = key
                
    def set_author(self,author):
        if author != None:
            self.author = author
        
    def set_title(self,title):
        if title != None:
            self.title = title
        
    def set_journal(self,journal):
        if journal != None:
            self.journal = journal
        
    def set_year(self,year):
        if year != None:
            self.year = year
        
    def set_volume(self,volume):
        if volume != None:
            self.volume = volume
        
    def set_pages(self,pages):
        if pages != None:
            self.pages = pages
        
    def set_month(self,month):
        if month != None:
            self.month = month
        
    def set_publisher(self,publisher):
        if publisher != None:
            self.publisher = publisher
        
    def set_url(self,url):
        if url != None:
            self.url = url
    def set_booktitle(self, booktitle):
        if booktitle != None:
            self.booktitle = booktitle
            
    def get_url(self):
        return self.url
    
    def toString(self):
        bib_str = '@inproceedings{' + self.key + ',\n' + \
              'author = {' + self.author + '},\n'+\
              'title = {' + self.title + '},\n'+\
              'year = {' + self.year + '},\n' + \
              'pages = {' + self.pages + '},\n' + \
              'publisher = {' + self.publisher + '},\n' + \
              'url = {' +  self.url + '},\n' + \
              'booktitle = {' +  self.booktitle + '}\n' + \
              '}\n'
        return bib_str
        

def download_URL(url, folderName):
    index = url.rfind('/')
    file_name = url[index+1:]
    print 'downloading ' + url
    urlretrieve(url, folderName + '/'+file_name)


def getAuthors(authorStr):
    authorStr = authorStr.strip()
    authorList = authorStr.split(',')
    for index in xrange(len(authorList)):
        authorList[index] = authorList[index].strip()
 
    return ' and '.join(authorList)

def getPageNum(pageStr):
    pageStr = pageStr.strip();
    pageArray = pageStr.split(':')
    page = pageArray[1]
    page = page.split(',')
    page = page[0]
    return page.strip()
    
def getLink(prefix, url):
    if len(url) < len(prefix):
        url = prefix + url
    return url

def getKey(urlStr):
    index = urlStr.rfind('/')
    file_name = urlStr[index+1:]
    return file_name[:-4]

def valid_XML_char_ordinal(i):
    return ( # conditions ordered by presumed frequency
        0x20 <= i <= 0xD7FF 
        or i in (0x9, 0xA, 0xD)
        or 0xE000 <= i <= 0xFFFD
        or 0x10000 <= i <= 0x10FFFF
        )
   
def myReplace(inputMath):
	inputStr = inputMath.group()
	outputStr = inputStr[6:]
	return outputStr[0:-7]

def preProcess(content):
	content_clearn = ''
	for i in xrange(len(content)):
		if valid_XML_char_ordinal(ord(content[i])):
			content_clearn = content_clearn + content[i]
		else:
			content_clearn = content_clearn + '___'
			
	p = re.compile("<span>[a-zA-Z-]*</span>")
	content_clearn = p.sub(myReplace, content_clearn)
	return content_clearn

def scanningArticle(url,year_str):
    print url
    content = urllib2.urlopen(url).read()
    content = preProcess(content)
    year_num = int(year_str)-2000
    booktitle_str = 'Proceedings of the ' + str(30+year_num-13) + 'th International Conference on Machine Learning (ICML-' + str(year_num)+')'
#     print content
#     print '--------------------------------'
#     print content_clearn
    dom = soupparser.fromstring(content) 
    
    body = dom[1]
    articleList = body.xpath('//div/p[@class="title"]')
    authorList = body.xpath('//div//p//span[@class="authors"]')
    infoList = body.xpath('//div//p//span[@class="info"]')
    linkList = body.xpath('//div//p[@class="links"]')
     
    bib_list = []
    for article, author, info, link in zip(articleList,authorList, infoList,linkList):
        bib_temp = Mybibtex()
        bib_temp.set_title(article.text.strip())
        bib_temp.set_author(getAuthors(author.text))
        bib_temp.set_url(getLink(url, link[1].attrib['href']))
        bib_temp.set_author(getAuthors(author.text))
        bib_temp.set_publisher('JMLR Workshop and Conference Proceedings')
        bib_temp.set_pages(getPageNum(info.text))
        bib_temp.set_key(getKey(bib_temp.get_url()))
        bib_temp.set_year(year_str)
        bib_temp.set_booktitle(booktitle_str)
        bib_list.append(bib_temp)
         
        print article.text
        print getAuthors(author.text)
        print getPageNum(info.text)
#         print link[1].attrib
        print getLink(url, link[1].attrib['href'])
        print 
 
 
    folderName = 'icml_' + year_str
    if not os.path.exists(folderName):
        os.makedirs(folderName)
     
    bib_file_name = 'icml_'+year_str+'.bib' 
    f = codecs.open(folderName + '/' + bib_file_name, encoding='utf-8', mode='w')
#     f = open( bib_file_name, 'w')
    for i in range(len(bib_list)):
#         print str(bib_list[i])
        f.write(bib_list[i].toString())
      
    f.close()
     
#     for i in range(len(bib_list)):
#             download_URL(bib_list[i].url,folderName)

    
          
if __name__ == "__main__":
    year_str = '2014'
    url = "http://jmlr.org/proceedings/papers/v32/"
#     url = "file:///home/jwh/Desktop/temp/ICML_2013.html"
#     my_parse(url,year_str)     
    scanningArticle(url,year_str)
    print 'Done'



# @inproceedings{mehta13, 
#     Publisher = {JMLR Workshop and Conference Proceedings}, 
#     Title = {Sparsity-Based Generalization Bounds for Predictive Sparse Coding}, 
#     Author = {Nishant Mehta and Alexander G. Gray}, 
#     Pages = {36-44}, 
#     Year = {2013}, 
#     Booktitle = {Proceedings of the 30th International Conference on Machine Learning (ICML-13)} 
#    }
