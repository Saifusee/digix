from cusimp.imports_for_index_file import *

# Connecting to MYSQL Database
sql = dbconnection.Connection() 

# Executing Public Pages Login and Register
public_page = PublicPage(sql) 

# Exceuting Main Application Window
if (public_page.user != {}): #if Authentication is successful 
    main_window = AppWindow(public_page.user) 
else:
    pass
    


# userexm = {
#     'user_id': 4,
#     'email': 'admin1@gmail.com',
#     'username': 'admin1',
#     'password': 'QQ@@qq22',
#     'date_of_joining': datetime.datetime(2022, 3, 1, 0, 0),
#     'date_of_leaving': datetime.datetime(2022, 3, 30, 0, 0)
# }
# main_window = AppWindow(userexm)
