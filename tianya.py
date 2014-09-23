import requests
from bs4 import BeautifulSoup

f  = open('text.txt', 'w')
for i in range(1, 484):
	url = "http://bbs.tianya.cn/post-no05-146165-" + str(i) + ".shtml"
	r = requests.get(url)

	soup = BeautifulSoup(r.content)

	g_data = soup.find_all("div", {"js_username": "%E5%8E%86%E5%8F%B2%E6%8C%91%E5%B1%B1%E5%B7%A5"})
	for item in g_data:
		text = item.contents[3].find_all('div', {'class', 'bbs-content'})[0].text.strip()
		if "=============" in text or '----------------' in text:
			pass
		else:

			f.write('%s\n'  %(text.encode('utf-8')))

f.close()