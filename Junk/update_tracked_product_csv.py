from project import Session
from fulltest import Product, Store
from sqlalchemy import and_, or_
import csv

grouping_csv_file_prefix = "TestingData/CSVs/"


def test_traked_groupings(product_groupings:list, tracked_groupings: list, optics_stores_products_length:int,multipule_sku_values):
    total_products_grouped = 0
    
    for group in product_groupings:
        total_products_grouped += (len(group) - 1)
        print((len(group)-1))
    print("product_groupings=")
    print(total_products_grouped)
    total_products_grouped += len(tracked_groupings)
    print(optics_stores_products_length - (total_products_grouped))

    return (optics_stores_products_length - (total_products_grouped - multipule_sku_values)) == 0

def create_grouping_csv(product_groupings:list[list[Product]], tracked_groupings: list, table_type: str):
     with open(grouping_csv_file_prefix + table_type + 'product_groupings' +'.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['store1','name1', 'price2','store2','name2', 'price2','store3','name3', 'price3','store4','name4', 'price4',])

            for group in product_groupings:
                writer.writerow([(x.store_id,x.name,x.price) for x in group])

     print("DONE??")


    

if __name__ == "__main__":
    session = Session()
    final_product_groupings = []
    final_tracked_product_list = []
    optics_stores =  optics_stores = session.query(Store).all()

    store_id_name_dict = {}
    for store in optics_stores:
        store_id_name_dict[store.id] = store.name
    
    telescopesnz = optics_stores.pop(0)
    telescopesnz_products = telescopesnz.products
    telescopesnz_products.sort(key=lambda x:x.internal_sku)
    print(type(telescopesnz_products[0].store_id))


    optics_stores_products = session.query(Product).filter(
             and_ (
                 or_(
                 Product.tracked != "FALSE",
             
             and_(Product.simular_sku != "0",
             Product.simular_sku != ""),
             
             and_(Product.internal_sku != "",
                  Product.internal_sku != "0")),
             Product.store_id != 1 )
         ).all()
    multipule_sku_values = 0
    for product in optics_stores_products:
        if product.internal_sku != "0" and product.internal_sku != "" and product.simular_sku != "0" and product.simular_sku != "": # check why there are still empty strings here 
            #print((product.internal_sku,product.simular_sku))
            multipule_sku_values += 1

    print(multipule_sku_values)

    optics_stores_products.sort(key=lambda x:x.internal_sku) #??
    
    for product in telescopesnz_products:
        temp_list = [product]
        temp_internal_sku = product.internal_sku
        count = 0

        for product in optics_stores_products:
            if optics_stores_products[count].internal_sku == temp_internal_sku or optics_stores_products[count].simular_sku == temp_internal_sku:
                temp_list.append(optics_stores_products[count])
                count += 1
            else:
                count += 1 
        #print(temp_list)
        final_product_groupings.append(temp_list)

    for product in optics_stores_products:
        #print(product.tracked)
        if product.tracked != "FALSE": # might have to fix this so that it is a boolean from the beginign 
            final_tracked_product_list.append(product)

    for product in final_tracked_product_list:
        print(product)
        #print((product.tracked,product.internal_sku,product.simular_sku))

    # do this for all ....
    if test_traked_groupings(final_product_groupings,final_tracked_product_list,len(optics_stores_products),multipule_sku_values):
        print("finished")
        create_grouping_csv(final_product_groupings,final_tracked_product_list,"optics")



print("new")

print(len(telescopesnz_products))
print(len(optics_stores_products))
print(len(final_product_groupings))
print(len(final_tracked_product_list))


print(final_product_groupings[17])




      