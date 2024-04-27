import json
import re
import time

import requests
import connector
import pandas as pd
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

start_year = int(input('Enter start year : '))
current_year = int(input('Enter current year : ')) + 1
sc_id = str(input('Enter company id : ').upper())

format = '.csv'
all_links = []


def scrape_money_control(driver, url, year):
    yearly_links = []
    print(url)
    while url:
        driver.get(url)
        # driver.implicitly_wait(10)
        # Find all elements with the specified class name
        # pagination = driver.find_element(By.XPATH, value='//div[@class="pages MR10 MT15"]')

        pagination = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//div[@class="pages MR10 MT15"]')))

        elements = pagination.find_elements_by_css_selector('a[href]')
        pagination_link = [element.get_attribute('href') for element in elements]
        pagination_link.insert(0, url)
        texts = pagination.find_elements_by_css_selector('a')
        anchor_texts = [text.text for text in texts]
        # print(anchor_texts)

        if 'Next »' in anchor_texts or '« Previous' in anchor_texts:
            # Extract and print the href attribute (link) from each anchor tag
            # driver.find_element(By.PARTIAL_LINK_TEXT, 'Next')
            for anchor in pagination_link[:-1]:
                request = requests.get(anchor)
                soup = BeautifulSoup(request.text, "html.parser")
                all_div = soup.find_all('div', attrs={'class': 'MT15 PT10 PB10'})

                div_ = soup.find_all("div", attrs={'class': 'FL PR20'})
                for title in div_:
                    href = title.find('a')['href']
                    article_url = "https://www.moneycontrol.com" + href
                    yearly_links.append(article_url)
                    all_links.append(article_url)
        else:
            # Extract and print the href attribute (link) from each anchor tag
            # driver.find_element(By.PARTIAL_LINK_TEXT, 'Next')
            for anchor in pagination_link[:]:
                request = requests.get(anchor)
                soup = BeautifulSoup(request.text, "html.parser")
                all_div = soup.find_all('div', attrs={'class': 'MT15 PT10 PB10'})

                div_ = soup.find_all("div", attrs={'class': 'FL PR20'})
                for title in div_:
                    href = title.find('a')['href']
                    article_url = "https://www.moneycontrol.com" + href
                    yearly_links.append(article_url)
                    all_links.append(article_url)

        try:
            # next_page = driver.find_element(By.XPATH, value="//a[@class='red-12']")
            # next_page.click()
            driver.find_element(By.PARTIAL_LINK_TEXT, 'Next').click()

            get_url = driver.current_url
            # print("C_url :" + str(get_url))
            # url = connector.next_page_url(page_no=page_no, next_no=next_no)
            url = get_url
            print('===================================== NEXT ===================================================')
            print("U_url :" + str(url))

        except TimeoutException:
            url = None
        except NoSuchElementException:
            url = None

    # create single file
    df = pd.DataFrame({
        'articles': yearly_links
    })
    if df.shape[0] != 0:
        df.to_csv("{0}_{1}{2}".format(sc_id, year, format), index=False)

    driver.quit()


for year in range(start_year, current_year):
    print("{0},{1}".format(sc_id, year))

    driver = connector.get_driver()
    url = connector.get_base_url(company=sc_id, year=year)
    scrape_money_control(driver, url, year)
    time.sleep(10)

# create single file year-wise
df = pd.DataFrame({
    'articles': all_links
})
if df.shape[0] != 0:
    df.to_csv("{0}_{1}_{2}{3}".format(sc_id, start_year, current_year-1, format), index=False)