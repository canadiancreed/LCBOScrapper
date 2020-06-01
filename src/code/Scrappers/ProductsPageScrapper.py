import requests

from bs4 import BeautifulSoup

from Global import Global

###
# This collects all potential product URLs for a particular category.
###


class ProductsPageScraper:

    ###
    # All functionality for handling data on LCBO product pages
    ###

    """
    This function will load the initial page for the specific category, collect the total amount of available pages,
    then collections all product urls that exists on every page.

    :param string product_category - The product category to load
    :return list productsURL - Returns a list of product URLs
    """

    def collect_products_urls(self, product_category):

        productsURL = []

        url = Global.base_url() + product_category + "?pageView=grid&orderBy=5&fromPage=catalogEntryList&beginIndex=0"
        headers = {"User-Agent": Global.url_headers()}

        response = requests.get(url, headers=headers)

        html_soup = BeautifulSoup(response.text, 'html.parser')

        pages = html_soup.find_all('a', attrs={'data-page-number': True})

        # Check if pages is empty. If so, there's less then one page of data to process, and handle accordingly
        if not pages:
            last_page_amount = 1
        else:
            last_page_amount = int(pages.pop().text)

        # Get initial page content

        Global.write_to_log_file("main.log", "Starting Page 0 of " + product_category)

        beverages = html_soup.find_all('div', class_='row product')

        for beverage in beverages:
            name = beverage.find('div', class_='product_name')

            productsURL.append(name.a['href'])

        Global.write_to_log_file("main.log", "Ending Page 0 of " + product_category)

        # Now time to loop through the rest of the pages
        for pageValue in range(1, last_page_amount):

            Global.write_to_log_file("main.log", "Starting Page " + str(pageValue) + " of " + product_category)

            beginIndex = pageValue * 12

            url = Global.base_url() + product_category + "?pageView=grid&orderBy=5&fromPage=catalogEntryList&beginIndex=" + str(
                beginIndex)
            headers = {"User-Agent": Global.url_headers()}

            response = requests.get(url, headers=headers)

            html_soup = BeautifulSoup(response.text, 'html.parser')

            beverages = html_soup.find_all('div', class_='row product')

            for beverage in beverages:
                name = beverage.find('div', class_='product_name')

                productsURL.append(name.a['href'])

            Global.write_to_log_file("main.log", "Ending Page " + str(pageValue) + " of " + product_category)

        return productsURL
