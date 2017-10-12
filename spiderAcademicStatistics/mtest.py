#!/usr/bin python
# -*- coding:utf-8 -*-

import requests

# url = 'https://scholar.google.com/citations'
url = 'https://scholar.google.com/citations?user=WXQ7lBQAAAAJ&hl=zh-CN'
# url = 'https://scholar.google.com/citations?user=WXQ7lBQAAAAJ&hl=zh-CN&cstart=0&pagesize=80'

# headers = {'content-type':'application/x-www-form-urlencoded',
#            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
#            'x-chrome-uma-enabled':'1',
#            'x-client-data':'CKi1yQEIhrbJAQijtskBCMG2yQEI+pzKAQipncoB'}
headers = {'content-type':'application/x-www-form-urlencoded',
           'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
           }

# data = {'user':'WXQ7lBQAAAAJ','hl':'zh-CN','cstart':'20','pagesize':'80','json':'1'}
# data = {'user':'WXQ7lBQAAAAJ','hl':'zh-CN','cstart':'100','pagesize':'100'}
data = {'cstart':'100','pagesize':'100'}

session = requests.Session()
session.get(url=url,headers=headers)
cookies = session.cookies

re = session.post(url=url,headers=headers,data=data,cookies=cookies)
print(re.status_code)
print(re.content)
print('--------------')
print(re.text)