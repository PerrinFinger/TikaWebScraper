from fulltest import Store, Product
from bs4 import BeautifulSoup   
import requests
import json
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from project import Session, engine

CSVFOLDERNAME = "StoreCSVs/"
JSON_SUFFIX = "products.json?limit=250"



def update(store:Store):
    links = find_product_pages(store)
    return



def find_product_pages(store: Store):
    catogories = store.catogory_dict
    catogory_links = {}
    for catogory in catogories:
        catogory_link = []
        #print(store.collection_link + "/" + catogory)
        response = requests.get(store.collection_link + "/" + catogory)
        soup = BeautifulSoup(response.text, "html.parser")
        product_titles = soup.find_all("h5", class_="mx-2 mx-md-0 py-2 uppercase text-center")
        

        if len(product_titles) == 0:
            product_titles = soup.find_all("div", class_="product-content-wrap top")
            for title in product_titles:
                product_link = title.find("a")
                catogory_link.append(product_link.get("href"))

        else:
           
            for title in product_titles:
                product_link = title.find("a")
                temp = product_link.get("href")
                #print(temp)
                temp_req = requests.get(temp)
                temp_soup = BeautifulSoup(temp_req.text, "html.parser")
                temp_soup = temp_soup.find_all("div", class_ = "button wp-element-button product_type_variable add_to_cart_button add")
                #print(temp_soup)
                if len(temp_soup) != 0:
                    for link in temp_soup:
                        catogory_link.append(link.get("href"))
                else:
                    catogory_link.append(temp)

        catogory_links[catogory] = catogory_link
    return catogory_links



def scrape_product_pages(product_links: dict, store: Store):
    for cat in product_links:
        print(cat)
        print(product_links[cat])
        for link in product_links[cat]:
            #print(link)
            print(link)

            l = requests.get(link)
            print(l)
            soup = BeautifulSoup(l.text, "html.parser")


            name = soup.find("h1", class_ = "product_title entry-title title-detail")

            if name:
                name = name.text.strip()
            else:
                print("passing")  # need to figure out how to handle this / how it relates to the find products function !!

            #print(name)
            form  = soup.find("form", class_ = "variations_form cart")
            #print("Test")
            if form:
                product_creator(form, store, cat, link, name)

            else:
                # print("cart bundled_item_cart_content variations_form")
                #form = soup.find_all("div",class_ = "details")
                print(link)
                

                # form = soup.find_all("form", class_ = "cart cart_group bundle_form layout_default group_mode_parent")
                # form2 = form[0].find_all("div", class_ = "details")
                # print(type(form2))
                # print(len(form2))
                # print(form2[1])
                #product_creator(form, store, cat, link, name)
                # <span class="sku text-brand">MA 110</span>
              

            #print(form)
    return

def product_creator(form: str, store: Store, cat: str, link: str, name: str ):
        data = form['data-product_variations']
        data = json.loads(data)
        name_prefix = name
        for d in data:
            product_type = cat 
            product_link = link
            brand = "Ocean South"
            price = d['display_price']
            external_sku = d['sku']
            instock = d['is_in_stock']

            name = ""
            t = list(d['attributes'].values())
            name += " ("
            for i in range(len(t)):
                name += t[i] + " "
            name += ")"
            temp_product = Product(name_prefix + name, product_type, product_link, brand, price, external_sku, instock)
            name = ""
            
                
            #temp_product.set_varration_dict(d['attributes'])
            store.products.append(temp_product)

        return



if __name__ == "__main__":
    session = Session()
    stores = [
        Store("covers",
                            "coversystems",
                            "https://coversystems.co.nz/collections/",
                            True,
                            {"marine-covers": 2, "bimini-tops": 1, "t-tops": 1, "rocket-launchers": 1, "rv-caravan-covers":1}),

        Store("covers",
                    "ocean_south",
                    "https://oceansouth.co.nz/product-category",
                    False,
                    {"boat-covers/style-to-fit": 1, "boat-covers/inflatable-covers": 1, "biminis/aluminum-biminis": 1, "sailboat-bimini-tops": 1,
                     "biminis/bimini-extension-kit": 1, "rocket-launchers-boat-arches/boat-arches": 1, "t-tops-boat-tops/t-tops": 1, 
                     "t-tops-boat-tops/shade-extensions": 1, "t-tops-boat-tops/t-top-enclosures": 1})
    ]

    for store in stores:
        if store.shopify:
            pass
            # store.inital_populate(session)
            # session.add(store)

            # if store.name == "coversystems":
            #     for product in store.products:
            #         product.set_internal_sku(product.external_sku)
            
        else:
            scrape_product_pages(find_product_pages(store),store)
            session.add(store)
            




    session.commit()
    session.close()

















    # temp = find_product_pages(ocean_south)
    # scrape_product_pages(temp, ocean_south)

    # cover_systems.inital_populate(session)
    # cover_systems.find_external_sku_matches(ocean_south.products)
    # cover_systems.set_tika_internal_sku()

    # ocean_south.export_to_csv(testing=True)
    # cover_systems.export_to_csv(testing=True)


    # session.add_all(cover_systems.products)
    # session.add_all(ocean_south.products)
    # session.add(cover_systems)
    # session.add(ocean_south)
    # session.commit()

    # #cover_systems.find_external_sku_matches(session)

    # print("finshed")