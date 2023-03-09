from CONSTANT.table_constants import *
from CONSTANT.application_setting_constants import * 
from PIL import ImageTk
import mysql.connector as driver

# Get Shop or Organization Details
def getShopDetails():
    #DATABASE CONFIGURATION
    db_connection = driver.connect(
        host=DATABASE_host,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD   
    )
    query = db_connection.cursor(dictionary=True)

    query.execute(f"SELECT * FROM `{DATABASE_NAME}`.`{SHOP_TABLE_NAME}` WHERE `{SHOP_ID}` = 1")
    shop_details = query.fetchall()[0]

    
    return shop_details

    