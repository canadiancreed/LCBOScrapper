import requests

from bs4 import BeautifulSoup

from Global import Global

url = Global.base_url()+"wine-14?pageView=grid&orderBy=5&fromPage=catalogEntryList&beginIndex=0"
headers = {"User-Agent": Global.url_headers()}

response = requests.get(url, headers=headers)

html_soup = BeautifulSoup(response.text, 'html.parser')

# probably a way to put this all on one line, but eh
pages = html_soup.find_all('a', attrs={'data-page-number': True})
last_page_amount = pages.pop().text

beverages = html_soup.find_all('div', class_ = 'row product')

for beverage in beverages:

    name = beverage.find('div', class_ = 'product_name')

    #print(name.a.text)
# print(type(beverage))
# print(len(beverage))
# print(beverage)
