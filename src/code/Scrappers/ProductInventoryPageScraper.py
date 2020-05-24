import csv

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from Global import Global


###
# All functionality for handling data on LCBO product inventory pages
###


class ProductInventoryPageScraper:
    current_product_inventory_data = []

    """
    Returns all inventory data for a specific product id

    :param integer product_id - The id of the product
    :return dict inventory data
    """

    def get_product_inventory_data(self, product_id):

        # launch url. Store ID needs to render to a real store to validate
        url = Global.base_url() + "/PhysicalStoreInventoryView?langId=-1&storeId=10203&productId=" + product_id

        # create a new Firefox session
        options = Options()
        options.add_argument('--blink-settings=imagesEnabled=false')  # Prevents images from being loaded
        options.headless = True

        driver = webdriver.Firefox(options=options, executable_path=r'C:\GeckoDriver\geckodriver.exe')
        driver.implicitly_wait(30)
        driver.get(url)

        # Selenium hands the page source to Beautiful Soup
        html_soup = BeautifulSoup(driver.page_source, 'lxml')

        # Parse the table that contains inventory data
        inventory_table_body = html_soup.find_all('div', {'id': 'inventoryTableBody'})

        # Create dictionary to collect inventory data in
        inventory_data = Global.populate_base_inventory_location_data_dict(product_id)

        # Loop through the collected data and parse out what we want
        for inventory_row_data in inventory_table_body:
            for inventory_column_data_spans in inventory_row_data:
                inventory_column_data = inventory_column_data_spans.find_all('span')

                if inventory_column_data[0].text in inventory_data:
                    inventory_data.update({inventory_column_data[0].text: inventory_column_data[1].text})
                else:
                    Global.write_to_log_file("missing_inventory_location.log", inventory_column_data[0].text)

        self.current_product_inventory_data = inventory_data

        # Prevents zombie firefox processes?
        driver.quit()

        return None

    """
    Writes Product Inventory Page Data to csv - this may be refactor to be placed in Global or a library file in future

    :param integer file_name - Name of file to save too
    :param integer line_number - signals if the csv headers should be written. If first line, then yes. Otherwise no.
    :return null None
    """

    def write_to_file(self, file_name, line_number):
        default_file_path = Global.get_data_directory() + "/" + file_name

        with open(default_file_path, mode='a+', newline='\n', encoding='utf-8') as csv_file:
            fieldnames = self.current_product_inventory_data.keys()
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            if line_number == 1:
                writer.writeheader()

            writer.writerow(self.current_product_inventory_data)

        return None
