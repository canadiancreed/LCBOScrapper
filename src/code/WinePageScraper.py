from ProductInventoryPageScraper import ProductInventoryPageScraper
from ProductPageScraper import ProductPageScraper


class WinePageScraper:

    pps = ProductPageScraper()
    pips = ProductInventoryPageScraper()

    product_id = pps.get_product_data()

    print(pips.get_product_inventory_data(product_id))
