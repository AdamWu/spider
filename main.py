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
import time
import random
import datetime
import uuid

#context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)

ROOT = 'result/'

DEFAULT_HEADERS = {
    'x-requestted-with': 'XMLHttpRequest',
    'Accept-Language': 'zh-cn',
    'Accept-Encoding': 'gzip, deflate',
    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
    'ContentType': 'application/x-www-form-urlencoded; chartset=UTF-8',
}
DEFAULT_TIMEOUT = 100
 
queue = Queue.Queue()

visited = set()

logging.basicConfig(filename='dump.log', format='%(asctime)s %(message)s', level=logging.INFO)


URL = 'https://mp.weixin.qq.com/s/ekLzkxbEv4CPlitYRv9-HQ'

IGNORES = [
    '/pp/[a-z]+',
    '/square/',
    '/group/',
    '/pic/',
    '/html/',
    '/pp/#p=-1',
    '/pp/#p=^10',
]

FILTERS = [
    'http://pp.163.com/',
]

def generateFileName(name, ext):
    if len(name) == 0:
        name = datetime.datetime.now().strftime('%y%m%d%H%M%S')
    
    filename = os.path.join(ROOT, name) + ext
    i = 0
    while os.path.exists(filename):
        filename = os.path.join(ROOT, name) + str(i) + ext
        i = i + 1

    return filename

def save(images):
    logging.info("save %s", len(images))
    for url in images:
        title = images[url]
        print 'save ', url, title

        # download
        try:
            request = urllib2.Request(url, headers=DEFAULT_HEADERS)
            response = urllib2.urlopen(request, timeout=DEFAULT_TIMEOUT)
            
        except urllib2.URLError as e:
            print 'We failed to reach a server.'
            print e
        except urllib2.HTTPError as e: 
            print 'The server could not fulfill the request.' 
            print e

        # save to file
        try:
            data = response.read()
        except ssl.SSLError as e:
            print "error read"
            print e

        filename = generateFileName(title, '.jpg')
        f = open(filename, 'wb')
        f.write(data)
        f.close()
        time.sleep(random.uniform(0,1))


def create_dir(dir):
    if not os.path.exists(dir):
        print('Creating directory ' + dir)
        os.makedirs(dir)
 
def main():
    # project dir
    create_dir(ROOT)

    Spider(DEFAULT_HEADERS, DEFAULT_TIMEOUT)

    queue.put(URL)

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

        save(images)

        # new urls
        for link in links:
            if (link not in visited) and link[0:18] == 'http://pp.163.com/':

                exist = False
                for ignore in IGNORES:
                    match = re.search(re.compile(ignore), link)
                    if match:
                        #logging.info("exclude %s", link)
                        exist = True
                        break

                if exist == False:  
                    queue.put(link)
    

    print 'done'
 
if __name__ == "__main__":
    main()
