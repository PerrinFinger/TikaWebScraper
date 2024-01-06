from project import Session
from fulltest import Product, Store
from sqlalchemy import and_, or_
import csv


file_path = "C:/Users/GGPC/sqlalchemytesting/TestingData/CSVs/matched.csv"
file_path_two = "C:/Users/GGPC/sqlalchemytesting/TestingData/CSVs/tika.csv"


if __name__ == "__main__":
    # session = Session()
    # matched = session.query(Product).filter(
    #     and_(
    #         Product.store_id == 2,
    #         or_(
    #             Product.tracked != "FALSE",
    #             Product.internal_sku != "0",
    #             Product.simular_sku != "0"
    #         )
    #     )
    # ).all()
    # with open(file_path,'w',encoding='utf_8') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(["name","brand","price","external_sku","internal_sku","simular_sku","tracked"])
    #     for product in matched:
    #         writer.writerow([product.name,product.brand,product.price,product.external_sku,product.internal_sku,product.simular_sku,product.tracked])

    # print("finsihed")


    session = Session()

    products = session.query(Store).first().products
    with open(file_path_two,'w',encoding='utf_8') as f:
         writer = csv.writer(f)
         writer.writerow(["name","brand","price","external_sku","internal_sku","simular_sku","tracked"])
         for product in products:
            writer.writerow([product.name,product.brand,product.price,product.external_sku,product.internal_sku,product.simular_sku,product.tracked])





