#!python
# encoding: utf-8
import sys,os
import urllib
import urllib2
import re
import ssl
import Queue
from spider import Spider
import logging


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
 
queue = Queue.Queue()

visited = set()

logging.basicConfig(filename='dump.log', format='%(asctime)s %(message)s', level=logging.INFO)

def save(images):
    for imgurl in images:
        print 'save ', imgurl 
        strs = imgurl.split('/')
        u = urllib.urlopen(imgurl)
        data = u.read()
        f = open(os.path.join(ROOT, strs[-1]), 'wb')
        f.write(data)
        f.close()

def create_dir(dir):
    if not os.path.exists(dir):
        print('Creating directory ' + dir)
        os.makedirs(dir)
 
def main():
    # project dir
    create_dir(ROOT)

    Spider(DEFAULT_HEADERS, DEFAULT_TIMEOUT)

    queue.put("http://pp.163.com/pp/#p=10&c=-1&m=3&page=1")

    # start 
    while queue.empty() == False:
        url = queue.get()
        print "crawl ", url
        logging.info('now crawl %s', url)
        html = Spider.crawl(url)
        images = Spider.analyse(html)
        links = Spider.analyse_links(html)
   
        queue.task_done()

        visited.add(url)

        # new urls
        for link in links:
            if (link not in visited) and link[0:18] == 'http://pp.163.com/':
                queue.put(link)

        save(images)

    print 'done'
 
if __name__ == "__main__":
    main()
