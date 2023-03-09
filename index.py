from os import path
import sys
sys.path.append(path.dirname(__file__))
import tkinter as tk
from tkinter import ttk
from authenticate.public_page import PublicPage
from database import dbconnection
from app import app
from error_index import *


try: 
    # Establishing Connection to Database
    try:
        sql = dbconnection.Connection()
    except Exception:
        raise Exception("Db fail")

    # Setting up app logo to file directory
    sql.query.execute(f"SELECT `{SHOP_LOGO}` FROM `{DATABASE_NAME}`.`{SHOP_TABLE_NAME}` WHERE `{SHOP_ID}` = 1;")
    shop_logo_binary_data = sql.query.fetchall()[0][SHOP_LOGO]
    if type(shop_logo_binary_data) == None.__class__:
        pass
    else:
        image_file = open(path.join(PATH_TO_IMAGES, FILE_APP_LOGO), "wb")
        image_file.write(shop_logo_binary_data)
        image_file.close()
    
    # Rendering Public Pages 
    try:
        public_page = PublicPage(sql) 
    except Exception:
        raise Exception("Authentication fail")
    
    # Exceuting Main Application Window
    if (public_page.user != {}): #if Authentication is successful 
        try:
            main_window = app.AppWindow(public_page.user, sql) 
        except Exception:
            raise Exception()
    else:
        pass
    # # To hold pyinstaller cmd window
    # input("Application running successfully, please press any key....")
except Exception as errors:
    print(f"Development Error (Index.py): {errors}")
    # # To hold pyinstaller cmd window
    # input("Application execution terminated with errors, please press any key....")
    if str(errors) == "Db fail":
        ErrorModalForIndex("Something went wrong, connection to database got interrupted, please check your internet connection and try again.")
    elif str(errors) == "Authentication fail":
        ErrorModalForIndex("Something went wrong, connection to authetication module failed, please contact your software developer.")
    else:
        ErrorModalForIndex("Something went wrong, please try again.")
    
    
# import datetime   
# # Establishing Connection to Database
# sql = dbconnection.Connection()

# # Setting up app logo to file directory
# sql.query.execute(f"SELECT `{SHOP_LOGO}` FROM `{DATABASE_NAME}`.`{SHOP_TABLE_NAME}` WHERE `{SHOP_ID}` = 1;")
# shop_logo_binary_data = sql.query.fetchall()[0][SHOP_LOGO]
# # Setting up app logo to file directory
# if type(shop_logo_binary_data) == None.__class__:
#     pass
# else:
#     image_file = open(path.join(PATH_TO_IMAGES, FILE_APP_LOGO), "wb")
#     image_file.write(shop_logo_binary_data)
#     image_file.close()

# #######          ADMIN          ##########
# userexm = {
#     USER_ID: 2,
#     EMAIL: 'admin2@gmail.com',
#     USERNAME: 'admin2',
#     PASSWORD: 'QQ@@qq22',
#     USER_AUTHORITY: AUTHORITY_PRIMARY,
#     DATE_OF_JOINING: datetime.datetime(2022, 3, 1, 0, 0),
#     DATE_OF_LEAVING: datetime.datetime(2022, 3, 30, 0, 0)
# }
# main_window = app.AppWindow(userexm, sql)



# ##########          MANAGEMENT          ##########
# userexm = {
#     USER_ID: 4,
#     EMAIL: 'management2@gmail.com',
#     USERNAME: 'management2',
#     PASSWORD: 'QQ@@qq22',
#     USER_AUTHORITY: AUTHORITY_SECONDARY,
#     DATE_OF_JOINING: datetime.datetime(2022, 3, 1, 0, 0),
#     DATE_OF_LEAVING: datetime.datetime(2022, 3, 30, 0, 0)
# }
# main_window = app.AppWindow(userexm, sql)

# ##########          EMPLOYEE          ##########
# userexm = {
#     USER_ID: 6,
#     EMAIL: 'employee2@gmail.com',
#     USERNAME: 'employee2',
#     PASSWORD: 'QQ@@qq22',
#     USER_AUTHORITY: AUTHORITY_TERTIARY,
#     DATE_OF_JOINING: datetime.datetime(2022, 3, 1, 0, 0),
#     DATE_OF_LEAVING: datetime.datetime(2022, 3, 30, 0, 0)
# }
# main_window = app.AppWindow(userexm, sql)
