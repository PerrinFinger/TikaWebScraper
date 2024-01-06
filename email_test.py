import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date
from project import Session
from fulltest import Product, Store
import operator
#staff@telescopes.net.nz
# sunshine@weatherstation.co.nz

if __name__ == "__main__":


    session = Session()
    price_changes_dict = {}
    stock_changes_dict = {}

    # Email details
    from_email = 'tikawebscrapper@gmail.com'
    to_email = ['matthamiltonperrin@gmail.com', 'sunshine@weatherstation.co.nz']
    subject = "Optics Pricing Update({})".format(str(date.today()))
    email_body = "Hope you're having a great day :)<br>"
    email_body += "<br>Here are your weather stations updates for {} <br>".format(str(date.today())) # change per update need to change 

    def get_updated_products(session):
        temp1 = session.query(Product).filter(Product.price_change == True)
        temp2 = session.query(Product).filter(Product.instock_change == True)
        
        price_changes = [x for x in temp1 if x.internal_sku != "0" or x.simular_sku != "0" or x.tracked != "FALSE"]
        stock_changes = [x for x in temp2 if x.internal_sku != "0" or x.simular_sku != "0" or x.tracked != "FALSE"]

        # price_changes = session.query(Product).filter(Product.price_change == True)
        # stock_changes = session.query(Product).filter(Product.instock_change == True)


        return [price_changes, stock_changes]

    def format_products(l, body):
        #body = body + "You currently have <b>118 products</b> being tracked for Jacobs Optics!<br>" + "<br>"
        price_changes, stock_changes = l[0], l[1]
        # print(price_changes.all())
        # print()
        price_changes = sorted(price_changes,key=operator.attrgetter('store_id'))
        stock_changes = sorted(stock_changes,key=operator.attrgetter('store_id'))
        # print(type(price_changes))
        # print(price_changes)

        for product in price_changes:
            if product.store_id in price_changes_dict.keys():
                price_changes_dict[product.store_id].append(product)
            else:
                price_changes_dict[product.store_id] = [product]

        for product in stock_changes:
            if product.store_id in stock_changes_dict.keys():
                stock_changes_dict[product.store_id].append(product)
            else:
                stock_changes_dict[product.store_id] = [product]
            

        for store in price_changes_dict.keys():
            products = price_changes_dict[store]
            store_object = session.query(Store).filter(Store.id == store).first()
            store_name = store_object.name
            print(store_name)
            body = body + "<br>Here are the <b>{} price changes</b> for {} Today:<br>".format(len(products),store_name)

            for product in products:
                body = body + product.price_change_str() + "<br>"
            body = body + "<br>"


        
        for store in stock_changes_dict.keys():
            products = stock_changes_dict[store]
            store_object = session.query(Store).filter(Store.id == store).first()
            store_name = store_object.name
            body =  body + "<br>Here are the <b>{} stock changes</b> for {} Today:<br>".format(len(products),store_name)


            for product in products:
                body = body + product.stock_change_str() + "<br>"
            body = body + "<br>"
        print(price_changes_dict.keys())
        return body

    email_body = format_products(get_updated_products(session), email_body)


    # # Create email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(email_body, 'html'))  # Use a different variable name for MIMEText

    # Connect to the SMTP server
    smtp_server = 'smtp.gmail.com'  # Replace with your SMTP server
    smtp_port = 25  # Replace with your SMTP port (common ports are 25, 465, 587)
    smtp_user = 'tikawebscrapper@gmail.com'  # Replace with your email address
    smtp_password = 'wavtblalngudmfvx'  # Replace with your email password

    # Send email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        
        for email in to_email:
            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = email
            msg['Subject'] = subject
            msg.attach(MIMEText(email_body, 'html'))
            
            server.sendmail(from_email, email, msg.as_string())
        
        server.quit()
        print('Email sent successfully!')
    except Exception as e:
        print(f'Error: {e}')

    session.close()