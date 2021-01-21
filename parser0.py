import requests
from bs4 import BeautifulSoup
import logging

storage_number = 1
link = f"https://stroypark.su/catalog/dveri/dveri-mejkomnatnyie?page={storage_number}"
responce = requests.get(f'{link}?page={storage_number}').text
soup = BeautifulSoup(responce, 'lxml')
title = soup.find('section', class_='c-breadcrumb')
title_name = title.find_all('div', class_='c-layout')

for name in title_name:
    name = name.text
    name = name.replace('<a href="/">  ', '</a>').strip()

responce1 = requests.get(f'{link}?page={storage_number}').text
tovar = BeautifulSoup(responce1, 'lxml')
block = tovar.find('div', class_='c-good-item-content')
tovar_block = block.find_all('div', class_='c-good-item-code')

for tovar_name in tovar_block:
    print(tovar_name)



