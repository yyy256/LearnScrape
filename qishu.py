import requests
from bs4 import BeautifulSoup
import re

url = "http://www.qisuu.com/s/1/"

get_url = requests.get(url)
book_html = BeautifulSoup(get_url.content)

all_books = book_html.find_all('div', {'class': 'listBox'})

for book in all_books[0].find_all(href=re.compile('Shtml')):
    book_url = 'http://www.qisuu.com' + book.get('href')
    get_book = requests.get(book_url)

    book_name = re.sub(r'[\r\n\t\《》]', '', book.text)
    with open(book_name + '.txt', 'wb') as f:
        f.write()