from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy import Column, String, Integer, Float, Table, ForeignKey, Boolean, PickleType, DateTime
from sqlalchemy.ext.mutable import MutableList,MutableDict
import csv
import os 
import datetime
import requests
import json
from project import Session, engine
from sqlalchemy import and_, or_

CSVFOLDERNAME = "Data/StoreCSVs/" # Change this 
TESTINGCSVFOLDERNAME = "TestingData/CSVs/"

JSON_SUFFIX = "products.json?limit=250"
Base = declarative_base()



class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    varration_dict = Column(MutableDict.as_mutable(PickleType))
    product_type = Column(String)
    product_link = Column(String)
    brand = Column(String)

    price = Column(Float)
    price_history = Column(MutableList.as_mutable(PickleType),
                                    default=[])
    price_change = Column(Boolean)

    instock = Column(Boolean)
    instock_change = Column(Boolean)

    external_sku = Column(String)
    internal_sku = Column(String,default="0")
    simular_sku = Column(String,default="0")
    #tracked = Column(Boolean, default=False)
    tracked = Column(String,default="FALSE")
    store_id = Column(Integer, ForeignKey('stores.id'))

    #simular_products = relationship("SimularProduct")  To be added later 

    def __init__(self, name: str,product_type: str,product_link: str,brand: str, price: float, external_sku: str,instock: bool):
        self.name = name
        self.product_type = product_type
        self.product_link = product_link
        self.brand = brand
        self.price = price
        self.external_sku = external_sku
        self.instock = instock
        self.price_history = [[datetime.date.today(),price]]
        self.price_change = False
        self.instock_change = False

    def __repr__(self):
        return "<Product('%s','%s', '%s', '%s','%s','%s')>" % (self.name, self.price,self.external_sku, self.internal_sku ,self.simular_sku,self.tracked) # might need to change this back 
    
    def price_change_str(self):
        return "Name:{}<br> Price:{} <br> Prev Price:{}<br><br>".format(self.name,self.price,self.price_history[-2][1])
    
    def stock_change_str(self):
        return "Name: {} Now instock =  {} <br>".format(self.name,self.instock)
    
    def set_varration_dict(self, varration_dict: dict):
        self.varration_dict = varration_dict 


    def set_internal_sku(self, internal_sku: str):
        self.internal_sku = internal_sku

    def set_tracked(self, tracked: str):
        self.tracked = tracked 

    def set_simular_sku(self,sku:str):
        self.simular_sku = sku


    def update_price(self, price: float,testing=False):
        
        if float(self.price) != float(price):
            
            print([self.price,price,self.price_change,self.external_sku])
            self.price_history.append([datetime.date.today(), price])
            self.price = float(price)
            self.price_change = True
            #print("pricechange")

        else:
            if self.price_change == True:
                print("Should be channging from true to false")
            self.price_change = False


        #session.commit()

    def update_instock(self, instock: str, session):
        if self.instock != instock:
            self.instock = instock
            self.instock_change = True
        else:
            self.instock_change = False
        #session.commit()

    def compare_price(self, price):
        if self.price != price:
            self.update_price(price)
            return True #### ?????
        else:
            self.price_change = False
            return False #### ?????
        
    def compare_instock(self, instock):
        if self.instock != instock:
            self.update_instock(instock)
            return True
        else:
            self.instock_change = False
            return False
        




class Store(Base):
    __tablename__ = 'stores'
    id = Column(Integer, primary_key=True)
    shop_type = Column(String)
    name = Column(String)
    collection_link = Column(String)
    catogory_dict = Column(MutableDict.as_mutable(PickleType),default={})
    shopify = Column(Boolean)
    

    products = relationship("Product")
    
    def __init__(self,shop_type,name,collection_link,shopify,catogory_dict):
        self.shop_type = shop_type
        self.name = name
        self.collection_link = collection_link
        self.shopify = shopify
        self.catogory_dict = catogory_dict
        


    def __repr__(self):
        return "<Store('%s')>" % (self.name)
    
    def get_product_by_external_sku(self, external_sku: str, name: str):
