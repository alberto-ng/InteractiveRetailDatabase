DROP DATABASE IF EXISTS Retail;
CREATE DATABASE Retail;
USE Retail;

-- creating  needed tables

-- customer.csv
CREATE TABLE IF NOT EXISTS Customer
(
    Customer_ID VARCHAR(10) NOT NULL,
    Customer_First_Name VARCHAR(30) NOT NULL,
    Customer_Last_Name VARCHAR(30) NOT NULL,
    Customer_Phone VARCHAR(20),
    Customer_Email VARCHAR(50),
    Customer_Type VARCHAR(10) NOT NULL,
    Soft_Delete CHAR(1) NOT NULL DEFAULT 1,

    CONSTRAINT PK_Customer PRIMARY KEY  (Customer_ID)
);

-- payment.csv
CREATE TABLE IF NOT EXISTS Card
(
    Card_ID INTEGER NOT NULL,
    Payment_Type VARCHAR(10) NOT NULL,
    Card_Number VARCHAR(20) NOT NULL,
    CVV VARCHAR(5) NOT NULL,
    Card_Name VARCHAR(50) NOT NULL,
    Customer_ID VARCHAR(10) NOT NULL,

    CONSTRAINT PK_Card PRIMARY KEY  (Card_ID)
);

CREATE TABLE IF NOT EXISTS Payment
(
    Payment_ID VARCHAR(10) NOT NULL,
    Payment_Mode VARCHAR(30) NOT NULL,
    Customer_ID VARCHAR(10) NOT NULL,
    Card_ID INTEGER,
    Payment_Amount INTEGER,

    CONSTRAINT PK_Payment PRIMARY KEY  (Payment_ID)
);

-- orders.csv
CREATE TABLE IF NOT EXISTS Orders
(
    Order_ID VARCHAR(10) NOT NULL,
    Order_Date DATE NOT NULL,
    Order_Status VARCHAR(30) NOT NULL,
    Order_ETA VARCHAR(20) NOT NULL,
    Payment_ID VARCHAR(10) NOT NULL,

    CONSTRAINT PK_Order PRIMARY KEY  (Order_ID)
);

-- orderProduct.csv
CREATE TABLE IF NOT EXISTS ShoppingCart
(
    Order_ID VARCHAR(10) NOT NULL,
    Product_ID VARCHAR(10) NOT NULL,
    Order_Quantity INTEGER NOT NULL,
    OP_ID VARCHAR(10) NOT NULL,

    CONSTRAINT PK_ShoppingCart PRIMARY KEY  (OP_ID)
);

-- product.csv
CREATE TABLE IF NOT EXISTS Product
(
    Product_ID VARCHAR(10) NOT NULL,
    Product_Name VARCHAR(30) NOT NULL,
    Product_Amount INTEGER,
    Group_ID INTEGER NOT NULL,
    Supplier_ID VARCHAR(10) NOT NULL,

    CONSTRAINT PK_Product PRIMARY KEY  (Product_ID)
);

-- productDetail.csv
CREATE TABLE IF NOT EXISTS ProductDetail
(
    Product_ID VARCHAR(10) NOT NULL,
    Product_Weight INTEGER NOT NULL,
    Product_Width INTEGER NOT NULL,
    Product_Height INTEGER NOT NULL,
    Product_Color VARCHAR(20) NOT NULL,

    CONSTRAINT PK_ProductDetail PRIMARY KEY  (Product_ID)
);

-- productGroup.csv
CREATE TABLE IF NOT EXISTS ProductGroup
(
    Group_ID INTEGER NOT NULL,
    Group_Name VARCHAR(20) NOT NULL,

    CONSTRAINT PK_ProductGroup PRIMARY KEY  (Group_ID)
);

-- supplier.csv
CREATE TABLE IF NOT EXISTS Supplier
(
    Supplier_ID VARCHAR(10) NOT NULL,
    Supplier_Name VARCHAR(30) NOT NULL,
    Supplier_Quantity INTEGER NOT NULL,

    CONSTRAINT PK_Supplier PRIMARY KEY  (Supplier_ID)
);



-- linking foreign key
 ALTER TABLE Card ADD CONSTRAINT FK_Card_Customer_ID
    FOREIGN KEY (Customer_ID) REFERENCES Customer (Customer_ID) ON DELETE NO ACTION ON UPDATE CASCADE;

ALTER TABLE Payment ADD CONSTRAINT FK_Payment_Customer_ID
    FOREIGN KEY (Customer_ID) REFERENCES Customer (Customer_ID) ON DELETE NO ACTION ON UPDATE CASCADE;
ALTER TABLE Payment ADD CONSTRAINT FK_Payment_Card_ID
    FOREIGN KEY (Card_ID) REFERENCES Card (Card_ID) ON DELETE NO ACTION ON UPDATE CASCADE;

ALTER TABLE Orders ADD CONSTRAINT FK_Order_Payment_ID
    FOREIGN KEY (Payment_ID) REFERENCES Payment (Payment_ID) ON DELETE NO ACTION ON UPDATE CASCADE;

ALTER TABLE ShoppingCart ADD CONSTRAINT FK_ShoppingCart_Order_ID
    FOREIGN KEY (Order_ID) REFERENCES Orders (Order_ID) ON DELETE NO ACTION ON UPDATE CASCADE;
ALTER TABLE ShoppingCart ADD CONSTRAINT FK_ShoppingCart_Product_ID
    FOREIGN KEY (Product_ID) REFERENCES Product (Product_ID) ON DELETE NO ACTION ON UPDATE CASCADE;

ALTER TABLE Product ADD CONSTRAINT FK_Product_Group_ID
    FOREIGN KEY (Group_ID) REFERENCES ProductGroup (Group_ID) ON DELETE NO ACTION ON UPDATE CASCADE;
ALTER TABLE Product ADD CONSTRAINT FK_Product_Supplier_ID
    FOREIGN KEY (Supplier_ID) REFERENCES Supplier (Supplier_ID) ON DELETE NO ACTION ON UPDATE CASCADE;

ALTER TABLE ProductDetail ADD CONSTRAINT FK_ProductDetail_Product_ID
    FOREIGN KEY (Product_ID) REFERENCES Product (Product_ID) ON DELETE NO ACTION ON UPDATE CASCADE;

CREATE VIEW Customer_View AS
SELECT Customer_ID, Customer_First_Name, Customer_Last_Name, Customer_Phone, Customer_Email, Customer_Type
FROM Customer
WHERE Soft_Delete = '1';

CREATE INDEX Customer_FN
ON Customer (Customer_First_Name);

CREATE INDEX Customer_LN
ON Customer (Customer_Last_Name);