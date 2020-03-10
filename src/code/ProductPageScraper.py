import requests

from bs4 import BeautifulSoup

from Global import Global


class ProductPageScraper:

    def get_product_data(self):
        product_data = {}

        # Sample url
        url = Global.base_url() + "/wine-14/sogrape-mateus-ros%C3%A9-166#.XYFxfyhKguV"
        headers = {"User-Agent": Global.url_headers()}

        response = requests.get(url, headers=headers)

        html_soup = BeautifulSoup(response.text, 'html.parser')

        data = html_soup.find('div', class_='padded-container')

        product_details = self.__get_product_details_list(data)

        product_data.update({'Alcohol': product_details.get('Alcohol')})
        product_data.update({'Bottle Size': product_details.get('Bottle Size')})
        product_data.update({'Country': product_details.get('Country')})
        product_data.update({'Description': self.__get_product_description(data)})
        product_data.update({'Id': self.__get_product_id(data)})
        product_data.update({'Image': self.__get_product_image(data)})
        product_data.update({'Manufacturer': product_details.get('Manufacturer')})
        product_data.update({'Name': self.__get_product_name(data)})
        product_data.update({'Price': self.__get_product_price(data)})
        product_data.update({'Sugar': product_details.get('Sugar')})
        product_data.update({'Sweetness': product_details.get('Sweetness')})
        product_data.update({'Style': product_details.get('Style')})
        product_data.update({'Varietal': product_details.get('Varietal')})

        return self.__get_product_id(data)

    def write_to_file(self):
        return None

    def __get_product_details_list(self, data):
        product_details = {}

        try:
            product_details_section = data.find_all('div', {'class', 'product-details-list'})

            for product_detail_section in product_details_section:
                product_detail = product_detail_section.find_all('span')

                product_details.update({'Bottle Size': product_detail[0].text.strip()})
                product_details.update({"Alcohol": product_detail[1].text})
                product_details.update({"Country": product_detail[2].text.strip()})
                product_details.update({"Manufacturer": product_detail[3].text})
                product_details.update({"Sugar": product_detail[4].text.strip()})
                product_details.update({"Sweetness": product_detail[5].text.strip()})
                product_details.update({"Style": product_detail[6].text})
                product_details.update({"Varietal": product_detail[7].text})
        except:
            pass

        return product_details

    def __get_product_description(self, data):
        product_description = None

        try:
            product_description = data.find('p', {'class': 'hidden-xs'}).text
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
