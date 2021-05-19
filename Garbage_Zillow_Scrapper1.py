import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


headers = {'accept': '*/*',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'en-US,en;q=0.9',
'cookie': """zguid=23|%248c06b63e-c299-44ab-b33c-197d23366613; zgsession=1|03e87937-9128-4bec-ac08-5d7a7b93180f; g_state={"i_p":1620200038538,"i_l":2}; G_ENABLED_IDPS=google; JSESSIONID=8D1854BB47EEB4E4A9AD1B9C5830DB1C; AWSALB=G0k0HigYhPCP52JT+iHWUFZDThgBF11WXGHpOUvIckbbixKmlKx/+mBibYojzqBDSMH3wXUXdSNl9tpln0Yh86Ony0oqSUvrX2aVjnud6JZt/e5QxVKZweVKVmln; AWSALBCORS=G0k0HigYhPCP52JT+iHWUFZDThgBF11WXGHpOUvIckbbixKmlKx/+mBibYojzqBDSMH3wXUXdSNl9tpln0Yh86Ony0oqSUvrX2aVjnud6JZt/e5QxVKZweVKVmln; search=6|1622888540411%7Cregion%3Dnew-york-ny%26rect%3D40.915281%252C-73.700272%252C40.495865%252C-74.255641%26disp%3Dmap%26mdm%3Dauto%26pt%3Dpmf%252Cpf%26fs%3D1%26fr%3D0%26mmm%3D1%26rs%3D0%26ah%3D0%26singlestory%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%09%096181%09%09%09%09%09%09""",
'referer': 'https://www.zillow.com/new-york-ny/',
'sec-fetch-dest': 'empty',
'sec-fetch-mode': 'cors',
'sec-fetch-site': 'same-origin',
'sec-gpc': '1',
'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}

final_list = []
for pages in range(1, 21):
    url = f'https://www.zillow.com/new-york-ny/{pages}_p/'
    r = requests.get(url, headers=headers)
    time.sleep(5)
    soup = BeautifulSoup(r.text, 'html.parser')
    container = soup.find('ul', 'photo-cards photo-cards_wow photo-cards_short photo-cards_extra-attribution')
    for box in container:
        if box.find('div', id='nav-ad-container') == None:
            try:
                sqft = int(box.find_all('li')[2].get_text().split(' ')[0].replace(',',''))
            except:
                pass
            try:
                bedrooms = int(box.find('li').get_text().split(' ')[0])
            except:
                bedrooms = box.find('li').get_text()
            try:
                listing_by = box.find('p', 'list-card-extra-info').get_text().split('LISTING BY: ')[1]
            except:
                listing_by = ''
            try:
                bathrooms = int(box.find_all('li')[1].get_text().split(' ')[0])
            except:
                bathrooms = box.find_all('li')[1].get_text()
            dict = {
                'Type': box.find('li','list-card-statusText').get_text().split(' ')[1],
                'Price': int(box.find('div', 'list-card-price').get_text().replace('$','').replace(',','')),
                'Bedrooms': bedrooms,
                'Bathrooms': bathrooms,
                'Sqft': sqft,
                'Street': box.find('address', 'list-card-addr').get_text(),
                'Listing By': listing_by,
                'Link': box.find('a')['href']

            }
            print(dict)

            final_list.append(dict)

df = pd.DataFrame(final_list)
df.to_csv('NewYork1' + '.csv', index=False)
