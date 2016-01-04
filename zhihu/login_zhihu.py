# coding=utf-8

import requests
import json
import os
import re
import pickle

def save_cookies(requests_cookiejar, filename):
    with open(filename, 'wb') as f:
        pickle.dump(requests_cookiejar, f)

def load_cookies(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

def get_xsrf(session, url):
    sign_html = session.get(url).content
    return re.findall(r'_xsrf" value="(.*?)"/>', sign_html)[0]

def get_captcha(session, url):
    captcha_html = session.get(url, stream = True)
    with open('captcha.gif', 'wb') as f:
        for chunk in captcha_html.iter_content():
            f.write(chunk)

def login(session):
    if os.path.exists('zhihucookies'):
        log_status = session.cookies.update(load_cookies('zhihucookies'))
    else:
        sign_url = "https://www.zhihu.com/#signin"
        login_url = "http://www.zhihu.com/login/email"
        captcha_url = "http://www.zhihu.com/captcha.gif"
        headers = {'Host' : 'www.zhihu.com',
            'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0',
            'Referer' : 'https://www.zhihu.com/'}
        login_data = {}
        login_data['email'] = raw_input("input your email: ")
        login_data['password'] = raw_input("input your password: ")
        login_data['remember_me'] = "true"
        get_captcha(s, captcha_url)
        login_data['captcha'] = raw_input('input your captcha: ')
        login_data['_xsrf'] = get_xsrf(s, sign_url)

        log_status = session.post(login_url, headers = headers, data = login_data)
        save_cookies(session.cookies, 'zhihucookies')
    return json.loads(log_status.content)['msg']

if __name__ == '__main__':
    s = requests.session()
    log_status = login(s)
