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

all_urls = {}1
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
for key in all_urls.keys():
    all_data = {}
    url1 = all_urls[key]['url1']

    try:
        h1 = requests.get(url1)
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
        contact_person = contact_details[0].find_all('div', {'class':'name'})[0].text.strip()
        all_data[u'Contact_Person'] = contact_person
        links = contact_details[0].find('li', {'class':'item'})
        website = links.find('a').get('href').strip()
        all_data[u'Website'] = website

        sh_table = contact_details[0].find_all('div', {'class':'sh-table'})
        tr = sh_table[0].find_all('div', {'class', 'tr'})

        for row in tr:
            key = row.find_all('span', {'class':'th'})[0].text.strip()
            if key in ['Telephone:', 'Mobile:', 'Address:']:
                all_data[key] = row.find_all('span', {'class':'td'})[0].text.split('\n')[0].strip()

        h2 = requests.get(url2)
        s2 = BeautifulSoup(h2.content)

        company_info = s2.find_all('div', {'class':'export-info company-info-item'})
        tr = company_info[0].find_all('tr')
        for row in tr:
            key = row.find_all('th')[0].text.strip()
            if key in ['Annual Export Revenue:', 'Main Markets:']:
                all_data[key] = row.find_all('td')[0].text.strip()

        h3 = requests.get(url3)
        s3 = BeautifulSoup(h3.content)

        pro_base_info = s3.find_all('div', {'class':'pro-base-info'})
        tr = pro_base_info[0].find_all('div', {'class':'tr'})


        for row in tr[1:]:
            key = row.find_all('span', {'class':'th'})[0].text.strip()
            if key in ['Min. order:', 'Payment Terms:']:
                all_data[key] = row.find_all('span', {'class':'td'})[0].text.strip()

        price = tr[0].text.split('\n')[0].split(':')[1]
        all_data[u'Price'] = price

        if 'Min. order:' not in all_data.keys:
            try:
                num = tr[0].find('td').text.strip()
                unit = re.findall(u'\((.*?)\)', tr[0].find('th').text)[0]
                MOQ = num + ' ' + unit
            except:
                MOQ = u''
            all_data[u'Min. order:'] = MOQ
    except:
        pass
    all_datas[key] = all_data
    time.sleep(choice(sleep))

