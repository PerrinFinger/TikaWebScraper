from fulltest import Product,Store
from project import Session


if __name__ == "__main__":
    session = Session()
    products = session.query(Product).all()

    for product in products:
        product.name += " (" + product.varration_dict['title'] + ")"

    session.commit()
    session.close()
