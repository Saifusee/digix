import tkinter as tk
from tkinter import ttk
import datetime
from app.main.other_components.custom_combobx import CustomCombobox
from app.main.other_components.custom_text import CustomText
from database.dbconnection import Connection
from error import ErrorModal
from CONSTANT.index import *

class UpdateEmploymentStatus(tk.Toplevel):
    def __init__(self, container, user_id, logged_in_user, refreshedTableMethod, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        if type(container) == None.__class__:
            pass
        else:
            centerTkinterToplevel(container, self, dx=600, dy=250)

        # Setting up db connection
        mysql = Connection()

        
        self.configure(background=TTK_FRAME_DEFAULT_BG_COLOR)
        self.columnconfigure(0, weight=1)
        self.user_id = user_id
        self.logged_in_user = logged_in_user
        self.username = ""
        self.selected_user_authority = ""
        self.old_status = ""
        self.value_list = ""
        self.combobox_data = tk.StringVar()

        # Update Data
        self.fetchData(mysql)
        head_lb = ttk.Label(self, text="Update Employment Status", style="QuantityPopUpLabel.TLabel")
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
        self.combobox.bind("<<ComboboxSelected>>", self.comboboxSelected)

        self.text_frame = ttk.Frame(self)
        self.text_frame.columnconfigure(0, weight=1)
        self.reason_entry = CustomText(
            self.text_frame,
            height=5,
            width=30,
            wrap=tk.NONE,
            font=("TkdefaultFont", 10, "bold")
            )
        self.reason_entry.grid(row=0, column=0, sticky="nsew")
        self.reason_entry.grid_scrollbar(row=0, column=0)

        self.submit_button = ttk.Button(self, text="Submit", command=lambda: self.submitData(mysql, lambda: refreshedTableMethod()), style="SignButton.TButton")
        self.submit_button.grid(row=4, column=0, sticky="nsew", padx=10, pady=10)

        self.error_lb = ttk.Label(self, style="ErrorLoginRegisterLabel.TLabel", wraplength=250)

        # If selected user is admin then other user can't modify them
        if self.selected_user_authority == AUTHORITY_PRIMARY and not (self.logged_in_user[USER_AUTHORITY] == AUTHORITY_PRIMARY):
            self.combobox.configure(state="disabled")
            self.submit_button.configure(state="disabled")
            self.reason_entry.configure(state="disabled")
            self.error_lb.configure(text="This operation is restricted for users other than admins")
            self.error_lb.grid(row=5, column=0, sticky="ew", padx=10, pady=10)
    


    # When Combobox is selected
    def comboboxSelected(self, event):
        if self.combobox_data.get() == NOT_EMPLOYED or self.combobox_data.get() == ABSCONDED:
            self.text_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        else:
            self.text_frame.grid_forget()



    # Fetch Data
    def fetchData(self, mysql):
        query = f"SELECT * FROM `{DATABASE_NAME}`.`{USER_TABLE_NAME}` WHERE `{USER_ID}` = {self.user_id}"
        mysql.query.execute(query)
        data = mysql.query.fetchall()[0]

        self.username = data[USERNAME]
        self.old_status = data[EMPLOYMENT_STATUS]
        self.selected_user_authority = data[USER_AUTHORITY]
        self.combobox_data.set(self.old_status)
        self.value_list = list(EMPLOYMENT_OPTIONS)
            


    # Submit values
    def submitData(self, mysql, refreshedTableMethod):
        # If there's no reason for leaving and abcsond
        if (self.combobox_data.get() == NOT_EMPLOYED or self.combobox_data.get() == ABSCONDED) and len(self.reason_entry.get(1.0, "end-1c").strip()) == 0:
            self.error_lb.configure(text="Reason for job resignation cannot be empty.")
            self.error_lb.grid(row=5, column=0, sticky="ew", padx=10, pady=10)
        else:
            self.combobox.configure(state="disabled")
            self.submit_button.configure(state="disabled")
            self.reason_entry.configure(state="disabled")
            try:
                # Ensuring that logged in user is not normal employee during this operation
                query = f"SELECT * FROM `{DATABASE_NAME}`.`{USER_TABLE_NAME}` WHERE `{USER_ID}` = {self.logged_in_user[USER_ID]}"
                mysql.query.execute(query)
                logged_user_data = mysql.query.fetchall()[0]
                if logged_user_data[USER_AUTHORITY] == AUTHORITY_TERTIARY:
                    self.error_lb.configure(text="You are no longer eligible to perform this operation")
                    self.error_lb.grid(row=5, column=0, sticky="ew", padx=10, pady=10)
                elif self.old_status == self.combobox_data.get():
                    self.error_lb.configure(text="Nothing to update")
                    self.error_lb.grid(row=5, column=0, sticky="ew", padx=10, pady=10)
                else:
                    mod_1 = ""
                    mod = ""
                    # if user is absconded or resigned
                    if self.combobox_data.get() == NOT_EMPLOYED or self.combobox_data.get() == ABSCONDED:
                        mod_1 = f""" , `{DATE_OF_LEAVING}` = '{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}' , 
                        `{LEAVE_REASON}` = %s """
                    # if user is rehired
                    elif self.combobox_data.get() == EMPLOYED:
                        mod = f""" , `{DATE_OF_REHIRING}` = '{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}' ,
                        `{USER_AUTHORITY}` = '{AUTHORITY_TERTIARY}' """
                    # Updating User Record
                    query = f"UPDATE `{DATABASE_NAME}`.`{USER_TABLE_NAME}` SET `{EMPLOYMENT_STATUS}` = '{self.combobox_data.get()}' {mod_1} {mod} WHERE `{USER_ID}` = {self.user_id}"
                    if len(mod_1) > 0:
                        mysql.query.execute(query, (self.reason_entry.get(1.0, "end-1c").strip(),))
                    else:
                        mysql.query.execute(query)
                    mysql.db_connection.commit()

                    ## Creating User Log
                        
                    # Log for Target User
                    query_log = f"""INSERT INTO `{DATABASE_NAME}`.`{USER_LOGS_TABLE_NAME}`
                    (`{USER_LOGS_LOG}`, `{USER_LOGS_FOREIGNKEY_ACTIVE_USER_ID}`, `{USER_LOGS_FOREIGNKEY_TARGET_USER_ID}`)
                    VALUES (%s, %s, %s);"""
                    # If user is absconded or resigned then create this log 
                    if self.combobox_data.get() == NOT_EMPLOYED or self.combobox_data.get() == ABSCONDED:
                        a = f"User no longer work for this organization."
                        mysql.query.execute(query_log, (a, self.logged_in_user[USER_ID], self.user_id))
                        mysql.db_connection.commit()
                    # If user is rehired
                    elif self.combobox_data.get() == EMPLOYED:
                        a = f"User is rehired to this organization with user authority '{AUTHORITY_TERTIARY}'."
                        mysql.query.execute(query_log, (a, self.logged_in_user[USER_ID], self.user_id))
                        mysql.db_connection.commit()

                    # Create basic log
                    a = f"User employment status updated from '{self.old_status}' to '{self.combobox_data.get()}'"
                    mysql.query.execute(query_log, (a, self.logged_in_user[USER_ID], self.user_id))
                    mysql.db_connection.commit()
                    # Log for Active User
                    b = f"User changed employment status user '{self.username}' with user id {self.user_id} from '{self.old_status}' to '{self.combobox_data.get()}'"
                    mysql.query.execute(query_log, (b, None, self.logged_in_user[USER_ID]))
                    mysql.db_connection.commit()


                    self.error_lb.configure(style="SuccessfulLoginRegisterLabel.TLabel", text="Record Updated Successfully")
                    self.error_lb.grid(row=5, column=0, sticky="ew", padx=10, pady=10)

                    # Refreshed Treeview
                    refreshedTableMethod()
            except Exception as error:
                print(f"Development Error (Updating User Authority): {error}")
                ErrorModal("Something went wrong.")