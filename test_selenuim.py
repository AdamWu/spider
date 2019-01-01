#coding:utf-8
#引入selenium中的webdriver
from selenium import webdriver
import time
#webdriver中的PhantomJS方法可以打开一个我们下载的静默浏览器。
#输入executable_path为当前文件夹下的phantomjs.exe以启动浏览器
driver =webdriver.PhantomJS(executable_path="webkit/phantomjs.exe")
 
#使用浏览器请求页面
driver.get("https://www.baidu.com/")
#加载3秒，等待所有数据加载完毕
time.sleep(3)

print driver.page_source

links = driver.find_elements_by_xpath('//a')
for link in links:
	print link.text 


#关闭浏览器
driver.close()
