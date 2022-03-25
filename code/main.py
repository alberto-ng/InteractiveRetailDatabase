# Importing needed libraries
import csv
import mysql.connector

host = input("Enter mysql host name: ")
user = input("Enter mysql user (ex. root): ")
password = input("Enter password for mysql user: ")

# connect to mysql db
connect = mysql.connector.connect(#host="localhost",
                                  host=host,
                                  #user="root",
                                  user=user,
                                  #password="",
                                  password=password,
                                  database='Retail',
                                  auth_plugin='mysql_native_password')

curs = connect.cursor()

# read csv
with open("Customer.csv") as f:
    columns = f.readline()
    data = f.readlines()

customer = []
for i in data:
    i = i.strip().split(",")

    temp = []
    for j in range(len(i)):
        temp.append(i[j])

    customer.append(tuple(temp))

# insert into Retail DB
insert = "INSERT IGNORE INTO Customer("
col = "Customer_ID, Customer_First_Name, Customer_Last_Name, Customer_Phone, Customer_Email, Customer_Type)"
val = " VALUES(%s,%s,%s,%s,%s,%s);"
# bulk insert
curs.execute("START TRANSACTION;")

r = True
try:
    curs.executemany(insert + col + val, customer)
    connect.commit()
except:
    print("insert fail, rolled back.")
    r = False
    curs.execute("ROLLBACK;")
finally:
    if r:
        curs.execute("COMMIT;")
# connect.commit()


with open("Payment.csv") as f:
    columns = f.readline()
    data = f.readlines()

with open("Bill.csv") as f:
    b_columns = f.readline()
    b_data = f.readlines()

payment = []
card = []
count = 0
for i in data:
    i = i.strip().split(",")
    x = b_data[count].strip().split(",")[1]
    # print(x)

    temp1 = []
    temp2 = []
    for j in range(len(i) - 1):
        if 2 > j or j == 6:
            temp1.append(i[j])
        if 2 <= j:
            temp2.append(i[j])
    temp1.append(count)
    temp1.append(x)
    temp2.append(count)
    count += 1
    payment.append(tuple(temp1))
    card.append(tuple(temp2))

with open("Bill.csv") as f:
    b_columns = f.readline()
    b_data = f.readlines()

bill = []
for i in data:
    i = i.strip().split(",")

    temp = []
    for j in range(len(i)):
        if j == 1:
            temp.append(i[j])

    bill.append(tuple(temp))

# insert into Retail DB
insert = "INSERT IGNORE INTO Card("
col = "Payment_Type, Card_Number, CVV, Card_Name, Customer_ID, Card_ID)"
val = " VALUES(%s,%s,%s,%s,%s,%s);"
# bulk insert
# print(card)
curs.executemany(insert + col + val, card)
connect.commit()

insert = "INSERT IGNORE INTO Payment("
col = "Payment_ID, Payment_Mode, Customer_ID, Card_ID, Payment_Amount)"
val = " VALUES(%s,%s,%s,%s,%s);"
# bulk insert
# print(payment)
curs.executemany(insert + col + val, payment)
connect.commit()

with open("Orders.csv") as f:
    columns = f.readline()
    data = f.readlines()

orders = []
for i in data:
    i = i.strip().split(",")

    temp = []
    for j in range(len(i)):
        if j == 1:
            # reformat date
            date = i[j][-4:] + "/" + i[j][:-5]
            # print(date)
            temp.append(date)
        else:
            temp.append(i[j])

    orders.append(tuple(temp))

# insert into Retail DB
insert = "INSERT IGNORE INTO Orders("
col = "Order_ID, Order_Date, Order_Status, Order_ETA, Payment_ID)"
val = " VALUES(%s,%s,%s,%s,%s);"
# bulk insert
curs.executemany(insert + col + val, orders)
connect.commit()

with open("ProductGroup.csv") as f:
    columns = f.readline()
    data = f.readlines()

