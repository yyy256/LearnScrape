# -*- coding: utf-8 -*-
"""
Created on Tue Mar 03 14:49:45 2015

@author: yaoyu
"""
# 下载R语言会议的所有讲演稿

import requests
from bs4 import BeautifulSoup
import re

url = "http://cos.name/chinar/"

html = requests.get(url)
data = BeautifulSoup(html.content)

# 获取每届会议的url
# urls = [link.get('href') for link in data.find_all('a') if 'summary' in link.get('href')]
urls = [link.get('href') for link in data.find_all(href=re.compile('summary'))]

summary_url = []
for url in urls:
    if url not in summary_url:
        if 'http' in url:
            summary_url.append(url)
        else:
            summary_url.append('http://cos.name' + url[2:])

# 下载文件
for url in summary_url:
    h = requests.get(url)
    d = BeautifulSoup(h.content)
    links = d.find_all(href=re.compile('uploads'), text = True)
    for link in links:
        l = link.get('href')
        dl = requests.get(l, timeout = 10)
        with open(link.text.strip().replace('/', '') + '.' + l.split('.')[-1], 'wb') as f:
            f.write(dl.content)
                