# have added a additional check that the name of the prouduct to allow for the fact that some sites have duplicate external skus 

        for product in self.products:
            if product.external_sku == external_sku and product.name == name:
                return product
        return None
    
# Check this 
    def find_external_sku_matches(self, other_stores_products: list[Product]):
        for product in self.products: # Note that this is only going to be run through the tika owned stores 
            for other_product in other_stores_products:
                if product.external_sku == other_product.external_sku:
                    print("Yes")
                    product.set_internal_sku(product.external_sku)
                    other_product.set_internal_sku(product.external_sku)
                    break


    def set_tika_internal_sku(self):
        for product in self.products:
            product.set_internal_sku(product.external_sku)
    

    

    def export_to_csv(self,testing):
        if testing == True:
            temp = TESTINGCSVFOLDERNAME
        else:
            temp = CSVFOLDERNAME

        with open(temp + self.name +'.csv', 'w', newline='', encoding='utf-8') as f:
            print("Working")
            writer = csv.writer(f)
            if self.shop_type != "covers":
                writer.writerow(['type','brand','name', 'price', 'external_sku', 'internal_sku',"simular_sku","tracked_sku"])

                for product in self.products:
                    writer.writerow([product.product_type,product.brand,product.name, product.price, product.external_sku,product.internal_sku,product.simular_sku,product.tracked])
            else:
                 writer.writerow(['type','brand','varations','name', 'price', 'external_sku', 'internal_sku',"simular_sku","tracked_sku"])

                 for product in self.products:
                    writer.writerow([product.product_type,product.brand,product.varration_dict,product.name, product.price, product.external_sku,product.internal_sku,product.simular_sku,product.tracked])


