# mobile
import requests
from bs4 import BeautifulSoup
import time
import sys
import re
from random import choice
import pandas as pd
import json
import pickle

reload(sys)
sys.setdefaultencoding('utf-8')

category_url = map(lambda x: "http://m.made-in-china.com/search/supplier?word=Laptops%2BAccessories&page=" + str(x), range(1,61))
# category_url = map(lambda x: "http://m.made-in-china.com/search/supplier?word=Auto%2BSafety&page=" + str(x), range(1,61))

header_info = {'Accept':'application/json',
'Accept-Encoding':'gzip, deflate, sdch',
'Accept-Language':'zh-CN,zh;q=0.8',
'Connection':'keep-alive',
'Cookie':'sf_img=AM; inquiry_id=TAzOTg5MTIzMTI1NDQyMjU6MTAxLjgxLjcxLjE4NAM; pid=TAxLjgxLjcxLjE4NDIwMTUwNDMwMTczMzU4NTYxNDYzMjI1NjgM; _sc=jAxNTA0MzAxNzQ3MjYwOTMwMDA6MDIxNDU3NTIxNTM2Mzg4ODgyOQM; fo=true; __utma=144487465.1346161509.1430386440.1430807401.1430807401.1; __utmz=144487465.1430807401.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ar=jM5MTAxNAMiEsfjQ5NjQ2NAMiEsfjQ4NDM2NAMiEsfjE2Njg3NAM; lr_user=1; abde=QQ; _pd=zAwMzI1MjM1NiEsfjg1ODYwMTI1NiEsfjYzNDI5MzEyNiEsfjE5MzA3NTgyNiEsfjIyNDUwNTcyNiEsfzQ0ODQzMjM1NiEsfjk2OTgwMTI1NiEsfjY3ODkzNzA1NiEsfzUxNDEzNTM1NiEsfzAwMDM4NTE1N; _gat=1; _gali=J-searchArea; _ga=GA1.2.1346161509.1430386440',
'Host':'m.made-in-china.com',
'Referer':'http://m.made-in-china.com/search/supplier?word=Laptops+Accessories',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36',
'X-Requested-With':'XMLHttpRequest'}

# header_info = {'Accept':'application/json',
# 'Accept-Encoding':'gzip, deflate, sdch',
# 'Accept-Language':'zh-CN,zh;q=0.8',
# 'Connection':'keep-alive',
# 'Cookie':'sf_img=AM; inquiry_id=TAzOTg5MTIzMTI1NDQyMjU6MTAxLjgxLjcxLjE4NAM; pid=TAxLjgxLjcxLjE4NDIwMTUwNDMwMTczMzU4NTYxNDYzMjI1NjgM; _sc=jAxNTA0MzAxNzQ3MjYwOTMwMDA6MDIxNDU3NTIxNTM2Mzg4ODgyOQM; fo=true; __utma=144487465.1346161509.1430386440.1430807401.1430807401.1; __utmz=144487465.1430807401.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ar=jM5MTAxNAMiEsfjQ5NjQ2NAMiEsfjQ4NDM2NAMiEsfjE2Njg3NAM; lr_user=1; abde=QQ; _pd=zAwMzI1MjM1NiEsfjg1ODYwMTI1NiEsfjYzNDI5MzEyNiEsfjE5MzA3NTgyNiEsfjIyNDUwNTcyNiEsfzQ0ODQzMjM1NiEsfjk2OTgwMTI1NiEsfjY3ODkzNzA1NiEsfzUxNDEzNTM1NiEsfzAwMDM4NTE1N; _gali=J-searchArea; _ga=GA1.2.1346161509.1430386440; _gat=1',
# 'Host':'m.made-in-china.com',
# 'Referer':'http://m.made-in-china.com/search/supplier?word=Auto+Safety',
# 'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36',
# 'X-Requested-With':'XMLHttpRequest'}

# 从电脑网页上获取所需类别的公司名
f = open('computer.pkl', 'rb')
all_urls = pickle.load(f)
f.close()

# f = open('urls.pkl', 'rb')
# all_urls = pickle.load(f)
# f.close()

# 在手机页面上搜索公司名获得公司信息和产品信息的url
sleep = range(1, 3)
laptops_accessories_url = {}
for name in all_urls.keys():
    search_url = "http://m.made-in-china.com/search/supplier?word=" + requests.utils.quote(name).replace('%20', '+')
    try:
        r = requests.get(search_url)
        soup = BeautifulSoup(r.content)
        url1 = "http://m.made-in-china.com" + soup.find('div', 'pro-detail').find('a').get('href') # 主页
        url2 = url1 + '/info/' # info
        r1 = requests.get(url1+'/productlist')
        soup1 = BeautifulSoup(r1.content)
        url3 = "http://m.made-in-china.com" + soup1.find('a', 'pro-thumb').get('href') # 产品
        laptops_accessories_url[name] = {'url1':url1, 'url2':url2, 'url3':url3}
    except:
        pass

