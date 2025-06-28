from bs4 import BeautifulSoup
from rich import print
import lxml
import requests
import os
import pandas as pd

os.system('cls')


url = requests.get('https://news.ycombinator.com/news').content.decode('utf-8')
soup = BeautifulSoup(url, 'lxml')

article_list = {
    'title': [],
    'href': [],
    'score': []
}

article_rows = []

for i in soup.find_all(name='span', class_='titleline'):
    article_list['title'].append(i.find('a').get_text())
    article_list['href'].append(i.find('a').get('href'))

for i in soup.find_all(name='span', class_='score'):
    article_list['score'].append(int(i.get_text().split()[0]))


# article_list_sorted = sorted(article_list, key= lambda x : x['score'], reverse=True)




print(article_list)
print('-'*100)
print(article_rows)