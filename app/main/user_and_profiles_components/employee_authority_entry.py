import tkinter as tk
from tkinter import ttk
from app.main.other_components.custom_combobx import CustomCombobox
from database.dbconnection import Connection
from error import ErrorModal
from CONSTANT.index import *

class UpdateEmployeeAuthority(tk.Toplevel):
    def __init__(self, container, user_id, logged_in_user, refreshedTableMethod, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        if type(container) == None.__class__:
            pass
        else:
            centerTkinterToplevel(container, self, dx=600, dy=250)

        # Setting up database conncetion
        mysql = Connection()

        self.geometry("275x275")
        self.configure(background=TTK_FRAME_DEFAULT_BG_COLOR)
        self.columnconfigure(0, weight=1)
        self.user_id = user_id
        self.logged_in_user = logged_in_user
        self.username = ""
        self.old_autohrity = ""
        self.value_list = ""
        self.combobox_data = tk.StringVar()

        # Update Data
        self.fetchData(mysql)
        head_lb = ttk.Label(self, text="Update Employee Authority", style="QuantityPopUpLabel.TLabel")
        head_lb.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        head_lb = ttk.Label(self, text=f"Username: {self.username}", style="QuantityPopUpLabel.TLabel")
        head_lb.grid(row=1, column=0, sticky="ew", padx=10, pady=10)

        self.combobox = CustomCombobox(
            self,
            valueList=self.value_list, 
            textvariable=self.combobox_data,
            state="readonly",
            justify="center",
            font=("TkDefaultFont", 10, "bold"),
            style="ShowProduct.TCombobox"
            )
        self.combobox.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        self.submit_button = ttk.Button(self, text="Submit", command=lambda: self.submitData(mysql, lambda: refreshedTableMethod()), style="SignButton.TButton")
        self.submit_button.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)

        self.error_lb = ttk.Label(self, style="ErrorLoginRegisterLabel.TLabel", wraplength=250)


        # If selected user is admin then other user can't modify them
        if self.old_autohrity == AUTHORITY_PRIMARY and not (self.logged_in_user[USER_AUTHORITY] == AUTHORITY_PRIMARY):
            self.combobox.configure(state="disabled")
            self.submit_button.configure(state="disabled")
            self.error_lb.configure(text="This operation is restricted for users other than admins")
            self.error_lb.grid(row=4, column=0, sticky="ew", padx=10, pady=10)
    


    # Fetch Data
    def fetchData(self, mysql):
        query = f"SELECT * FROM `{DATABASE_NAME}`.`{USER_TABLE_NAME}` WHERE `{USER_ID}` = {self.user_id}"
        mysql.query.execute(query)
        data = mysql.query.fetchall()[0]

        self.username = data[USERNAME]
        self.old_autohrity = data[USER_AUTHORITY]
        self.combobox_data.set(self.old_autohrity)
        self.value_list = list(AUTHORITY_OPTIONS)
        # If logged in user is not Admin then he cannot make more admins
        if not (self.logged_in_user[USER_AUTHORITY] == AUTHORITY_PRIMARY):
            self.value_list.remove(AUTHORITY_PRIMARY)






    # Submit values
    def submitData(self, mysql, refreshedTableMethod):
        self.combobox.configure(state="disabled")
        self.submit_button.configure(state="disabled")
        try:
            # Ensuring that logged in user is not normal employee during this operation
            query = f"SELECT * FROM `{DATABASE_NAME}`.`{USER_TABLE_NAME}` WHERE `{USER_ID}` = {self.logged_in_user[USER_ID]}"
            mysql.query.execute(query)
            logged_user_data = mysql.query.fetchall()[0]
            if logged_user_data[USER_AUTHORITY] == AUTHORITY_TERTIARY:
                self.error_lb.configure(text="You are no longer eligible to perform this operation")
                self.error_lb.grid(row=4, column=0, sticky="ew", padx=10, pady=10)
            else:
                # Updating User Record
                query = f"UPDATE `{DATABASE_NAME}`.`{USER_TABLE_NAME}` SET `{USER_AUTHORITY}` = '{self.combobox_data.get()}' WHERE `{USER_ID}` = {self.user_id}"
                mysql.query.execute(query)
                mysql.db_connection.commit()

                ## Creating User Log
                # Log for Target User
                query_log = f"""INSERT INTO `{DATABASE_NAME}`.`{USER_LOGS_TABLE_NAME}`
                (`{USER_LOGS_LOG}`, `{USER_LOGS_FOREIGNKEY_ACTIVE_USER_ID}`, `{USER_LOGS_FOREIGNKEY_TARGET_USER_ID}`)
                VALUES (%s, %s, %s);"""
                a = f"User authority changed from '{self.old_autohrity}' to '{self.combobox_data.get()}'"
                mysql.query.execute(query_log, (a, self.logged_in_user[USER_ID], self.user_id))
                mysql.db_connection.commit()
                # Log for Active User
                b = f"User changed authority of user '{self.username}' with user id {self.user_id} from '{self.old_autohrity}' to '{self.combobox_data.get()}'"
                mysql.query.execute(query_log, (b, None, self.logged_in_user[USER_ID]))
                mysql.db_connection.commit()

                self.error_lb.configure(style="SuccessfulLoginRegisterLabel.TLabel", text="Record Updated Successfully")
                self.error_lb.grid(row=4, column=0, sticky="ew", padx=10, pady=10)

                # Refreshed Treeview
                refreshedTableMethod()
        except Exception as error:
            print(f"Development Error (Updating User Authority): {error}")
            ErrorModal("Something went wrong.")