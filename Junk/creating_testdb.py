from project import Session
from fulltest import Product, Store
from sqlalchemy import delete



if __name__ == "__main__":
    session = Session()
    s = session.query(Product).all()
    print(len(s))








    