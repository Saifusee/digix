import sys
sys.path.append("..")
from database.dbconnection import Connection
from migrations_and_seeds.table_structure import TableStructure
from migrations_and_seeds.seeds import Seeds

class DatabaseMigrationsAndSeedsIndex():
    def __init__(self):
        try:
            self.db_conn = Connection()
            self.cond1 = bool(True)
            self.cond2 = bool(True)
        except Exception as errors:
            print(f"Development Error (Establishing connection to database) = {errors}")
    
    def delete_database_and_create_new_one(self):
        try:
            while (self.cond1):
                print("\n/////////////////////////////////////////////////////////////////////////////////")
                print("/////////////////////////////////////////////////////////////////////////////////")
                self.inp1 = input("Do you want to delete existing database and create new one?\nPress 'Y' or 'y' for 'Yes'\nPress 'N' or 'n' for 'No or Exit'\n")
                
                if ((self.inp1.lower().strip() == 'y') or (self.inp1.lower().strip() == 'yes')):
                    #Seeding Dummy data un database
                    self.table_structure = TableStructure(self.db_conn)
                    print("\n---------------- Database deletion and new database creation successful -----------------")
                    self.cond1 = False
                    
                elif ((self.inp1.lower().strip() == 'n') or (self.inp1.lower().strip() == 'no') or (self.inp1.lower().strip() == 'e') or (self.inp1.lower().strip() == 'exit')):
                    print("\n---------------- Execution Completed. Thank You ----------------")
                    self.cond1 = False
                    
                else:
                    print("\nInvalid input, Try again.")
                    self.cond1 = True
        except Exception as errors:
            print(f"Development Error = {errors}")
                
    def seed_data(self):
        try:
            while (self.cond2):
                print("\n/////////////////////////////////////////////////////////////////////////////////")
                print("/////////////////////////////////////////////////////////////////////////////////")
                self.inp2 = input("\nDo you want to seed data in database?\nPress 'Y' or 'y' for 'Yes'\nPress 'N' or 'n' for 'No or Exit'\n")
                
                if ((self.inp2.lower().strip() == 'y') or (self.inp2.lower().strip() == 'yes')):
                    print("\n---------------- Seeding of dummy data into database initiated.... ----------------")
                    #Seeding Dummy data un database
                    self.seeds = Seeds(self.db_conn) 
                    print("\n-------------------------------- Seeding Successful --------------------------------")
                    self.cond2 = False
                    
                elif ((self.inp2.lower().strip() == 'n') or (self.inp2.lower().strip() == 'no') or (self.inp2.lower().strip() == 'e') or (self.inp2.lower().strip() == 'exit')):
                    print("\n---------------- Execution Completed. Thank You ----------------")
                    self.cond2 = False
                else:
                    print("\nInvalid input, Try again.")
                    self.cond2 = True
                    
        except Exception as errors:
            print(f"Development Error = {errors}")

database_migrations_and_seeds_index = DatabaseMigrationsAndSeedsIndex()
database_migrations_and_seeds_index.delete_database_and_create_new_one()
database_migrations_and_seeds_index.seed_data()