# sleep = range(1, 5)
# laptops_accessories_url = {}
# nourls = []
# for url in category_url:
#     try:
#         r = requests.get(url, headers = header_info)
#         soup = BeautifulSoup(r.content)
#         json_data = json.loads(soup.p.text)
#         for one in json_data:
#             url1 = "http://m.made-in-china.com/company/" + str(one['id']) # 主页
#             url2 = "http://m.made-in-china.com/company/" + str(one['id']) + '/info/' # info
#             r1 = requests.get(url1+'/productlist')
#             soup1 = BeautifulSoup(r1.content)
#             url3 = "http://m.made-in-china.com" + soup1.find('a', 'pro-thumb').get('href') # 产品

#             laptops_accessories_url[one['name']] = {'url1':url1, 'url2':url2, 'url3':url3}
#     except:
#         nourls.append(url)
#     time.sleep(choice(sleep))

# 获得公司及产品信息
all_datas = {}
for company in laptops_accessories_url.keys():
    all_data = {}
    url1 = laptops_accessories_url[company]['url1'] # 主页
    url2 = laptops_accessories_url[company]['url2'] # info
    url3 = laptops_accessories_url[company]['url3'] # 产品页
    try:
        # 主页
        h1 = requests.get(url1, timeout=2)
        s1 = BeautifulSoup(h1.content)

        company_info1 = s1.find_all('table','company-intro')
        tr = company_info1[0].find_all('tr')
        for row in tr:
            key = row.find_all('th')[0].text.strip()
            if key in ['Business Type:', 'Main Products:']:
                all_data[key] = row.find_all('td')[0].text.strip().replace(u'\xa0', ' ')

        # info
        h2 = requests.get(url2, timeout=2)
        s2 = BeautifulSoup(h2.content)

        company_info = s2.find_all('table','company-intro')
        tr = company_info[-1].find_all('tr')
        for row in tr:
            key = row.find_all('th')[0].text.strip()
            if key in ['Telephone Number:', 'Mobile:', 'Address:', 'Contact Person:']:
                all_data[key] = row.find_all('td')[0].text.strip().replace(u'\xa0', ' ')

        # 产品
        h3 = requests.get(url3, timeout=2)
        s3 = BeautifulSoup(h3.content)

        tr = s3.find('table', 'order-detail').find_all('tr')
        for row in tr:
            try:
                name = row.find('th').text.strip()
            except:
                name = ''
            if name == u'Payment Terms:':
                all_data[u'Payment Terms'] = row.find('td').text.strip()
            elif name == u'Min.Order:':
                all_data[u'MOQ'] = row.find('td').text.strip()
            elif name == u'Price:':
                num = row.find('table').find_all('td')[2].text.strip()
                unit = re.findall(u'\((.*?)\)', row.find('table').find_all('td')[0].text.strip())[0]
                MOQ = str(num) + ' ' + unit
                high_price = row.find('table').find_all('td')[3].text.strip()
                low_price = row.find('table').find_all('td')[-1].text.strip()
                if high_price == low_price:
                    price = high_price+' / '+unit
                else:
                    price = low_price+'-'+''.join(re.findall(r'[\d+\.]', high_price))+' / '+unit
                all_data[u'MOQ'] = MOQ
                all_data[u'price'] = price
    except:
        pass

    all_datas[company] = all_data
    time.sleep(choice(sleep))

# 去除空值
res = {}
for k in all_datas.keys():
    if all_datas[k] != {}:
        res[k] = all_datas[k]

res_df = pd.DataFrame(res.values(), index = res.keys())
res_df.to_excel('c:/users/yaoyu/desktop/alibaba.xlsx')


# web
import requests
from bs4 import BeautifulSoup
import time
import sys
import re
from random import choice
import pandas as pd

