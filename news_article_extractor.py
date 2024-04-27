import re
import os
import csv
import json
import time

import requests
import pandas as pd
from bs4 import BeautifulSoup

df = pd.DataFrame(
    columns=['datePublished', 'company', 'author', 'headline', 'description', 'articleBody', 'tags', 'keywords', 'url'])

urls = pd.read_csv('ONG_2011_2024.csv')['articles'].tolist()
company = 'ONGC'
counter = 1
next_counter = 50


def get_blog_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    all_script = soup.find_all('script', attrs={'type': 'application/ld+json'})

    raw_articles_str = all_script[2].get_text().replace('\r\n', ' ')

    parts = re.split(r"""("[^"]*"|'[^']*')""", raw_articles_str)

    parts[::2] = map(lambda s: "".join(s.split()), parts[::2])

    article_str = "".join(parts)
    article_str = article_str[1:]
    article_str = article_str[:-1]
    article_dict = json.loads(article_str, strict=False)

    all_tags = soup.find_all('div', attrs={'class': 'tags_first_line'})

    lst_all_tags = [i.get_text() for i in all_tags]

    tags = lst_all_tags[0].replace('Tags:', '')
    tags = tags.replace('\n', '')
    tags = tags.split('#')
    tags = tags[1:]
    tags = ', '.join([str(elem).strip() for elem in tags])

    article_dict['tags'] = tags
    # print(article_dict['author']['name'])
    return article_dict


for url in urls:
    if counter == next_counter:
        print("i'm sleeping...")
        time.sleep(10)
        next_counter += 50
    try:
        article_dict = get_blog_content(url)

        # print(article_dict['datePublished'])
        # print(article_dict['author']['name'])
        # print(article_dict['headline'])
        # print(article_dict['description'])
        # print(article_dict['articleBody'])
        # print(article_dict['tags'])
        # print(article_dict['url'])
        print('-----------------------------------------------------------------------------')
        article_list = [[article_dict['datePublished'],
                         company,
                         article_dict['author']['name'],
                         article_dict['headline'],
                         article_dict['description'],
                         article_dict['articleBody'],
                         article_dict['tags'],
                         article_dict['keywords'],
                         url]]

        df = df._append(pd.DataFrame(article_list,
                                     columns=['datePublished', 'company', 'author', 'headline',
                                              'description', 'articleBody', 'tags', 'keywords', 'url']),
                        ignore_index=True)
        print(df.head())
        print(df.tail())
    except Exception as e:
        article_list = [
            ['error', company, 'error', 'error', 'error', 'error', 'error', 'error', 'error']]
        df = df._append(pd.DataFrame(article_list,
                                     columns=['datePublished', 'company', 'author', 'headline',
                                              'description', 'articleBody', 'tags', 'keywords', 'url']),
                        ignore_index=True)
        continue

    counter += 1

print(df)
df.to_csv("ongc_news.csv", index=False)
