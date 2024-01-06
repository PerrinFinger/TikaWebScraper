
from flask import session
from fulltest import Product, Store
from bs4 import BeautifulSoup   
import requests
import json
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

import time

from project import Session

CSVFOLDERNAME = "TestingData/CSVs"
JSON_SUFFIX = "products.json?limit=250"
Base = declarative_base()
session = Session()


def find_product_pages(store: Store):
    catogories = store.catogory_dict
    for catogory in catogories:
        browser=webdriver.Chrome()
        browser.get(store.collection_link + "/" + catogory)

        for i in range(3):
            browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(3)
            clickable = browser.find_element(By.CLASS_NAME,"load-next")
            time.sleep(3)
            ActionChains(browser).click(clickable).perform()

        print("WORKS")
        page_source = browser.page_source
        soup  = BeautifulSoup(page_source, "html.parser")

        product_titles = soup.find_all("article",class_ = "product-card show-msg")

        for title in product_titles:

            
            product_link = title.find('a').get('href')
            browser.get(product_link)
            time.sleep(1)
            #print(product_link)

            #res = requests.get(product_link)
            res  = browser.page_source
            soup = BeautifulSoup(res,'html.parser')
            
            #head = soup.find('head')
            #print(head)
            #product_info = head.find('script', {'type': 'application/ld+json'})
            product_info = soup.find('script', {'type': 'application/ld+json'})
        

            product = json.loads(product_info.text)
            #product = json.loads(product_info[0].text)

            name = product['name']
            product_type = catogory
            
            brand = product['brand']['name']
            price = product['offers']['price']
            external_sku = product['sku']

            instock = product['offers']['availability']
            if "InStock" in instock:
                instock = True
            else:
                instock = False


            temp_product = Product(name, product_type, product_link, brand, price, external_sku, instock)
            store.products.append(temp_product)
            



        # print(len(product_titles))
        # print(product_titles[0].find('a').get('href'))


        

    return

weather_station = Store("weather_stations",
                        "weather_station",
                        "https://weatherstation.co.nz/collections/",
                        True,
                        {"full-wireless-weather-stations": 1, "partial-wireless-weather-stations":1,"wifi-enabled-weather-stations":1,"accessories-parts":1})




electronic_world = Store("weather_stations",
                        "electronic_world",
                        "https://www.electronicworld.co.nz/shop",
                        False,
                        {"weather-station": 1})

weather_station.inital_populate(session)
find_product_pages(electronic_world)
weather_station.find_external_sku_matches(electronic_world.products)
electronic_world.export_to_csv(testing = True)




