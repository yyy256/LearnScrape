import urllib
import re
urls = ["http://baidu.com","http://sina.com","http://163.com"]
i = 0
regex = '<title>(.+?)</title>'
pattern = re.compile(regex)
while i < len(urls):
	htmlfile = urllib.urlopen(urls[i])
	htmltext = htmlfile.read()
	titles = re.findall(pattern,htmltext)
	print titles
	i+=1
	
import urllib
import re
symbolslist = ["AAPL","spy","goog","nflx"]
i = 0
while i < len(symbolslist):
	url = "http://finance.yahoo.com/q?s="+symbolslist[i]+"&ql=1"
	htmlfile = urllib.urlopen(url)

	htmltext = htmlfile.read()

	regex = '<span id="yfs_l84_'+symbolslist[i]+'">(.+?)</span>'

	pattern = re.compile(regex)

	price = re.findall(pattern, htmltext)

	print "the price of",symbolslist[i],"is",price
	i+=1
	
	
	
import urllib
import re
symbolsfile = open("symbols.txt")
symbolslist = symbolsfile.read()
newsymbolslist = symbolslist.split("\n")
i = 0
while i < len(newsymbolslist):
	url = "http://finance.yahoo.com/q?s="+newsymbolslist[i]+"&ql=1"
	htmlfile = urllib.urlopen(url)

	htmltext = htmlfile.read()

	regex = '<span id="yfs_l84_[^.]*">(.+?)</span>'

	pattern = re.compile(regex)

	price = re.findall(pattern, htmltext)

	print "the price of",newsymbolslist[i],"is",price
	i+=1
	
	
	
import urllib
import re
htmltext = urllib.urlopen("https://www.google.com/finance?q=aapl").read()
regex = '<span id="ref_[^.]*_l">(.+?)</span>'
pattern = re.compile(regex)
results = re.findall(pattern,htmltext)
print results

import urllib
import re
htmltext = urllib.urlopen("https://www.google.com/finance/getprices?q=AAPL&x=NASD&i=10&p=25m&f=c&df=cpct&auto=1&ts=1379243033430&ei=LI81Utj3FImykgWDowE").read()

print htmltext

execfile #在python shell 中执行.py文件


import urllib
import re
import json
htmltext = urllib.urlopen("http://www.bloomberg.com/markets/watchlist/recent-ticker/AAPL:AR")
data = json.load(htmltext)

print htmltext



import urllib
import re
import json
htmltext = urllib.urlopen("http://www.bloomberg.com/markets/chart/data/1D/AAPL:US")


data = json.load(htmltext)

datapoints = data["data_values"]

for point in datapoints:
	print point[1]
print "the number of points is", len(datapoints)






import urlparse
import urllib
from bs4 import BeautifulSoup

url = "http://nytimes.com"
urls = [url] #stack of urls to scrape
visited = [url] #historic record of urls
while len(urls) > 0:
	try:
	    htmltext = urllib.urlopen(urls[0]).read()
	except:
		print urls[0]
	soup = BeautifulSoup(htmltext)
	urls.pop(0)
	print len(urls)
	for tag in soup.findAll('a',href=True):
		tag['href'] = urlparse.urljoin(url,tag['href'])
		if url in tag['href'] and tag['href'] not in visited:
			urls.append(tag['href'])
			visited.append(tag['href'])
print visited
		

