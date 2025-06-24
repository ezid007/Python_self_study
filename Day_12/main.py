from bs4 import BeautifulSoup
import requests
import lxml
import os
from rich import print

os.system('cls')

url = 'https://www.empireonline.com/movies/features/best-movies-2/'

response = requests.get(url).text

soup = BeautifulSoup(response, 'lxml')

movies= soup.find_all(name='h2')
movie_list = []

for i in movies:
    i.find('strong')
    movie_list.append(i.text)
    
movie_list_invers = movie_list[::-1]


filename = 'Day_12\\movie_list_100_2.txt'

with open(filename, 'w', encoding='utf-8') as file:
    for i in movie_list_invers:
        file.write(f'{i}\n')

