from project import Session
from fulltest import Store

if __name__ == "__main__":

    session = Session()
    csv_prefix =  "C:/Users/GGPC/sqlalchemytesting/Data/StoreCSVs/Final_CSV's/Telescopes/"
    csv_suffix = " Matched.csv"
    optics_stores = [

        Store("optics",
              "telscopesnz",
              "https://www.telescopes.net.nz/collections/",
              True,
              {"telescopes": 3, "sport-optics": 3, "accessories": 5}),


        Store("optics",
              "jacobs",
              "https://www.jacobsdigital.co.nz/collections/",
              True,
              {"telescopes": 1, "telescope-accessories": 1, "binoculars": 1, "spotting-scopes": 1}),


        Store("optics",
              "astronz",
              "https://astronz.nz/collections/",
              True,
              {"telescopes": 2, "binoculars": 1, "accessories": 5, "astrophotography-mounts": 2, "eyepieces": 1}),


        Store("optics",
              "nature",
              "https://nature.co.nz/collections/",
              True,
              {"optics-telescopes": 2, "optics-binoculars": 1, "optics-telescope-accessories": 2, "optics-spottingscopes": 1}),


        Store("optics",
              "ScopeUOut",
              "https://www.scopeuout.co.nz/collections/",
              True,
              {"telescopes": 2, "binoculars": 7, "spotting-scopes": 2}),


        Store("optics",
              "OneCheq",
              "https://onecheq.co.nz/collections/",
              True,
              {"telescopes": 2, "binoculars": 3})

    ]


    for store in optics_stores:
        store.inital_populate(session)
        session.add(store)
        if store.name != 'telscopesnz':
            store.import_from_csv(csv_prefix + store.name + csv_suffix )

        else:
            for product in store.products:
                product.set_internal_sku(product.external_sku)


    session.commit()
    session.close()
