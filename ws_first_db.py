from project import Session
from fulltest import Product, Store
from bs4 import BeautifulSoup  
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time


def ss_find_product_pages(store: Store,session,update=False,):
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

                name = soup.find("meta",property = "og:title")['content'].strip()
                product_type = catogory
                product_link = link
                brand = soup.find("h5",class_ = "brandName").text
                price = soup.find("meta",property = "product:price:amount")['content']
                external_sku = soup.find("span", class_ = "VariationProductSKU").text.strip()
                instock = soup.find("meta",property = "og:availability")['content']
                if instock == "instock":
                    instock = True
                else:
                    False

                if update:
                    temp = store.get_product_by_external_sku(external_sku,name)
                    if temp:
                        temp.update_price(price,testing=True)
                        temp.update_instock(instock,session)

                else:
                    temp_product = Product(name, product_type, product_link, brand, price, external_sku, instock)
                    store.products.append(temp_product)


def  pb_find_product_pages (store:Store,session,update=False):
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

            if update:
                temp = store.get_product_by_external_sku(external_sku,name)
                if temp:
                    temp.update_price(price,testing=True)
                    temp.update_instock(instock,session)
                else:
                    print("product not found!!!!!!")

            else:
                temp_product = Product(name, product_type, product_link, brand, price, external_sku, instock)
                store.products.append(temp_product)



def ew_find_product_pages(store: Store,session,update=False):
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

            if update:
                temp = store.get_product_by_external_sku(external_sku,name)
                if temp:
                    temp.update_price(price,testing=True)
                    temp.update_instock(instock,session)

            else:
                temp_product = Product(name, product_type, product_link, brand, price, external_sku, instock)
                store.products.append(temp_product)
            session.commit()

    return

def md_find_product_pages(store: Store,session,update=False):

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
            if update:
                print("TTTTT")
                temp = store.get_product_by_external_sku(external_sku,name.strip())
                print(temp)
                if temp:
                    temp.update_price(price,testing=True)
                    temp.update_instock(instock,session)
                    session.commit()
            else:
                temp_product = Product(name, product_type, product_link, brand, price, external_sku, instock)
                store.products.append(temp_product)

        browser.close()
    return

custom_function_list = [ss_find_product_pages,pb_find_product_pages,ew_find_product_pages,md_find_product_pages]

if __name__ == "__main__":
    #Base.metadata.create_all(engine) can just run full test I think 
    session = Session()
    csv_prefix =  "C:/Users/GGPC/sqlalchemytesting/Data/StoreCSVs/Final_CSV's/WeatherStations/"
    csv_suffix = " Matched.csv"
    #custom_function_list = [ss_find_product_pages,pb_find_product_pages,ew_find_product_pages,md_find_product_pages]

    weather_station_stores_shopify = [

        # Weather_Stations (Tika)
         Store("weather_stations",
                        "weather_station",
                        "https://weatherstation.co.nz/collections/",
                        True,
                        {"full-wireless-weather-stations": 1, "partial-wireless-weather-stations":1,"wifi-enabled-weather-stations":1,"accessories-parts":1}),

        # Jacobs
        Store("weather_stations",
              "jacobs_ws",
              "https://www.jacobsdigital.co.nz/collections/",
              True,
              {"weather-stations":1})
              
    ]
    weather_station_stores_no_shopify = [
    


        # Scientific Sales
        Store("weather_stations",
                        "scientific_sales",
                        "https://www.scientificsales.co.nz",
                        False,
                        {"weather-stations/":2}),

        # Pbtech
        Store("weather_stations",
                            "pb_tech",
                            "https://www.pbtech.co.nz/category/more/",
                            False,
                            {"homewares":1}),

        # Electronic World        
        Store("weather_stations",
                                "electronic_world",
                                "https://www.electronicworld.co.nz/shop",
                                False,
                                {"weather-station": 1}),

        # Marine Deals 
         Store("weather_stations",
                            "marine_deals_ws",
                            "https://www.marine-deals.co.nz/marine-electronics/wireless-weather-station",
                            False,
                            {"weather-stations":1,"weather-station-sensors":1,"weather-station-accessories":1})

    ]


    for store in weather_station_stores_shopify:
                
        store.inital_populate(session)
        session.add(store)
        if store.name != 'weather_station':
            store.import_from_csv(csv_prefix + store.name + csv_suffix )

        else:
            for product in store.products:
                product.set_internal_sku(product.external_sku)


    for i in range(len(weather_station_stores_no_shopify)): # 1 for now 
        store = weather_station_stores_no_shopify[i]
        custom_function_list[i](store,session)
        session.add(store)
        store.import_from_csv(csv_prefix + store.name + csv_suffix ) #adding now 
       


    session.commit()
    session.close()















