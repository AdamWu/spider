#!python
# encoding: utf-8
import urllib
import urllib2
import ssl
import gzip, StringIO
import re
import chardet
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time
import logging

driver = webdriver.PhantomJS(executable_path="webkit/phantomjs.exe")


class Spider:

    # static member
    headers = ''
    timeout = 0

    def __init__(self, headers, timeout):
        Spider.headers = headers
        Spider.timeout = timeout
    

    @staticmethod
    def crawl(url):
        driver.get(url)
        #time.sleep(1)

    @staticmethod
    def analyse_imgs(html):
        pattern = re.compile('<img .*? data-src="(.*?)".*?>',re.S)  
        items = re.findall(pattern, html)
        return items

    @staticmethod
    def analyse():
        items = {}

        elements = driver.find_elements_by_xpath("//*[@data-type='jpeg']")

        try:
            WebDriverWait(driver, 30).until(lambda driver: len(elements) > 0)
        except TimeoutException:
            print 'TimeoutException'
            logging.error("TimeoutException")
            return items

        for element in elements:
            title = ""
            el_title = element.find_elements_by_xpath("./following-sibling::span")
            if len(el_title) > 0:
                title = el_title[0].text
            else:
                # 上一个<p>
                el_title = element.find_elements_by_xpath("../preceding-sibling::p")
                if len(el_title) > 0 and len(el_title[-1].text) > 0:
                    title = el_title[-1].text
                else:
                    # 下一个<p>
                    el_title = element.find_elements_by_xpath("../following-sibling::p")
                    if len(el_title) > 0 and len(el_title[0].text) > 0:
                        title = el_title[0].text
                    else:
                        # 上上个<p>
                        el_title = element.find_elements_by_xpath("../preceding-sibling::p")
                        if len(el_title) > 0:
                            el_title = el_title[-1].find_elements_by_xpath("./preceding-sibling::p")
                            if len(el_title) > 0:
                                title = el_title[-1].text

            if len(title) > 50:
                title = ""
            #print "title", title
            items[element.get_attribute('data-src')] = title
        
        return items

    @staticmethod
    def analyse_links(html):
        pattern = re.compile('(?<=href=").*?(?=")', re.I)
        links = re.findall(pattern, html)
        return links

