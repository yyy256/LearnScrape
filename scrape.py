#Scrape
import requests
from bs4 import BeautifulSoup

url = "http://www.yellowpages.com/los-angeles-ca/coffee?g=los%20angeles%2C%20ca&q=coffee"
url_page_2 = url + "page=" + str(2) + "&s=relevance"
r = requests.get(url)
soup = BeautifulSoup(r.content)
# links = soup.find_all("a")
# for link in links:
	# if "http" in link.get("href"):
		# print "<a href='%s'>%s</a>" %(link.get("href"), link.text)
	 
	 
g_data = soup.find_all("div", {"class": "info"})

for item in g_data:
	#print item.contentss[0].text
	#business_name = item.contentss[0].find_all("a", {"class": "business-name"})[0].text
	try:
		print item.contents[1].find_all("span", {"itemprop": "streetAddress"})[0].text
	except:
		pass
	try:
		print item.contents[1].find_all("span", {"itemprop": "addressLocality"})[0].text.replace(',', '')
	except:
		pass
	try:
		print item.contents[1].find_all("span", {"itemprop": "addressRegion"})[0].text
	except:
		pass
	try:
		print item.contents[1].find_all("span", {"itemprop": "postalCode"})[0].text
	except:
		pass
	#print item.contents[1].find_all("p", {"class": "adr"})[0].text
	try:
		print item.contents[1].find_all("li", {"class": "primary"})[0].text
	except:
		pass



# scrape fang.com housetitle and price

for i in range(1, 3):
	url = "http://pinggu.fang.com/pghouse-c0hz/h313-i3" + str(i) + "/"

	html = urllib.urlopen(url).read()
	soup = BeautifulSoup(html, 'html5')

	g_data = soup.find_all("div", {"class": "house"})

	for item in g_data:
		try:
			title = item.contents[1].find_all('span', {'class', 'housetitle'})[0].text.strip()
		except:
			pass

		try:
			price = item.contents[1].find_all('span', {'class', 'price'})[0].text.strip()
		except:
			pass

		print title, price
	time.sleep(6)
