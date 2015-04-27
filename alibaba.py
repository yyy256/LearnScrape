import requests
from bs4 import BeautifulSoup
import time
import sys
import re
from random import choice
import pandas as pd

reload(sys)
sys.setdefaultencoding('utf-8')


url = "http://www.alibaba.com/Products"
a1 = requests.get(url)
a2 = BeautifulSoup(a1.content)
a3 = a2.find_all(href=re.compile('pid'))

category_id = [re.match(r'.*?pid(.*?)$', a4.get('href')).group(1) for a4 in a3[:40]]

companys_profile_url = []
companys_contact_url = []
products_url = []
for id in category_id:
	category_url = "http://www.alibaba.com/catalogs?IndexArea=company_en&c=CID" + str(id) + "&atm=&f0=y&Country=CN"
    category_get = requests.get(category_url)
    category_html = BeautifulSoup(category_get.content)

	companys_profile_url.extend([url.get('href') for url in category_html.find_all(href=re.compile('top-nav-bar'))[:16]])
	companys_contact_url.extend([url.get('href') for url in category_html.find_all(href=re.compile('contactinfo'))[:16]])

	all_company = category_html.find_all('div', {'class':'f-icon m-item  '})

	for company in all_company[:16]:
		all_products = company.find_all(href=re.compile('detail'))
		products_url.append(all_products[0].get('href'))

# 去重
companys_profile_url = pd.unique(companys_profile_url)
companys_contact_url = pd.unique(companys_contact_url)
products_url = pd.unique(products_url)

sleep = range(1, 5)
# profile data
profile_datas = {}
for company_profile_url in companys_profile_url:
	try:
	    company_profile_get = requests.get(company_profile_url, timeout=2)
	    if company_profile_get:
		    company_profile_html = BeautifulSoup(company_profile_get.content)

		    Company_Name = company_profile_html.find_all('div', {'class':'m-header'})[0].find_all('h3')[0].text.strip()

		    right_table = company_profile_html.find_all('table', {'class': 'table right'})[0].find_all('tr')
		    
		    profile_data = {}
			for row in right_table[:-1]:
				key = row.find_all('th')[0].text.strip()
				if key in ['Business Type:', 'Main Products:', 'Total Annual Sales Volume:', 'Main Markets:']:
			        profile_data[key] = row.find_all('td')[-1].text.strip()

		    profile_datas[Company_Name] = profile_data
        time.sleep(choice(sleep))
	except:
		pass


# contact data
contact_datas = {}
for company_contact_url in companys_contact_url:
	try:
		company_contact_get = requests.get(company_contact_url, timeout=2)
		if company_contact_get:
			company_contact_html = BeautifulSoup(company_contact_get.content)

			Company_Name = company_contact_html.find_all('table', {'class':'company-info-data table'})[0].find_all('tr')[0].find_all('td')[-1].text.strip()
			company_info = company_contact_html.find_all('table', {'class':'company-info-data table'})[0].find_all('tr')
			for row in company_info:
				if row.find_all('th')[0].text.strip() == 'Company Name:':
					Company_Name = row.find_all('td')[-1].text.strip()
				elif row.find_all('th')[0].text.strip() == 'Website:':
					Website = '&'.join([a.get('href') for a in row.find_all('a')])
				else:
					pass


			contact_person = company_contact_html.find_all('div', {'class':'contact-info'})[0].find_all('h1')[0].text.strip()

			contact_detail = company_contact_html.find_all('dl', {'class':'dl-horizontal'})
			contact_data = {}
			dt = contact_detail[1].find_all('dt')
			dd = contact_detail[1].find_all('dd')
			for row in range(len(dt)):
				key = dt[row].text.strip()
				if key in ['Address:', 'City:', 'Country/Region:', 'Province/State:', 'Telephone:', 'Mobile Phone:']:
				    contact_data[key] = dd[row].text.strip()
			contact_data["contact_person"] = contact_person
			contact_data["Website"] = Website

		contact_datas[Company_Name] = contact_data
        time.sleep(choice(sleep))
    except:
    	pass

# product data
product_datas = {}
for product_url in products_url:
	try:
		product_get = requests.get(product_url, timeout=2)
		if product_get:
		    product_html = BeautifulSoup(product_get.content)

			Company_Name = product_html.find_all('div',{'class':'company'})[0].find_all('a')[0].text.strip()
			
			product_table = product_html.find_all('table', {'class': 'btable w'})[0].find_all('tr')
			product_data = {}
			for row in product_table:
				key = row.find_all('th')[0].text.strip()
				if key in ['FOB Price:', 'Min.Order Quantity:', 'Payment Terms:']:
			        product_data[key] = row.find_all('td')[-1].text.strip()
		
		product_datas[Company_Name] = product_data
        time.sleep(choice(sleep))
	except:
		pass

contact_df = pd.DataFrame(contact_datas.values(), index = contact_datas.keys())
profile_df = pd.DataFrame(profile_datas.values(), index = profile_datas.keys())
product_df = pd.DataFrame(product_datas.values(), index = product_datas.keys())
df1 = pd.merge(profile_df, contact_df, how="left", left_index=True, right_index=True)
df2 = pd.merge(df1, product_df, how="left", left_index=True, right_index=True)
df2.to_excel('c:/users/yaoyu/desktop/alibaba.xlsx')