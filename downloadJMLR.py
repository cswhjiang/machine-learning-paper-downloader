# -*- coding: utf-8 -*-

import urllib
from urllib import urlretrieve  
#import sys,os,string  
#from HTMLParser import HTMLParser
import HTMLParser,sys,os,string  
from htmlentitydefs import name2codepoint
import re,htmlentitydefs
import codecs
import io

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
                     url=' '):
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
          
    def toString(self):
        bib_str = '@ARTICLE{' +self.key + ',\n' + \
              'author = {' + self.author+ '},\n'+\
              'title = {' + self.title + '},\n'+\
              'journal = {' + self.journal + '},\n' + \
              'year = {' + self.year+ '},\n' + \
              'volume = {' + self.volume+ '},\n' + \
              'pages = {' + self.pages+ '},\n' + \
              'month = {' + self.month+ '},\n' + \
              'publisher = {' + self.publisher +'},\n' + \
              'url = {' +  self.url +'}\n' + \
              '}\n'
        return bib_str
        
def checkURL(url):
    prefix = 'http://www.jmlr.org'
    if not( url[0:len(prefix)] == prefix):
        return prefix + url
    else:
        return  url
    
class MyHTMLParser(HTMLParser.HTMLParser):
    
    def extract_bibtex(self, html, volume ):
        self.tag_stack = []
        self.bibtex_list = []
        self.volume = str(volume)
        self.bibtex = Mybibtex()
        self.feed(html)
        return self.bibtex_list
    
#    def get_bibtex_list(self):
#        return self.bibtex_list
        
    def handle_starttag(self, tag, attrs):   
        if len(self.tag_stack) > 0:
            self.tag_stack.append(tag.lower())
            
        if tag == 'dl':
            self.tag_stack.append(tag.lower())
#            print '---------'
        elif tag == 'a':
#            print 'start tag: a', attrs
            if len(attrs)>=2:
                current_url = attrs[1][1]
                current_url1 = attrs[0][1]
#                print 'current_url', current_url
#                print 'current_url1', current_url1
                if current_url[-3:] == 'pdf':
                    a = current_url.rfind('/')
#                    print '     key:', current_url[a+1:-4]
#                    print '     URL:', current_url 
                    self.bibtex.set_key(current_url[a+1:-4])
                    self.bibtex.set_url(checkURL(current_url))
                elif current_url1[-3:] == 'pdf':
                    a = current_url1.rfind('/')
#                    print '     key:', current_url1[a+1:-4]
#                    print '     URL:', current_url1 
                    self.bibtex.set_key(current_url1[a+1:-4])
                    self.bibtex.set_url(current_url1)
         
            
    def handle_endtag(self, tag):

        if len(self.tag_stack)>0:
            self.tag_stack.pop()
            if tag == 'dl':
                self.tag_stack = []
                self.bibtex.set_journal('Journal of Machine Learning Research')
                self.bibtex.set_publisher('JMLR.org')
                self.bibtex.set_volume(self.volume)
                self.bibtex_list.append(self.bibtex)
                self.bibtex = Mybibtex()
                
            
        
    def handle_data(self, data):   
        data = data.strip(); 
        data = data.strip('\n'); 
        if len(self.tag_stack) > 0:
            if self.tag_stack[-1] == 'dt':
#                print '    title:', data
                if data != '':
                    self.bibtex.set_title(data)
            elif self.tag_stack[-1] == 'b' :
#                print '    author:', data
                if data != '':
                    self.bibtex.set_author(data)
            elif self.tag_stack[-1] == 'dd':
                data = data.strip();
                data = data.strip('\n');

                data = data.lstrip(';')
                data = data.rstrip('.')
                data = data.strip();
#                print '   data:', data
                a = data.find(':')
                b = data.find(',')

                month_str = data[0:a]
                month_str_index1 = month_str.find('(')
                month_str_index2 = month_str.find(')')
                
#                print '    month:', data[0:a]
#                print '    pages:', data[a+1:b]
#                print '    year:', data[b+1:] 
                
                if data[a+1:b] != '':
                    self.bibtex.set_pages(data[a+1:b])
                if data[b+1:].strip() != '':
                    self.bibtex.set_year(data[b+1:].strip())
                if month_str[month_str_index1+1:month_str_index2] != '':
                    self.bibtex.set_month(month_str[month_str_index1+1:month_str_index2])

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
            
#     p = re.compile("<span>[a-zA-Z-]*</span>")
#     content_clearn = p.sub(myReplace, content_clearn)
    return content_clearn

##
# Removes HTML or XML character references and entities from a text string.
#
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.
def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)
             
#download file
def download_URL(url, folder_name):
    index = url.rfind('/')
    file_name = url[index+1:]
    print 'downloading ' + url
    try:
        urlretrieve(url, folder_name + '/'+file_name)
    except:
        print 'urlretrieve error: ' + url
        pass
    
      

def my_parse(v):
    folder_name = 'Volume_' + str(v)
    bib_name = 'jmlr_' + str(v) + '.bib'
    bib_name = folder_name + '/' + bib_name
    
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        
#    url = 'http://jmlr.csail.mit.edu/papers/v14/'
    prefix_url = 'http://jmlr.csail.mit.edu/papers/v'
    url = prefix_url+ str(v)
    
    print '======= analyzing '+ url

    fp = urllib.urlopen(url)
    try:
        data = fp.read()
    finally:
        fp.close()
#     data = preProcess(data)
    data = data.decode('utf-8')
    data = unescape(data)
    data = data.replace('<i>','')
    data = data.replace('</i>','')
    data = data.replace('<sub>','')
    data = data.replace('</sub>','')
    data = data.replace('<small>','')
    data = data.replace('</small>','')
    data = data.replace('<sup>','')
    data = data.replace('</sup>','') 

    
#    print data
    parser = MyHTMLParser()
    bib_list = parser.extract_bibtex(data,volume=v)

#     f = open(bib_name, 'w')
    f = codecs.open(bib_name, encoding='utf-8', mode='w')
#     f = io.open(bib_name, 'wb', encoding='utf8')
    for i in range(len(bib_list)):
        print bib_list[i].url
        f.write(bib_list[i].toString())
        
    f.close()

    for i in range(len(bib_list)):
        download_URL(bib_list[i].url, folder_name)

          
if __name__ == "__main__":
#    my_parse()
    for a in range(1,15):
        my_parse(a)
              
    print 'Done'


