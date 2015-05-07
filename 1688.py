import requests
from bs4 import BeautifulSoup
import time
import sys
import re
from random import choice

reload(sys)
sys.setdefaultencoding('utf-8')

# 获取代理ip
p = "http://www.proxy360.cn/default.aspx"
p1 = requests.get(p)
p2 = BeautifulSoup(p1.content)
p3 = p2.find_all('span', {'style': 'width:140px;'}) # 服务器
p4 = p2.find_all('span', {'style': 'width:50px;'}) # 端口
ip = [item.text.strip() for item in p3]
port = [item.text.strip() for item in p4]

iplist = []
#proxies = {}
for i in range(1, len(ip)):
    ip_port = 'http://'+ip[i]+':'+port[i]
   # ip_port1 = 'https://'+ip[i]+':'+port[i]
    b = "http://www.baidu.com"
    try:

        b1 = requests.get(b, proxies={"http": ip_port}, timeout=0.1)
        if b1:
            iplist.append("http" + "#" + ip_port)
            #proxies['http'].append(ip_port)
    except:
        pass
    try:

        b2 = requests.get(b, proxies={"https": ip_port}, timeout=0.1)
        if b2:
           iplist.append("https" + "#" + ip_port)
            #proxies['https'].append(ip_port)
    except:
        pass


cookies = {"incap_ses_200_257263": "wYlQGwtJbygxH394bovGAj9pw1QAAAAAWGZqailkicbiEpaojW4ZNg==",	
"visid_incap_257263":"u5uzZVSpSay8oR2eanjo3j9pw1QAAAAAQUIPAAAAAAC9LV/MTKpRk8PNyNSDl9+a",
"CNZZDATA4793016":	"cnzz_eid%3D1848069623-1422087813-http%253A%252F%252Fwww.baidu.com%252F%26ntime%3D1422087813"}


url = "http://page.1688.com/cp/cp1.html?spm=0.0.0.0.IdQHU2" # 公司黄页网址

r = requests.get(url)
soup = BeautifulSoup(r.content)

g_data = soup.find_all("dl", {"class": "cell-tags"})

# category_url = []
# for item in g_data:
#     for u in item.find_all("a"):
#         if u.get("href") != "":
#             category_url.append(u.get("href"))


# 提取关键字
category_word = []
for item in g_data:
    for u in item.find_all("a"):
        if u.get("href") != "" and  u.get("class") == None:
            category_word.append(u.get("title"))


# company_yellow_url = []
# for cate_url in category_url:
# 	for i in range(100):
# 		r1 = requests.get(cate_url)
#         soup1 = BeautifulSoup(r1.content)
#         g_data1 = soup1.find_all("a", {"offer-stat": "morecompany"})
#         company_url = [item.get("href") for item in g_data1]
#         for com_url in company_url:
#         	r2 = requests.get(com_url)
#             soup2 = BeautifulSoup(r2.content)
# 			g_data2 = soup2.find_all("a", {"class": "comment-link"})
# 			company_yellow_url.append(g_data2[0].get("href"))
#         time.sleep(2)

# 提取每个公司的黄页地址
# company_yellow_url = []
# for word in category_word:
# 	for i in range(100):
# 		search_url = "http://s.1688.com/company/company_search.htm?keywords=" + urllib.quote(word.encode('gbk')) + "&pageSize=50&beginPage=" + str(i)
#         r1 = requests.get(search_url)
#         soup1 = BeautifulSoup(r1.content)
#         g_data1 = soup1.find_all("a", {"offer-stat": "morecompany"})
#         company_url = [item.get("href") for item in g_data1]
#         for com_url in company_url:
#             try:
#                 r2 = requests.get(com_url, timeout=1)
#                 soup2 = BeautifulSoup(r2.content)
#                 g_data2 = soup2.find_all("a", {"class": "comment-link"})
#                 if len(g_data2) == 0:
#                     company_yellow_url.append(com_url)
#                 else:
#                     company_yellow_url.append(g_data2[0].get("href"))
#             except:
#                 company_yellow_url.append("")
            
#         time.sleep(2)

# 模拟登陆
s = requests.session()
login_data = {'email': 'yyy256@qq.com', 'password': 'zaq12wsx'}
s.post('http://login.1688.com/member/signin.htm', login_data)

