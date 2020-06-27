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
                Global.write_to_log_file("error.log", "Creation of the directory " + path + " failed. {0}".format(err))

        Global.default_path = path

        return None

    @staticmethod
    def write_to_log_file(file_name, data):
        with open(Global.root_data_dir() + Global.current_date + "/" + file_name, "a+") as f:
            f.write(str(data) + '\n')
            f.close()

        return None

    # Prepopulating the array prevents data from being assigned to the wrong column in the csv file.
    # Not the best way probably, but the best for now
    @staticmethod
    def populate_base_inventory_location_data_dict(product_id):

        inventory_data = {"Product Id": product_id}

        with open("../resources/LCBO data/LCBO locations.txt", 'r') as file:
            for line in file:
                inventory_data.update({line.strip(): 0})

        return inventory_data

    """
    Select category dictionary based on startup parameter. Any category thats over 50 pages gets its own entry
    
    :param string dictionary_option-String that will select the key for the requested directory 
    :return dict product_dict-Product dictionary
    """

    @staticmethod
    def product_dict_data(dictionary_option):

        dictionary_products = {
            "WINE": {"WINE": "wine-14"},
            "RED_WINE": {"RED_WINE": "wine-14/red-wine-14001"},
            "WHITE_WINE": {"WHITE_WINE": "wine-14/white-wine-14002"},
            "OTHER_WINE": {"ROSE": "wine-14/ros%C3%A9-wine-14003",
                           "CHAMPAGNE": "wine-14/champagne-14004",
                           "CHAMPAGNE_WHITE": "wine-14/champagne-14004/white-14004001",
                           "CHAMPAGNE_ROSE": "wine-14/champagne-14004/ros%C3%A9-14004002",
                           "SPARKLING": "wine-14/sparkling-wine-14005",
                           "SPARKLING_WHITE": "wine-14/sparkling-wine-14005/white-14005003-1",
                           "SPARKLING_RED": "wine-14/sparkling-wine-14005/ros%C3%A9-red-14005004",
                           "DESERT_WINE": "wine-14/dessert-wine-14006",
                           "DESERT_WHITE": "wine-14/dessert-wine-14006/white-14006005-1",
                           "ICE": "wine-14/icewine-14007",
                           "ICE_WHITE": "wine-14/white-14007007-1",
                           "ICE_RED": "wine-14/red-14007008",
                           "ICE_SPARKLING": "wine-14/sparkling-14007009",
                           "FORTIFIED": "wine-14/fortified-wine",
                           "FORTIFIED_MADEIRA_MARSALA": "wine-14/madeira-marsala-14008010",
                           "FORTIFIED_PORT": "wine-14/port-14008011",
                           "FORTIFIED_SHERRY": "wine-14/sherry-14008012",
                           "FORTIFIED_NEWWORLD": "wine-14/new-world-fortified-14008013",
                           "FORTIFIED_EURO": "wine-14/european-fortified-14008014",
                           "SPECIALTY": "wine-14/specialty-wines-14009",
                           "SPECIALTY_FLAVOURED": "wine-14/flavoured-wine-14009015",
                           "SPECIALTY_FRUIT": "wine-14/fruit-wine-14009016",
                           "SPECIALTY_VERMOUTH": "wine-14/vermouth-aperitif-14009017"},
            "SPIRITS": {"SPIRITS": "spirits-15"},
            "OTHER_SPIRITS": {"BRANDY": "spirits-15/brandy-15011",
                              "COGNAC": "spirits-15/cognac-armagnac-15012",
                              "COGNAC_VS": "spirits-15/cognac-armagnac-15012/vs-15012023",
                              "COGNAC_VSOP": "spirits-15/cognac-armagnac-15012/vsop-15012024",
                              "COGNAC_XO": "spirits-15/cognac-armagnac-15012/xo-15012025",
                              "COGNAC_UNIQUE": "spirits-15/cognac-armagnac-15012/unique-selections-15012026",
                              "EAU_DE_VIE": "spirits-15/eau-de-vie-15013",
                              "EAU_DE_VIE_FRUIT": "spirits-15/eau-de-vie-15013/fruit-spirit-15013028",
                              "GIN": "spirits-15/gin-15014",
                              "GRAPPA": "spirits-15/grappa",
                              "LIQUOR": "spirits-15/liqueur-liquor-15015",
                              "LIQUOR_Aniseed": "spirits-15/liqueur-liquor-15015 / aniseed-15015029",
                              "LIQUOR_Bitters": "spirits-15/liqueur-liquor-15015 / bitters-herbs-15015030",
                              "LIQUOR_Chocolate": "spirits-15/liqueur-liquor-15015 / chocolate-15015031",
                              "LIQUOR_Coffee": "spirits-15/liqueur-liquor-15015 / coffee-15015032",
                              "LIQUOR_Cream": "spirits-15/liqueur-liquor-15015 / cream-15015033",
                              "LIQUOR_Fruit": "spirits-15/liqueur-liquor-15015 / fruit-flavoured-15015034",
                              "LIQUOR_Floral": "spirits-15/liqueur-liquor-15015 / floral-15015035",
                              "LIQUOR_Mint": "spirits-15/liqueur-liquor-15015 / mint-15015036",
                              "LIQUOR_Nut": "spirits-15/liqueur-liquor-15015 / nut-15015037",
                              "LIQUOR_Spice": "spirits-15/liqueur-liquor-15015 / spice-15015038",
                              "LIQUOR_Sweet": "spirits-15/liqueur-liquor-15015 / sweet-flavours-15015039",
                              "RUM": "spirits-15/rum-15016",
                              "RUM_WHITE": "spirits-15/rum-15016 / white-15016040-1",
                              "RUM_Amber": "spirits-15/rum-15016 / amber-15016041",
                              "RUM_Dark": "spirits-15/rum-15016 / dark-15016042",
                              "RUM_Spiced": "spirits-15/rum-15016 / spiced-15016043",
                              "RUM_Flavoured": "spirits-15/rum-15016 / flavoured-15016044",
                              "RUM_Cachaca": "spirits-15/rum-15016 / cachaca-15016045",
                              "SHOCHU": "spirits-15/shochu-soju-15017",
                              "TEQUILLA": "spirits-15/tequila-15018",
                              "TEQUILLA_BLANCO": "spirits-15/tequila-15018 / blanco-15018046",
                              "TEQUILLA_REPOSADO": "spirits-15/tequila-15018 / reposado-15018047",
                              "TEQUILLA_ANEJO": "spirits-15/tequila-15018 / a % C3 % B1ejo-15018048",
                              "TEQUILLA_Mescal": "spirits-15/tequila-15018 / mezcal-15018051",
                              "TEQUILLA_Regular": "spirits-15/tequila-15018 / regular",
                              "VODKA": "spirits-15/vodka-15019",
                              "VODKA_Unflavoured": "spirits-15/vodka-15019 / unflavoured-vodka-15019272",
                              "VODKA_Flavoured": "spirits-15/vodka-15019 / flavoured-vodka-15019052"},
            "WHISKEY": {"WHISKEY": "spirits-15/whisky-whiskey-15020"},
            "OTHER_WHISKEY": {"WHISKEY_Canadian": "spirits-15/whisky-whiskey-15020/canadian-whisky-15020053",
                              "WHISKEY_American": "spirits-15/whisky-whiskey-15020/bourbon-american-whiskey-15020054",
                              "WHISKEY_International": "spirits-15/whisky-whiskey-15020/international-whiskey-15020056",
                              "WHISKEY_Irish": "spirits-15/whisky-whiskey-15020/irish-whiskey-15020057",
                              "WHISKEY_SCOTCH_BLEND": "spirits-15/whisky-whiskey-15020/scotch-whisky-blends-15020058",
                              "WHISKEY_SCOTCH_SINGLE": "spirits-15/whisky-whiskey-15020/scotch-single-malts-15020059",
                              "WHISKEY_SPICED": "spirits-15/whisky-whiskey-15020/spiced-flavoured-15020055-1", },
            "BEER_CIDER": {"BEER_CIDER": "beer-cider-16"},
            "LAGER": {"LAGER": "beer-cider-16/lager-16023",
                      "LAGER_EURO": "beer-cider-16/lager-16023/european-16023286",
                      "LAGER_AMBER": "beer-cider-16/lager-16023/amber-lager-16023299",
                      "LAGER_BOCK": "beer-cider-16/lager-16023/bock-16023072",
                      "LAGER_DARK": "beer-cider-16/lager-16023/dark-lager-16023073",
                      "LAGER_FLAVOURED": "beer-cider-16/lager-16023/flavoured-beer-16023306-1",
                      "LAGER_LIGHT": "beer-cider-16/lager-16023/light-lager-16023300-1",
                      "LAGER_PALE": "beer-cider-16/lager-16023/pale-lager-16023071",
                      "LAGER_PILSNER": "beer-cider-16/lager-16023/pilsner-16023285",
                      "LAGER_SMOKED_BARREL": "beer-cider-16/lager-16023/smoked-barrel-aged-beer-16023307-1",
                      "LAGER_STRONG": "beer-cider-16/lager-16023/strong-lager-16023302-1"},
            "ALE_HYBRID": {"ALE": "beer-cider-16/ale-16022",
                           "ALE_AMERICAN": "beer-cider-16/ale-16022/american-pale-ale-16022287",
                           "ALE_BELGIAN": "beer-cider-16/ale-16022/belgian-ale-16022064",
                           "ALE_BELGIAN_STRONG": "beer-cider-16/ale-16022/belgian-strong-ale-16022288",
                           "ALE_BROWN": "beer-cider-16/ale-16022/brown-ale-16022289",
                           "ALE_FLAVOURED": "beer-cider-16/ale-16022/flavoured-beer-16022290",
                           "ALE_IPA": "beer-cider-16/ale-16022/india-pale-ale-%28ipa%29-16022066",
                           "ALE_PALE": "beer-cider-16/ale-16022/pale-ale-16022065",
                           "ALE_PORTER": "ale-16022/porter-16022062",
                           "ALE_SCOT_IRISH": "ale-16022/scottish-irish-ale-16022292",
                           "ALE_SOUR": "ale-16022/sour-16022061",
                           "ALE_STOUT": "ale-16022/stout-16022063",
                           "ALE_WHEAT": "ale-16022/wheat-16022060",
                           "HYBRID": "beer-cider-16/hybrid-16024",
                           "HYBRID_AMBER": "beer-cider-16/hybrid-16024/amber-hybrid-beer-16024297",
                           "HYBRID_PALE": "beer-cider-16/hybrid-16024/pale-hybrid-beer-16024305-1",
                           "HYBRID_ALTBIER": "beer-cider-16/hybrid-16024/altbier-16024075"},
            "OTHER": {"SPECIALTY": "beer-cider-16/specialty-16025",
                      "SPECIALTY_SAKE": "beer-cider-16/specialty-16025/sake-rice-wine-16025078",
                      "SPECIALTY_MEAD": "beer-cider-16/specialty-16025/mead-16025079",
                      "SPECIALTY_NON_ALCOHOLIC": "beer-cider-16/specialty-16025/non-alcohol-16025318",
                      "SPECIALTY_GLUTEN": "beer-cider-16/specialty-16025/gluten-free-16025319",
                      "SPECIALTY_BELGIAN": "beer-cider-16/specialty-16025/belgian",
                      "CIDER": "beer-cider-16/cider-16028",
                      "CIDER_TRADITIONAL": "beer-cider-16/cider-16028/traditional-cider-16028081",
                      "CIDER_FLAVOURED": "beer-cider-16/cider-16028/flavoured-cider-16028082",
                      "CIDER_MIXED": "beer-cider-16/cider-16028/mixed-%28flavoured-traditional%29-16028279",
                      "CIDER_MIXED_PACK": "beer-cider-16/cider-16028/mixed-pack-%28cider-flavoured-cider%29-16028280",
                      "CIDER_CIDER": "beer-cider-16/cider-16028/cider-16028309-1",
                      "RADLER_SHANDY": "beer-cider-16/radler-shandy-16117",
                      "RADLER_SHANDY_RADLER": "beer-cider-16/radler-shandy-16117/radler-16117303-1",
                      "RADLER_SHANDY_SHANDY": "beer-cider-16/radler-shandy-16117/shandy-16117304-1",
                      "COOLERS": "coolers-18-1",
                      "COOLERS_BASE": "coolers-18-1/coolers-18029",
                      "COOLERS_SELTZER": "coolers-18-1/coolers-18029/seltzers",
                      "COOLERS_CAESARS": "coolers-18-1/coolers-18029/caesars",
                      "COOLERS_TEAS": "coolers-18-1/coolers-18029/teas",
                      "COOLERS_COCKTAILS": "coolers-18-1/coolers-18029/cocktails",
                      "COOLERS_TRADITIONAL": "coolers-18-1/coolers-18029/traditional",
                      "COOLERS_SODA": "coolers-18-1/coolers-18029/sodas",
                      "COOLERS_CREAM": "coolers-18-1/coolers-18029/creams",
                      "COOLERS_NICHE": "coolers-18-1/coolers-18029/niche",
                      "COOLERS_LARGE_PACKS": "coolers-18-1/coolers-18029/large-packs",
                      "COOLERS_FROZEN": "coolers-18-1/coolers-18029/frozen-pouches",
                      "COOLERS_LIGHT": "coolers-18-1/coolers-18029/light",
                      "COOLERS_WINE": "coolers-18-1/coolers-18029/wine-inspired",
                      "PREMIXED_COCKTAILS": "coolers-18-1/premixed-cocktails-18030",
                      "PREMIXED_COCKTAILS_CITRUS": "coolers-18-1/premixed-cocktails-18030/citrus-18030094-1",
                      "PREMIXED_COCKTAILS_SHOTS": "coolers-18-1/premixed-cocktails-18030/shots",
                      "PREMIXED_COCKTAILS_PREMIXED": "coolers-18-1/premixed-cocktails-18030/premixed"}
        }

        product_dict = dictionary_products.get(dictionary_option, "Invalid month")

        return product_dict
