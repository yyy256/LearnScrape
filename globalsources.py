import requests
from bs4 import BeautifulSoup
import time
import sys
import re
from random import choice

reload(sys)
sys.setdefaultencoding('utf-8')

FMs_url = "http://www.globalsources.com/gsol/I/Facility-Management-suppliers/s/2000000003844/3000000194803/28259"
ACs_url = "http://www.globalsources.com/gsol/I/Access-Control-suppliers/s/2000000003844/3000000180105/22643"
SCs_url = "http://www.globalsources.com/gsol/I/Security-Camera-suppliers/s/2000000003844/3000000180139/22642"

FMs_urls = map(lambda x: FMs_url + '/' + str(x) + '.htm', range(20, 360, 20))
ACs_urls = map(lambda x: ACs_url + '/' + str(x) + '.htm', range(20, 120, 20))
SCs_urls = map(lambda x: SCs_url + '/' + str(x) + '.htm', range(20, 500, 20))

category_urls = FMs_urls + ACs_urls + SCs_urls
category_urls.append(FMs_url + '.htm')
category_urls.append(ACs_url + '.htm')
category_urls.append(SCs_url + '.htm')


sleep = range(1, 5)
companys_profile_url = []
companys_contact_url = []
products_url = []
for category_url in category_urls:
    category_get = requests.get(category_url)
    category_html = BeautifulSoup(category_get.content)

    all_company = category_html.find_all('div', {'class':'listing_table_row clearfix '})

    for company in all_company:
    	company_location = company.find_all('span', {'class':'ib'})[0].text.strip()
    	if company_location == 'China (mainland)':
	        company_homepage = company.find_all('a', {'class':'supplierTit'})[0].get('href')
	        company_url = re.match(r'(.*)Homepag.*?', company_homepage).group(1)
	        companys_profile_url.append(company_url + 'CompanyProfile.htm')
	        companys_contact_url.append(company_url + 'ContactUs.htm')

	        product_url = company.find_all('a', {'class':'majorPP_con'})[0].get('href')
	        products_url.append(product_url)
    time.sleep(choice(sleep))

# 去重
companys_profile_url = pd.unique(companys_profile_url)
companys_contact_url = pd.unique(companys_contact_url)
products_url = pd.unique(products_url)


sleep = range(1, 5)
# profile data
profile_datas = {}
no_profile_url = []
for company_profile_url in companys_profile_url:
    try:
        company_profile_get = requests.get(company_profile_url, timeout=2)
        if company_profile_get:
            company_profile_html = BeautifulSoup(company_profile_get.content)

            Company_Name = company_profile_html.find_all('p', {'class':'spName'})[0].text.strip()

            basic_info = company_profile_html.find_all('div', {'class':'proDetCont clearfix mt10'})

            profile_data = {}
            for row in basic_info:
                if row.find_all('p')[0].text.strip() == 'Business Type:':
                    profile_data['Business_Type'] = [p.text.split(u'\xa0')[0] for p in row.find_all('div', {'class':'fl ml5'})[0].find_all('p')]
                elif row.find_all('p')[0].text.strip() == 'Past Export Markets/Countries:':
                    Main_Markets = {}
                    big_type = [b.text.strip() for b in row.find_all('strong')]

                    for i in range(len(big_type)):
                        Main_Markets[big_type[i]] = [l.text.replace(u'\xa0', u' ').split(' ')[0] for l in row.find_all('ul')[i].find_all('li')]
                    profile_data['Main_Markets'] = Main_Markets

                elif row.find_all('p')[0].text.strip() == 'Total Annual Sales:':
                    profile_data['Total_Revenue'] = row.find_all('p')[1].text.replace(u'\xa0', u' ').strip()
            
            profile_datas[Company_Name] = profile_data
        time.sleep(choice(sleep))
    except:
        no_profile_url.append(company_profile_url)


# contact data
contact_datas = {}
no_contact_url = []
for company_contact_url in companys_contact_url:
    try:
        company_contact_get = requests.get(company_contact_url, timeout=2)
        if company_contact_get:
            company_contact_html = BeautifulSoup(company_contact_get.content)

            company_info = company_contact_html.find_all('div', {'class':'clearfix mt5'})
            Company_Name = company_info[0].find_all('p', {'class':'fl ml5'})[0].text.strip()

            contact_data = {}
            for row in company_info[1:]:
                key = row.find_all('p', {'class':'fl c6 proDetTit'})[0].text.strip()
                if key in ['Address:', 'City:', 'Country:', 'State/Province:', 'Phone Number:', 'Homepage Address:', 'Mobile:']:
                    contact_data[key] = re.sub(r'[\r\n\t\xa0]', ' ', row.find_all('p', {'class':'fl ml5'})[0].text).strip()
            
            contact_person = company_contact_html.find_all('p', {'class':'contName ml10 mt10'})[0].text.replace(u'\xa0', u' ')
            contact_data["contact_person"] = contact_person

        contact_datas[Company_Name] = contact_data
        time.sleep(choice(sleep))
    except:
        no_contact_url.append(company_contact_url)

# product data
product_datas = {}
no_product_url =[]
for product_url in products_url:
    try:
        product_get = requests.get(product_url, timeout=2)
        if product_get:
            product_html = BeautifulSoup(product_get.content)

            Company_Name = product_html.find_all('a', {'class':'pp_supName'})[0].text.strip()
            
            product_detail = product_html.find_all('ul', {'class':'pp_infoList mt25'})[0].find_all('li')
            product_data = {}
            for row in product_detail:
                key = row.find_all('strong')[0].text.strip()
                if key == 'MOQ:':
                    product_data['Min.Order Quantity'] = re.sub(r'[\n ]', '', row.find_all('span')[0].text)
                elif key == 'FOB Price:':
                    try:
                        product_data['FOB Price'] = re.sub(r'[\n ]', '', row.find_all('label')[0].text)
                    except:
                        pass
        
            PT = product_html.find_all('ul', {'class':'pp_secList2 mt5'})[0]
            if PT.find_all('strong')[0].text.strip() == "Payment Terms:":
                product_data['Payment Terms'] = PT.find_all('span')[0].text.strip()

        product_datas[Company_Name] = product_data
        time.sleep(choice(sleep))
    except:
        no_product_url.append(product_url)

contact_df = pd.DataFrame(contact_datas.values(), index = contact_datas.keys())
profile_df = pd.DataFrame(profile_datas.values(), index = profile_datas.keys())
product_df = pd.DataFrame(product_datas.values(), index = product_datas.keys())
df1 = pd.merge(profile_df, contact_df, how="left", left_index=True, right_index=True)
df2 = pd.merge(df1, product_df, how="left", left_index=True, right_index=True)
df2.to_excel('c:/users/yaoyu/desktop/globalsources.xlsx')

