#!python
# encoding: utf-8
import sys,os
import urllib
import urllib2
import re
import Queue
from spider import Spider
import logging
import time
import random
import datetime
import uuid
import json
import ssl
import socket
import shutil

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

logging.basicConfig(filename='dump'+datetime.datetime.now().strftime('%Y%m%d%H%M%S')+'.log', format='%(asctime)s %(message)s', level=logging.INFO)

def generateFileName(name, ext, dir):
    if len(name) == 0:
        name = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    
    filename = os.path.join(dir, name) + ext
    i = 0
    while os.path.exists(filename):
        filename = os.path.join(dir, name) + str(i) + ext
        i = i + 1

    return filename

def save(images, subdir):

    logging.info("save images %s", len(images))

    subdir = re.sub('[\/:*?"<>|]','-',subdir).replace('.','')

    dstdir = os.path.join(ROOT, subdir)
    if os.path.exists(dstdir):
        shutil.rmtree(dstdir)
    create_dir(dstdir)

    i = 0
    for url in images:
        title = images[url]
        if len(title) == 0:
            title = str(i)
            i = i + 1
        print 'download image ... ', title,  url
        logging.info("download image %s %s", title, url)

        # download
        try:
            request = urllib2.Request(url, headers=DEFAULT_HEADERS)
            response = urllib2.urlopen(request, timeout=DEFAULT_TIMEOUT)
            
        except urllib2.URLError as e:
            logging.error("cannot reach the server.  %s", url)
        except urllib2.HTTPError as e:
            logging.error("cannot fulfill the request. %s", url)


        # save to file
        try:
            data = response.read()
            title = re.sub('[\/:*?"<>|]','-', title).replace('\n','-').replace('\r','-')
            filename = generateFileName(title, '.jpg', dstdir)
            print filename
            f = open(filename, 'wb')
            f.write(data)
            f.close()
        except ssl.SSLError as e:
            logging.error("SSLError. %s", url)
        except socket.timeout as e:
            logging.error("socket timeout. %s", url)


        time.sleep(random.uniform(0.1,1))


def create_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
 
def main():
    # project dir
    create_dir(ROOT)

    Spider(DEFAULT_HEADERS, DEFAULT_TIMEOUT)

    # 读取url列表
    file = open('msglist.json')
    text = file.read()
    file.close()
    urls = json.loads(text)

    urls_visited = []
    if os.path.exists('visited.txt'):
        file = open('visited.txt', 'r')
        for line in file:
            urls_visited.append(line.rstrip())

    urlmap = {}
    for item in urls:
        title = item['title']
        url = item['url']
        if url in urls_visited:
            print 'visited', url
            continue

        urlmap[url] = title
        queue.put(url)

    # start 
    file = open('visited.txt', 'a')
    while queue.empty() == False:
        url = queue.get()
        print "crawl ", url
        logging.info('now crawl %s', url)
        Spider.crawl(url)
        print "analyse ", url
        logging.info('now analyse %s', url)
        images = Spider.analyse()
   
        queue.task_done()

        visited.add(url)

        save(images, urlmap[url])

        file.write(url+'\n')
        file.flush()

    file.close()
    print 'finished'
    logging.info('finished')
 
if __name__ == "__main__":
    main()
