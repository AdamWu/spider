import time
import json
import random
from selenium import webdriver
import urllib
import urllib2

post = {}

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')

driver = webdriver.Chrome(executable_path="webkit/chromedriver.exe",chrome_options = chrome_options)

driver.get('https://mp.weixin.qq.com')
time.sleep(3)

# 输入账户密码
driver.find_element_by_name('account').clear()
driver.find_element_by_name('account').send_keys("calvinmankor@139.com")
driver.find_element_by_name('password').clear()
driver.find_element_by_name('password').send_keys("120688wuyunze")

# 模拟点击
time.sleep(5)
driver.find_element_by_xpath('./*//a[@class="btn_login"]').click()

# 扫码
time.sleep(10)

# 获取cookies, 保存到文件
driver.get('https://mp.weixin.qq.com')
cookie_items = driver.get_cookies()
for cookie_item in cookie_items:
	post[cookie_item['name']] = cookie_item['value']
with open('cookies.txt', 'w+') as f:
	f.write(json.dumps(post))
