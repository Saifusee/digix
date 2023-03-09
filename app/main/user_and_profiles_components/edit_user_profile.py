import tkinter as tk
from tkinter import ttk
from CONSTANT.index import *
from app.main.other_components.custom_text import CustomText
from app.base import Base
from error import ErrorModal
import re
from app.main.user_and_profiles_components.update_username_toplevel import UpdateUsername
from app.main.user_and_profiles_components.update_email_toplevel import UpdateEmail
from app.main.user_and_profiles_components.update_password_toplevel import UpdatePassword

class EditUserProfile(ttk.Frame, Base):
    def __init__(self, container, mysql, user):

        # Note: when we call, instance.method(), method automatically take instance as first argument which we define as self
        # when we call, Class.method(), method need instance manually as first argument bcz it doesn't know whic one to take
        ttk.Frame.__init__(self, container)
        Base.__init__(self, mysql, user)
                
        self.primary_contact_data = tk.StringVar()
        self.secondary_contact_data = tk.StringVar()

        
        headlb = ttk.Label(self, text="Update Profile", style="ApplicationLabel1.TLabel", anchor="center")
        headlb.grid(row=0, column=0, columnspan=2, sticky="ew")
        
        lb = ttk.Label(self, text="Username: ", style="LoginLabel.TLabel")
        lb.grid(row=1, column=0, sticky="w")

        self.username_label = ttk.Label(self, style="LoginLabel.TLabel")
        self.username_label.grid(row=1, column=1)

        lb = ttk.Label(self, text="E-Mail: ", style="LoginLabel.TLabel")
        lb.grid(row=2, column=0, sticky="w")

        self.email_label = ttk.Label(self, style="LoginLabel.TLabel")
        self.email_label.grid(row=2, column=1)

        lb = ttk.Label(self, text="Primary Contact: {}".format(self.superscript("*")), style="LoginLabel.TLabel")
        lb.grid(row=3, column=0, sticky="w")
        
        input = ttk.Entry(self, width=60,  textvariable=self.primary_contact_data, font=("TkdefaultFont", 10, "bold"))
        input.grid(row=3, column=1, padx=(10,10), pady=(10,10))
        self.bindFormFields(input, self.validate_input)

        lb = ttk.Label(self, text="Secondary Contact: ", style="LoginLabel.TLabel")
        lb.grid(row=4, column=0, sticky="w")
        
        input = ttk.Entry(self, width=60,  textvariable=self.secondary_contact_data, font=("TkdefaultFont", 10, "bold"))
        input.grid(row=4, column=1, padx=(10,10), pady=(10,10))
        self.bindFormFields(input, self.validate_input)

        lb = ttk.Label(self, text="Address: {}".format(self.superscript("*")), style="LoginLabel.TLabel")
        lb.grid(row=5, column=0, sticky="w")
        
        self.address_entry = CustomText(
            self,
            height=5,
            wrap=tk.NONE,
            font=("TkdefaultFont", 10, "bold")
            )
        self.address_entry.grid(row=5, column=1, padx=(10,10), pady=(10,10))
        self.address_entry.grid_scrollbar(row=5, column=1)
        self.bindFormFields(self.address_entry, self.validate_input)

        self.fetchUserDetails()

        self.button = ttk.Button(self,
                            text="Submit",
                            command=self.commandSubmitCategory,
                            style="SignButton.TButton"
                            )
        self.button.grid(row=6, column=0, columnspan=2, sticky="ew", padx=(10,10), pady=(20,20))

        fr = ttk.Frame(self)
        fr.columnconfigure(0, weight=1)
        fr.columnconfigure(1, weight=1)
        fr.columnconfigure(2, weight=1)
        fr.grid(row=7, column=0, columnspan=2, sticky="nsew", padx=(10,10), pady=(10,10))

        update_username_button = ttk.Button(
            fr, 
            text="Change Username", 
            command=lambda: UpdateUsername(self, self.current_user[USER_ID], self.mysql), 
            style="SingleRecordLinkButton.TButton"
            )
        update_username_button.grid(row=0, column=0, sticky="ns")

        update_email_button = ttk.Button(
            fr, 
            text="Change E-Mail", 
            command=lambda: UpdateEmail(self, self.current_user[USER_ID], self.mysql), 
            style="SingleRecordLinkButton.TButton"
            )
        update_email_button.grid(row=0, column=1, sticky="ns")

        update_email_button = ttk.Button(
            fr, 
            text="Change Password", 
            command=lambda: UpdatePassword(self, self.current_user[USER_ID], self.mysql), 
            style="SingleRecordLinkButton.TButton"
            )
        update_email_button.grid(row=0, column=2, sticky="ns")
        
        self.lbsuc = ttk.Label(self, anchor="center")




    # Fetch Shop Details
    def fetchUserDetails(self):
        que = f"SELECT * FROM `{DATABASE_NAME}`.`{USER_TABLE_NAME}` WHERE `{USER_ID}` = {self.current_user[USER_ID]}"
        user_data = self.executeFetchSqlQuery(USER_TABLE_NAME, que)[0]

        self.username_label.configure(text=f"{user_data[USERNAME]} (User Id = {user_data[USER_ID]})")
        self.email_label.configure(text=user_data[EMAIL])
        self.primary_contact_data.set(self.checkNullFormat(user_data[USER_CONTACT_1]))
        self.secondary_contact_data.set(self.checkNullFormat(user_data[USER_CONTACT_2]))
        self.address_entry.delete(1.0, "end-1c")
        self.address_entry.insert(1.0, self.checkNullFormat(user_data[USER_ADDRESS]))



    # When Submit button pressed
    def commandSubmitCategory(self):
        self.button.configure(state="disabled")
        self.lbsuc.grid(row=22, column=0, columnspan=2, sticky="ew")
        self.button.configure(state="disabled")

        try:
            # Updating Shop Details
            query = f"""UPDATE `{DATABASE_NAME}`.`{USER_TABLE_NAME}` SET
            `{USER_CONTACT_1}` = %s, `{USER_CONTACT_2}` = %s, `{USER_ADDRESS}` = %s WHERE `{USER_ID}` = {self.current_user[USER_ID]};"""
            query_parameters = (
                self.primary_contact_data.get().strip(),
                self.secondary_contact_data.get().strip(),
                self.address_entry.get(1.0, "end-1c").strip()
                )
            self.executeCommitSqlQuery(SHOP_TABLE_NAME, query, query_parameters)
            
            # After Saving
            self.lbsuc.configure(
                style="SuccessfulLoginRegisterLabel.TLabel",
                text="Shop/Organization's Details are updated, please relaunch the application to see the changes."
            )
            self.lbsuc.grid(row=22, column=0, columnspan=2, sticky="ew")
        
            
        except Exception as error:
            self.lbsuc.configure(
                style="ErrorLoginRegisterLabel.TLabel",
                text="Something went wrong. "
            )
            self.lbsuc.grid(row=22, column=0, columnspan=2, sticky="ew")
            print(f"Development Error (Storing User Profile Data): {error}")
            ErrorModal("Something went wrong while creating new category, please contact software developer.")
           
           
           
    def validate_input(self, event):
        pass       
        contact_regex = r"^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})?[-. ]*(\d{4})(?: *x(\d+))?\s*$"

        if self.primary_contact_data.get() == "" or self.primary_contact_data.get().isspace():
            self.lbsuc.configure(
                style="ErrorLoginRegisterLabel.TLabel",
                text="Primary contact field cannot be empty."
            )
            self.lbsuc.grid(row=22, column=0, columnspan=2, sticky="ew")
            self.button.configure(state="disabled")
        elif not (re.fullmatch(contact_regex, self.primary_contact_data.get().strip())):
            self.lbsuc.configure(
                style="ErrorLoginRegisterLabel.TLabel",
                text="Invalid Primary Contact."
            )
            self.lbsuc.grid(row=22, column=0, columnspan=2, sticky="ew")
            self.button.configure(state="disabled")
        elif len(self.secondary_contact_data.get()) > 0 and not (re.fullmatch(contact_regex, self.secondary_contact_data.get().strip())):
            self.lbsuc.configure(
                style="ErrorLoginRegisterLabel.TLabel",
                text="Invalid Secondary Contact."
            )
            self.lbsuc.grid(row=22, column=0, columnspan=2, sticky="ew")
            self.button.configure(state="disabled")
        elif self.address_entry.get(1.0, "end-1c") == "" or self.address_entry.get(1.0, "end-1c").isspace():
            self.lbsuc.configure(
                style="ErrorLoginRegisterLabel.TLabel",
                text="Address filed cannot be empty."
            )
            self.lbsuc.grid(row=22, column=0, columnspan=2, sticky="ew")
            self.button.configure(state="disabled")
        elif len(self.address_entry.get(1.0, "end-1c").strip()) > 255:
            self.lbsuc.configure(
                style="ErrorLoginRegisterLabel.TLabel",
                text="Address cannot be exceeded more than 255 characters"
            )
            self.lbsuc.grid(row=22, column=0, columnspan=2, sticky="ew")
            self.button.configure(state="disabled")
        else:
            self.lbsuc.grid_forget()
            self.lbsuc.configure(
                style="SuccessfulLoginRegisterLabel.TLabel",
                text=f"{self.current_user[USERNAME]} Details are updated, please relaunch the application to see the changes."
            )
            self.button.configure(state="normal")
      
             
    # Resetting the Page
    def customReset(self):

        # Fetch and render shop data
        self.fetchUserDetails()
        # Error Label Reset
        self.lbsuc.configure(
            style="SuccessfulLoginRegisterLabel.TLabel",
            text=f"{self.current_user[USERNAME]} Details are updated, please relaunch the application to see the changes."
        )
        self.lbsuc.grid_forget()
        # Submit Button Disabled
        self.button.configure(state="normal")

    