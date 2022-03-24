import sys
sys.path.append("..")
from cusimp.constants import *
from cusimp.table_constants import *

class Seeds():
    def __init__(self, mysql):
        self.mysql = mysql
    
        #Seeding to USER TABLE
        self.seed_user_table()
    
    #DEFINITION OF USER TABLE
    def seed_user_table(self):
        print(f"\nInitiating Seeding Table = {USER_TABLE_NAME}")
        query = f"INSERT INTO {USER_TABLE_NAME} ({USERNAME}, {EMAIL}, {PASSWORD}) VALUES (%s, %s, %s)"
        values = [
        ('admin1', 'admin1@gmail.com', 'QQ@@qq22'),
        ('admin2', 'admin2@gmail.com', 'QQ@@qq22'),
        ('admin3', 'admin3@gmail.com', 'QQ@@qq22'),
        ('admin4', 'admin4@gmail.com', 'QQ@@qq22'),
        ('admin5', 'admin5@gmail.com', 'QQ@@qq22'),
        ]
        self.mysql.query.executemany(query, values)
        self.mysql.db_connection.commit()
        print(f"Table Seeding Successful = {USER_TABLE_NAME} ")
        