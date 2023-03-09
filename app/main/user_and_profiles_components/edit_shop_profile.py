import tkinter as tk
from tkinter import ttk, filedialog
from io import BytesIO
from PIL import Image, ImageTk
from CONSTANT.index import *
from app.main.other_components.custom_text import CustomText
from app.base import Base
from error import ErrorModal
import re

class EditShopProfile(ttk.Frame, Base):
    def __init__(self, container, mysql, user):

        # Note: when we call, instance.method(), method automatically take instance as first argument which we define as self
        # when we call, Class.method(), method need instance manually as first argument bcz it doesn't know whic one to take
        ttk.Frame.__init__(self, container)
        Base.__init__(self, mysql, user)
                
        self.org_name_data = tk.StringVar()
        self.owner_name_data = tk.StringVar()
        self.contact_1_data = tk.StringVar()
        self.contact_2_data = tk.StringVar()
        self.gstin_data = tk.StringVar()
        self.email_data = tk.StringVar()     
        self.logo_entry_data = tk.StringVar()
        self.logo_data = tk.Variable()
        
        headlb = ttk.Label(self, text="Update Shop/Organization's Details", style="ApplicationLabel1.TLabel", anchor="center")
        headlb.grid(row=0, column=0, columnspan=2, sticky="ew")
        
        lb = ttk.Label(self, text="Shop/Organization's Name: {}".format(self.superscript("*")), style="LoginLabel.TLabel")
        lb.grid(row=1, column=0, sticky="w")
        
        input = ttk.Entry(self, width=60,  textvariable=self.org_name_data, font=("TkdefaultFont", 10, "bold"))
        input.grid(row=1, column=1, padx=(10,10), pady=(10,10))
        self.bindFormFields(input, self.validate_input)

        lb = ttk.Label(self, text="Owner Name: {}".format(self.superscript("*")), style="LoginLabel.TLabel")
        lb.grid(row=2, column=0, sticky="w")
        
        input = ttk.Entry(self, width=60,  textvariable=self.owner_name_data, font=("TkdefaultFont", 10, "bold"))
        input.grid(row=2, column=1, padx=(10,10), pady=(10,10))
        self.bindFormFields(input, self.validate_input)

        lb = ttk.Label(self, text="Contact 1: {}".format(self.superscript("*")), style="LoginLabel.TLabel")
        lb.grid(row=3, column=0, sticky="w")
        
        input = ttk.Entry(self, width=60,  textvariable=self.contact_1_data, font=("TkdefaultFont", 10, "bold"))
        input.grid(row=3, column=1, padx=(10,10), pady=(10,10))
        self.bindFormFields(input, self.validate_input)

        lb = ttk.Label(self, text="Contact 2:", style="LoginLabel.TLabel")
        lb.grid(row=4, column=0, sticky="w")
        
        input = ttk.Entry(self, width=60,  textvariable=self.contact_2_data, font=("TkdefaultFont", 10, "bold"))
        input.grid(row=4, column=1, padx=(10,10), pady=(10,10))
        self.bindFormFields(input, self.validate_input)

        lb = ttk.Label(self, text="E-Mail: {}".format(self.superscript("*")), style="LoginLabel.TLabel")
        lb.grid(row=5, column=0, sticky="w")
        
        input = ttk.Entry(self, width=60,  textvariable=self.email_data, font=("TkdefaultFont", 10, "bold"))
        input.grid(row=5, column=1, padx=(10,10), pady=(10,10))
        self.bindFormFields(input, self.validate_input)

        lb = ttk.Label(self, text="GSTIN: ", style="LoginLabel.TLabel")
        lb.grid(row=6, column=0, sticky="w")
        
        input = ttk.Entry(self, width=60,  textvariable=self.gstin_data, font=("TkdefaultFont", 10, "bold"))
        input.grid(row=6, column=1, padx=(10,10), pady=(10,10))
        self.bindFormFields(input, self.validate_input)

        lb = ttk.Label(self, text="Address: {}".format(self.superscript("*")), style="LoginLabel.TLabel")
        lb.grid(row=7, column=0, sticky="w")
        
        self.address_entry = CustomText(
            self,
            height=5,
            wrap=tk.NONE,
            font=("TkdefaultFont", 10, "bold")
            )
        self.address_entry.grid(row=7, column=1, padx=(10,10), pady=(10,10))
        self.address_entry.grid_scrollbar(row=7, column=1)
        self.bindFormFields(self.address_entry, self.validate_input)

        lb = ttk.Label(self, text="Modify Shop Logo: ", style="LoginLabel.TLabel")
        lb.grid(row=8, column=0, sticky="w")
        
        logo_entry = ttk.Entry(self, width=60, state="disabled", justify="center", textvariable=self.logo_entry_data, font=("TkdefaultFont", 10, "bold"))
        logo_entry.grid(row=8, column=1, padx=(10,10), pady=(10,10))
        self.bindFormFields(logo_entry, self.validate_input)
        logo_entry.bind("<Button-1>", self.uploadLogo)

        self.fetchShopDetails()

        self.button = ttk.Button(self,
                            text="Submit",
                            command=self.commandSubmitCategory,
                            style="SignButton.TButton"
                            )
        self.button.grid(row=9, column=0, columnspan=2, sticky="ew")
        
        self.lbsuc = ttk.Label(self, anchor="center")

    
    

    # Fetch Shop Details
    def fetchShopDetails(self):
        que = f"SELECT * FROM `{DATABASE_NAME}`.`{SHOP_TABLE_NAME}` WHERE `{SHOP_ID}` = 1"
        shop_data = self.executeFetchSqlQuery(SHOP_TABLE_NAME, que)[0]

        self.org_name_data.set(self.checkNullFormat(shop_data[SHOP_NAME]))
        self.owner_name_data.set(self.checkNullFormat(shop_data[SHOP_OWNER_NAME]))
        self.contact_1_data.set(self.checkNullFormat(shop_data[SHOP_CONTACT_1]))
        self.contact_2_data.set(self.checkNullFormat(shop_data[SHOP_CONTACT_2]))
        self.gstin_data.set(self.checkNullFormat(shop_data[SHOP_GST_NUMBER]))
        self.email_data.set(self.checkNullFormat(shop_data[SHOP_EMAIL]))
        self.address_entry.delete(1.0, "end-1c")
        self.address_entry.insert(1.0, self.checkNullFormat(shop_data[SHOP_ADDRESS]))



    # When Submit button pressed
    def commandSubmitCategory(self):
        self.button.configure(state="disabled")
        self.lbsuc.grid(row=22, column=0, columnspan=2, sticky="ew")
        self.button.configure(state="disabled")

        try:
            # Updating Shop Details
            query = f"""UPDATE `{DATABASE_NAME}`.`{SHOP_TABLE_NAME}` SET
            `{SHOP_NAME}` = %s, `{SHOP_OWNER_NAME}` = %s, `{SHOP_CONTACT_1}` = %s, `{SHOP_CONTACT_2}` = %s, `{SHOP_EMAIL}` = %s,
            `{SHOP_GST_NUMBER}` = %s, `{SHOP_ADDRESS}` = %s , `{SHOP_LOGO}` = %s WHERE `{SHOP_ID}` = 1;"""
            query_parameters = (
                self.org_name_data.get().strip(),
                self.owner_name_data.get().strip(),
                self.contact_1_data.get().strip(),
                self.contact_2_data.get().strip(),
                self.email_data.get().strip(),
                self.gstin_data.get().strip(),
                self.address_entry.get(1.0, "end-1c").strip(),
                self.logo_data.get()
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
            print(f"Development Error (Storing Shop Profile Data): {error}")
            ErrorModal("Something went wrong while creating new category, please contact software developer.")
           
           
           
    def validate_input(self, event):
        
        contact_regex = r"^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})?[-. ]*(\d{4})(?: *x(\d+))?\s*$"
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z]+\.[A-Z|a-z]{2,}\b'

        if self.org_name_data.get() == "" or self.org_name_data.get().isspace():
            self.lbsuc.configure(
                style="ErrorLoginRegisterLabel.TLabel",
                text="Organization's name cannot be empty."
            )
            self.lbsuc.grid(row=22, column=0, columnspan=2, sticky="ew")
            self.button.configure(state="disabled")
        elif self.owner_name_data.get() == "" or self.owner_name_data.get().isspace():
            self.lbsuc.configure(
                style="ErrorLoginRegisterLabel.TLabel",
                text=" Owner name cannot be empty."
            )
            self.lbsuc.grid(row=22, column=0, columnspan=2, sticky="ew")
            self.button.configure(state="disabled")
        elif self.contact_1_data.get() == "" or self.contact_1_data.get().isspace():
            self.lbsuc.configure(
                style="ErrorLoginRegisterLabel.TLabel",
                text="Primary Contact cannot be empty."
            )
            self.lbsuc.grid(row=22, column=0, columnspan=2, sticky="ew")
            self.button.configure(state="disabled")
        elif not (re.fullmatch(contact_regex, self.contact_1_data.get().strip())):
            self.lbsuc.configure(
                style="ErrorLoginRegisterLabel.TLabel",
                text="Invalid Primary Contact."
            )
            self.lbsuc.grid(row=22, column=0, columnspan=2, sticky="ew")
            self.button.configure(state="disabled")
        elif len(self.contact_2_data.get().strip()) > 0 and (not (re.fullmatch(contact_regex, self.contact_2_data.get().strip()))):
            self.lbsuc.configure(
                style="ErrorLoginRegisterLabel.TLabel",
                text="Invalid Secondary Contact."
            )
            self.lbsuc.grid(row=22, column=0, columnspan=2, sticky="ew")
            self.button.configure(state="disabled")
        elif self.email_data.get() == "" or self.email_data.get().isspace():
            self.lbsuc.configure(
                style="ErrorLoginRegisterLabel.TLabel",
                text="E-Mail field cannot be empty."
            )
            self.lbsuc.grid(row=22, column=0, columnspan=2, sticky="ew")
            self.button.configure(state="disabled")
        elif not (re.fullmatch(email_regex, self.email_data.get().strip())):
            self.lbsuc.configure(
                style="ErrorLoginRegisterLabel.TLabel",
                text="Invalid E-Mail."
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
        elif (len(self.gstin_data.get().strip()) > 0) and ((not len(self.gstin_data.get().strip()) == 15) or (not (self.gstin_data.get().isalnum()))):
            self.lbsuc.configure(
                style="ErrorLoginRegisterLabel.TLabel",
                text="Invalid GSTIN. GSTIN is 15 digit alphanumeric value"
            )
            self.lbsuc.grid(row=22, column=0, columnspan=2, sticky="ew")
            self.button.configure(state="disabled")
        else:
            self.lbsuc.grid_forget()
            self.lbsuc.configure(
                style="SuccessfulLoginRegisterLabel.TLabel",
                text="Shop/Organization's Details are updated, please relaunch the application to see the changes."
            )
            self.button.configure(state="normal")



    # When Upload Logo
    def uploadLogo(self, event):
        # Selecting File and opening it in program
        filepath = filedialog.askopenfilename(initialdir="/images", filetypes=(("All images", ".*"), ("jpeg images", ".jpeg"), ("jpg images", ".jpg"), ("ico images", ".ico")))
        image_data = Image.open(filepath)
        # Create a bytesio instance and saving image data as bytes in variable
        bytes_buffer = BytesIO()
        image_data.save(bytes_buffer, "ICO")
        self.logo_data.set(bytes_buffer.getvalue())

        # Modifying Select Image Entry
        startindex = filepath.rfind("/")
        filename = filepath[startindex+1:]
        self.logo_entry_data.set(filename)


            
      
             
    # Resetting the Page
    def customReset(self):

        self.logo_entry_data.set("None Selected")
        self.logo_data.set("")
        # Fetch and render shop data
        self.fetchShopDetails()
        # Error Label Reset
        self.lbsuc.configure(
            style="SuccessfulLoginRegisterLabel.TLabel",
            text="Shop/Organization's Details are updated, please relaunch the application to see the changes."
        )
        self.lbsuc.grid_forget()
        # Submit Button Disabled
        self.button.configure(state="normal")

    