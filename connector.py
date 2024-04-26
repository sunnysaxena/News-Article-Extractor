# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--ignore-certificate-errors')

options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")


def get_base_url(company, year):
    # set webdriver path here it may vary
    return "https://www.moneycontrol.com/stocks/company_info/stock_news.php?sc_id=" + \
        str(company) + "&durationType=Y&Year=" + str(year)


def next_page_url(page_no, next_no):
    return 'https://www.moneycontrol.com/stocks/company_info/stock_news.php?sc_id=RI&scat=&pageno=' + str(
        page_no) + '&next=' + str(next_no) + '&durationType=Y&Year=2023&duration=1&news_type='


def get_driver():
    return webdriver.Chrome('chromedriver')  # , options=options)


def get_page_no_and_next(url, sc_id, page_no, next, year):
    request = requests.get(url)
    soup = BeautifulSoup(request.text, "html.parser")

    all_page_no = soup.find_all('div', attrs={'class': 'pages MR10 MT15'})
    page_list = [i.text for i in all_page_no[0].find_all('a')]

    if any(map(str.isdigit, page_list[-1])):
        return int(page_list[-1]), next
    else:
        next = next + 1
        page_no = int(page_list[-2])
        url = 'https://www.moneycontrol.com/stocks/company_info/stock_news.php?sc_id=' + sc_id + '&scat=&pageno=' + str(
            page_no) + '&next=' + str(next) + '&durationType=Y&Year=' + str(year) + '&duration=1&news_type='
        return get_page_no_and_next(url, sc_id, page_no, next, year)
