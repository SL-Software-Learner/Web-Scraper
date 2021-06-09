import os
import requests
from bs4 import BeautifulSoup
from string import punctuation
your_dir = os.getcwd()
punctuation = punctuation.replace("'", "")
page = int(input())
type_art = input()


def request(u):
    r = requests.get(u, headers={'Accept-Language': 'en-US,en;q=0.5'}).content
    return BeautifulSoup(r, 'html.parser')


for k in range(page):
    os.mkdir('Page_' + str(k + 1))
    os.chdir('Page_' + str(k + 1))
    url = 'https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&page=' + str(k + 1)
    art_url = 'https://www.nature.com'
    soup = request(url)
    art = soup.find_all('article')
    for el in art:
        if el.find('span', class_='c-meta__type').text == type_art:
            soup_art = request(art_url + el.find('a', class_='c-card__link u-link-inherit').get('href'))
            h = soup_art.find('h1').text
            table = h.maketrans('', '', punctuation)
            head = h.translate(table).replace(' ', '_')
            f = open((head + '.txt'), 'w', encoding='utf8')
            h = soup_art.find('div', class_='c-article-body u-clearfix')
            if h is None:
                h = soup_art.find('div', class_='article-item__body')
            for i in h:
                try:
                    f.write(i.text)
                except AttributeError:
                    continue
            f.close()
    os.chdir(your_dir)
