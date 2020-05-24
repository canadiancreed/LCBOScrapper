import csv
import os
from datetime import datetime

###
# All functionality that is application wide in scope
###

class Global:
    default_path = ""

    current_date = ""

    @staticmethod
    def base_url():
        return "https://www.lcbo.com/webapp/wcs/stores/servlet/en/lcbo/"

    @staticmethod
    def url_headers():
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"

    @staticmethod
    def root_data_dir():
        return "../../data/"

    @staticmethod
    def get_data_directory():
        return Global.default_path

    @staticmethod
    def set_current_date():
        Global.current_date = datetime.today().strftime('%Y-%m-%d')

    @staticmethod
    def create_data_directory(product_name):

        path = Global.root_data_dir() + Global.current_date + "/" + product_name

        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except OSError as err:
                print("Creation of the directory " + path + " failed. {0}".format(err))

        Global.default_path = path

        return None

    @staticmethod
    def write_to_log_file(file_name, data):
        f = open(Global.root_data_dir() + Global.current_date + "/" + file_name, "a+")
        f.write(data + '\n')
        f.close()

        return None

    @staticmethod
    def product_dict_data():

        product_dict = {}

        # Load txt file with catorgies names, throw into dict
        with open("../resources/LCBO categories.csv", 'r') as file:
            for row in csv.reader(file):
                product_dict.update({row[0]:row[1]})

        return product_dict

    # Prepopulating the array prevents data from being assigned to the wrong column in the csv file.
    # Not the best way probably, but the best for now
    @staticmethod
    def populate_base_inventory_location_data_dict(product_id):

        inventory_data = {"Product Id":product_id}

        with open("../resources/LCBO locations.txt", 'r') as file:
            for line in file:
                inventory_data.update({line.strip():0})

        return inventory_data
