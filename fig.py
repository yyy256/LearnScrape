#!/usr/bin/python
import re
import urllib

def getHtml(url):
	page = urllib.urlopen(url)
	html = page.read()
	return html

def getImg(html):
	reg = r'class="BDE_Image" src="(.*?\.jpg)" pic'
	imgre = re.compile(reg)
	imglist = re.findall(imgre, html)
	x = 0
	for imgurl in imglist:
		urllib.urlretrieve(imgurl, '%s.jpg' % x)
		x += 1

html = getHtml("http://tieba.baidu.com/p/3107021627?pn=1")
print getImg(html)