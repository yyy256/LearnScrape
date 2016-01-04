# coding=utf-8

from login_zhihu import *
from bs4 import BeautifulSoup
import pandas as pd

s = requests.session()
s.cookies.update(load_cookies('zhihucookies'))

def find_date_time(url, data_time):
    """find the last data time as start argument"""
    html = s.post(url, data = {'start':data_time, '_xsrf': _xsrf})
    r1 = BeautifulSoup(html.json()['msg'][1])
    if r1.text == u'':
        return 0, []
    else:
        r2 = r1.find_all('div', {'class': 'zm-profile-section-item zm-item clearfix'})
        return r2[-1]['data-time'], map(get_questions, r2)

def get_questions(r):
    data_time = r['data-time']
    url = r.a.get('href')
    action = r.find('div').find(text=True).strip()
    title = r.a.text.strip()
    return {'data_time': data_time, 'action': action, 'title': title, 'url': url}

def get_question_tag(url):
    r = s.get("https://www.zhihu.com" + url)
    r1 = BeautifulSoup(r.content)
    r2 = r1.find('div', {'class': 'zm-tag-editor-labels zg-clear'}).text.strip()
    time.sleep(2)
    return {'url': url, 'tag': r2}

if __name__ == '__main__':
    _xsrf = dict(s.cookies)['_xsrf']
    url = "https://www.zhihu.com/people/man-rocket-65/activities"
    home_url = "https://www.zhihu.com/people/man-rocket-65"
    r = BeautifulSoup(s.get(home_url).content).find_all('div', {'class': 'zm-profile-section-item zm-item clearfix'})
    data_time = r[-1]['data-time']
    questions_list = map(get_questions, r)
    while data_time:
        data_time, questions = find_date_time(url, data_time)
        questions_list.extend(questions)
        time.sleep(3)

    question_df = pd.DataFrame(questions_list)
    question_url = question_df.ix[question_df['action'].isin([u'关注了问题', u'赞同了回答']), 'url'].tolist()
    tag_list = map(get_question_tag, question_url)
    tag_df = pd.DataFrame(tag_list)
