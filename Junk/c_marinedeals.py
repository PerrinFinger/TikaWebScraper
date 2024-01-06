from fulltest import Store, Product
from bs4 import BeautifulSoup   
import requests
import json
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from selenium import webdriver
import time

from project import Session

CSVFOLDERNAME = "StoreCSVs/"
JSON_SUFFIX = "products.json?limit=250"
Base = declarative_base()
session = Session()



def find_product_pages(store: Store):
    catogories = store.catogory_dict
    for catogory in catogories:
        browser=webdriver.Chrome()
        browser.get(store.collection_link + "/" + catogory)

        for i in range(6):
            browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(3)
        page_source = browser.page_source


        soup  = BeautifulSoup(page_source, "html.parser")
        names = soup.find_all("h2",  class_ = "product-name")

        for name in names:
            name = name.find("a")
            product_type = catogory
            product_link  = name.get('href')
            print(product_link)
            product_page = requests.get(product_link)
            soup  = BeautifulSoup(product_page.text, "html.parser")
            #product_script = soup.find("div",class_= "trustspot trustspot-main-widget")
            #print(product_script)
            product_info = soup.find('script', {'type': 'application/ld+json'})
            print(product_info)

            product = json.loads(product_info.text)
            name = product['name']
            
            brand = product['brand']['name']
            price = product['offers']['price']
            external_sku = product['sku']

            instock = product['offers']['availability']
            if "InStock" in instock:
                instock = True
            else:
                instock = False
            print(instock)
            temp_product = Product(name, product_type, product_link, brand, price, external_sku, instock)
            store.products.append(temp_product)

        browser.close()

    return

weather_station = Store("weather_stations",
                        "weather_station",
                        "https://weatherstation.co.nz/collections/",
                        True,
                        {"full-wireless-weather-stations": 1, "partial-wireless-weather-stations":1,"wifi-enabled-weather-stations":1,"accessories-parts":1})


marine_deals_ws = Store("weather_stations",
                            "marine_deals_ws",
                            "https://www.marine-deals.co.nz/marine-electronics/wireless-weather-station",
                            False,
                            {"weather-stations":1,"weather-station-sensors":1,"weather-station-accessories":1})


weather_station.inital_populate(session)
find_product_pages(marine_deals_ws)

weather_station.find_external_sku_matches(marine_deals_ws.products)
marine_deals_ws.export_to_csv(testing=True)


