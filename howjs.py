import requests
from bs4 import BeautifulSoup

urls = ["http://www.yslbeautycn.com/makeup/?start=20&sz=12&format=ajax&lazy=true", 
"http://www.yslbeautycn.com/makeup/?start=8&sz=12&format=ajax&lazy=true",
"http://www.yslbeautycn.com/makeup/?start=8&sz=12&format=ajax&lazy=true",
"http://www.yslbeautycn.com/skincare/?format=ajax",
"http://www.yslbeautycn.com/skincare/?start=8&sz=12&format=ajax&lazy=true",
"http://www.yslbeautycn.com/fragrance/?format=ajax",
"http://www.yslbeautycn.com/gifts/?format=ajax",
"http://www.yslbeautycn.com/on/demandware.store/Sites-ysl-cn-Site/zh_CN/Search-Show?cgid=Star-Products&format=ajax",
"http://www.yslbeautycn.com/on/demandware.store/Sites-ysl-cn-Site/zh_CN/Search-Show?cgid=Star-Products&start=12&sz=12&format=ajax&lazy=true"]

with open('p.csv', 'w') as f:
	for url in urls:
    		r = requests.get(url)
    		soup = BeautifulSoup(r.content)
    		product_names = [item.contents[0].encode('utf-8') for item in soup.find_all("a", {"class": "product_name"})]

    		product_subtitles = [item.contents[0].encode('utf-8') for item in soup.find_all("span", {"class": "product_subtitle"})]

    		prices = [item.contents[2].strip().encode('utf-8') for item in soup.find_all("p", {"class":re.compile(r"^product_price")})]
    		
    		for i in range(len(product_names)):
    			f.write('%s,%s,%s\n' %(product_names[i], product_subtitles[i], prices[i]))
