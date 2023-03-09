import tkinter as tk
from tkinter import ttk
from CONSTANT.index import *
from app.base import Base
from error import ErrorModal
import re
from app.main.other_components.custom_text import CustomText

class CreateSupplier(ttk.Frame, Base):
    def __init__(self, container, mysql, user):

        # Note: when we call, instance.method(), method automatically take instance as first argument which we define as self
        # when we call, Class.method(), method need instance manually as first argument bcz it doesn't know whic one to take
        ttk.Frame.__init__(self, container, padding=12)
        Base.__init__(self, mysql, user)
        
        self.name_data = tk.StringVar()
        self.contact_1_data = tk.StringVar()
        self.contact_2_data = tk.StringVar()
        self.address_data = tk.StringVar()
        self.gstin_data = tk.StringVar()
        self.org_name_data = tk.StringVar()
        self.org_contact_1_data = tk.StringVar()
        self.org_contact_2_data = tk.StringVar()
        self.org_address_data = tk.StringVar()
        self.thread_flag = False
        self.after_id = 0
        
        
        # Page Heading
        headlb = ttk.Label(self, text="Register New Supplier", style="ApplicationLabel1.TLabel", anchor="center")
        headlb.grid(row=0, column=0, columnspan=4, sticky="ew")
        
        
        ##  Main Content  ##
        
        name_label = ttk.Label(self, text="Supplier Name: {}".format(self.superscript("*")), style="LoginLabel.TLabel")
        name_label.grid(row=2, column=0, sticky="w")
        
        self.name_entry = ttk.Entry(self, width=40,  textvariable=self.name_data, font=("TkdefaultFont", 10, "bold"))
        self.name_entry.grid(row=2, column=1, padx=(10,10), pady=(10,10))
        self.bindFormFields(self.name_entry, self.validate_supplier)
        
        contact_1_label = ttk.Label(self, text="Primary Contact: {}".format(self.superscript("*")), style="LoginLabel.TLabel")
        contact_1_label.grid(row=2, column=2, sticky="w")
        
        self.contact_1_entry = ttk.Entry(self, width=40,  textvariable=self.contact_1_data, font=("TkdefaultFont", 10, "bold"))
        self.contact_1_entry.grid(row=2, column=3, padx=(10,10), pady=(10,10))
        self.bindFormFields(self.contact_1_entry, self.validate_supplier)
        
        contact_2_label = ttk.Label(self, text="Secondary Contact: ", style="LoginLabel.TLabel")
        contact_2_label.grid(row=3, column=0, sticky="w")
        
        self.contact_2_entry = ttk.Entry(self, width=40,  textvariable=self.contact_2_data, font=("TkdefaultFont", 10, "bold"))
        self.contact_2_entry.grid(row=3, column=1, padx=(10,10), pady=(10,10))
        self.bindFormFields(self.contact_2_entry, self.validate_supplier)
          
        address_label = ttk.Label(self, text="Supplier Address: {}".format(self.superscript("*")), style="LoginLabel.TLabel")
        address_label.grid(row=3, column=2, sticky="w")
        
        self.address_entry = ttk.Entry(self, width=40,  textvariable=self.address_data, font=("TkdefaultFont", 10, "bold"))
        self.address_entry.grid(row=3, column=3, padx=(10,10), pady=(10,10))
        self.bindFormFields(self.address_entry, self.validate_supplier)

        address_label = ttk.Label(self, text="Supplier GSTIN: ", style="LoginLabel.TLabel")
        address_label.grid(row=4, column=0, sticky="w")

        self.gstin_entry = ttk.Entry(self, width=40,  textvariable=self.gstin_data, font=("TkdefaultFont", 10, "bold"))
        self.gstin_entry.grid(row=4, column=1, padx=(10,10), pady=(10,10))
        self.bindFormFields(self.gstin_entry, self.validate_supplier)
        
        org_name_label = ttk.Label(self, text="Supplier's Organization Name: ", style="LoginLabel.TLabel")
        org_name_label.grid(row=4, column=2, sticky="w")
        
        self.org_name_entry = ttk.Entry(self, width=40,  textvariable=self.org_name_data, font=("TkdefaultFont", 10, "bold"))
        self.org_name_entry.grid(row=4, column=3, padx=(10,10), pady=(10,10))
        self.bindFormFields(self.org_name_entry, self.validate_supplier)
        
        
        org_contact_1_label = ttk.Label(self, text="Organization's Primary Contact: ", style="LoginLabel.TLabel")
        org_contact_1_label.grid(row=5, column=0, sticky="w")
        
        self.org_contact_1_entry = ttk.Entry(self, width=40,  textvariable=self.org_contact_1_data, font=("TkdefaultFont", 10, "bold"))
        self.org_contact_1_entry.grid(row=5, column=1, padx=(10,10), pady=(10,10))
        self.bindFormFields(self.org_contact_1_entry, self.validate_supplier)
          
        org_contact_2_label = ttk.Label(self, text="Organization's Secondary Contact: ", style="LoginLabel.TLabel")
        org_contact_2_label.grid(row=5, column=2, sticky="w")
        
        self.org_contact_2_entry = ttk.Entry(self, width=40,  textvariable=self.org_contact_2_data, font=("TkdefaultFont", 10, "bold"))
        self.org_contact_2_entry.grid(row=5, column=3, padx=(10,10), pady=(10,10))
        self.bindFormFields(self.org_contact_2_entry, self.validate_supplier)
        
        org_address_label = ttk.Label(self, text="Organization's Address: ", style="LoginLabel.TLabel")
        org_address_label.grid(row=6, column=0, sticky="w")
        
        self.org_address_entry = ttk.Entry(self, width=40,  textvariable=self.org_address_data, font=("TkdefaultFont", 10, "bold"))
        self.org_address_entry.grid(row=6, column=1, padx=(10,10), pady=(10,10))
        self.bindFormFields(self.org_address_entry, self.validate_supplier)
        
        supplier_desc_label = ttk.Label(self, text="Description: ", style="LoginLabel.TLabel")
        supplier_desc_label.grid(row=6, column=2, sticky="w")
        
        self.supplier_desc_entry = CustomText(
            self,
            height=5,
            width=40,
            wrap=tk.NONE,
            font=("TkdefaultFont", 10, "bold")
            )
        self.supplier_desc_entry.grid(row=6, column=3, padx=(10,10), pady=(10,10))
        self.supplier_desc_entry.grid_scrollbar(row=6, column=3)
        self.bindFormFields(self.supplier_desc_entry, self.validate_supplier)
  
        # Submit Button
        self.button = ttk.Button(self,
                            text="Submit",
                            command=self.commandSubmitSupplier,
                            style="SignButton.TButton",
                            state="disabled"
                            )
        self.button.grid(row=7, column=0, columnspan=4, sticky="ew", pady=12)
        
        # Error Label
        self.lbsuc = ttk.Label(self, anchor="center")
    
    
        
    def commandSubmitSupplier(self):
        self.button.configure(state="disabled")
        # Check for Duplicates Entry
        suppliers = self.queryFetchAllSuppliers()
        flag_1 = self.checkDuplicates(suppliers, self.contact_1_data.get(), SUPPLIER_CONTACT_1)
        flag_2 = self.checkDuplicates(suppliers, self.contact_1_data.get(), SUPPLIER_CONTACT_2)
        flag_3 = self.checkDuplicates(suppliers, self.contact_2_data.get(), SUPPLIER_CONTACT_1)
        flag_4 = self.checkDuplicates(suppliers, self.contact_2_data.get(), SUPPLIER_CONTACT_2)
        
        # If Duplicates present
        if flag_1 or flag_2 or flag_3 or flag_4:
                # Fetching if supplier with same contact exists
                query = self.saved_query_supplier + f""" 
                WHERE {SUPPLIER_CONTACT_1} = %s
                OR {SUPPLIER_CONTACT_1} = %s
                OR {SUPPLIER_CONTACT_2} = %s
                OR {SUPPLIER_CONTACT_2} = %s
                """
                q_param = (self.contact_1_data.get().strip(), self.contact_2_data.get().strip(), self.contact_1_data.get().strip(), self.contact_2_data.get().strip())
                data = self.executeFetchSqlQuery(SUPPLIER_TABLE_NAME, query, q_param)
                self.validateGui(
                    None,
                    None,
                    "disabled",
                    1,
                    "ErrorLoginRegisterLabel.TLabel",
                    f"Contact Details already registered with:\nSupplier id = {data[0][SUPPLIER_ID]}\nSupplier Name = {data[0][SUPPLIER_NAME]}",
                    error_label_grid_row=8
                    )

        # If Duplicates not present
        else:
            try:
                # Saving to Database
                query = f"""INSERT INTO `{DATABASE_NAME}`.`{SUPPLIER_TABLE_NAME}`(
                    `{SUPPLIER_NAME}`, `{SUPPLIER_CONTACT_1}`, `{SUPPLIER_CONTACT_2}`, `{SUPPLIER_ADDRESS}`, `{SUPPLIER_GSTIN}`,
                    `{SUPPLIER_ORGANIZATION_NAME}`, `{SUPPLIER_ORGANIZATION_CONTACT_1}`,
                    `{SUPPLIER_ORGANIZATION_CONTACT_2}`, `{SUPPLIER_ORGANIZATION_ADDRESS}`, {SUPPLIER_DESCRIPTION}
                    )
                VALUES (
                    %(name)s, %(c_1)s, %(c_2)s, %(address)s, %(gstin)s,
                    %(org_name)s, %(org_c_1)s, %(org_c_2)s, %(org_address)s, %(org_desc)s 
                    )"""
                    
                query_parameters = {
                    "name": self.name_data.get().strip(),
                    "c_1": self.contact_1_data.get().strip(),
                    "c_2": self.contact_2_data.get().strip(),
                    "address": self.address_data.get().strip(),
                    "gstin": self.gstin_data.get().strip().upper(),
                    "org_name": self.org_name_data.get().strip(),
                    "org_c_1": self.org_contact_1_data.get().strip(),
                    "org_c_2": self.org_contact_2_data.get().strip(),
                    "org_address": self.org_address_data.get().strip(),
                    "org_desc": self.supplier_desc_entry.get(1.0, "end-1c").strip()
                }
                        
                self.executeCommitSqlQuery(SUPPLIER_TABLE_NAME, query, query_parameters)
                
                # After Saving
                self.validateGui(None, None, "disabled", 1, "SuccessfulLoginRegisterLabel.TLabel", "Supplier registered successfully", 8)

                self.after_id = self.after(5000, self.customReset)
                self.thread_flag = True
                
            except Exception as error:
                self.validateGui(
                    None,
                    None,
                    "disabled",
                    1,
                    "ErrorLoginRegisterLabel.TLabel", 
                    "Something went wrong.",
                    error_label_grid_row=8
                    )
                print(f"Development Error (Creating Supplier Record): {error}")
                ErrorModal("Something went wrong while registering supplier, please contact software developer.")
           
           
     
     # Validate form      
    def validate_supplier(self, event):
        
        # If after pressing submit button, self.after() active then terminates
        self.terminateAfter(self, self.thread_flag, self.after_id)
        
        contact_regex = r"^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})?[-. ]*(\d{4})(?: *x(\d+))?\s*$"
        
        if self.name_data.get() == "" or self.name_data.get().isspace():
            self.validateGui(self.name_entry, "ErrorEntry.TEntry", "disabled", 1, "ErrorLoginRegisterLabel.TLabel", "Supplier name cannot be empty.", 8)
            
        elif len(self.name_data.get())  > 75:
            self.validateGui(
                self.name_entry,
                "ErrorEntry.TEntry",
                "disabled",
                1,
                "ErrorLoginRegisterLabel.TLabel",
                "Supplier name should be less than 75 characters",
                error_label_grid_row=8
                )
            
        elif self.contact_1_data.get() == "" or self.contact_1_data.get().isspace():
            self.validateGui(
                self.contact_1_entry, 
                "ErrorEntry.TEntry",
                "disabled", 
                1,
                "ErrorLoginRegisterLabel.TLabel",
                "Primary Contact cannot be empty.",
                error_label_grid_row=8
                )
            
        elif (not re.fullmatch(contact_regex, self.contact_1_data.get())):
            self.validateGui(
                self.contact_1_entry,
                "ErrorEntry.TEntry",
                "disabled",
                1, 
                "ErrorLoginRegisterLabel.TLabel",
                "Primary contact format invalid, must be 7-13 digit, can include country or std codes, +91-, 0124-",
                error_label_grid_row=8
                )
            
        elif len(self.contact_2_data.get()) >= 1 and (not re.fullmatch(contact_regex, self.contact_2_data.get())):
            self.validateGui(
                self.contact_2_entry,
                "ErrorEntry.TEntry", 
                "disabled",
                1,
                "ErrorLoginRegisterLabel.TLabel",
                "Secondary contact format invalid, must be 7-13 digit, can include country or std codes, +91-, 0124-",
                error_label_grid_row=8
                )
            
        elif self.address_data.get() == "" or self.address_data.get().isspace():
            self.validateGui(self.address_entry, "ErrorEntry.TEntry", "disabled", 1, "ErrorLoginRegisterLabel.TLabel", "Address cannot be empty.", 8)

        elif len(self.gstin_data.get()) > 0  and not (len(self.gstin_data.get()) == 15):
            self.validateGui(self.gstin_entry, "ErrorEntry.TEntry", "disabled", 1, "ErrorLoginRegisterLabel.TLabel", "GSTIN is 15 digit value.", 8)
            
        elif len(self.address_data.get())  > 75:
            self.validateGui(
                self.address_entry,
                "ErrorEntry.TEntry", 
                "disabled",
                1, 
                "ErrorLoginRegisterLabel.TLabel",
                "Address should be less than 75 characters.",
                error_label_grid_row=8
                )
            
        elif len(self.org_name_data.get()) >= 1 and len(self.org_name_data.get()) > 75:
            self.validateGui(
                self.org_name_entry,
                "ErrorEntry.TEntry",
                "disabled",
                1,
                "ErrorLoginRegisterLabel.TLabel",
                "Supplier's organization name should be less than 75 characters.",
                error_label_grid_row=8
                )
            
        elif len(self.org_contact_1_data.get()) >= 1 and (not re.fullmatch(contact_regex, self.org_contact_1_data.get())):
            self.validateGui(
                self.org_contact_1_entry,
                "ErrorEntry.TEntry",
                "disabled", 
                1,
                "ErrorLoginRegisterLabel.TLabel",
                "Organization's primary contact format invalid, must be 7-13 digit, can include country or std codes, +91-, 0124-",
                error_label_grid_row=8
                )
            
        elif len(self.org_contact_2_data.get()) >= 1 and (not re.fullmatch(contact_regex, self.org_contact_2_data.get())):
            self.validateGui(
                self.org_contact_2_entry,
                "ErrorEntry.TEntry",
                "disabled",
                1,
                "ErrorLoginRegisterLabel.TLabel",
                "Organization's secondary contact format invalid, must be 7-13 digit, can include country or std codes, +91-, 0124-",
                error_label_grid_row=8
                )
            
        elif len(self.org_address_data.get()) >= 1 and len(self.org_address_data.get())  > 75:
            self.validateGui(
                self.org_address_entry,
                "ErrorEntry.TEntry",
                "disabled",
                1,
                "ErrorLoginRegisterLabel.TLabel",
                "Organization's Address must be less than 75 characters.",
                error_label_grid_row=8
                )
            
        elif len(self.supplier_desc_entry.get(1.0, "end-1c")) >= 1 and len(self.supplier_desc_entry.get(1.0, "end-1c"))  > 500:
            self.validateGui(
                None,
                None,
                "disabled",
                1, 
                "ErrorLoginRegisterLabel.TLabel", 
                "Description must be less than 500 characters.",
                error_label_grid_row=8
                )
            
        else:
            self.validateGui(
                None,
                None,
                "normal",
                0, 
                "SuccessfulLoginRegisterLabel.TLabel", 
                "Supplier registered successfully",
                error_label_grid_row=8
                )        
        
    # Resetting all entry fields
    def resetEntries(self):
        self.name_entry.configure(style="TEntry")
        self.contact_1_entry.configure(style="TEntry")
        self.contact_2_entry.configure(style="TEntry")
        self.address_entry.configure(style="TEntry")
        self.gstin_entry.configure(style="TEntry")
        self.org_name_entry.configure(style="TEntry")
        self.org_contact_1_entry.configure(style="TEntry")
        self.org_contact_2_entry.configure(style="TEntry")
        self.org_address_entry.configure(style="TEntry")
    
    
         
    # Resetting the Page
    def customReset(self):
        self.validateGui(None, None, "disabled", 0, "SuccessfulLoginRegisterLabel.TLabel", "Supplier registered successfully", 8)
        
        # Data Reset
        self.name_data.set("")
        self.contact_1_data.set("")
        self.contact_2_data.set("")
        self.address_data.set("")
        self.gstin_data.set("")
        self.org_name_data.set("")
        self.org_contact_1_data.set("")
        self.org_contact_2_data.set("")
        self.org_address_data.set("")
        self.supplier_desc_entry.delete(1.0, "end-1c")

    