# Updates product objects with manualy matched skus 
    def import_from_csv(self, filename: str):
        with open(filename, newline='',errors="ignore") as csvfile:
            readCSV = csv.DictReader(csvfile)
            for row in readCSV:
                product = self.get_product_by_external_sku(row["external_sku"].strip(),row["name"].strip())
                if product:
                    
                    product.set_internal_sku(row["internal_sku"])
                    product.set_tracked(row["tracked_sku"])
                    product.set_simular_sku(row["simular_sku"])
                    
                    # Testing only ?
                    org_price = product.price
                    new_price = row["price"]
                    product.update_price(new_price)
                    
                    # Can't be done because the matched csv files don't include instock

                    # org_stock = product.instock
                    # new_stock = row["instock"]
                    # product.update_instock(new_stock)
                    product.instock_change = False

                # else:
                #     pass
                    # Are these an issue ? 
                    #print("Product not found")
                    #print(row)
                    #print(row["external_sku"])




    ############## New stuff #####################
    def inital_populate(self,session):
        for key in self.catogory_dict:
            if self.shopify and self.shop_type != "covers":
                self.scrape_collection_json(self.collection_link + key +"/"+ JSON_SUFFIX,self.collection_link + key + "products/",key,session)
            elif self.shopify and self.shop_type == "covers":
                self.scrape_collection_json_covers(self.collection_link + key +"/"+ JSON_SUFFIX,self.collection_link + key + "products/",key,session)
                print("COVERS!!!!!!!!!!!!!!!WOOOOOOOOOOOOOOOOOO")
            else:
                return NotImplemented
            





    def scrape_collection_json_covers(self, page_link: str,product_baselink: str,catogory: str, session):
        req = requests.get(page_link)
        data = req.json()
        for product in data['products']:
            name = product['title']
            brand = product['vendor']
            product_type = catogory
            product_link = product_baselink + product['handle']
            varraints = product['variants']
            #print(varraints)

            for i in range(len(varraints)):
                temp_dict = varraints[i]
                price = temp_dict['price']
                in_stock = temp_dict['available']
                external_sku = temp_dict['sku']
                temp_product = Product(name,product_type,product_link,brand,price,external_sku,in_stock)
                temp_product.name += " (" + temp_dict['title'] + ")"
                # var_dict = {}
                # var_dict['title'] = temp_dict['title']
                # temp_product.set_varration_dict(var_dict)
                self.products.append(temp_product)

            if len(data['products']) == 250:
                self.scrape_collection_json(page_link + "&page=2",product_baselink,catogory,session)



    def scrape_collection_json(self, page_link: str,product_baselink: str,catogory: str, session, count = 1, page_indentifier = ''):
        req = requests.get(page_link + page_indentifier)
        data = req.json()
        for product in data['products']:
            
            name = product['title']
            product_type = catogory
            product_link = product_baselink + product['handle']
            brand = product['vendor']
            price = float(product['variants'][0]['price'])
            
            #tags = product['tags']
            external_sku = product['variants'][0]['sku'].strip()
            in_stock = product['variants'][0]['available']

            if len(external_sku) > 1:
                temp_product = Product(name,product_type,product_link,brand,price,external_sku,in_stock)
                self.products.append(temp_product)
    

        if len(data['products']) == 250:
            count += 1 
            page_indentifier = "&page=" + str(count)
            self.scrape_collection_json(page_link ,product_baselink,catogory,session,count, page_indentifier)




        


    # def scrape_collection_json_covers_update(self, page_link: str,product_baselink: str,catogory: str, session):
    #     req = requests.get(page_link)
    #     data = req.json()
    #     print("YES")
    #     for product in data['products']:
    #         varraints = product['variants']
    #         for var in varraints:
    #             price = var['price']
    #             in_stock = var['available']
    #             external_sku = var['sku']
                    
    #             temp_product = session.query(Product).filter(
    #         and_ (or_(Product.internal_sku != "0",
    #         Product.tracked != "FALSE",
    #         Product.simular_sku != "0"),
    #         Product.external_sku == external_sku)
    #     ).all()
        

    #         if len(temp_product) != 1:
    #             print("NotWorking")
    #         else:
    #             temp_product = session.query(Product).filter(Product.external_sku == external_sku).first()
    #             temp_product.compare_price(price)
    #             temp_product.compare_instock(in_stock)
    #             #session.commit()



    #     if len(data['products']) == 250:
    #             self.scrape_collection_json(page_link + "&page=2",product_baselink,catogory,session)
            




    def update_store(self,session,count):
        for key in self.catogory_dict:
            if self.shopify and self.shop_type != "covers":
                self.scrape_collection_json_update(self.collection_link + key +"/"+ JSON_SUFFIX,self.collection_link + key + "products/",key,session,count)
            
            elif self.shopify and self.shop_type == "covers":
                self.scrape_collection_json_covers_update(self.collection_link + key +"/"+ JSON_SUFFIX,self.collection_link + key + "products/",key,session)
            
            else:
                return NotImplemented




    def scrape_collection_json_update(self, page_link: str,product_baselink: str,catogory: str, session,store_id, count = 1, page_indentifier = ""):

    # break down the begining of the two functions into a seperate function 
            #store_id = session.query(Store)
            req = requests.get(page_link + page_indentifier)
            data = req.json()

            for product in data['products']:
                external_sku = product['variants'][0]['sku'].strip()
                price = float(product['variants'][0]['price'])
                instock = product['variants'][0]['available']

                temp_product = self.get_product_by_external_sku(external_sku,product['title'].strip())
                
                if not temp_product:
                    print("No temp product")
                    pass
                else:
                    temp_product.update_price(price,testing=True)
                    temp_product.update_instock(instock,session)
                    
                    # Do I need this here ? 
                    session.commit()

                    
                
            if len(data['products']) == 250:
                count += 1 
                page_indentifier = "&page=" + str(count)
                self.scrape_collection_json_update(page_link + "&page=" + str(count),product_baselink,catogory,session,store_id,count, page_indentifier)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
