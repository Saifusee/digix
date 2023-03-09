from CONSTANT.index import *
import mysql.connector as driver

class Connection():
    def __init__(self):
        #DATABASE CONFIGURATION
        self.db_connection = driver.connect(
            host=DATABASE_host,
            user=DATABASE_USER,
            password=DATABASE_PASSWORD   
        )
        self.query = self.db_connection.cursor(dictionary=True)
        # Creating Database if it not already exists
        self.query.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME};")
        # driver instance
        self.driver = driver
        
        

