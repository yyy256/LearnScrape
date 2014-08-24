#-*- coding: UTF-8 -*- 

import requests
import json
import re
from bs4 import BeautifulSoup

s = requests.session()
login_data = {'email': '**********', 'password': '********'}

s.post('http://www.zhihu.com/login', login_data)

r = s.get('http://www.zhihu.com/people/yang-yao-yu-26/followees')

data = r.text
hash_id = re.findall(r'hash_id&quot;: &quot;(.*?)&quot',data)[0]
# hash_id = re.findall(r'user_hash":"(.*?)"}',data)[0]

_xsrf = re.findall(r'_xsrf" value="(.*?)"/>',data)[0]

offsets = 0


params = json.dumps({"hash_id": hash_id,"order_by": "created","offset": offsets})
payload = {"method":"next", "params": params, "_xsrf": _xsrf}

header_info = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/36.0.1985.125 Chrome/36.0.1985.125 Safari/537.36',
    'Host':'www.zhihu.com',
    'Origin':'http://www.zhihu.com',
    'Connection':'keep-alive',
    'Referer':'http://www.zhihu.com/people/yang-yao-yu-26/followees',
    'Content-Type':'application/x-www-form-urlencoded'
    }

click_url = 'http://www.zhihu.com/node/ProfileFolloweesListV2'
r = s.post(click_url,data=payload,headers=header_info)

# soup = BeautifulSoup(data)

# followees = soup.find_all("div", {"class" : "zm-profile-card zm-profile-section-item zg-clear no-hovercard"})

res = re.findall(r'<a title=\\"(.*?)\\"\\ndata-tip', r.text)
print res
