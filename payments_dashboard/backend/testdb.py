import pymysql

try:
    conn = pymysql.connect(host="localhost", user="root", password="Y@$hL@d276", database="visa_payment_network")
    print("Connected successfully!")
except pymysql.MySQLError as e:
    print("Error: ", e)