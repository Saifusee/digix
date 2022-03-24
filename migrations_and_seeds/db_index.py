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
            print(f"Development Error = {errors}")
    
    def delete_database_and_create_new_one(self):
        try:
            while (self.cond1):
                
                self.inp1 = input("Do you want to delete existing database and create new one?\nPress 'Y' or 'y' for 'Yes'\nPress 'N' or 'n' for 'No or Exit'\n")
                
                if ((self.inp1 == 'Y') or (self.inp1 == 'y') or (self.inp1 == 'YES') or (self.inp1 == 'yes') or (self.inp1 == 'Yes')):
                    #Seeding Dummy data un database
                    self.table_structure = TableStructure(self.db_conn)
                    print("\nDatabase deletion and new database creation successfull")
                    self.cond1 = False
                    
                elif ((self.inp1 == 'N') or (self.inp1 == 'n') or (self.inp1 == 'NO') or (self.inp1 == 'No') or (self.inp1 == 'nO') or (self.inp1 == 'no')):
                    print("\nExecution Completed. Thank You")
                    self.cond1 = False
                    
                else:
                    print("\nInvalid input, Try again.")
                    self.cond1 = True
        except Exception as errors:
            print(f"Development Error = {errors}")
                
    def seed_data(self):
        try:
            while (self.cond2):
                
                self.inp2 = input("\nDo you want to seed data in database?\nPress 'Y' or 'y' for 'Yes'\nPress 'N' or 'n' for 'No or Exit'\n")
                
                if ((self.inp2 == 'Y') or (self.inp2 == 'y') or (self.inp2 == 'YES') or (self.inp2 == 'yes') or (self.inp2 == 'Yes')):
                    #Seeding Dummy data un database
                    self.seeds = Seeds(self.db_conn) 
                    print("\nSeeding Successfull")
                    self.cond2 = False
                    
                elif ((self.inp2 == 'N') or (self.inp2 == 'n') or (self.inp2 == 'NO') or (self.inp2 == 'No') or (self.inp2 == 'nO') or (self.inp2 == 'no')):
                    print("\nExecution Completed. Thank You")
                    self.cond2 = False
                else:
                    print("\nInvalid input, Try again.")
                    self.cond2 = True
                    
        except Exception as errors:
            print(f"Development Error = {errors}")

database_migrations_and_seeds_index = DatabaseMigrationsAndSeedsIndex()
database_migrations_and_seeds_index.delete_database_and_create_new_one()
database_migrations_and_seeds_index.seed_data()