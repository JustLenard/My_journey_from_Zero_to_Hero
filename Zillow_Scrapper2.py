import requests
import pandas as pd
import time

querystring = {"searchQueryState":"{\"pagination\":{\"currentPage\":4},\"mapBounds\":{\"west\":-76.9937035703125,\"east\":-70.9622094296875,\"south\":38.91268989807701,\"north\":42.452102554844785},\"mapZoom\":8,\"regionSelection\":[{\"regionId\":6181,\"regionType\":6}],\"isMapVisible\":false,\"filterState\":{\"isAllHomes\":{\"value\":true},\"sortSelection\":{\"value\":\"globalrelevanceex\"}},\"isListVisible\":true}","wants":"\\{\"cat1\":\\[\"listResults\"\\],\"cat2\":\\[\"total\"\\]\\}","requestId":"2"}
headers = {
    "cookie": """zguid=23|%248c06b63e-c299-44ab-b33c-197d23366613; zgsession=1|03e87937-9128-4bec-ac08-5d7a7b93180f; g_state={"i_p":1620200038538,"i_l":2}; G_ENABLED_IDPS=google; JSESSIONID=8DE077A4682CBF6F2B2059E8790A23D0; search=6|1623236356679%7Cregion%3Dnew-york-ny%26rect%3D50.62214%252C-68.327143%252C23.705962%252C-125.374896%26disp%3Dmap%26mdm%3Dauto%26pt%3Dpmf%252Cpf%26fs%3D1%26fr%3D0%26mmm%3D1%26rs%3D0%26ah%3D0%09%096181%09%09%09%09%09%09; AWSALB=2Q6m0jMu5wRRwnXKk8q0seAvXW8XJAkTxW7lQKq0UevfPfylHyq8c357EqElENi0UJJ+jSzAN5BgfkACgP24TsZfVJW1r7S7ZPdyJkrZGFI7WVTlEAvvQm4RWw94; AWSALBCORS=2Q6m0jMu5wRRwnXKk8q0seAvXW8XJAkTxW7lQKq0UevfPfylHyq8c357EqElENi0UJJ+jSzAN5BgfkACgP24TsZfVJW1r7S7ZPdyJkrZGFI7WVTlEAvvQm4RWw94""",
    "authority": "www.zillow.com",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "accept": "*/*",
    "sec-gpc": "1",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://www.zillow.com/homes/for_sale/?searchQueryState=%7B%22pagination%22%3A%7B%22currentPage%22%3A2%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-76.9937035703125%2C%22east%22%3A-70.9622094296875%2C%22south%22%3A38.91268989807701%2C%22north%22%3A42.452102554844785%7D%2C%22mapZoom%22%3A8%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A6181%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Afalse%2C%22filterState%22%3A%7B%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%7D%2C%22isListVisible%22%3Atrue%7D",
    "accept-language": "en-US,en;q=0.9",
    "dnt": "1"
}


final_list = []
n = 1
while True:
    url = f'https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState=%7B%22pagination%22%3A%7B%22currentPage%22%3A{n}'+'%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-76.9937035703125%2C%22east%22%3A-70.9622094296875%2C%22south%22%3A38.91268989807701%2C%22north%22%3A42.452102554844785%7D%2C%22mapZoom%22%3A8%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A6181%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Afalse%2C%22filterState%22%3A%7B%22isAllHomes%22%3A%7B%22value%22%3Atrue%7D%2C%22sortSelection%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%7D%2C%22isListVisible%22%3Atrue%7D&wants={%22cat1%22:[%22listResults%22],%22cat2%22:[%22total%22]}&requestId=3'
    # url = 'https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState=%7B%22mapBounds%22%3A%7B%22west%22%3A-74.23661818888648%2C%22east%22%3A-74.18005576518043%2C%22south%22%3A40.51060576689493%2C%22north%22%3A40.566050295912014%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A6181%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Afalse%2C%22filterState%22%3A%7B%22isAllHomes%22%3A%7B%22value%22%3Atrue%7D%2C%22sortSelection%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%7D%2C%22isListVisible%22%3Atrue%2C%22category%22%3A%22cat1%22%2C%22mapZoom%22%3A14%2C%22pagination%22%3A%7B%22currentPage%22%3A'+f'{n}'+'%7D%7D&wants={%22cat1%22:[%22listResults%22],%22cat2%22:[%22total%22]}&requestId=70'
    r = requests.get(url, headers=headers, params=querystring, timeout= 5).json()
    n += 1
    p = r['cat1']['searchResults']['listResults']
    print(len(p))
    for x in range(len(p)):
        try:
            brokerphone = p[x]['brokerPhone']
        except:
            brokerphone = ''
        try:
            brokername = p[x]['brokerName']
        except:
            brokername = ''
        dict = {
            'zpid': p[x]['zpid'].replace("'",''),
            'statusText':p[x]['statusText'].replace("'",''),
            'unformattedPrice':int(p[x]['hdpData']['homeInfo']['price']),
            'price':p[x]['price'].replace("'",''),
            'zestimate':p[x]['zestimate'],
            'addressStreet':p[x]['addressStreet'],
            'addressCity':p[x]['addressCity'],
            'addressState':p[x]['addressState'],
            'beds':p[x]['beds'],
            'baths':p[x]['baths'],
            'area':p[x]['area'],
            'daysOnZillow':p[x]['hdpData']['homeInfo']['daysOnZillow'],
            'brokerName':brokername,
            'brokerPhone':brokerphone,
            'Image Link':p[x]['imgSrc'],
            'detailUrl':p[x]['detailUrl'],
        }
        print(dict)
        final_list.append(dict)
        print(len(p))
    try:
        if len(p) != 40:
            break
    except:
        break
    time.sleep(1)

df = pd.DataFrame(final_list)
df.to_csv('NewYork2' + '.csv', index=False)
