import csv
import requests

from bs4 import BeautifulSoup
from Global import Global


###
# All functionality for handling data on LCBO product pages
###


class ProductPageScraper:
    current_product_data = {}

    # This array won't match the final DB schema, but data transformation isn't part of this functions brief.
    # This is isolated in it's own function to organize the dict structure, as it can change at the source

    def populate_base_product_data_dict(self):
        product_data = {"Alcohol/Vol:": "", "Bottle Size:": "", "Made In:": "", "Description": "", "Id": "",
                        "Image": "", "By:": "", "Name": "", "Price": "", "Release Date:": "", "Sugar Content:": "",
                        "Sweetness Descriptor:": "", "Style:": "", "Varietal:": ""
                        }

        return product_data

    def get_product_data(self, url):

        # Sample url
        headers = {"User-Agent": Global.url_headers()}

        response = requests.get(url, headers=headers)

        html_soup = BeautifulSoup(response.text, 'html.parser')

        product_details = self.__get_product_details_list(html_soup)

        product_data = self.populate_base_product_data_dict()

        product_data["Description"] = self.__get_product_description(html_soup)
        product_data["Id"] = self.__get_product_id(html_soup)
        product_data["Image"] = self.__get_product_image(html_soup)
        product_data["Keyword"] = self.__get_product_keyword(html_soup)
        product_data["Name"] = self.__get_product_name(html_soup)
        product_data["Price"] = self.__get_product_price(html_soup)

        for product_key, product_value in product_details.items():
            product_data[product_key] = product_value

        self.current_product_data = product_data

        return self.__get_product_id(html_soup)

    def write_to_file(self, file_name, line_number):
        default_file_path = Global.get_data_directory() + "/" + file_name

        with open(default_file_path, mode='a+', newline='\n', encoding='utf-8') as csv_file:
            fieldnames = self.current_product_data.keys()
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            if line_number == 1:
                writer.writeheader()

            writer.writerow(self.current_product_data)

        return None

    def __get_product_details_list(self, data):
        product_details = {}

        try:
            product_details_section = data.find('div', {'class', 'product-details-list'})

            product_detail_keys = {}
            product_detail_values = {}

            product_detail_keys = product_details_section.find_all('b')
            product_detail_values = product_details_section.find_all('span')

            for x in range(0, len(product_detail_keys)):
                product_details.update({product_detail_keys[x].text.strip(): product_detail_values[x].text.strip()})

        except Exception as e:
            print(e)

        return product_details

    def __get_product_description(self, data):
        product_description = None

        try:
            product_description = data.find('div', {'class': 'product-text-content'}).text
        except:
            pass

        return product_description

    def __get_product_id(self, data):
        product_id = None

        try:
            product_id = data.find('input', {'id': 'pdId'}).get('value')
        except:
            pass

        return product_id

    def __get_product_image(self, data):
        product_image = None

        try:
            product_image = data.find('img', {'id': 'productMainImage'}).get('src')
        except:
            pass

        return product_image

    def __get_product_keyword(self, data):
        product_keyword = None

        try:
            product_keyword = data.find('input', {'id': 'productKeyword'}).get('value')
        except:
            pass

        return product_keyword

    def __get_product_name(self, data):
        product_name = None

        try:
            product_name = data.find('h1', {'role': 'heading'}).text
        except:
            pass

        return product_name

    def __get_product_price(self, data):
        product_price = None

        try:
            product_price = data.find('span', {'class': 'price'}).text
        except:
            pass

        return product_price.strip()
