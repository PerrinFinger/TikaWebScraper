from project import Session 
from fulltest import Store, Product

if __name__ == "__main__":
    session = Session()
    stores = session.query(Store).all()
    print(stores)


    for store in stores:
        for i in range(len(store.products)):
            temp = store.products[i].external_sku
            for j in range(len(store.products)):
                if store.products[j].external_sku == temp and i != j:
                    print(temp)




    #might need to check this later ??
    first = session.query(Product).filter(Product.external_sku == "08266").all()
    print(first)



    # for i in range(1,7):
    #     print(i)