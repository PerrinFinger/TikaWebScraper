from fulltest import Store, Product
from bs4 import BeautifulSoup   
import requests
import json
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from project import Session
import time

session = Session()
def  find_product_pages (store:Store):
    catogories = store.catogory_dict

    for catogory in catogories:

        res = requests.get("https://www.pbtech.co.nz/category/more/homewares")
        soup  = BeautifulSoup(res.text,"html.parser")

        product_titles = soup.findAll("div", class_ = "text-center text-lg-start")
        for title in product_titles:
            link = "https://www.pbtech.co.nz/" + title.find('a').get('href')
            res = requests.get(link)
            soup  = BeautifulSoup(res.text,"html.parser")
            product_info =  soup.findAll('script', {'type': 'application/ld+json'})
            product_info = product_info[1]
            product_info = json.loads(product_info.text)
            product = product_info[1]
            #print(product['offers'][-1])

            name = product['name']
            product_type = catogory
            product_link = link
            brand = product['brand']['name']
            price = product['offers'][0]['price']
            external_sku = product['sku']
            instock = product['offers'][0]['availability']
            if "InStock" in instock:
                instock = True
            else:
                instock = False


            temp_product = Product(name, product_type, product_link, brand, price, external_sku, instock)
            store.products.append(temp_product)

        
weather_station = Store("weather_stations",
                        "weather_station",
                        "https://weatherstation.co.nz/collections/",
                        True,
                        {"full-wireless-weather-stations": 1, "partial-wireless-weather-stations":1,"wifi-enabled-weather-stations":1,"accessories-parts":1})


pb_tech = Store("weather_stations",
                            "pb_tech",
                            "https://www.pbtech.co.nz/category/more/",
                            False,
                            {"homewares":1})


weather_station.inital_populate(session)
find_product_pages(pb_tech)
weather_station.find_external_sku_matches(pb_tech.products)
pb_tech.export_to_csv(testing = True)