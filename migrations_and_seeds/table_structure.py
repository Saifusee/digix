import sys
sys.path.append("..")
from cusimp.constants import *
from cusimp.table_constants import *

class TableStructure():
    def __init__(self, mysql):
        self.mysql = mysql
        
        #Deleting Existing Datbase and Creating New Database
        mysql.query.execute(f"DROP DATABASE {DATABASE_NAME}")
        mysql.query.execute(f"CREATE DATABASE {DATABASE_NAME}")
        mysql.query.execute(f"USE {DATABASE_NAME}")
        
        #CREATE USER TABLE
        self.user_table()
        self.otp_table()
    
    #DEFINITION OF USER TABLE
    def user_table(self):
        try:
            query = f"""CREATE TABLE `{DATABASE_NAME}`.`{USER_TABLE_NAME}`
            ( `{USER_ID}` INT NOT NULL AUTO_INCREMENT ,
            `{USERNAME}` VARCHAR(255) ,
            `{EMAIL}` VARCHAR(255) NOT NULL ,
            `{PASSWORD}` TEXT ,
            `{D_O_JOINING}` DATETIME ,
            `{D_O_LEAVING}` DATETIME ,
            PRIMARY KEY (`{USER_ID}`),
            UNIQUE (`{USERNAME}`),
            UNIQUE (`{EMAIL}`)) ENGINE = InnoDB"""
            self.mysql.query.execute(query)
        except Exception as error:
            print(f"Development Error (Creating User Table): {error}")
        
    #DEFINITION OF OTP TABLE
    def otp_table(self):
        try:
            query = f"""CREATE TABLE `{DATABASE_NAME}`.`{OTP_TABLE_NAME}`
            ( `{OTP_ID}` INT NOT NULL AUTO_INCREMENT ,
            `{OTP_REFERENCE}` VARCHAR(255) NOT NULL ,
            `{OTP_VALUE}` INT(8) NOT NULL ,
            PRIMARY KEY (`{OTP_ID}`) ) ENGINE = InnoDB"""
            self.mysql.query.execute(query)
        except Exception as error:
            print(f"Development Error (Creating OTP Table): {error}")
    