ip_url = "http://erwx.daili666.com/ip/?tid=556175342540914&num=1&filter=on"
def query(url):
    ip_r = requests.get(ip_url)
    ip_s = BeautifulSoup(ip_r.content)
    ip = ip_s.text.strip()
    return ip
    
# 从搜索页面中提取每个公司的id以便得到公司的黄页地址
import datetime   
starttime = datetime.datetime.now()   
company_id1 = []

all_i = []
for word in category_word[0]:
    for i in range(1, 3):
        search_url = "http://s.1688.com/company/company_search.htm?keywords=" + requests.utils.quote(word.encode('gbk')) + "&pageSize=50&beginPage=" + str(i)
        r1 = False        
        while not r1 or g_data1 == []:
            #ip = choice(iplist).split('#')  
            # if not r1 or g_data1 == []:
                
            ip = 'http://' + query(ip_url)
            # else:
            #     ip = ip
            try:       
                r1 = requests.get(search_url, timeout=1, proxies={'http': ip})
                soup1 = BeautifulSoup(r1.content)
                g_data1 = soup1.find_all("li", {"class": "company-list-item"})
                if g_data1 == []:
                    all_i.append(i)
                #test = g_data1[1]
                for item in g_data1:
                    company_id1.append(item.get("companyid"))
            except:
        	    r1 = False        
endtime = datetime.datetime.now()   
print (endtime - starttime).seconds

            
     
        #time.sleep(2)
c_i = []
for id in company_id1:
    if id not in c_i:
        c_i.append(id)
len(c_i)
# 从公司的黄页地址中提取信息
with open('test.csv', 'w') as f:
    for id in c_i[:100]:
        company_url_detail = "http://corp.1688.com/page/index.htm?memberId=" + id + "&fromSite=company_site&tab=companyWeb_detail"
        company_url_contact = "http://corp.1688.com//page/index.htm?memberId=" + id + "&fromSite=company_site&tab=companyWeb_contact"
        detail = [u"主营产品或服务:", u"注册资本:", u"法定代表人:", u"地址 :", u"电话 :"]
        # contact = []
        r3 = False
        while not r3:
            ip = 'http://' + choice(iplist)
            try:
                r3 = requests.get(company_url_detail, timeout=1, proxies={'http': ip})
                soup3 = BeautifulSoup(r3.content)
                g_data3 = soup3.find_all('tr', {'class':'content-info'})
                company_name = soup3.find_all('h1', {'class': 'company-name'})[0].get("title")
            except:
                r3 = False
        
        
        

        
        
        title = [item.find_all('td', {'class': re.compile('title')})[0].text.strip() for item in g_data3]
        info = [re.sub(r'[\n\s]', '', item.find_all('td', {'class': re.compile('info')})[0].text) for item in g_data3]
        r4 = False
        while not r4 and g_data4:
            ip = 'http://' + choice(iplist)
            #ip = choice(iplist).split('#')
            try:
                r4 = requests.get(company_url_contact, timeout=1, proxies={'http': ip})
                soup4 = BeautifulSoup(r4.content)
                #company_name = soup4.find_all('h1', {'class': 'company-name'})[0].get("title")
        #r4 = False
                g_data4 = soup4.find_all('tr', {'class':'content-info'})
            except:
                r4 = False
        

        title.extend([item.find_all('td', {'class': re.compile('title')})[0].text.strip() for item in g_data4])
        info.extend([re.sub(r'[\n\s]', '', item.find_all('td', {'class': re.compile('info')})[0].text) for item in g_data4])


        # for d in detail:
        #     for item in g_data3:
        #         if d == item.find_all('td',{'class':'title'})[0].text.strip():
        #             best_item = item.find_all('td', {'class':'info'})
        #         else:
        #             d_a = ""
        out = []
        for d in detail:
            try:
                ind = title.index(d)
                out.append(info[ind])
            except:
                out.append("")

        f.write('%s,%s,%s,%s,%s,%s\n' %(company_name, out[0], out[1], out[2], out[3], out[4]))

        time.sleep(5)

iplist1 = iplist
ff = open('C:\\Users\\yaoyu\\Downloads\\EhmX_Wh6.txt', 'r')
iplist = [id.strip() for id in ff.readlines()]
ff.close()




import pandas

