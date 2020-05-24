import requests

from bs4 import BeautifulSoup

from Global import Global

# url = Global.base_url()+"wine-14?pageView=grid&orderBy=5&fromPage=catalogEntryList&beginIndex=0"
url = Global.base_url()+"beer-cider-16/cider-16028/cider-16028309-1?pageView=grid&orderBy=5&fromPage=catalogEntryList&beginIndex=0"
headers = {"User-Agent": Global.url_headers()}

response = requests.get(url, headers=headers)

html_soup = BeautifulSoup(response.text, 'html.parser')

# probably a way to put this all on one line, but eh
pages = html_soup.find_all('a', attrs={'data-page-number': True})
last_page_amount = int(pages.pop().text)

# Get initial page content

beverages = html_soup.find_all('div', class_ = 'row product')

for beverage in beverages:
    name = beverage.find('div', class_ = 'product_name')
    print(str(count) + " - " + name.a.text + ", " + name.a['href'])

# Now time to loop through the rest of the pages

for x in range(1, last_page_amount):
    beginIndex = x * 12

    url = Global.base_url() + "beer-cider-16/cider-16028/cider-16028309-1?pageView=grid&orderBy=5&fromPage=catalogEntryList&beginIndex=" + str(beginIndex)
    headers = {"User-Agent": Global.url_headers()}

    response = requests.get(url, headers=headers)

    html_soup = BeautifulSoup(response.text, 'html.parser')

    beverages = html_soup.find_all('div', class_='row product')

    for beverage in beverages:
        name = beverage.find('div', class_='product_name')

        print(str(count) + " - " + name.a.text + ", " + name.a['href'])

        count = count + 1

# print(type(beverage))
# print(len(beverage))
# print(beverage)
