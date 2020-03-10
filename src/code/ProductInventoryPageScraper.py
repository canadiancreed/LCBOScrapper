from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

from Global import Global


class ProductInventoryPageScraper:

    """
    Returns all inventory data for a specific product id

    :param integer product_id - The id of the product
    :return dict inventory data
    """
    def get_product_inventory_data(self, product_id):

        #launch url
        url = Global.base_url() + "/PhysicalStoreInventoryView?langId=-1&storeId=10203&productId="+product_id

        # create a new Firefox session
        options = Options()
        options.headless = True

        driver = webdriver.Firefox(options=options, executable_path=r'C:\GeckoDriver\geckodriver.exe')
        driver.implicitly_wait(30)
        driver.get(url)

        #Selenium hands the page source to Beautiful Soup
        html_soup=BeautifulSoup(driver.page_source, 'lxml')

        #Parse the table that contains inventory data
        inventory_table_body = html_soup.find_all('div', {'id': 'inventoryTableBody'})

        #Create dictionary to collect inventory data in
        inventory_data = {}

        #Loop through the collected data and parse out what we want
        for inventory_row_data in inventory_table_body:
            for inventory_column_data_spans in inventory_row_data:
                inventory_column_data = inventory_column_data_spans.find_all('span')

                inventory_data.update({inventory_column_data[0].text: inventory_column_data[1].text})

        return inventory_data
