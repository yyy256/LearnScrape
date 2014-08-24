#-*- coding: UTF-8 -*- 

#www.so.com 联想词
import urllib2
import urllib
import re
import time
from random import choice

iplist = ['123.125.116.243:6583', '123.125.116.242:11351', '219.234.82.83:7145', '123.125.116.243:36013']


list1 = ["科比", "艾弗森"]
for item in list1:
	ip = choice(iplist)
	gjc = urllib.quote(item)
	url = "http://sug.so.360.cn/suggest?callback=suggest_so&encodein=utf-8&encodeout=utf-8&format=json&fields=word,obdata&word=" + gjc
	headers = {
				"GET":url,
				"Host":"sug.so.360.cn",
				"Referer":"http://www.so.com/",
				"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/34.0.1847.116 Chrome/34.0.1847.116"
	}

	# proxy_support = urllib2.ProxyHandler({'http':'http://'+ip})

	# opener = urllib2.build_opener(proxy_support)
	# urllib2.install_opener(opener)
	req = urllib2.Request(url)

	for key in headers:
		req.add_header(key, headers[key])

	html = urllib2.urlopen(req).read()
	# print html
	ss = re.findall("\"(.*?)\"", html)
	# print ss

	for item in ss:
		print item

	time.sleep(6)

#www.baidu.com 相关搜索
for item in list1:
	gjc = urllib.quote(item)
	url = 'http://www.baidu.com/s?word=' + gjc + '&tn=sitehao123&ie=utf-8'
	html = urllib.urlopen(url).read()
	s = re.findall('src=0\">(.*?)<', html)

	for item in s:
		print item