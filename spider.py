#!python
# encoding: utf-8
import sys,os
import urllib
import urllib2
import ssl
import gzip, StringIO
import re

#context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)

ROOT = 'result/'

DEFAULT_HEADERS = {
    'x-requestted-with': 'XMLHttpRequest',
    'Accept-Language': 'zh-cn',
    'Accept-Encoding': 'gzip, deflate',
    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
    'ContentType': 'application/x-www-form-urlencoded; chartset=UTF-8',
}
DEFAULT_TIMEOUT = 120
 
 
def get(url):
    req = urllib2.Request(url, headers=DEFAULT_HEADERS)
    response = urllib2.urlopen(req, timeout=DEFAULT_TIMEOUT)
    html = response.read()

    # check zip
    if html[:6] == '\x1f\x8b\x08\x00\x00\x00':
        html = gzip.GzipFile(fileobj=StringIO.StringIO(html)).read()
    html = html.decode('gbk').encode('utf8')
    return html
 
def parse(html):
    print "parse"
    #print html      
    pattern = re.compile('<div class="pic-area".*?<img  class="z-tag data-lazyload-src".*?data-lazyload-src="(.*?)".*?>.*?</div>',re.S)  
    myItems = re.findall(pattern, html)
    items = []    
    for item in myItems:
        items.append(item)

    return items

def save(images):
    i = 0
    for imgurl in images:       
        u = urllib.urlopen(imgurl)
        data = u.read()
        f = open(os.path.join(ROOT, str(i)+'.jpg'), 'wb')
        f.write(data)
        f.close()
        i = i + 1

 
def main():
    html = get("http://pp.163.com/longer-yowoo/pp/10069141.html")
    images = parse(html)
    save(images)
 
 
if __name__ == "__main__":
    main()
