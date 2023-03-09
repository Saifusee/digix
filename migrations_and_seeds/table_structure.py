from re import sub
from CONSTANT.index import *

class TableStructure():
    def __init__(self, mysql):
        self.mysql = mysql
        
        print("\n---------------- Database deletion and new database creation initiated.... ----------------")
        #Deleting Existing Datbase and Creating New Database
        mysql.query.execute(f"DROP DATABASE {DATABASE_NAME}")
        mysql.query.execute(f"CREATE DATABASE {DATABASE_NAME}")
        mysql.query.execute(f"ALTER DATABASE {DATABASE_NAME} DEFAULT CHARACTER SET UTF8;") # MySQL will store unicode characters intact such as rupee symbol
        mysql.query.execute(f"USE {DATABASE_NAME}")
        
        # CREATE SHOP TABLE
        self.shop_table()
        # CREATE USER TABLE
        self.user_table()
        # CREATE USER TABLE
        self.user_logs_table()
        # CREATE OTP TABLE
        self.otp_table()
        # CREATE CATEGORY TABLE
        self.category_table()
        # CREATE SUB-CATEGORY TABLE
        self.sub_category_table()
        # CREATE SUPPLIER TABLE
        self.supplier_table()
        # CREATE PRODUCT TABLE
        self.product_table()
        # CREATE PRODUCT LOGS TABLE
        self.product_logs_table()
        #CREATE SALES ORDER TABLE
        self.sales_order_table()
        # CREATE SALES_ORDER_PRODUCT TABLE
        self.sales_order_product_table()
        # CREATE SALES ORDER LOGS TABLE
        self.sales_order_logs_table()        
        #CREATE SALES ORDER TABLE
        self.purchase_order_table()
        # CREATE SALES_ORDER_PRODUCT TABLE
        self.purchase_order_product_table()
        # CREATE PURCHASE ORDER LOGS TABLE
        self.purchase_order_logs_table()
        # CREATE RETURN CANCEL ORDER TABLE
        self.return_cancel_order_table()
        # CREATE RETURN_CANCEL_ORDER_PRODUCT TABLE
        self.return_cancel_order_product_table()
    
    
    
    # DEFINITION OF SHOP TABLE
    def shop_table(self):
        try:
            print(f"Table Creation and Structuring Initiated = {SHOP_TABLE_NAME} ")
            query = f"""CREATE TABLE `{DATABASE_NAME}`.`{SHOP_TABLE_NAME}`
            (
            `{SHOP_ID}` INT NOT NULL AUTO_INCREMENT ,
            `{SHOP_NAME}` VARCHAR(255) NOT NULL DEFAULT "Shop name here",
            `{SHOP_OWNER_NAME}` VARCHAR(255) NOT NULL DEFAULT "Shop's owner name here",
            `{SHOP_CONTACT_1}` VARCHAR(255) NOT NULL DEFAULT "+91-0000000000",
            `{SHOP_CONTACT_2}` VARCHAR(255) NULL DEFAULT "",
            `{SHOP_EMAIL}` VARCHAR(255) NOT NULL DEFAULT "abcd@xyz.com",
            `{SHOP_GST_NUMBER}` VARCHAR(255) NULL DEFAULT "",
            `{SHOP_ADDRESS}` TEXT NULL ,
            `{SHOP_LOGO}` MEDIUMBLOB NULL ,
            PRIMARY KEY (`{SHOP_ID}`)
            ) ENGINE = InnoDB"""
            self.mysql.query.execute(query)
            print(f"Table Creation and Structuring Successful = {SHOP_TABLE_NAME}\n")

            # Inserting dummy shop details first
            query = f"""INSERT INTO {SHOP_TABLE_NAME} 
            ({SHOP_NAME}, {SHOP_CONTACT_1}, {SHOP_CONTACT_2}, {SHOP_EMAIL}, {SHOP_ADDRESS}, {SHOP_OWNER_NAME}, {SHOP_GST_NUMBER} )
            VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            values = [
            (
            "Shop name here",
            "+91-0000000000", 
            "+91-0000000000",
            "abcd@xyz.com",  
            "Shop's address here",
            "Shop's owner name here",
            "---------------"
            ),
            ]
            self.mysql.query.executemany(query, values)
            self.mysql.db_connection.commit()
        except Exception as error:
            print(f"Development Error (Creating Shop Table): {error}\n")



    # DEFINITION OF USER TABLE
    def user_table(self):
        try:
            print(f"Table Creation and Structuring Initiated = {USER_TABLE_NAME} ")
            query = f"""CREATE TABLE `{DATABASE_NAME}`.`{USER_TABLE_NAME}`
            ( `{USER_ID}` INT NOT NULL AUTO_INCREMENT ,
            `{USERNAME}` VARCHAR(255) UNIQUE NOT NULL ,
            `{EMAIL}` VARCHAR(255) UNIQUE NOT NULL ,
            `{PASSWORD}` TEXT ,
            `{USER_CONTACT_1}` VARCHAR(15) NULL ,
            `{USER_CONTACT_2}` VARCHAR(15) NULL  ,
            `{USER_ADDRESS}` VARCHAR(255) NULL ,
            `{USER_AUTHORITY}` ENUM {AUTHORITY_OPTIONS} DEFAULT '{AUTHORITY_TERTIARY}',
            `{EMPLOYMENT_STATUS}` ENUM {EMPLOYMENT_OPTIONS} DEFAULT '{EMPLOYED}',
            `{DATE_OF_JOINING}` DATETIME DEFAULT CURRENT_TIMESTAMP,
            `{DATE_OF_LEAVING}` DATETIME NULL,
            `{DATE_OF_REHIRING}` DATETIME NULL,
            `{LEAVE_REASON}` TEXT NULL,
            PRIMARY KEY (`{USER_ID}`),
            UNIQUE (`{USERNAME}`),
            UNIQUE (`{EMAIL}`))
            ENGINE = InnoDB"""
            self.mysql.query.execute(query)
            print(f"Table Creation and Structuring Successful = {USER_TABLE_NAME}\n")
        except Exception as error:
            print(f"Development Error (Creating User Table): {error}\n")



    # DEFINITION OF PRODUCT LOGS TABLE
    def user_logs_table(self):
        try:
            print(f"Table Creation and Structuring Initiated = {USER_LOGS_TABLE_NAME} ")
            query = f"""CREATE TABLE `{DATABASE_NAME}`.`{USER_LOGS_TABLE_NAME}`
            ( `{USER_LOGS_ID}` BIGINT NOT NULL AUTO_INCREMENT , 
            `{USER_LOGS_LOG}` TEXT NOT NULL ,
            `{USER_LOGS_FOREIGNKEY_ACTIVE_USER_ID}` INT NULL DEFAULT NULL ,
            `{USER_LOGS_FOREIGNKEY_TARGET_USER_ID}` INT NULL DEFAULT NULL , 
            `{CREATED_AT}` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP , 
            PRIMARY KEY (`{USER_LOGS_ID}`) ,
            CONSTRAINT `{USER_LOGS_ACTIVE_USER_CONSTRAINT}` FOREIGN KEY (`{USER_LOGS_FOREIGNKEY_ACTIVE_USER_ID}`)
            REFERENCES `{DATABASE_NAME}`.`{USER_TABLE_NAME}`(`{USER_ID}`) ON DELETE RESTRICT ON UPDATE CASCADE ,
            CONSTRAINT `{USER_LOGS_TARGET_USER_CONSTRAINT}` FOREIGN KEY (`{USER_LOGS_FOREIGNKEY_TARGET_USER_ID}`)
            REFERENCES `{DATABASE_NAME}`.`{USER_TABLE_NAME}`(`{USER_ID}`) ON DELETE RESTRICT ON UPDATE CASCADE
            )
            ENGINE = InnoDB;"""
            self.mysql.query.execute(query)
            print(f"Table Creation and Structuring Successful = {USER_LOGS_TABLE_NAME}\n ")
        except Exception as error:
            print(f"Development Error (Creating USER LOGS Table): {error}\n")
        
        
        
    # DEFINITION OF OTP TABLE
    def otp_table(self):
        try:
            print(f"Table Creation and Structuring Initiated = {OTP_TABLE_NAME} ")
            query = f"""CREATE TABLE `{DATABASE_NAME}`.`{OTP_TABLE_NAME}`
            ( `{OTP_ID}` INT NOT NULL AUTO_INCREMENT ,
            `{OTP_REFERENCE}` VARCHAR(255) NOT NULL ,
            `{OTP_VALUE}` INT(8) NOT NULL ,
            PRIMARY KEY (`{OTP_ID}`) ) ENGINE = InnoDB"""
            self.mysql.query.execute(query)
            print(f"Table Creation and Structuring Successful = {OTP_TABLE_NAME} \n")
        except Exception as error:
            print(f"Development Error (Creating OTP Table): {error}\n")
            
            
            
    # DEFINITION OF CATEGORY TABLE
    def category_table(self):
        try:
            print(f"Table Creation and Structuring Initiated = {CATEGORY_TABLE_NAME} ")
            query = f"""CREATE TABLE `{DATABASE_NAME}`.`{CATEGORY_TABLE_NAME}` ( `{CATEGORY_ID}` INT NOT NULL AUTO_INCREMENT ,
            `{CATEGORY_NAME}` VARCHAR(255) UNIQUE NOT NULL , PRIMARY KEY (`{CATEGORY_ID}`)) ENGINE = InnoDB;"""
            self.mysql.query.execute(query)
            print(f"Table Creation and Structuring Successful = {CATEGORY_TABLE_NAME}\n ")
        except Exception as error:
            print(f"Development Error (Creating CATEGORY Table): {error}\n")
         
         
            
    # DEFINITION OF SUB-CATEGORY TABLE
    def sub_category_table(self):
        try:
            print(f"Table Creation and Structuring Initiated = {SUB_CATEGORY_TABLE_NAME} ")
            query = f"""CREATE TABLE `{DATABASE_NAME}`.`{SUB_CATEGORY_TABLE_NAME}`
            ( `{SUB_CATEGORY_ID}` INT NOT NULL AUTO_INCREMENT ,
            `{SUB_CATEGORY_NAME}` VARCHAR(255) NOT NULL ,
            `{SUB_CATEGORY_FOREIGNKEY_CATEGORY_ID}` INT NOT NULL ,
            PRIMARY KEY (`{SUB_CATEGORY_ID}`) ,
            CONSTRAINT `{CATEGORY_SUB_CATEGORY_CONSTRAINT}` FOREIGN KEY (`{SUB_CATEGORY_FOREIGNKEY_CATEGORY_ID}`)
            REFERENCES `{DATABASE_NAME}`.`{CATEGORY_TABLE_NAME}`(`{CATEGORY_ID}`) ON DELETE CASCADE ON UPDATE CASCADE)
            ENGINE = InnoDB;"""
            self.mysql.query.execute(query)
            print(f"Table Creation and Structuring Successful = {SUB_CATEGORY_TABLE_NAME}\n ")
        except Exception as error:
            print(f"Development Error (Creating SUB-CATEGORY Table): {error}\n")
            
            
            
    # DEFINITION OF SUPPLIER TABLE
    def supplier_table(self):
        try:
            print(f"Table Creation and Structuring Initiated = {SUPPLIER_TABLE_NAME} ")
            query = f"""CREATE TABLE `{DATABASE_NAME}`.`{SUPPLIER_TABLE_NAME}`
            ( `{SUPPLIER_ID}` INT NOT NULL AUTO_INCREMENT ,
            `{SUPPLIER_NAME}` VARCHAR(255) NOT NULL ,
            `{SUPPLIER_CONTACT_1}` VARCHAR(15) UNIQUE NOT NULL ,
            `{SUPPLIER_CONTACT_2}` VARCHAR(15) NULL  ,
            `{SUPPLIER_ADDRESS}` VARCHAR(255) NOT NULL ,
            `{SUPPLIER_GSTIN}` VARCHAR(15) NULL ,
            `{SUPPLIER_ACTIVE_STATE}` BOOLEAN NOT NULL DEFAULT 1 ,
            `{SUPPLIER_ORGANIZATION_NAME}` VARCHAR(255) NULL ,
            `{SUPPLIER_ORGANIZATION_CONTACT_1}` VARCHAR(15) NULL ,
            `{SUPPLIER_ORGANIZATION_CONTACT_2}` VARCHAR(15) NULL ,
            `{SUPPLIER_ORGANIZATION_ADDRESS}` VARCHAR(255) NULL ,
            `{SUPPLIER_DESCRIPTION}` TEXT NULL ,
            `{CREATED_AT}` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP , 
            PRIMARY KEY (`{SUPPLIER_ID}`)
            )
            ENGINE = InnoDB;"""
            self.mysql.query.execute(query)
            print(f"Table Creation and Structuring Successful = {SUPPLIER_TABLE_NAME}\n ")
        except Exception as error:
            print(f"Development Error (Creating SUPPLIER Table): {error}\n")
            
            
            
    # DEFINITION OF PRODUCT TABLE
    def product_table(self):
        try:
            print(f"Table Creation and Structuring Initiated = {PRODUCT_TABLE_NAME} ")
            query = f"""CREATE TABLE `{DATABASE_NAME}`.`{PRODUCT_TABLE_NAME}`
            ( `{PRODUCT_ID}` INT NOT NULL AUTO_INCREMENT ,
            `{PRODUCT_NAME}` VARCHAR(255) NOT NULL ,
            `{PRODUCT_PRICE}` FLOAT(10,2) NOT NULL ,
            `{PRODUCT_QUANTITY}` INT NOT NULL DEFAULT '0' ,
            `{PRODUCT_REORDER_QUANTITY}` INT NOT NULL DEFAULT '0' ,
            `{PRODUCT_DESCRIPTION}` TEXT NULL ,
            `{PRODUCT_FOREIGNKEY_CATEGORY_ID}` INT NULL ,
            `{PRODUCT_FOREIGNKEY_SUB_CATEGORY_ID}` INT NULL ,
            `{CREATED_AT}` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP , 
            `{UPDATED_AT}` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ,
            `{PRODUCT_PRICE_UPDATE_DATETIME}` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP , 
            `{PRODUCT_IS_DELETED}` BOOLEAN NOT NULL DEFAULT 0 ,
            PRIMARY KEY (`{PRODUCT_ID}`) ,
            CONSTRAINT `{PRODUCT_CATEGORY_CONSTRAINT}` FOREIGN KEY (`{PRODUCT_FOREIGNKEY_CATEGORY_ID}`)
            REFERENCES `{DATABASE_NAME}`.`{CATEGORY_TABLE_NAME}`(`{CATEGORY_ID}`) ON DELETE SET NULL ON UPDATE CASCADE ,
            CONSTRAINT `{PRODUCT_SUB_CATEGORY_CONSTRAINT}` FOREIGN KEY (`{PRODUCT_FOREIGNKEY_SUB_CATEGORY_ID}`)
            REFERENCES `{DATABASE_NAME}`.`{SUB_CATEGORY_TABLE_NAME}`(`{SUB_CATEGORY_ID}`) ON DELETE SET NULL ON UPDATE CASCADE
            ) 
            ENGINE = InnoDB;"""
            self.mysql.query.execute(query)
            print(f"Table Creation and Structuring Successful = {PRODUCT_TABLE_NAME}\n ")
        except Exception as error:
            print(f"Development Error (Creating PRODUCT Table): {error}\n")
    
    
    
    # DEFINITION OF PRODUCT LOGS TABLE
    def product_logs_table(self):
        try:
            print(f"Table Creation and Structuring Initiated = {PRODUCT_LOGS_TABLE_NAME} ")
            query = f"""CREATE TABLE `{DATABASE_NAME}`.`{PRODUCT_LOGS_TABLE_NAME}`
            ( `{PRODUCT_LOGS_ID}` BIGINT NOT NULL AUTO_INCREMENT , 
            `{PRODUCT_LOGS_LOG}` TEXT NOT NULL ,
            `{PRODUCT_LOGS_FOREIGNKEY_PRODUCT_ID}` INT NULL DEFAULT NULL ,
            `{PRODUCT_LOGS_FOREIGNKEY_USER_ID}` INT NULL DEFAULT NULL , 
            `{CREATED_AT}` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP , 
            PRIMARY KEY (`{PRODUCT_LOGS_ID}`) ,
            CONSTRAINT `{PRODUCT_LOGS_PRODUCT_CONSTRAINT}` FOREIGN KEY (`{PRODUCT_LOGS_FOREIGNKEY_PRODUCT_ID}`)
            REFERENCES `{DATABASE_NAME}`.`{PRODUCT_TABLE_NAME}`(`{PRODUCT_ID}`) ON DELETE RESTRICT ON UPDATE CASCADE ,
            CONSTRAINT `{PRODUCT_LOGS_USER_CONSTRAINT}` FOREIGN KEY (`{PRODUCT_LOGS_FOREIGNKEY_USER_ID}`)
            REFERENCES `{DATABASE_NAME}`.`{USER_TABLE_NAME}`(`{USER_ID}`) ON DELETE RESTRICT ON UPDATE CASCADE
            )
            ENGINE = InnoDB;"""
            self.mysql.query.execute(query)
            print(f"Table Creation and Structuring Successful = {PRODUCT_LOGS_TABLE_NAME}\n ")
        except Exception as error:
            print(f"Development Error (Creating PRODUCT LOGS Table): {error}\n")



    # DEFINITION OF SALES ORDER TABLE
    def sales_order_table(self):
        try:
            print(f"Table Creation and Structuring Initiated = {SALES_ORDER_TABLE_NAME} ")
            query = f"""CREATE TABLE `{DATABASE_NAME}`.`{SALES_ORDER_TABLE_NAME}`
            ( `{SALES_ORDER_ID}` BIGINT NOT NULL AUTO_INCREMENT , 
            `{SALES_ORDER_C_NAME}` VARCHAR(255) NOT NULL ,
            `{SALES_ORDER_C_MOBILE}` VARCHAR(15) NOT NULL ,
            `{SALES_ORDER_C_EMAIL}` VARCHAR(255) NULL ,
            `{SALES_ORDER_PAYMENT_MODE}` ENUM {S_O_PAYMENT_MODE_OPTIONS} DEFAULT '{CASH}',
            `{SALES_ORDER_TOTAL_PRICE}` FLOAT(10,2) NOT NULL ,
            `{SALES_ORDER_FOREIGNKEY_USER_ID}` INT NULL DEFAULT NULL ,
            `{SALES_ORDER_STATUS}` ENUM {S_O_ORDER_STATUS_OPTIONS} DEFAULT '{ORDER_COMPLETED}',
            `{CREATED_AT}` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP , 
            PRIMARY KEY (`{SALES_ORDER_ID}`) ,
            CONSTRAINT `{SALES_ORDER_USER_CONSTRAINT}` FOREIGN KEY (`{SALES_ORDER_FOREIGNKEY_USER_ID}`)
            REFERENCES `{DATABASE_NAME}`.`{USER_TABLE_NAME}`(`{USER_ID}`) ON DELETE RESTRICT ON UPDATE CASCADE
            )
            ENGINE = InnoDB;"""
            self.mysql.query.execute(query)
            print(f"Table Creation and Structuring Successful = {SALES_ORDER_TABLE_NAME}\n ")
        except Exception as error:
            print(f"Development Error (Creating SALES ORDER Table): {error}\n")
    


    # DEFINITION OF SALES_ORDER_PRODUCT TABLE
    def sales_order_product_table(self):
        try:
            print(f"Table Creation and Structuring Initiated = {SALES_ORDER_PRODUCT_TABLE_NAME} ")
            query = f"""CREATE TABLE `{DATABASE_NAME}`.`{SALES_ORDER_PRODUCT_TABLE_NAME}`
            ( `{S_O_P_ID}` BIGINT NOT NULL AUTO_INCREMENT , 
            `{S_O_P_FOREIGNKEY_SALES_ORDER_ID}` BIGINT NULL DEFAULT NULL ,
            `{S_O_P_FOREIGNKEY_PRODUCT_ID}` INT NULL DEFAULT NULL ,
            `{PRODUCT_NAME}` VARCHAR(255) NOT NULL ,
            `{S_O_P_PRODUCT_PRICE}` FLOAT(10,2) NOT NULL ,
            `{S_O_P_PRODUCT_QUANTITY}` INT NOT NULL DEFAULT '1' ,
            `{S_O_P_PRODUCT_TOTAL_AMOUNT}` FLOAT(10,2) NOT NULL ,
            `{CANCELLED_QUANTITY}` INT NOT NULL DEFAULT 0 ,
            `{RETURNED_QUANTITY}` INT NOT NULL DEFAULT 0 , 
            `{REFUNDED_AMOUNT}` FLOAT(10,2) NOT NULL DEFAULT 0.00 ,
            `{CREATED_AT}` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP , 
            PRIMARY KEY (`{S_O_P_ID}`) ,
            CONSTRAINT `{S_O_P_SALES_ORDER_CONSTRAINT}` FOREIGN KEY (`{S_O_P_FOREIGNKEY_SALES_ORDER_ID}`)
            REFERENCES `{DATABASE_NAME}`.`{SALES_ORDER_TABLE_NAME}`(`{SALES_ORDER_ID}`) ON DELETE CASCADE ON UPDATE CASCADE , 
            CONSTRAINT `{S_O_P_PRODUCT_CONSTRAINT}` FOREIGN KEY (`{S_O_P_FOREIGNKEY_PRODUCT_ID}`)
            REFERENCES `{DATABASE_NAME}`.`{PRODUCT_TABLE_NAME}`(`{PRODUCT_ID}`) ON DELETE RESTRICT ON UPDATE CASCADE
            )
            ENGINE = InnoDB;"""
            self.mysql.query.execute(query)
            print(f"Table Creation and Structuring Successful = {SALES_ORDER_PRODUCT_TABLE_NAME}\n ")
        except Exception as error:
            print(f"Development Error (Creating SALES_ORDER_PRODUCT Table): {error}\n")



    # DEFINITION OF SALES ORDER LOGS TABLE
    def sales_order_logs_table(self):
        try:
            print(f"Table Creation and Structuring Initiated = {SALES_ORDER_LOGS_TABLE_NAME} ")
            query = f"""CREATE TABLE `{DATABASE_NAME}`.`{SALES_ORDER_LOGS_TABLE_NAME}`
            ( `{SALES_ORDER_LOGS_ID}` BIGINT NOT NULL AUTO_INCREMENT , 
            `{SALES_ORDER_LOGS_LOG}` TEXT NOT NULL ,
            `{SALES_ORDER_LOGS_FOREIGNKEY_SALES_ORDER_ID}` BIGINT NULL DEFAULT NULL ,
            `{SALES_ORDER_LOGS_FOREIGNKEY_USER_ID}` INT NULL DEFAULT NULL , 
            `{CREATED_AT}` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP , 
            PRIMARY KEY (`{PRODUCT_LOGS_ID}`) ,
            CONSTRAINT `{SALES_ORDER_LOGS_SALES_ORDER_CONSTRAINT}` FOREIGN KEY (`{SALES_ORDER_LOGS_FOREIGNKEY_SALES_ORDER_ID}`)
            REFERENCES `{DATABASE_NAME}`.`{SALES_ORDER_TABLE_NAME}`(`{SALES_ORDER_ID}`) ON DELETE RESTRICT ON UPDATE CASCADE ,
            CONSTRAINT `{SALES_ORDER_LOGS_USER_CONSTRAINT}` FOREIGN KEY (`{SALES_ORDER_LOGS_FOREIGNKEY_USER_ID}`)
            REFERENCES `{DATABASE_NAME}`.`{USER_TABLE_NAME}`(`{USER_ID}`) ON DELETE RESTRICT ON UPDATE CASCADE
            )
            ENGINE = InnoDB;"""
            self.mysql.query.execute(query)
            print(f"Table Creation and Structuring Successful = {SALES_ORDER_LOGS_TABLE_NAME}\n ")
        except Exception as error:
            print(f"Development Error (Creating SALES ORDER LOGS Table): {error}\n")



    # DEFINITION OF PURCHASE ORDER TABLE
    def purchase_order_table(self):
        try:
            print(f"Table Creation and Structuring Initiated = {PURCHASE_ORDER_TABLE_NAME} ")
            query = f"""CREATE TABLE `{DATABASE_NAME}`.`{PURCHASE_ORDER_TABLE_NAME}`
            ( `{PURCHASE_ORDER_ID}` BIGINT NOT NULL AUTO_INCREMENT , 
            `{PURCHASE_ORDER_FOREIGNKEY_SUPPLIER_ID}` INT NULL DEFAULT NULL ,
            `{SUPPLIER_NAME}` VARCHAR(255) NOT NULL ,
            `{SUPPLIER_CONTACT_1}` VARCHAR(15) NOT NULL ,
            `{SUPPLIER_ADDRESS}` VARCHAR(255) NULL ,
            `{SUPPLIER_GSTIN}` VARCHAR(255) NULL ,
            `{SUPPLIER_ORGANIZATION_NAME}` VARCHAR(255) NULL ,
            `{SUPPLIER_ORGANIZATION_CONTACT_1}` VARCHAR(15) NULL ,
            `{SUPPLIER_ORGANIZATION_ADDRESS}` VARCHAR(255) NULL ,
            `{PURCHASE_ORDER_PAYMENT_MODE}` ENUM {P_O_PAYMENT_MODE_OPTIONS} DEFAULT '{CHEQUE}',
            `{PURCHASE_ORDER_STATUS}` ENUM {P_O_ORDER_STATUS_OPTIONS} DEFAULT '{ORDER_PENDING}',
            `{PURCHASE_ORDER_TOTAL_PRICE}` DOUBLE(10,2) NOT NULL ,
            `{PURCHASE_ORDER_PAYMENT_STATUS}` ENUM {P_O_PAYMENT_STATUS_OPTIONS} DEFAULT '{PAYMENT_PENDING}',
            `{PURCHASE_ORDER_DELIVERY_STATUS}` ENUM {P_O_DELIVERY_STATUS_OPTIONS} DEFAULT '{DISPATCHED}',
            `{PURCHASE_ORDER_FOREIGNKEY_USER_ID}` INT NULL DEFAULT NULL ,
            `{CREATED_AT}` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP , 
            PRIMARY KEY (`{PURCHASE_ORDER_ID}`) ,
            CONSTRAINT `{PURCHASE_ORDER_USER_CONSTRAINT}` FOREIGN KEY (`{PURCHASE_ORDER_FOREIGNKEY_USER_ID}`)
            REFERENCES `{DATABASE_NAME}`.`{USER_TABLE_NAME}`(`{USER_ID}`) ON DELETE RESTRICT ON UPDATE CASCADE ,
            CONSTRAINT `{PURCHASE_ORDER_SUPPLIER_CONSTRAINT}` FOREIGN KEY (`{PURCHASE_ORDER_FOREIGNKEY_SUPPLIER_ID}`)
            REFERENCES `{DATABASE_NAME}`.`{SUPPLIER_TABLE_NAME}`(`{SUPPLIER_ID}`) ON DELETE RESTRICT ON UPDATE CASCADE
            )
            ENGINE = InnoDB;"""
            self.mysql.query.execute(query)
            print(f"Table Creation and Structuring Successful = {PURCHASE_ORDER_TABLE_NAME}\n ")
        except Exception as error:
            print(f"Development Error (Creating PURCHASE ORDER Table): {error}\n")
    


    # DEFINITION OF PURCHASE_ORDER_PRODUCT TABLE
    def purchase_order_product_table(self):
        try:
            print(f"Table Creation and Structuring Initiated = {PURCHASE_ORDER_PRODUCT_TABLE_NAME} ")
            query = f"""CREATE TABLE `{DATABASE_NAME}`.`{PURCHASE_ORDER_PRODUCT_TABLE_NAME}`
            ( `{P_O_P_ID}` BIGINT NOT NULL AUTO_INCREMENT , 
            `{P_O_P_FOREIGNKEY_PURCHASE_ORDER_ID}` BIGINT NULL DEFAULT NULL ,
            `{P_O_P_FOREIGNKEY_PRODUCT_ID}` INT NULL DEFAULT NULL ,
            `{PRODUCT_NAME}` VARCHAR(255) NOT NULL ,
            `{P_O_P_PRODUCT_PRICE}` FLOAT(10,2) NOT NULL ,
            `{P_O_P_PRODUCT_QUANTITY}` INT NOT NULL DEFAULT '1' ,
            `{P_O_P_PRODUCT_TOTAL_AMOUNT}` FLOAT(10,2) NOT NULL ,
            `{CANCELLED_QUANTITY}` INT NOT NULL DEFAULT 0 ,
            `{RETURNED_QUANTITY}` INT NOT NULL DEFAULT 0 , 
            `{REFUNDED_AMOUNT}` FLOAT(10,2) NOT NULL DEFAULT 0.00 ,
            `{CREATED_AT}` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP , 
            PRIMARY KEY (`{P_O_P_ID}`) ,
            CONSTRAINT `{P_O_P_PURCHASE_ORDER_CONSTRAINT}` FOREIGN KEY (`{P_O_P_FOREIGNKEY_PURCHASE_ORDER_ID}`)
            REFERENCES `{DATABASE_NAME}`.`{PURCHASE_ORDER_TABLE_NAME}`(`{PURCHASE_ORDER_ID}`) ON DELETE CASCADE ON UPDATE CASCADE , 
            CONSTRAINT `{P_O_P_PRODUCT_CONSTRAINT}` FOREIGN KEY (`{P_O_P_FOREIGNKEY_PRODUCT_ID}`)
            REFERENCES `{DATABASE_NAME}`.`{PRODUCT_TABLE_NAME}`(`{PRODUCT_ID}`) ON DELETE RESTRICT ON UPDATE CASCADE
            )
            ENGINE = InnoDB;"""
            self.mysql.query.execute(query)
            print(f"Table Creation and Structuring Successful = {PURCHASE_ORDER_PRODUCT_TABLE_NAME}\n ")
        except Exception as error:
            print(f"Development Error (Creating PURCHASE_ORDER_PRODUCT Table): {error}\n")



    # DEFINITION OF PURCHASE ORDER LOGS TABLE
    def purchase_order_logs_table(self):
        try:
            print(f"Table Creation and Structuring Initiated = {PURCHASE_ORDER_LOGS_TABLE_NAME} ")
            query = f"""CREATE TABLE `{DATABASE_NAME}`.`{PURCHASE_ORDER_LOGS_TABLE_NAME}`
            ( `{PURCHASE_ORDER_LOGS_ID}` BIGINT NOT NULL AUTO_INCREMENT , 
            `{PURCHASE_ORDER_LOGS_LOG}` TEXT NOT NULL ,
            `{PURCHASE_ORDER_LOGS_FOREIGNKEY_PURCHASE_ORDER_ID}` BIGINT NULL DEFAULT NULL ,
            `{PURCHASE_ORDER_LOGS_FOREIGNKEY_USER_ID}` INT NULL DEFAULT NULL , 
            `{CREATED_AT}` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP , 
            PRIMARY KEY (`{PRODUCT_LOGS_ID}`) ,
            CONSTRAINT `{PURCHASE_ORDER_LOGS_PURCHASE_ORDER_CONSTRAINT}` FOREIGN KEY (`{PURCHASE_ORDER_LOGS_FOREIGNKEY_PURCHASE_ORDER_ID}`)
            REFERENCES `{DATABASE_NAME}`.`{PURCHASE_ORDER_TABLE_NAME}`(`{PURCHASE_ORDER_ID}`) ON DELETE RESTRICT ON UPDATE CASCADE ,
            CONSTRAINT `{PURCHASE_ORDER_LOGS_USER_CONSTRAINT}` FOREIGN KEY (`{PURCHASE_ORDER_LOGS_FOREIGNKEY_USER_ID}`)
            REFERENCES `{DATABASE_NAME}`.`{USER_TABLE_NAME}`(`{USER_ID}`) ON DELETE RESTRICT ON UPDATE CASCADE
            )
            ENGINE = InnoDB;"""
            self.mysql.query.execute(query)
            print(f"Table Creation and Structuring Successful = {PURCHASE_ORDER_LOGS_TABLE_NAME}\n ")
        except Exception as error:
            print(f"Development Error (Creating PURCHASE ORDER LOGS Table): {error}\n")



    # DEFINITION OF RETURN CANCEL ORDER TABLE
    def return_cancel_order_table(self):
        try:
            print(f"Table Creation and Structuring Initiated = {RETURN_CANCEL_ORDER_TABLE_NAME} ")
            query = f"""CREATE TABLE `{DATABASE_NAME}`.`{RETURN_CANCEL_ORDER_TABLE_NAME}`
            ( `{RETURN_CANCEL_ORDER_ID}` BIGINT NOT NULL AUTO_INCREMENT , 
            `{RETURN_CANCEL_ORDER_FOREIGNKEY_SALES_ORDER_ID}` BIGINT NULL DEFAULT NULL ,
            `{RETURN_CANCEL_ORDER_FOREIGNKEY_PURCHASE_ORDER_ID}` BIGINT NULL DEFAULT NULL ,
            `{RETURN_CANCEL_ORDER_STATUS}` ENUM {RETURN_CANCEL_ORDER_STATUS_OPTIONS} DEFAULT '{ORDER_COMPLETED}',
            `{RETURN_CANCEL_ORDER_TOTAL_REFUND_AMOUNT}` FLOAT(10,2) NOT NULL ,
            `{RETURN_CANCEL_ORDER_FOREIGNKEY_USER_ID}` INT NULL DEFAULT NULL ,
            `{CREATED_AT}` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP , 
            PRIMARY KEY (`{RETURN_CANCEL_ORDER_ID}`) ,
            CONSTRAINT `{RETURN_CANCEL_ORDER_SALES_ORDER_CONSTRAINT}` FOREIGN KEY (`{RETURN_CANCEL_ORDER_FOREIGNKEY_SALES_ORDER_ID}`)
            REFERENCES `{DATABASE_NAME}`.`{SALES_ORDER_TABLE_NAME}`(`{SALES_ORDER_ID}`) ON DELETE RESTRICT ON UPDATE CASCADE ,
            CONSTRAINT `{RETURN_CANCEL_ORDER_PURCHASE_ORDER_CONSTRAINT}` FOREIGN KEY (`{RETURN_CANCEL_ORDER_FOREIGNKEY_PURCHASE_ORDER_ID}`)
            REFERENCES `{DATABASE_NAME}`.`{PURCHASE_ORDER_TABLE_NAME}`(`{PURCHASE_ORDER_ID}`) ON DELETE RESTRICT ON UPDATE CASCADE , 
            CONSTRAINT `{RETURN_CANCEL_ORDER_USER_CONSTRAINT}` FOREIGN KEY (`{RETURN_CANCEL_ORDER_FOREIGNKEY_USER_ID}`)
            REFERENCES `{DATABASE_NAME}`.`{USER_TABLE_NAME}`(`{USER_ID}`) ON DELETE RESTRICT ON UPDATE CASCADE
            )
            ENGINE = InnoDB;"""
            self.mysql.query.execute(query)
            print(f"Table Creation and Structuring Successful = {RETURN_CANCEL_ORDER_TABLE_NAME}\n ")
        except Exception as error:
            print(f"Development Error (Creating RETURN CANCEL ORDER Table): {error}\n")



    # DEFINITION OF RETURN_CANCEL_ORDER_PRODUCT TABLE
    def return_cancel_order_product_table(self):
        try:
            print(f"Table Creation and Structuring Initiated = {RETURN_CANCEL_ORDER_PRODUCT_TABLE_NAME} ")
            query = f"""CREATE TABLE `{DATABASE_NAME}`.`{RETURN_CANCEL_ORDER_PRODUCT_TABLE_NAME}`
            ( `{R_C_O_P_ID}` BIGINT NOT NULL AUTO_INCREMENT , 
            `{R_C_O_P_FOREIGNKEY_RETURN_CANCEL_ORDER_ID}` BIGINT NULL DEFAULT NULL ,
            `{R_C_O_P_FOREIGNKEY_PRODUCT_ID}` INT NULL DEFAULT NULL ,
            `{PRODUCT_NAME}` VARCHAR(255) NOT NULL ,
            `{R_C_O_P_PRODUCT_REFUND_AMOUNT}` FLOAT(10,2) NOT NULL ,
            `{R_C_O_P_PRODUCT_CANCEL_QUANTITY}` INT NOT NULL DEFAULT '0' ,
            `{R_C_O_P_PRODUCT_RETURN_QUANTITY}` INT NOT NULL DEFAULT '0' ,
            `{R_C_O_P_REASON}` TEXT NULL ,
            `{CREATED_AT}` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP , 
            PRIMARY KEY (`{R_C_O_P_ID}`) ,
            CONSTRAINT `{R_C_O_P_RETURN_CANCEL_ORDER_CONSTRAINT}` FOREIGN KEY (`{R_C_O_P_FOREIGNKEY_RETURN_CANCEL_ORDER_ID}`)
            REFERENCES `{DATABASE_NAME}`.`{RETURN_CANCEL_ORDER_TABLE_NAME}`(`{RETURN_CANCEL_ORDER_ID}`) ON DELETE CASCADE ON UPDATE CASCADE , 
            CONSTRAINT `{R_C_O_P_PRODUCT_CONSTRAINT}` FOREIGN KEY (`{R_C_O_P_FOREIGNKEY_PRODUCT_ID}`)
            REFERENCES `{DATABASE_NAME}`.`{PRODUCT_TABLE_NAME}`(`{PRODUCT_ID}`) ON DELETE RESTRICT ON UPDATE CASCADE
            )
            ENGINE = InnoDB;"""
            self.mysql.query.execute(query)
            print(f"Table Creation and Structuring Successful = {RETURN_CANCEL_ORDER_PRODUCT_TABLE_NAME}\n ")
        except Exception as error:
            print(f"Development Error (Creating RETURN_CANCEL_ORDER_PRODUCT Table): {error}\n")