productG = []
for i in data:
    i = i.strip().split(",")

    temp = []
    for j in range(len(i)):
        temp.append(i[j])

    productG.append(tuple(temp))

# insert into Retail DB
insert = "INSERT IGNORE INTO ProductGroup("
col = "Group_ID, Group_Name)"
val = " VALUES(%s,%s);"
# bulk insert
curs.executemany(insert + col + val, productG)
connect.commit()

with open("Supplier.csv") as f:
    columns = f.readline()
    data = f.readlines()

supplier = []
for i in data:
    i = i.strip().split(",")

    temp = []
    for j in range(len(i)):
        temp.append(i[j])

    supplier.append(tuple(temp))

# insert into Retail DB
insert = "INSERT IGNORE INTO Supplier("
col = "Supplier_ID, Supplier_Name, Supplier_Quantity)"
val = " VALUES(%s,%s,%s);"
# bulk insert
curs.executemany(insert + col + val, supplier)
connect.commit()

with open("Product.csv") as f:
    columns = f.readline()
    data = f.readlines()

product = []
for i in data:
    i = i.strip().split(",")

    temp = []
    for j in range(len(i)):
        temp.append(i[j])

    product.append(tuple(temp))

# insert into Retail DB
insert = "INSERT IGNORE INTO Product("
col = "Product_ID, Product_Name, Product_Amount, Group_ID, Supplier_ID)"
val = " VALUES(%s,%s,%s,%s,%s);"
# bulk insert
curs.executemany(insert + col + val, product)
connect.commit()

with open("OrderProduct.csv") as f:
    columns = f.readline()
    data = f.readlines()

shoppingCart = []
for i in data:
    i = i.strip().split(",")

    temp = []
    for j in range(len(i)):
        temp.append(i[j])

    shoppingCart.append(tuple(temp))

# insert into Retail DB
insert = "INSERT IGNORE INTO ShoppingCart("
col = "Order_Quantity, Product_ID, Order_ID, OP_ID)"
val = " VALUES(%s,%s,%s,%s);"
# bulk insert
curs.executemany(insert + col + val, shoppingCart)
connect.commit()

with open("ProductDetails.csv") as f:
    columns = f.readline()
    data = f.readlines()

PD = []
for i in data:
    i = i.strip().split(",")

    temp = []
    for j in range(len(i)):
        temp.append(i[j])

    PD.append(tuple(temp))

# insert into Retail DB
insert = "INSERT IGNORE INTO ProductDetail("
col = "Product_ID, Product_Weight, Product_Width, Product_Height, Product_Color)"
val = " VALUES(%s,%s,%s,%s,%s);"
# bulk insert
curs.executemany(insert + col + val, PD)
connect.commit()

# display table
def option_1(user):
    while user != "n":
        print("Display: ")
        user = input(
            "Product, Customer, Card, Payment, Orders, ShoppingCart,ProductDetail, ProductGroup, Supplier: ")
        col = "SHOW COLUMNS FROM " + user + ";"

        curs.execute(col)
        str = ""

        # get column names
        for x in curs.fetchall():
            str += (x[0])
            str += (", ")
        str = str[:-2]
        if ", Soft_Delete" in str:
            str = str.split(", Soft_Delete")[0]

        searchF = input("Search by attribute? (y/n): ")

        if searchF == "y":
            att = input("Choose from (" + str + "): ")
            compare = input("Compare element: ")

        limit = input("View all ENTER 'all', view partial ENTER 'p': ")
        if limit == "p":
            if searchF == "y":
                if user == "Customer" or user == "customer":
                    curs.execute("SELECT COUNT(*) FROM " + user + " WHERE " + att + "=\"" +
                                 compare + "\" and Soft_Delete = 1;")
                else:
                    curs.execute("SELECT COUNT(*) FROM " + user + " WHERE " + att + "=\"" + compare + "\";")
            else:
                curs.execute("SELECT COUNT(*) FROM " + user + ";")
            result = "% s" % curs.fetchone()[0]
            # print(result)
            maximum = input("Enter from 1-" + result + ": ")

        if user == "Customer" or user == "customer":
            user = "Customer"
            query = "SELECT * FROM Customer_View"
        else:
            query = "SELECT * FROM " + user
        if limit == "p":
            if searchF == "y":
                query += " WHERE " + att + "=\"" + compare + "\""
            query += " LIMIT " + maximum + ";"
        else:
            if searchF == "y":
                query += " WHERE " + att + "=\"" + compare + "\""
            query += ";"
        curs.execute(query)

        print("\n" + str)

        for i in curs:
            print(i, sep="\t")

        user = input("View another table? (y/n):")
        print("\n")

