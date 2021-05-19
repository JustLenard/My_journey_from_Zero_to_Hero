import time
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

path = '/home/len/PycharmProjects/chromedriver'
follow_page = "https://www.royalroad.com/my/follows"
home = "https://www.royalroad.com/account/login?returnUrl=https%3A%2F%2Fwww.royalroad.com%2Fhome"
s = requests.session()
email = ''
my_password = ''

login_payload = {
    'Email': email,
    'Password': my_password,
}

login_req = s.post(home, data=login_payload)
follow = s.get(follow_page)
soup = BeautifulSoup(follow.text, 'html.parser')

fictions = soup.find_all('div', class_='fiction-list-item row')

fiction_links = []
for links in fictions:
    try:
        link = links.div.ul.li.find_next_sibling().a['href']
    except AttributeError:
        link = links.div.ul.li.a['href']
    fiction_links.append('https://www.royalroad.com' + link)
print(fiction_links)

cleaned_fl = []
with open('EditedList.txt', 'r+') as f:
    s = f.read()
    for i in fiction_links:
        if i not in s:
            cleaned_fl.append(i)
    f.write(str(cleaned_fl))
    print(cleaned_fl)
with open('Countdown.txt', 'r+') as countdown:
    c = int(countdown.read())
    c += 1
    print(c)
    if c > 50:
        with open('EditedList.txt', 'w') as f:
            f.write(str(cleaned_fl))
with open('Countdown.txt', 'w') as countdown:
    countdown.write(str(c))

browser = webdriver.Chrome(path)
browser.get(follow_page)
login = browser.find_element_by_id("email")
login.send_keys(email)
password = browser.find_element_by_id("password")
password.send_keys(my_password)
password.send_keys(Keys.RETURN)

time.sleep(3)
browser.find_element_by_xpath('//*[@id="ncmp__tool"]/div/div/div[3]/div[1]/button[2]').click()
time.sleep(1)


def scroll():
    browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    browser.execute_script("window.scrollBy(0,-500)")


for chapters in cleaned_fl:
    print('Checking new fiction-- ' + chapters)
    print('Looking through comment page nr: 1')
    check_be_first = []
    check_comment = []
    n = 1
    browser.get(chapters)
    time.sleep(1)
    scroll()
    current_url = browser.current_url
    get_out = False
    while get_out is False:
        try:
            scroll()
            time.sleep(1)
            check_comment = browser.find_elements_by_xpath(
                "//*[contains(text (), 'Your neighboring AI overlord sends his warm regards and thanks the author for the chapter.')]")
            check_be_first = browser.find_elements_by_xpath(
                "//*[contains(text (), 'No one has commented yet. Be the first!')]")
            if check_comment != []:
                print('I marked the place already-- breaking out of the loop\n')
                get_out = True

            if check_comment == [] and check_be_first == []:
                n += 1
                print('Looking through comment page nr: ' + str(n))
                browser.get(current_url + '?comments=' + str(n))
                time.sleep(1)
                scroll()
                time.sleep(1)
                check_comment = browser.find_elements_by_xpath(
                    "//*[contains(text (), 'Your neighboring AI overlord sends his warm regards and thanks the author for the chapter.')]")
                check_be_first = browser.find_elements_by_xpath(
                    "//*[contains(text (), 'No one has commented yet. Be the first!')]")
            if check_be_first != []:
                n = 1
                print('Marking the spot\n')
                time.sleep(2)
                scroll()
                time.sleep(2)
                browser.switch_to.frame("comment_ifr")
                browser.find_element_by_xpath("//body[@id='tinymce']/p").send_keys(
                    'Your neighboring AI overlord sends his warm regards and thanks the author for the chapter.')
                browser.switch_to.parent_frame()
                browser.find_element_by_xpath("//button[@class='btn btn-primary btn-sm']").click()
                time.sleep(2)
                button = browser.find_element_by_xpath(
                    "//div[@class='row margin-bottom-10 margin-left-0 margin-right-0']/a[1]")
                browser.execute_script("arguments[0].scrollIntoView(true);", button)
                button.click()
                time.sleep(2)
                current_url = browser.current_url
                print('Checking for mark on previous chapters:')
                print('Looking through comment page nr: 1')
        except:
            print('i am in excpet-- for some reason')
            quit()

browser.quit()