sleep = range(1, 5)
# Auto Parts & Accessories: Auto Safety
# Computer Products: Laptops & Accessories
tcc = map(lambda x: 'http://www.made-in-china.com/manufacturers-directory/item3/Tablet-Case-Cover-' + str(x) + '.html', range(1,30))
nlc = map(lambda x: 'http://www.made-in-china.com/manufacturers-directory/item3/Notebook-Laptop-Computer-and-Parts-' + str(x) + '.html', range(1,30))
pcp = map(lambda x: 'http://www.made-in-china.com/manufacturers-directory/item3/Palm-Computer-Pocket-PC-PDA-' + str(x) + '.html', range(1,19))
tp = map(lambda x: 'http://www.made-in-china.com/manufacturers-directory/item3/Tablet-PC-' + str(x) + '.html', range(1,40))
pb = map(lambda x: 'http://www.made-in-china.com/manufacturers-directory/item3/Power-Bank-' + str(x) + '.html', range(1,40))

page_urls = tcc + nlc + pcp + tp + pb

all_urls = {}
for url in page_urls:
    html = requests.get(url)
    soup = BeautifulSoup(html.content)
    lists = soup.find_all('div', {'class':'list-node even'})
    for company in lists:
        company_name = company.find_all("h2", {"class":"company-name"})[0].text.replace(u'\uf01d', '').strip()
        company_url = company.find_all("h2", {"class":"company-name"})[0].find('a').get('href')
        if 'china' in company_url:
            contact_url = company.find_all("div", {"class":"user-action"})[0].find('a').get('href')
            trade_url = company_url + '/custom/' + re.findall(r'_(.*?)_', contact_url)[0] +'/Trade-Capacity.html'
            product_url = company.find("div", {"class":"pro-name"}).find("a").get("href")
            all_urls[company_name] = {'url1':company_url, 'url2':trade_url, 'url3':product_url}
    time.sleep(choice(sleep))

all_datas = {}
for url_key in all_urls.keys():
    all_data = {}
    url1 = all_urls[url_key]['url1'] # 主页
    url2 = all_urls[url_key]['url2'] # Trade-Capacity
    url3 = all_urls[url_key]['url3'] # 产品页

    try:
        h1 = requests.get(url1, timeout=1)
        s1 = BeautifulSoup(h1.content)

        sh_table = s1.find_all('div', {'class':'info sh-table'})
        # Company_Name = sh_table[0].find_all('strong')[0].text
        # all_data[u'Company_Name'] = Company_Name

        tr = sh_table[0].find_all('div', {'class', 'tr'})

        for row in tr:
            key = row.find_all('span', {'class':'th'})[0].text.strip()
            if key in ['Business Type:', 'Main Products:']:
                all_data[key] = row.find_all('span', {'class':'td'})[0].text.strip().replace(u'\n', '').replace(u' ', '')

        contact_details = s1.find_all('div', {'class':'block index-contact-details'})
        try:
            contact_person = contact_details[0].find_all('div', {'class':'name'})[0].text.strip()
            all_data[u'Contact_Person'] = contact_person
        except:
            all_data[u'Contact_Person'] = u''
        try:
            links = contact_details[0].find('li', {'class':'item'})
            website = links.find('a').get('href').strip()
            all_data[u'Website'] = website
        except:
            all_data[u'Website'] = u''

        sh_table = contact_details[0].find_all('div', {'class':'sh-table'})
        tr = sh_table[0].find_all('div', {'class', 'tr'})

        for row in tr:
            key = row.find_all('span', {'class':'th'})[0].text.strip()
            if key in ['Telephone:', 'Mobile:', 'Address:']:
                all_data[key] = row.find_all('span', {'class':'td'})[0].text.split('\n')[0].strip()

        h2 = requests.get(url2, timeout=1)
        s2 = BeautifulSoup(h2.content)

        company_info = s2.find_all('div', {'class':'export-info company-info-item'})
        tr = company_info[0].find_all('tr')
        for row in tr:
            key = row.find_all('th')[0].text.strip()
            if key in ['Annual Export Revenue:', 'Main Markets:']:
                all_data[key] = row.find_all('td')[0].text.strip()

        h3 = requests.get(url3, timeout=1)
        s3 = BeautifulSoup(h3.content)

        pro_base_info = s3.find_all('div', {'class':'pro-base-info'})
        tr = pro_base_info[0].find_all('div', {'class':'tr'})


        for row in tr[1:]:
            key = row.find_all('span', {'class':'th'})[0].text.strip()
            if key in ['Min. order:', 'Payment Terms:']:
                all_data[key] = row.find_all('span', {'class':'td'})[0].text.strip()

        try:
            price = tr[0].text.split('\n')[0].split(':')[1]
            all_data[u'Price'] = price
        except:
            all_data[u'Price'] = u''

        if 'Min. order:' not in all_data.keys():
            try:
                num = tr[0].find('td').text.strip()
                unit = re.findall(u'\((.*?)\)', tr[0].find('th').text)[0]
                MOQ = num + ' ' + unit
            except:
                MOQ = u''
            all_data[u'Min. order:'] = MOQ
    except:
        pass
    all_datas[url_key] = all_data
    time.sleep(choice(sleep))