# delete customer
def option_2():
    col = "SHOW COLUMNS FROM Customer_View;"
    curs.execute(col)
    str = ""
    for x in curs.fetchall():
        str += (x[0])
        str += (", ")
    str = str[:-2]

    while True:
        user_input = input("Delete by (" + str + "): ")
        user_in2 = input("Enter compare value from " + user_input + ": ")
        curs.execute("UPDATE Customer SET Soft_Delete = '0' WHERE " + user_input + " = '" + user_in2 + "';")
        connect.commit()

        user_input = input("Continue another deletion (y/n): ")
        if user_input == "n":
            break

# update customer
def option_3():
    while True:
        user_in1 = input("Enter the customer ID that needs an update: ")
        user_in2 = input("Enter the updated customer ID: ")
        curs.execute("UPDATE Customer SET Customer_ID = " + user_in2 + " WHERE Customer_ID = " + user_in1 + ";")
        connect.commit()

        user_input = input("Continue updating another(y/n): ")
        if user_input == "n":
            break

# add customer
def option_4():
    while True:
        insert = "INSERT IGNORE INTO Customer("
        col = "Customer_ID, Customer_First_Name, Customer_Last_Name, Customer_Phone, Customer_Email, Customer_Type)"
        val = " VALUES(%s,%s,%s,%s,%s,%s);"

        temp = []
        temp.append(input("Enter Customer_ID: "))
        temp.append(input("Enter Customer_First_Name: "))
        temp.append(input("Enter Customer_Last_Name: "))
        temp.append(input("Enter Customer_Phone: "))
        temp.append(input("Enter Customer_Email: "))
        temp.append(input("Enter Customer_Type (Student, Employee, Business): "))

        curs.execute(insert + col + val, temp)
        connect.commit()

        user_input = input("Continue adding another customer (y/n): ")

        if user_input == "n":
            break

# fetch Supplier name, product name, product amount and product group
def option_5():
    query = "SELECT Supplier_Name, Product_Name, Group_Name, Product_Amount "
    query += "FROM ProductGroup LEFT JOIN Product "
    query += "ON ProductGroup.Group_ID = Product.Group_ID LEFT JOIN (SELECT Supplier_ID, Supplier_Name FROM Supplier) "
    query += "AS S ON Product.Supplier_ID = S.Supplier_ID;"

    # print(query)
    curs.execute(query)

    print("Supplier_Name, Product_Name, Group_Name, Product_Amount")
    for i in curs:
        print(i, sep="\t")

# fetch Order_ID, Product_Name, quantity, price, Order_ETA
def option_6():
    query = "SELECT Orders.Order_ID, Product.Product_Name, ShoppingCart.Order_Quantity AS quantity, "
    query += "Payment.Payment_Amount AS price, Orders.Order_ETA FROM Orders INNER JOIN ShoppingCart "
    query += "ON Orders.Order_ID = ShoppingCart.Order_ID LEFT JOIN Product ON Product.Product_ID = "
    query += "ShoppingCart.Product_ID LEFT JOIN Payment ON Orders.Payment_ID = Payment.Payment_ID;"

    curs.execute(query)

    print("Order_ID, Product_Name, quantity, price, Order_ETA")
    for i in curs:
        print(i, sep="\t")