log = {'ua':'039UW5TcyMNYQwiAiwTR3tCf0J/QnhEcUpkMmQ=|Um5Ockt0S3ZCe0V4QHVBfyk=|U2xMHDJ+H2QJZwBxX39Rb1d5WXcxUDZKOxVDFQ==|VGhXd1llXGNcYVVsUm9XYlZpXmNBeUJ3THlAfkV5TXBEe09zXQs=|VWldfS0RMQ03DTQULAwiAntHNhY4bjg=|VmNDbUMV|V2NDbUMV|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|W2FBET9gO30pUDlDOUcgWzdjX3FRbU12ShxK|XGBdfVMDPwo3CTISRWtXblJuU2pRbVBlXmBaLxIwDjMMMAw4DDgCPQQ+CzUAPGtFZVkPIXc=|XWdHFzlmPXsvVj9FP0EmXTFlWXdXakpzTnJMGkw=|XmREFDoUNAkpEC0TK30r|X2VFFTsVNQkpEC0VKX8p|QHpaCiR7IGYySyJYIlw7QCx4RGpKdlZvUmlVA1U=|QXtbCyV6IWczSiNZI106QS15RWtLdlZvUmdbDVs=|QnhYCCYIKBU1DDEFOG44|Q3lZCScJKRU1DDMONWM1|RH5eDiB/JGI2TyZcJlg/RCh8QG5OclJrVGhWAFY=|RX9fDyF+JWM3TiddJ1k+RSl9QW9PclJrVGtQBlA=|RnxcDCIMLBExCDcJMmQy|R31dDSMNLRExDTAMMAxaDA==|SHJSAixzKG46QypQKlQzSCRwTGJCfl5iX2NcYjRi|SXFRAS9vO2MfdRBxDFQpQD1cNxk5aV1hQX1DfSsLNhY4FjYKNws1DFoM|SnBQAC5xKmw4QShSKFYxSiZyTmBAfV1hXGBZYzVj|S3FRAS9vO2MfdRBxDFQpQD1cNxk5BSUZJBgjHUsd|THZWBihoPGQYchd2C1MuRzpbMB4+AyMfIhwmGE4Y|TXdXBykHJxo6BjsFMA9ZDw==|TndKd1dqSnVVaVBsTHJKcFBoXHxGfl5iXmdHe1tnXGFBf0trXmpKdE5uUGtLdU1tU2pKdEpqVGtLdUlpV2pKdUFhXmtLdE5uUWpKdlZpUHBPcVFuUXFOciQ=',
'TPL_username': 'yyy256@qq.com',
'TPL_password': '', 
'TPL_checkcode': '',    
'loginsite': 3,
'newlogin':0,
'TPL_redirect_url':'http://login.1688.com/member/jump.htm?target=http%3A%2F%2Flogin.1688.com%2Fmember%2FmarketSigninJump.htm%3FDone%3Dhttp%253A%252F%252Fmember.1688.com%252Fmember%252Foperations%252Fmember_operations_jump_engine.htm%253Ftracelog%253Dlogin%2526operSceneId%253Dafter_pass_from_taobao%2526defaultTarget%253Dhttp%25253A%25252F%25252Fwork.1688.com%25252F%25253Ftracelog%25253Dlogin_target_is_blank_1688',
'from':'b2b',
'fc':'default',
'style':'b2b',11
'css_style':'', 
#'tid':'',
'support':000001,
'CtrlVersion':'1,0,0,7',
'loginType':3,
'minititle': '',
'minipara': '', 
#'umto':    'NaN',
'pstrong':2,
'llnick':'' ,
'sign':'',
'need_sign':'',
# isIgnore  
'full_redirect':'true',
# popid 
# callback  
# guf   
# not_duplite_str   
# need_user_id  
# poy   
'gvfdcname':10,
'gvfdcre':'687474703A2F2F6C6F67696E2E313638382E636F6D2F6D656D6265722F7369676E696E2E68746D3F74726163656C6F673D6D656D6265725F7369676E6F75745F7369676E696E',
# from_encoding 
# sub   
'TPL_password_2':'1946ef9143ca258fe63837f5cac877934f10e52ff26e15f162c8da77a2277ca2e69f3ce895618957c821f1bdb4a044efda6a04909662632471fe248f789164751d80e1083078f5cd9a16036c756011dc22a96e901df50752ad188ac3bc35310f79c16d9da41e136a402a64fba55e9802786c40473dff3894b51af79858d9496b',
'loginASR':1,
'loginASRSuc':1}
# allp  
# oslanguage    zh-CN
# sr    1366*768
# osVer 
# naviVer   firefox|35