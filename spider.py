#!python
# encoding: utf-8
import urllib
import urllib2
import ssl
import gzip, StringIO
import re
import chardet

class Spider:

    # static member
    headers = ''
    timeout = 0

    def __init__(self, headers, timeout):
        Spider.headers = headers
        Spider.timeout = timeout
    

    @staticmethod
    def crawl(url):
        req = urllib2.Request(url, headers=Spider.headers)
        response = urllib2.urlopen(req, timeout=Spider.timeout)
        html = response.read()

        # check zip
        encoding = response.info().get('Content-Encoding')
        #if html[:6] == '\x1f\x8b\x08\x00\x00\x00':
        if encoding == 'gzip':
            html = gzip.GzipFile(fileobj=StringIO.StringIO(html)).read()

        # check charset
        charset = chardet.detect(html)['encoding']
        if charset != 'utf-8':
            html = html.decode('gbk', 'ignore').encode('utf8')
        return html

    @staticmethod
    def analyse(html):
        #print html      
        pattern = re.compile('<div class="pic-area".*?<img  class="z-tag data-lazyload-src".*?data-lazyload-src="(.*?)".*?>.*?</div>',re.S)  
        items = re.findall(pattern, html)
        return items

    @staticmethod
    def analyse_links(html):
        pattern = re.compile('(?<=href=").*?(?=")')
        links = re.findall(pattern, html)
        return links

