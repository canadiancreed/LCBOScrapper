import csv
import re
import json

from bs4 import BeautifulSoup
from urllib.request import urlopen

from Global import Global


###
# All functionality for handling data on LCBO product inventory pages
###


class ProductInventoryPageScraper:
    current_product_inventory_data = []
    current_product_store_data = []

    """
    Returns all inventory data for a specific product id
    Also collects store data, as the source collects that information as well

    :param integer product_id - The id of the product
    :return dict inventory data
    """

    def get_product_inventory_data(self, product_id):
        inventory_data = []

        # launch url. Store ID needs to render to a real store to validate
        url = Global.base_url() + "/PhysicalStoreInventoryView?langId=-1&storeId=10203&productId=" + product_id

        # Collect all script tags on this page
        soup = BeautifulSoup(urlopen(url).read(), "html.parser")
        scripts = [element.text for element in soup.findAll('script')]

        """
        Loop through collected scripts and select the one with the information we want.
        Then isolate the javascript array code, and collect it to a string. Then exit 
        Probably a better way of getting this, but its good enough for now
        """
        for script in scripts:
            if "storesArray" in script:
                inventory_data = re.findall(r"\[(.+?)\];", script, flags=re.S)

                break

        # Now that we have data (or blank), we filter it to be easier to put into a list for easier manipulation
        # The loop isn't really needed, but it works sadly so there it is.

        if inventory_data:
            store_data_inventory_dict = {}

            for data in inventory_data:
                # Change invalid names, add quotes around keys
                data = data.replace("city", "\"city\"")
                data = data.replace("description", "\"description\"")
                data = data.replace("address1", "\"addressOne\"")
                data = data.replace("address2", "\"addressTwo\"")
                data = data.replace("phone", "\"phone\"")
                data = data.replace("uniqueId", "\"uniqueId\"")
                data = data.replace("inventory", "\"inventory\"")

                # Remove javascript function
                data = data.replace("Math.floor(\"", "\"")
                data = data.replace("\"),", "\"")

                # Add square brackets to make json functions happy
                data = "[" + data + "]"

                filtered_inventory_data = json.loads(data)

                # loop through collected data, populate inventory and store data
                for store_data in filtered_inventory_data:
                    store_data_inventory_dict = {"productID": int(product_id),
                                                 "storeID": int(store_data["uniqueId"]),
                                                 "inventory": int(float(store_data["inventory"]))}

                    self.current_product_inventory_data.append(store_data_inventory_dict)

                    store_data_location_dict = {"city": str(store_data["city"]),
                                                "description": str(store_data["description"]),
                                                "addressOne": str(store_data["addressOne"]),
                                                "addressTwo": str(store_data["addressTwo"]),
                                                "phone": str(store_data["phone"].strip),
                                                "uniqueId": int(store_data["uniqueId"])}

                    self.current_product_store_data.append(store_data_location_dict)
        else:
            print("No inventory data for product ID " + product_id)

        return None

    """
    Writes Product Inventory Page Data to csv - this may be refactor to be placed in Global or a library file in future

    :param integer file_name - Name of file to save too
    :param integer line_number - signals if the csv headers should be written. If first line, then yes. Otherwise no.
    :return null None
    """

    def write_to_file(self, file_name, line_number):
        default_file_path = Global.get_data_directory() + "/" + file_name

        with open(default_file_path, mode='a+', encoding='utf8', newline='\n') as output_file:
            writer = csv.DictWriter(output_file, fieldnames=self.current_product_inventory_data[0].keys())

            if line_number == 1:
                writer.writeheader()

            writer.writerows(self.current_product_inventory_data)

        return None

    def clear_current_data_lists(self):
        self.current_product_inventory_data.clear()
        self.current_product_store_data.clear()

        return None
