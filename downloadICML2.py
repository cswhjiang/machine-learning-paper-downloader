# -*- coding: utf-8 -*-


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
        
# http://machinelearning.wustl.edu/mlpapers/paper_files/icml2003_Zinkevich03.pdf
def download_URL(paper_key, folderName):
    prefix = 'http://machinelearning.wustl.edu/mlpapers/paper_files/'
    file_name = paper_key+'.pdf'
    url = prefix+file_name
    print 'downloading ' + url
    urlretrieve(url, folderName + '/'+file_name)
   
def getURL(inputMathStr):
    s1 = 'href="../papers/'
    s2 = '">'
    l1 = len(s1)
    l2 = len(s2)
    outputStr = inputMathStr[l1:]
    return outputStr[0:-l2]


# http://machinelearning.wustl.edu/mlpapers/bibtex/icml2003_Zinkevich03
def getBibStr(paper_key):
    prefix = 'http://machinelearning.wustl.edu/mlpapers/bibtex/'
#     print prefix + paper_key
    content = urllib2.urlopen(prefix + paper_key).read()
    content = content.replace('<br>&nbsp;&nbsp;&nbsp','')
    
    p = re.compile('<gcse:search></gcse:search>[\s\S]*}</body>')
    all_str = p.findall(content)
    bibstr = all_str[0]
#     print all_str[0]
    s1 = '<gcse:search></gcse:search>'
    s2 = '</body>'
    l1 = len(s1)
    l2 = len(s2)
    bibstr = bibstr[l1:]
    
    return bibstr[0:-l2].strip()

def getPaperURL(page_url):
    paper_url_list = []
    content = urllib2.urlopen(page_url).read()
    p = re.compile('href="../papers/[\S]*">')
    all_str = p.findall(content)
    for singleStr in all_str:
        paper_url_list.append(getURL(singleStr))
    
    return paper_url_list
    
    
def handle_a_year_ICML(year_str, paper_key_list):
    bib_str_all = ''
    folderName = 'icml_' + year_str
    bib_file_name = 'icml_' + year_str + '.bib'
    if not os.path.exists(folderName):
        os.makedirs(folderName)
        
#     prefix = 'http://machinelearning.wustl.edu/mlpapers/papers/'
    for paper_key in paper_key_list:
        download_URL(paper_key, folderName)
        bib_str_all = bib_str_all + getBibStr(paper_key) + '\n'
    
#     f = codecs.open(folderName + '/' + bib_file_name, encoding='utf-8', mode='w')
    f = open( folderName + '/' + bib_file_name, 'w')
    f.write(bib_str_all)
    f.close()
    
if __name__ == "__main__":
    f = open( 'icml_url.txt', 'r')
    lines = f.readlines()
    for line in lines:
        line =  line.strip()
        year_str, page_url = line.split(' ')
        paper_key_list = getPaperURL(page_url)
        handle_a_year_ICML(year_str, paper_key_list)
#         print len(paper_key_list)
#         print paper_key_list
        


