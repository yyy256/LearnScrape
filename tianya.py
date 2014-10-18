# coding:utf-8

import sys
import requests
from bs4 import BeautifulSoup
import re

# 找出帖子版块、id、总页数、楼主
url = sys.argv[1]

r = requests.get(url)
soup = BeautifulSoup(r.content)
h = soup.find_all('div', {'class' : 'atl-menu clearfix js-bbs-act'})
louzhu= h[0].get('js_activityusername')

tiezi = soup.find_all("form", {"method" : "get", "action" : ""})
res = re.findall(r'goPage\((.*?)\);', tiezi[0].get('onsubmit'))[0].split(',')
bankuai = res[1].replace("'", "")
id = res[2]
page = res[3]

# 抓出帖子内容
f  = open('text.txt', 'w')
for i in range(1, int(page)):
	url = "http://bbs.tianya.cn/post-" + bankuai + "-" + id + "-" + str(i) + ".shtml"
	r = requests.get(url)

	soup = BeautifulSoup(r.content)

	g_data = soup.find_all("div", {"_host": louzhu})
	for item in g_data:
		text = item.find_all("div", {"class" : re.compile("bbs-content")})[0].text.strip()
		if len(text) < 1000:
			pass
		else:
			f.write('%s\n'  %(text.encode('utf-8')))

f.close()

print "Done"
