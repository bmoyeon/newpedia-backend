import csv
import requests
from bs4 import BeautifulSoup

in_file = open('newpedia.csv', 'w+', encoding = 'utf-8')
data_writer = csv.writer(in_file)
data_writer.writerow(['name', 'description'])
url = requests.get('https://ko.wikipedia.org/wiki/%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD%EC%9D%98_%EC%9D%B8%ED%84%B0%EB%84%B7_%EC%8B%A0%EC%A1%B0%EC%96%B4_%EB%AA%A9%EB%A1%9D')

html = url.text
bs = BeautifulSoup(html, 'html.parser')

categories = bs.select('span.mw-headline')
for category in categories:
    print(category.text)

infos = bs.select('ul > li')
for info in infos:
    if info.select('b'):
        name = info.select('b')[0].text
        descriptions = info.text.split(':')[1].strip(' ')
        descriptions = descriptions.split('[')
        for description in descriptions:
            if ']' in description:
                continue
            data_writer.writerow((name, description))

in_file.close()
