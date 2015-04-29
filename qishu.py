#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'yaoyu'

import requests
from bs4 import BeautifulSoup
import re
import os

if not os.path.exists('/home/yaoyu/金庸'):
    os.mkdir('/home/yaoyu/金庸')
os.chdir('/home/yaoyu/金庸')

url = "http://www.qisuu.com/s/1/"

get_urls = requests.get(url)
books_html = BeautifulSoup(get_urls.content)

all_books = books_html.find_all('div', {'class': 'listBox'})

for book in all_books[0].find_all(href=re.compile('Shtml')):
    book_url = 'http://www.qisuu.com' + book.get('href')
    get_book = requests.get(book_url)
    book_html = BeautifulSoup(get_book.content)
    dl_url = book_html.find_all(href=re.compile("http://dzs.qisuu.com/txt"))[0].get('href')
    dl_book = requests.get(dl_url)

    book_name = re.sub(u'[\u300a\u300b\u5168\u96c6]', '', book.text)
    with open(book_name + '.txt', 'wb') as f:
        f.write(dl_book.content)