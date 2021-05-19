from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd


pages = 21
search_term = 'laptop'


final_li = []
browser = webdriver.Chrome('/home/len/PycharmProjects/chromedriver')

for x in range(1, pages):
    url = f'https://www.amazon.com/s?k={search_term}&page={x}&qid=1620034168&ref=sr_pg_1'

    browser.get(url)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    time.sleep(3)
    container = soup.find_all('div', 'sg-col sg-col-4-of-12 sg-col-8-of-16 sg-col-12-of-20')
    for item in container:
        try:
            old_price = int(item.find('span', {'aria-hidden': 'true'}).get_text().replace('$', '').replace(',', '').split('.')[0])
        except:
            old_price = ''
        try:
            new_price = int(item.find('span', 'a-price-whole').get_text().replace(',','').replace('.',''))
        except:
            new_price = ''
        try:
            rating = float(item.find('span', 'a-icon-alt').get_text().split(' ')[0])
        except:
            rating = ''
        try:
            reviews = int(item.find('span', 'a-size-base').get_text())
        except:
            reviews = ''
        dict = {
            'Name': item.div.h2.a.text,
            'New Price': new_price,
            'Old Price': old_price,
            'Rating': rating,
            'Reviews': reviews,
            'Link': "https://www.amazon.com" + item.find('a', 'a-link-normal a-text-normal')['href']
        }
        print(dict)
        final_li.append(dict)

print(final_li)
print(len(final_li))

df = pd.DataFrame(final_li)
df.to_csv(search_term + '.csv', index=False)
browser.quit()
