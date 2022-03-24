import sys
sys.path.append("..")
from cusimp.constants import *
import mysql.connector as driver

class Connection():
    def __init__(self):
        #DATABASE CONFIGURATION
        self.db_connection = driver.connect(
            host=DATABASE_host,
            user=DATABASE_USER,
            password=DATABASE_PASSWORD,
            database=DATABASE_NAME
        )
        self.query = self.db_connection.cursor(dictionary=True)