all_datas = {}
for url_key in all_urls.keys():
    all_data = {}
    url1 = all_urls[url_key]['url1'] # 主页
    url2 = all_urls[url_key]['url2'] # Trade-Capacity
    url3 = all_urls[url_key]['url3'] # 产品页
    url4 = url1 + "/product-list-1.html" # 所有产品

    try:
        # 主页
        h1 = requests.get(url1, timeout=1)
        s1 = BeautifulSoup(h1.content)
        sh_table = s1.find_all('div', 'area-year')
        key, value = sh_table[0].find_all(text=re.compile('Type'))[0].strip().split(':')

        if key in ['Business Type', 'Main Products:']:
            all_data[key] = value.strip()

        contact_details = s1.find_all('div', {'class':'contact-detail'})

        tr = contact_details[0].find_all('div', {'class', 'tr'})
        for row in tr:
            key = row.find_all('span', {'class':'th'})[0].text.strip()
            if key in ['Telephone:', 'Mobile:', 'Address:', 'Contact Person:']:
                all_data[key] = [text for text in row.find('span', 'td').stripped_strings][0]
            elif key == "Website:":
                all_data[key] = row.find('a').get('href')

        # Trade-Capacity
        try:
            h2 = requests.get(url2, timeout=1)
            s2 = BeautifulSoup(h2.content)

            company_info = s2.find_all('div', {'class':'export-info company-info-item'})
            tr = company_info[0].find_all('tr')
            for row in tr:
                key = row.find_all('th')[0].text.strip()
                if key in ['Annual Export Revenue:', 'Main Markets:']:
                    all_data[key] = row.find_all('td')[0].text.strip()
        except:
            pass

        # 产品页
        try:
            h3 = requests.get(url3, timeout=1)
            s3 = BeautifulSoup(h3.content)
            pro_base_info = s3.find_all('div', {'class':'pro-base-info'})
            tr = pro_base_info[0].find_all('div', {'class':'tr'})
            for row in tr[1:]:
                key = row.find_all('span', {'class':'th'})[0].text.strip()
                if key in ['Min. order:', 'Payment Terms:']:
                    all_data[key] = row.find_all('span', {'class':'td'})[0].text.strip()
        except:
            all_data[u'Min. order:'] = u''
            all_data[u'Payment Terms:'] = u''
        try:
            price = tr[0].text.split('\n')[0].split(':')[1]
            all_data[u'Price'] = price
        except:
            all_data[u'Price'] = u''
        if 'Min. order:' not in all_data.keys():
            try:
                num = tr[0].find('td').text.strip()
                unit = re.findall(u'\((.*?)\)', tr[0].find('th').text)[0]
                MOQ = num + ' ' + unit
            except:
                MOQ = u''
            all_data[u'Min. order:'] = MOQ
        try:
            h4 = requests.get(url4, timeout=1)
            s4 = BeautifulSoup(h4.content)
            all_data[u'Main Products:'] = ','.join([l.text for l in s4.find('h1', 'pro-include').find_all('a')])
        except:
            all_data[u'Main Products:'] = u''
    except:
        pass
    all_datas[url_key] = all_data
    time.sleep(choice(sleep))


all_datas = {}
for url_key in all_urls.keys():
    all_data = {}
    url1 = all_urls[url_key]['url1'] + '/contact-info.html' # 联系页
    url2 = all_urls[url_key]['url2'] # Trade-Capacity

    # 主页
    try:
        h1 = requests.get(url1, timeout=1)
        s1 = BeautifulSoup(h1.content)
        website = [a.get('href') for a in s1.find_all('a') if a.text=="Click Here"][0]
        all_data[key] = requests.get(website).url
    except:
        pass

    # Trade-Capacity
    try:
        h2 = requests.get(url2, timeout=1)
        s2 = BeautifulSoup(h2.content)

        company_info = s2.find_all('div', {'class':'export-info company-info-item'})
        tr = company_info[0].find_all('tr')
        for row in tr:
            key = row.find_all('th')[0].text.strip()
            if key in ['Annual Export Revenue:', 'Main Markets:']:
                all_data[key] = row.find_all('td')[0].text.strip()
    except:
        pass
    all_datas[url_key] = all_data

dictMerged3 = dict1.copy()
dictMerged3.update( dict2 )