import tkinter as tk
from tkinter import ttk
from CONSTANT.index import *
from app.base import Base
from error import ErrorModal
import re
from app.main.other_components.custom_text import CustomText

class EditSupplier(tk.Toplevel, Base):
    def __init__(self, container, mysql, user, supplier_id, refreshedTableMethod):

        # Note: when we call, instance.method(), method automatically take instance as first argument which we define as self
        # when we call, Class.method(), method need instance manually as first argument bcz it doesn't know whic one to take
        tk.Toplevel.__init__(self, container)
        Base.__init__(self, mysql, user)
        
        self.refreshedTableMethod = lambda: refreshedTableMethod()
        
        self.supplier_id = supplier_id
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
        
        
        # Freeze other windows
        self.grab_set()
        
        # Main Frame
        self.main_frame = ttk.Frame(self, padding=5)
        self.main_frame.pack(side="left", fill="y", expand=1)
        
        # Page Heading
        headlb = ttk.Label(self.main_frame, text="Update Supplier", style="ApplicationLabel1.TLabel", anchor="center")
        headlb.grid(row=0, column=0, columnspan=4, sticky="ew")
        
        
        ##  Main Content  ##
        
        name_label = ttk.Label(self.main_frame, text="Supplier Name: {}".format(self.superscript("*")), style="LoginLabel.TLabel")
        name_label.grid(row=2, column=0, sticky="w")
        
        self.name_entry = ttk.Entry(self.main_frame, width=40,  textvariable=self.name_data, font=("TkdefaultFont", 10, "bold"))
        self.name_entry.grid(row=2, column=1, padx=(10,10), pady=(10,10))
        self.name_entry.configure(state="disabled")
        
        
        contact_1_label = ttk.Label(self.main_frame, text="Primary Contact: {}".format(self.superscript("*")), style="LoginLabel.TLabel")
        contact_1_label.grid(row=2, column=2, sticky="w")
        
        self.contact_1_entry = ttk.Entry(self.main_frame, width=40,  textvariable=self.contact_1_data, font=("TkdefaultFont", 10, "bold"))
        self.contact_1_entry.grid(row=2, column=3, padx=(10,10), pady=(10,10))
        self.bindFormFields(self.contact_1_entry, self.validate_supplier)  
        
        contact_2_label = ttk.Label(self.main_frame, text="Secondary Contact: ", style="LoginLabel.TLabel")
        contact_2_label.grid(row=3, column=0, sticky="w")
        
        self.contact_2_entry = ttk.Entry(self.main_frame, width=40,  textvariable=self.contact_2_data, font=("TkdefaultFont", 10, "bold"))
        self.contact_2_entry.grid(row=3, column=1, padx=(10,10), pady=(10,10))
        self.bindFormFields(self.contact_2_entry, self.validate_supplier)        
        
        address_label = ttk.Label(self.main_frame, text="Supplier Address: {}".format(self.superscript("*")), style="LoginLabel.TLabel")
        address_label.grid(row=3, column=2, sticky="w")
        
        self.address_entry = ttk.Entry(self.main_frame, width=40,  textvariable=self.address_data, font=("TkdefaultFont", 10, "bold"))
        self.address_entry.grid(row=3, column=3, padx=(10,10), pady=(10,10))
        self.bindFormFields(self.address_entry, self.validate_supplier)

        gst_label = ttk.Label(self.main_frame, text="Supplier GSTIN: ", style="LoginLabel.TLabel")
        gst_label.grid(row=4, column=0, sticky="w")
        
        self.gstin_entry = ttk.Entry(self.main_frame, width=40,  textvariable=self.gstin_data, font=("TkdefaultFont", 10, "bold"))
        self.gstin_entry.grid(row=4, column=1, padx=(10,10), pady=(10,10))
        self.bindFormFields(self.address_entry, self.validate_supplier)
        
        org_name_label = ttk.Label(self.main_frame, text="Supplier's Organization Name: ", style="LoginLabel.TLabel")
        org_name_label.grid(row=4, column=2, sticky="w")
        
        self.org_name_entry = ttk.Entry(self.main_frame, width=40,  textvariable=self.org_name_data, font=("TkdefaultFont", 10, "bold"))
        self.org_name_entry.grid(row=4, column=3, padx=(10,10), pady=(10,10))
        self.bindFormFields(self.org_name_entry, self.validate_supplier)
        
        org_contact_1_label = ttk.Label(self.main_frame, text="Organization's Primary Contact: ", style="LoginLabel.TLabel")
        org_contact_1_label.grid(row=5, column=0, sticky="w")
        
        self.org_contact_1_entry = ttk.Entry(self.main_frame, width=40,  textvariable=self.org_contact_1_data, font=("TkdefaultFont", 10, "bold"))
        self.org_contact_1_entry.grid(row=5, column=1, padx=(10,10), pady=(10,10))
        self.bindFormFields(self.org_contact_1_entry, self.validate_supplier)
        
        
        org_contact_2_label = ttk.Label(self.main_frame, text="Organization's Secondary Contact: ", style="LoginLabel.TLabel")
        org_contact_2_label.grid(row=5, column=2, sticky="w")
        
        self.org_contact_2_entry = ttk.Entry(self.main_frame, width=40,  textvariable=self.org_contact_2_data, font=("TkdefaultFont", 10, "bold"))
        self.org_contact_2_entry.grid(row=5, column=3, padx=(10,10), pady=(10,10))
        self.bindFormFields(self.org_contact_2_entry, self.validate_supplier)
        
        
        org_address_label = ttk.Label(self.main_frame, text="Organization's Address: ", style="LoginLabel.TLabel")
        org_address_label.grid(row=6, column=0, sticky="w")
        
        self.org_address_entry = ttk.Entry(self.main_frame, width=40,  textvariable=self.org_address_data, font=("TkdefaultFont", 10, "bold"))
        self.org_address_entry.grid(row=6, column=1, padx=(10,10), pady=(10,10))
        self.bindFormFields(self.org_address_entry, self.validate_supplier)
        
        supplier_desc_label = ttk.Label(self.main_frame, text="Description: ", style="LoginLabel.TLabel")
        supplier_desc_label.grid(row=6, column=2, sticky="w")
        
        self.supplier_desc_entry = CustomText(
            self.main_frame,
            height=5,
            width=40,
            wrap=tk.NONE,
            font=("TkdefaultFont", 10, "bold")
            )
        self.supplier_desc_entry.grid(row=6, column=3)
        self.supplier_desc_entry.grid_scrollbar(row=6, column=3)
        self.bindFormFields(self.supplier_desc_entry, self.validate_supplier)   
        
        
        # Submit Button
        self.button = ttk.Button(self.main_frame,
                            text="Update",
                            command=self.commandSubmitSupplier,
                            style="SignButton.TButton"
                            )
        self.button.grid(row=7, column=0, columnspan=2, sticky="ew", pady=12)
        
        # Cacnel Button
        self.cancel_button = ttk.Button(self.main_frame,
                            text="Cancel",
                            command=lambda: self.destroy(),
                            style="ResetCancelButton.TButton"
                            )
        self.cancel_button.grid(row=7, column=2, columnspan=2, sticky="ew", pady=12)
        
        # Error Label
        self.lbsuc = ttk.Label(self.main_frame, anchor="center")
        
        # Entry Field's Data Update
        self.fetchSupplier()

    
    
    
    # Fetch Data
    def fetchSupplier(self):
        data = self.queryFetchSingleSupplier(self.supplier_id)
        
        # Temporary value stored
        self.name_data_temp = data[0][SUPPLIER_NAME]
        self.contact_1_data_temp = data[0][SUPPLIER_CONTACT_1]
        self.contact_2_data_temp = self.checkNullFormat(data[0][SUPPLIER_CONTACT_2])
        self.address_data_temp = data[0][SUPPLIER_ADDRESS]
        self.gstin_data_temp = data[0][SUPPLIER_GSTIN]
        self.org_name_data_temp = self.checkNullFormat(data[0][SUPPLIER_ORGANIZATION_NAME])
        self.org_contact_1_data_temp = self.checkNullFormat(data[0][SUPPLIER_ORGANIZATION_CONTACT_1])
        self.org_contact_2_data_temp = self.checkNullFormat(data[0][SUPPLIER_ORGANIZATION_CONTACT_2])
        self.org_address_data_temp = self.checkNullFormat(data[0][SUPPLIER_ADDRESS])
        self.supplier_desc_data_temp = self.checkNullFormat(data[0][SUPPLIER_DESCRIPTION])

        # Data Reset
        self.name_data.set(self.name_data_temp)
        self.contact_1_data.set(self.contact_1_data_temp)
        self.contact_2_data.set(self.contact_2_data_temp)
        self.address_data.set(self.address_data_temp )
        self.gstin_data.set(self.gstin_data_temp )
        self.org_name_data.set(self.org_name_data_temp)
        self.org_contact_1_data.set(self.org_contact_1_data_temp )
        self.org_contact_2_data.set(self.org_contact_2_data_temp)
        self.org_address_data.set(self.org_address_data_temp)
        self.supplier_desc_entry.delete(1.0, "end-1c")
        self.supplier_desc_entry.insert(1.0, self.supplier_desc_data_temp)
    
    
     # Submit Button Press   
    def commandSubmitSupplier(self):
    
        self.button.configure(state="disabled")
        
        flag_1 = self.name_data_temp == self.name_data.get().strip() and self.contact_1_data_temp == self.contact_1_data.get().strip()
        flag_2 = self.contact_1_data_temp == self.contact_1_data.get().strip() and self.contact_2_data_temp == self.contact_2_data.get().strip()
        flag_3 = self.address_data_temp == self.address_data.get().strip() and self.org_name_data_temp == self.org_name_data.get().strip()
        flag_4 = self.org_contact_1_data_temp == self.org_contact_1_data.get().strip() and self.org_contact_2_data_temp == self.org_contact_2_data.get().strip()
        flag_5 = self.org_address_data_temp == self.org_address_data.get().strip() and self.supplier_desc_data_temp == self.supplier_desc_entry.get(1.0, "end-1c").strip()
        flag_6 = True

        if flag_1 and flag_2 and flag_3 and flag_4 and flag_5 and self.gstin_data_temp == self.gstin_data.get().strip().upper():
            self.validateGui(
                None,
                None,
                "disabled",
                1,
                "ErrorLoginRegisterLabel.TLabel",
                "Nothing to update, no changes are made.",
                error_label_grid_row=8
                )
        else:
            # If Duplicates present

            query = self.saved_query_supplier + f" WHERE ({SUPPLIER_ID} <> {self.supplier_id})"
            
            if not (self.contact_2_data.get() == "" or type(self.contact_2_data.get()) == None.__class__ or self.contact_2_data.get().isspace()):
                a = " AND ((" 
            else:
                a = " AND ("  
                          
            query = query + a + f""" {SUPPLIER_CONTACT_1} = %s
            OR {SUPPLIER_CONTACT_2} = %s)"""
            q_param = (self.contact_1_data.get().strip(), self.contact_1_data.get().strip())    
            if not (self.contact_2_data.get() == "" or type(self.contact_2_data.get()) == None.__class__ or self.contact_2_data.get().isspace()):
                query = query + f" OR ({SUPPLIER_CONTACT_1} = %s OR {SUPPLIER_CONTACT_2} = %s))"
                q_param = (self.contact_1_data.get().strip(), self.contact_1_data.get().strip(), self.contact_2_data.get().strip(), self.contact_2_data.get().strip()) 
            
            data = self.executeFetchSqlQuery(SUPPLIER_TABLE_NAME, query, q_param)
            
            if len(data) > 0:
                flag_z = False
                for record in data:
                    if record[SUPPLIER_ID] == self.supplier_id:
                        flag_z = True
                # If Contact Duplication is of the current record in database then allow changes and same contact
                if flag_z:
                    flag_6 = True
                else:
                    flag_6 = False
                    self.validateGui(
                        None,
                        None,
                        "disabled",
                        1,
                        "ErrorLoginRegisterLabel.TLabel",
                        f"Contact Details already registered as follow:\nSupplier id = {data[0][SUPPLIER_ID]}\nSupplier Name = {data[0][SUPPLIER_NAME]}",
                        error_label_grid_row=8
                        )
            
            if flag_6:
                try:
                    # Saving to Database
                    query = f"""UPDATE `{DATABASE_NAME}`.`{SUPPLIER_TABLE_NAME}` SET 
                        `{SUPPLIER_NAME}` = %(name)s,
                        `{SUPPLIER_CONTACT_1}` = %(c_1)s,
                        `{SUPPLIER_CONTACT_2}` = %(c_2)s,
                        `{SUPPLIER_ADDRESS}` = %(address)s,
                        `{SUPPLIER_GSTIN}` = %(gst)s,
                        `{SUPPLIER_ORGANIZATION_NAME}` = %(org_name)s,
                        `{SUPPLIER_ORGANIZATION_CONTACT_1}` = %(org_c_1)s,
                        `{SUPPLIER_ORGANIZATION_CONTACT_2}` = %(org_c_2)s,
                        `{SUPPLIER_ORGANIZATION_ADDRESS}` = %(org_address)s,
                        `{SUPPLIER_DESCRIPTION}` = %(org_desc)s 
                        WHERE {SUPPLIER_ID} = %(supplier_id)s
                        """
                    query_parameters = {
                        "name": self.name_data.get().strip(),
                        "c_1": self.contact_1_data.get().strip(),
                        "c_2": self.contact_2_data.get().strip(),
                        "address": self.address_data.get().strip(),
                        "gst": self.gstin_data.get().strip().upper(),
                        "org_name": self.org_name_data.get().strip(),
                        "org_c_1": self.org_contact_1_data.get().strip(),
                        "org_c_2": self.org_contact_2_data.get().strip(),
                        "org_address": self.org_address_data.get().strip(),
                        "org_desc": self.supplier_desc_entry.get(1.0, "end-1c").strip(),
                        "supplier_id": self.supplier_id
                    }
                    self.executeCommitSqlQuery(SUPPLIER_TABLE_NAME, query, query_parameters)
                    
                    # After Saving
                    self.validateGui(None, None, "disabled", 1, "SuccessfulLoginRegisterLabel.TLabel", "Supplier updated successfully", 8)
                    
                    self.refreshedTableMethod()
                    self.fetchSupplier()
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
                    ErrorModal("Something went wrong while updating supplier, please contact software developer.")
           
           
     
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
        self.validateGui(None, None, "disabled", 0, "SuccessfulLoginRegisterLabel.TLabel", "Supplier updated successfully", 8)
        
        # Entry Field's Data Update
        self.fetchSupplier()



    