# fetch how many products each supplier supply
def option_7():
    query = "SELECT Supplier.Supplier_Name , COUNT(*) AS numProduct, ProductGroup.Group_Name "
    query += "FROM Supplier, Product, ProductGroup WHERE Supplier.Supplier_ID = Product.Supplier_ID "
    query += "and Product.Group_ID = ProductGroup.Group_ID GROUP BY Supplier.Supplier_Name, ProductGroup.Group_Name;"
    curs.execute(query)

    print("Supplier_Name, numProduct, groupName")
    for i in curs:
        print(i, sep="\t")

# create csvs
def create_csv():
    with open("SQLDB_Customer", "w", newline="") as csvfile:
        col = "SHOW COLUMNS FROM Customer;"
        curs.execute(col)
        columns = []
        for x in curs.fetchall():
            columns.append(x[0])

        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()

        query = "SELECT * FROM Customer;"
        curs.execute(query)

        data = []
        for i in curs:
            data.append(i)

        for x in range(len(data) - 1):
            cID = columns[0]
            cFN = columns[1]
            cLN = columns[2]
            cPhone = columns[3]
            cEmail = columns[4]
            cType = columns[5]
            cSD = columns[6]

            writer.writerow({cID:data[x][0], cFN:data[x][1],cLN:data[x][2], cPhone:data[x][3],
                             cEmail:data[x][4], cType:data[x][5], cSD:data[x][6]})

    with open("SQLDB_Card", "w", newline="") as csvfile:
        col = "SHOW COLUMNS FROM Card;"
        curs.execute(col)
        columns = []
        for x in curs.fetchall():
            columns.append(x[0])

        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()

        query = "SELECT * FROM Card;"
        curs.execute(query)

        data = []
        for i in curs:
            data.append(i)

        for x in range(len(data) - 1):
            cID = columns[0]
            pType = columns[1]
            c_num = columns[2]
            cvv = columns[3]
            cName = columns[4]
            cusID = columns[5]

            writer.writerow({cID:data[x][0], pType:data[x][1],c_num:data[x][2], cvv:data[x][3],
                             cName:data[x][4], cusID:data[x][5]})

    with open("SQLDB_Payment", "w", newline="") as csvfile:
        col = "SHOW COLUMNS FROM Payment;"
        curs.execute(col)
        columns = []
        for x in curs.fetchall():
            columns.append(x[0])

        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()

        query = "SELECT * FROM Payment;"
        curs.execute(query)

        data = []
        for i in curs:
            data.append(i)

        for x in range(len(data) - 1):
            pID = columns[0]
            pM = columns[1]
            cID = columns[2]
            cardID = columns[3]
            pAmount = columns[4]

            writer.writerow({pID:data[x][0], pM:data[x][1],cID:data[x][2], cardID:data[x][3],
                             pAmount:data[x][4]})

    with open("SQLDB_Orders", "w", newline="") as csvfile:
        col = "SHOW COLUMNS FROM Orders;"
        curs.execute(col)
        columns = []
        for x in curs.fetchall():
            columns.append(x[0])

        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()

        query = "SELECT * FROM Orders;"
        curs.execute(query)

        data = []
        for i in curs:
            data.append(i)

        for x in range(len(data) - 1):
            oID = columns[0]
            oDate = columns[1]
            oStatus = columns[2]
            oETA = columns[3]
            pID = columns[4]

            writer.writerow({oID:data[x][0], oDate:data[x][1],oStatus:data[x][2], oETA:data[x][3],
                             pID:data[x][4]})

    with open("SQLDB_ShoppingCart", "w", newline="") as csvfile:
        col = "SHOW COLUMNS FROM ShoppingCart;"
        curs.execute(col)
        columns = []
        for x in curs.fetchall():
            columns.append(x[0])

        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()

        query = "SELECT * FROM ShoppingCart;"
        curs.execute(query)

        data = []
        for i in curs:
            data.append(i)

        for x in range(len(data) - 1):
            opID = columns[0]
            oID = columns[1]
            pID = columns[2]
            quant = columns[3]

            writer.writerow({opID:data[x][0], oID:data[x][1], pID:data[x][2], quant:data[x][3]})

    with open("SQLDB_Product", "w", newline="") as csvfile:
        col = "SHOW COLUMNS FROM Product;"
        curs.execute(col)
        columns = []
        for x in curs.fetchall():
            columns.append(x[0])

        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()

        query = "SELECT * FROM Product;"
        curs.execute(query)

        data = []
        for i in curs:
            data.append(i)

        for x in range(len(data) - 1):
            pID = columns[0]
            pName = columns[1]
            pAmount = columns[2]
            gID = columns[3]
            sID = columns[4]

            writer.writerow({pID:data[x][0], pName:data[x][1],
                             pAmount:data[x][2], gID:data[x][3], sID:data[x][4]})

    with open("SQLDB_ProductDetail", "w", newline="") as csvfile:
        col = "SHOW COLUMNS FROM ProductDetail;"
        curs.execute(col)
        columns = []
        for x in curs.fetchall():
            columns.append(x[0])

        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()

        query = "SELECT * FROM ProductDetail;"
        curs.execute(query)

        data = []
        for i in curs:
            data.append(i)

        for x in range(len(data) - 1):
            pID = columns[0]
            pWeigh = columns[1]
            pWid = columns[2]
            pH = columns[3]
            pC = columns[4]

            writer.writerow({pID:data[x][0], pWeigh:data[x][1],
                             pWid:data[x][2], pH:data[x][3], pC:data[x][4]})

    with open("SQLDB_Supplier", "w", newline="") as csvfile:
        col = "SHOW COLUMNS FROM Supplier;"
        curs.execute(col)
        columns = []
        for x in curs.fetchall():
            columns.append(x[0])

        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()

        query = "SELECT * FROM Supplier;"
        curs.execute(query)

        data = []
        for i in curs:
            data.append(i)

        for x in range(len(data) - 1):
            sID = columns[0]
            sN = columns[1]
            sQ = columns[2]

            writer.writerow({sID:data[x][0], sN:data[x][1], sQ:data[x][2]})

    with open("SQLDB_ProductGroup", "w", newline="") as csvfile:
        col = "SHOW COLUMNS FROM ProductGroup;"
        curs.execute(col)
        columns = []
        for x in curs.fetchall():
            columns.append(x[0])

        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()

        query = "SELECT * FROM ProductGroup;"
        curs.execute(query)

        data = []
        for i in curs:
            data.append(i)

        for x in range(len(data) - 1):
            gID = columns[0]
            gN = columns[1]

            writer.writerow({gID:data[x][0], gN:data[x][1]})

user_in = "-"
while user_in != "quit":
    print("\nChoose an option:")
    print("Display table:  ENTER 1")
    print("Delete Customer: ENTER 2")
    print("Update Customer ID: ENTER 3")
    print("Add Customer: ENTER 4")
    print("fetch Supplier name, product name, product amount and product group: ENTER 5")
    print("fetch Order_ID, Product_Name, quantity, price, Order_ETA: ENTER 6")
    print("fetch how many products each supplier supply: ENTER 7")
    print("ENTER quit TO QUIT")
    user_in = input()

    if user_in == "1":
        option_1(user_in)
    elif user_in == "2":
        option_2()
    elif user_in == "3":
        option_3()
    elif user_in == "4":
        option_4()
    elif user_in == "5":
        option_5()
    elif user_in == "6":
        option_6()
    elif user_in == "7":
        option_7()


create_csv()

curs.close()
