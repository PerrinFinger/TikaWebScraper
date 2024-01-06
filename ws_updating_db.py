from project import Session
from fulltest import Product, Store
from ws_first_db import custom_function_list








if __name__ == "__main__":
    session = Session()
    shopify_stores = session.query(Store).filter(Store.shopify == True).all()
    non_shopify_stores = session.query(Store).filter(Store.shopify == False).all()


    for store in shopify_stores:
        store.update_store(session,count = "2")


    for i in range(len(custom_function_list)):
        store = non_shopify_stores[i]
        if store.name != "scientific_sales" and store.name != "electronic_world" and store.name != "marine_deals_ws":
            print(store)
            custom_function_list[i](store,session,True)

        

    session.commit()
    session.close()



    

    print("finished")
        



    
