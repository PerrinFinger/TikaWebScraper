

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
CSVFOLDERNAME = "StoreCSVs/"
JSON_SUFFIX = "products.json?limit=250"
Base = declarative_base()


def find_product_pages(store: Store):
    catogories = store.catogory_dict
    for catogory in catogories:
        for i in range(catogories[catogory]):
            if i > 0:
                catogory = catogory + "?sort=featured&page=" + str(i+1)

            res = requests.get(store.collection_link + "/" + catogory)
            soup  = BeautifulSoup(res.text,"html.parser")
            
            content_wrapper = soup.find("div", class_= "ContentWrapper")
            product_titles = content_wrapper.find_all("div", class_= "ProductDetails")
            for title in product_titles:
                link  = title.find('a').get('href')
                res  = requests.get(link)
                soup  = BeautifulSoup(res.text,"html.parser")

                name = soup.find("meta",property = "og:title")['content']
                product_type = catogory
                product_link = link
                
                brand = soup.find("h5",class_ = "brandName").text
                price = soup.find("meta",property = "product:price:amount")['content']
                external_sku = soup.find("span", class_ = "VariationProductSKU").text.strip()
                print(external_sku)
                instock = soup.find("meta",property = "og:availability")['content']
                if instock == "instock":
                    instock = True
                else:
                    False
                temp_product = Product(name, product_type, product_link, brand, price, external_sku, instock)
                store.products.append(temp_product)


#print(product_info['content'])
        


#print(product_info[-1])
        
weather_station = Store("weather_stations",
                        "weather_station",
                        "https://weatherstation.co.nz/collections/",
                        True,
                        {"full-wireless-weather-stations": 1, "partial-wireless-weather-stations":1,"wifi-enabled-weather-stations":1,"accessories-parts":1})

scientific_sales = Store("weather_stations",
                        "scientific_sales",
                        "https://www.scientificsales.co.nz",
                        False,
                        {"weather-stations/":2})

weather_station.inital_populate(session)
find_product_pages(scientific_sales)
weather_station.find_external_sku_matches(scientific_sales.products)
scientific_sales.export_to_csv(testing = True)