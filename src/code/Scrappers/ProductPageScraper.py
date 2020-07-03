import csv
import requests

from bs4 import BeautifulSoup
from Global import Global


###
# All functionality for handling data on LCBO product pages
###


class ProductPageScraper:
    current_product_data = {}

    """
    Creates and returns the base product data dictionary
    
    This array won't match the final DB schema, but data transformation isn't part of this functions brief.
    This is isolated in it's own function to organize the dict structure, as it can change at the source

    :return dict product_data
    """

    def populate_base_product_data_dict(self):
        product_data = {"Alcohol/Vol:": "", "Bottle Size:": "", "Made In:": "", "Description": "", "Id": "",
                        "Image": "", "By:": "", "Name": "", "Price": "", "Release Date:": "", "Sugar Content:": "",
                        "Sweetness Descriptor:": "", "Style:": "", "Varietal:": ""
                        }

        return product_data

    """
    Populates the product_data dictionary with data from the product at the specific url passed
    
    :param string url - The url of the product to be processed
    :return int product_id - Returns the product_id for the specified product
    """

    def get_product_data(self, url):

        headers = {"User-Agent": Global.url_headers()}

        response = requests.get(url, headers=headers)

        html_soup = BeautifulSoup(response.text, 'html.parser')

        product_details = self.__get_product_details_list(html_soup, url)

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

    """
    Writes Product Inventory Page Data to csv - this may be refactor to be placed in Global or a library file in future

    :param integer file_name - Name of file to save too
    :param integer line_number - signals if the csv headers should be written. If first line, then yes. Otherwise no.
    :return null None
    """

    def write_to_file(self, file_name, line_number):
        default_file_path = Global.get_data_directory() + "/" + file_name

        with open(default_file_path, mode='a+', newline='\n', encoding='utf-8') as csv_file:
            fieldnames = self.current_product_data.keys()
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            if line_number == 1:
                writer.writeheader()

            writer.writerow(self.current_product_data)

        return None

    """
    Takes the data in the product details list section of the product page and processes it, returning it in a dictionary

    :param object data - Passed data of the processed page
    :return dictionary product_details - A dictionary of the product's details scrapped into a dictionary
    """

    def __get_product_details_list(self, data, url):
        product_details = {}

        try:
            product_details_section = data.find('div', {'class', 'product-details-list'})

            if product_details_section:
                product_detail_keys = product_details_section.find_all('b')
                product_detail_values = product_details_section.find_all('span')

                for x in range(0, len(product_detail_keys)):
                    product_details.update({product_detail_keys[x].text.strip(): product_detail_values[x].text.strip()})
            else:
                Global.write_to_log_file("error.log", "Product @ " + url + " contained no product details.")

        except Exception as e:
            Global.write_to_log_file("error.log", e)

        return product_details

    """
    Parses the product description from the product page

    :param object data - Passed data of the processed page
    :return string product_description
    """

    def __get_product_description(self, data):
        product_description = None

        try:
            product_description = data.find('div', {'class': 'product-text-content'}).text
        except Exception as e:
            Global.write_to_log_file("error.log", e)

        return product_description

    """
    Parses the product id from the product page

    :param object data - Passed data of the processed page
    :return int product_id
    """

    def __get_product_id(self, data):
        product_id = None

        try:
            product_id = data.find('input', {'id': 'pdId'}).get('value')
        except Exception as e:
            Global.write_to_log_file("error.log", e)

        return product_id

    """
    Parses the product image url from the product page

    :param object data - Passed data of the processed page
    :return string product_image
    """

    def __get_product_image(self, data):
        product_image = None

        try:
            product_image = data.find('img', {'id': 'productMainImage'}).get('src')
        except Exception as e:
            Global.write_to_log_file("error.log", e)

        return product_image

    """
    Parses the product keyword(s) string from the product page

    :param object data - Passed data of the processed page
    :return string product_keyword
    """

    def __get_product_keyword(self, data):
        product_keyword = None

        try:
            product_keyword = data.find('input', {'id': 'productKeyword'}).get('value')
        except Exception as e:
            Global.write_to_log_file("error.log", e)

        return product_keyword

    """
    Parses the product name from the product page

    :param object data - Passed data of the processed page
    :return string product_name
    """

    def __get_product_name(self, data):
        product_name = None

        try:
            product_name = data.find('h1', {'role': 'heading'}).text
        except Exception as e:
            Global.write_to_log_file("error.log", e)

        return product_name

    """
    Parses the product price from the product page

    :param object data - Passed data of the processed page
    :return double product_price
    """

    def __get_product_price(self, data):
        product_price = None

        try:
            product_price = data.find('span', {'class': 'price'}).text
            product_price.strip()
        except Exception as e:
            Global.write_to_log_file("error.log", e)

        return product_price
