import sys

from Global import Global
from Scrappers.ProductInventoryPageScraper import ProductInventoryPageScraper
from Scrappers.ProductPageScraper import ProductPageScraper
from Scrappers.ProductsPageScrapper import ProductsPageScraper


class Application:

    # First check if a category has been passed by the command line to process. If not, close.
    if len(sys.argv) > 1:
        category = sys.argv[1]
    else:
        sys.exit(1)

    psps = ProductsPageScraper()
    pps  = ProductPageScraper()
    pips = ProductInventoryPageScraper()

    # Sets data directory that we'll save everything too. Avoids script failure when script is run past midnight
    Global.set_current_date()

    # Get category contents. We do this so we can split the load across multiple shell instances. If input is invalid,
    # close and log an error
    product_dict_data = Global.product_dict_data(category)

    if product_dict_data == "Invalid month":
        print("Category " + category + " not found. Exiting")
        # Directory doesn't exist. Comment out code for now.
        #Global.write_to_log_file("main.log", "Category " + category + " not found. Exiting")
        sys.exit(1)

    # Loop through all products of specified family
    for description, product_category in product_dict_data.items():

        # Create data directory
        Global.create_data_directory(description)

        # Get URLs for all product in category
        product_urls = psps.collect_products_urls(product_category)

        # Gets product data for specific item
        for idx, product_url in enumerate(product_urls, start=1):
            product_id = pps.get_product_data(product_url)

            pps.write_to_file("product.csv", idx)

            pips.get_product_inventory_data(product_id)

            pips.write_to_file("inventory.csv", idx)

            Global.write_to_log_file("main.log", "Inventory and data for product " + str(idx) + " processed")

        Global.write_to_log_file("main.log", "Product and Inventory data for " + description + " complete")

        Global.write_to_log_file("main.log", "Product and Inventory data for " + description + " complete")

    # We'll need this or else you'll have zombie processes
    sys.exit(0)
