from project import Session
from fulltest import Store

if __name__ == "__main__":
    session = Session()
    stores = session.query(Store).all()
    for store in stores:
        #  if store.name != "telescopesnz":
        store.update_store(session,count = "2")
        #  else:
        #      print("working")
        
        #store.update_store(session,count="2")   # Do I need to pass the session into this function ??
    session.commit()
    session.close()




    











    