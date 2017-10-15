#!/usr/bin python
# -*- coding:utf-8 -*-

import requests

"""
    谷歌学术：https://scholar.google.com/citations?user=WXQ7lBQAAAAJ&hl=zh-CN
    pagesize列表数据的获取：
    1 url要带cstart和pagesize变量
    2 每次data和url同时迭代
    3 当没有数据的时候json中key-B的value为空
        200
        {"P":1,"B":""}
"""

url = 'https://scholar.google.com/citations?user=WXQ7lBQAAAAJ&hl=zh-CN'
headers = {'content-type':'application/x-www-form-urlencoded',
           'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
           'x-chrome-uma-enabled':'1',
           'x-client-data':'CKi1yQEIhrbJAQijtskBCMG2yQEI+pzKAQipncoB'}

session = requests.Session()
reget = session.get(url=url,headers=headers)
html1 = reget.text
print('--------------')
data = {'cstart':0,'pagesize':100,'json':1}
url = 'https://scholar.google.com/citations?user=WXQ7lBQAAAAJ&hl=zh-CN&cstart=0&pagesize=100'
repost = session.post(url=url,headers=headers,data=data)
print(repost.status_code)
print(repost.text)
print('--------------')
data = {'cstart':100,'pagesize':100,'json':1}
url = 'https://scholar.google.com/citations?user=WXQ7lBQAAAAJ&hl=zh-CN&cstart=100&pagesize=100'
repost = session.post(url=url,headers=headers,data=data)
print(repost.status_code)
print(repost.text)
print('--------------')
data = {'cstart':200,'pagesize':100,'json':1}
url = 'https://scholar.google.com/citations?user=WXQ7lBQAAAAJ&hl=zh-CN&cstart=200&pagesize=100'
repost = session.post(url=url,headers=headers,data=data)
print(repost.status_code)
print(repost.text)
print('--------------')
data = {'cstart':300,'pagesize':100,'json':1}
url = 'https://scholar.google.com/citations?user=WXQ7lBQAAAAJ&hl=zh-CN&cstart=300&pagesize=100'
repost = session.post(url=url,headers=headers,data=data)
print(repost.status_code)
print(repost.text)