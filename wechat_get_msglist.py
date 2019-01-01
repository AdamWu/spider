# -*- coding: utf-8 -*-
import urllib
import urllib2
import re
import requests
import time
import json
import random

# 目标url
url = "https://mp.weixin.qq.com"

headers = {
    "HOST": "mp.weixin.qq.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) Chrome/62.0.3202.62 Safari/537.36",
}

# 设置cookies
cookies_str = '{"bizuin": "3566806113", "xid": "50ebfd3ba036318d0b8ca3a111dd1c40", "uuid": "bcc14aa01325566eb87d81d11639bffb", "slave_user": "gh_0b9735a895c6", "pgv_si": "s9214551040", "openid2ticket_oYSSZ1MFghkgJh3deILU_ipjtAyw": "En+JtYDILLNoc3xk6bG3PqY6WruXA1CwFr+j1KfEjps=", "cert": "suFtd5rFdgcG7xIlIbiUA2j30sLrwGGX", "ua_id": "vbnDtqQnbrGJTLHLAAAAAFdmf4G7OQ5VLUnD34rSMjs=", "mm_lang": "zh_CN", "noticeLoginFlag": "1", "slave_sid": "cDIxYkRtd2pYdDFCOUg1Tzh3Nk1QeXJYT3JmSHFfRGxfZ3JDb0IzRE1TMEZnWWFocmhJMnZZcTlBOUJjWEluV3IzYVJtdldkZFl1TV9IR0xyeGptVU5ISzBYTGRYbWxUSF94QW02OW9jZVBiUkpmaERqbFY4b042ejNDc2NwcFo3aFhXR0hlcU1JWEc5VE1u", "data_bizuin": "3566806113", "ticket": "616d18064b2462c61ebc5fb3cc34dfa9da7495ec", "data_ticket": "xBY7KYA0eJw0yxykUhMx17huHoy+CJ1vl0bWARIBNcn4GihKj9KkVCYFs7hRyeh0", "pgv_pvi": "2753649664", "ticket_id": "gh_0b9735a895c6"}'
cookies = json.loads(cookies_str)

# 获取token
response = requests.get(url=url, cookies=cookies)
print "url", response.url
token = re.findall(r'token=(\d+)', str(response.url))[0]
print "token", token

# 获取制定公众号文章列表
appmsg_url = "https://mp.weixin.qq.com/cgi-bin/appmsg?"

"""
需要提交的data
以下个别字段是否一定需要还未验证。
注意修改yourtoken,number
number表示从第number页开始爬取，为5的倍数，从0开始。如0、5、10……
token可以使用Chrome自带的工具进行获取
fakeid是公众号独一无二的一个id，等同于后面的__biz
"""
data_query = {
    "token": token,
    "lang": "zh_CN",
    "f": "json",
    "ajax": "1",
    "random": random.random(),
    "action": "list_ex",
    "begin": "0",
    "count": "5",
    "query": "",
    "fakeid": "MzIwMDk5MzMzMQ==",
    "type": "9",
}

# 获取文章列表
msglist = []
for i in range(0, 200, 5):
    data_query['begin'] = i
    response = requests.get(url=appmsg_url, cookies=cookies, headers=headers, params=data_query)
    content_json = response.json()
    if content_json.has_key('app_msg_list'):
        for item in content_json['app_msg_list']:
            msglist.append({'title':item['title'], 'url':item['link']})
    else:
        print "error!!!", content_json

    time.sleep(random.uniform(1,5))

print(len(msglist))
for item in msglist:
    print(item['title'])

# 保存文件json
with open('msglist.txt', 'w+') as f:
    f.write(json.dumps(msglist))

"""
# 保存文件csv
with open('msglist.csv', 'w+') as f:
    for item in msglist:
        f.write("%s,%s\n" % (item['title'], item['url']))
"""


