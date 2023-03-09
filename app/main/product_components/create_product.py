import tkinter as tk
from tkinter import ttk
from CONSTANT.index import *
from app.base import Base
from error import ErrorModal
from app.main.other_components.custom_text import CustomText
from app.main.other_components.custom_combobx import CustomCombobox
import re

class CreateProduct(ttk.Frame, Base):
    def __init__(self, container, mysql, user):

        # Note: when we call, instance.method(), method automatically take instance as first argument which we define as self
        # when we call, Class.method(), method need instance manually as first argument bcz it doesn't know whic one to take
        ttk.Frame.__init__(self, container)
        Base.__init__(self, mysql, user)
                
        self.name_data = tk.StringVar()
        self.quantity_data = tk.StringVar(value=0)
        self.reorder_data = tk.StringVar(value=0)
        self.price_data = tk.StringVar()
        self.combobox_data_1 = tk.StringVar()
        self.combobox_data_2 = tk.StringVar()
        self.category_name_list = list()
        self.category_id_list = list()
        self.sub_category_name_list = list()
        self.sub_category_id_list = list()
        self.combobox_default_category = ["-------- Choose Category --------"]
        self.combobox_default_sub_category = ["-------- Choose Sub-Category --------"]
        self.combobox_default_id = [0]
        self.selected_category_id = ""
        self.selected_sub_category_id = ""
        self.thread_flag = False
        self.after_id = 0
        
        
        headlb = ttk.Label(self, text="Register New Product", style="ApplicationLabel1.TLabel", anchor="center")
        headlb.grid(row=0, column=0, columnspan=2, sticky="ew")
        
        lb_1 = ttk.Label(self, text="Product Name: {}".format(self.superscript("*")), style="LoginLabel.TLabel")
        lb_1.grid(row=1, column=0, sticky="w")
        
        self.product_name_entry = ttk.Entry(self, width=60,  textvariable=self.name_data, font=("TkdefaultFont", 10, "bold"))
        self.product_name_entry.grid(row=1, column=1, padx=(10,10), pady=(10,10))
        self.bindFormFields(self.product_name_entry, self.validate_input)
        
        lb_2 = ttk.Label(self, text="Product Price (\u20B9): {}".format(self.superscript("*")), style="LoginLabel.TLabel")
        lb_2.grid(row=2, column=0, sticky="w")
        
        self.price_entry = ttk.Entry(self, width=60,  textvariable=self.price_data, font=("TkdefaultFont", 10, "bold"))
        self.price_entry.grid(row=2, column=1, padx=(10,10), pady=(10,10))
        self.bindFormFields(self.price_entry, self.validate_input)
        
        
        lb_3 = ttk.Label(self, text="Current Quantity in Stock: {}".format(self.superscript("*")), style="LoginLabel.TLabel")
        lb_3.grid(row=3, column=0, sticky="w")
        
        self.quantity_entry = tk.Spinbox(
            self,
            width=4,
            wrap=True,
            from_=0,
            to=9999,
            textvariable=self.quantity_data,
            font=("TkDefaultFont", 12, "bold"),
            justify="center"
            )
        self.quantity_entry.grid(row=3, column=1, padx=(10,10), pady=(10,10))
        self.bindFormFields(self.quantity_entry, self.validate_input)
        
        
        
        lb_4 = ttk.Label(self, text="Reorder Quantity Value: {}".format(self.superscript("*")), style="LoginLabel.TLabel")
        lb_4.grid(row=4, column=0, sticky="w")
        
        self.reorder_entry = tk.Spinbox(
            self,
            width=4,
            wrap=True,
            from_=0,
            to=9999,
            textvariable=self.reorder_data,
            font=("TkDefaultFont", 12, "bold"),
            justify="center"
            )
        self.reorder_entry.grid(row=4, column=1, padx=(10,10), pady=(10,10))
        self.bindFormFields(self.reorder_entry, self.validate_input)
        
        
        lb_6 = ttk.Label(self, text="Product Category: {}".format(self.superscript("*")), style="LoginLabel.TLabel")
        lb_6.grid(row=5, column=0, sticky="w")
        
        # Fetching and storing relevant categories
        self.fetchCategory()
        
        
        self.category_combobox = CustomCombobox(
            self,
            textvariable=self.combobox_data_1,
            valueList=self.category_name_list, 
            defaultvalue=self.combobox_default_category,
            width=60,
            font=("TkdefaultFont", 10, "bold"),
            style="ShowProduct.TCombobox",
            state="readonly",
            justify="center",
            )
        self.category_combobox.grid(row=5, column=1)
        self.category_combobox.current(0)
        self.category_combobox.bind("<<ComboboxSelected>>", self.categoryComboboxSelected)
        self.category_combobox.bind("<KeyRelease>", self.validate_input)
        
        
        lb_6 = ttk.Label(self, text="Product Sub-Category: {}".format(self.superscript("*")), style="LoginLabel.TLabel")
        lb_6.grid(row=6, column=0, sticky="w")
        
        self.sub_category_combobox = CustomCombobox(
            self,
            textvariable=self.combobox_data_2,
            valueList=self.sub_category_name_list, 
            defaultvalue=self.combobox_default_sub_category,
            width=60,
            font=("TkdefaultFont", 10, "bold"),
            style="ShowProduct.TCombobox",
            state="readonly",
            justify="center",
            )
        self.sub_category_combobox.grid(row=6, column=1)
        self.sub_category_combobox.current(0)
        self.sub_category_combobox.bind("<<ComboboxSelected>>", self.subCategoryComboboxSelected)
        self.sub_category_combobox.bind("<KeyRelease>", self.validate_input)
        

        lb_5 = ttk.Label(self, text="Product Description: ", style="LoginLabel.TLabel")
        lb_5.grid(row=7, column=0, sticky="w")
        
        self.description_entry = CustomText(
            self,
            height=5,
            wrap=tk.NONE,
            font=("TkdefaultFont", 10, "bold")
            )
        self.description_entry.grid(row=7, column=1, padx=(10,10), pady=(10,10))
        self.description_entry.grid_scrollbar(row=7, column=1)
        self.bindFormFields(self.description_entry, self.validate_input)
        
        self.button = ttk.Button(self,
                            text="Submit",
                            command=self.commandSubmitProduct,
                            style="SignButton.TButton",
                            state="disabled"
                            )
        self.button.grid(row=8, column=0, columnspan=2, sticky="ew", pady=(15))
        
        self.lbsuc = ttk.Label(self, anchor="center")
        
    
    
    # Reset Entries
    def resetEntries(self):
        self.product_name_entry.configure(style="TEntry")
        self.price_entry.configure(style="TEntry")
        self.quantity_entry.configure(highlightcolor="SystemWindowFrame")
        self.reorder_entry.configure(highlightcolor="SystemWindowFrame")
        self.description_entry.configure(highlightcolor="SystemWindowFrame")
    
    
    
    # Fetch all categories
    def fetchCategory(self):
        data = self.queryFetchAllCategories()
        if len(data) > 0:
            self.category_name_list = self.dbValTuple(data, CATEGORY_NAME)
            # Combobx already have default value at 0 index
            self.category_id_list = self.combobox_default_id + self.dbValTuple(data, CATEGORY_ID)

        # Rendering here because if customreset calls, it will initialize
        self.category_combobox = CustomCombobox(
            self,
            textvariable=self.combobox_data_1,
            valueList=self.category_name_list, 
            defaultvalue=self.combobox_default_category,
            width=60,
            font=("TkdefaultFont", 10, "bold"),
            style="ShowProduct.TCombobox",
            state="readonly",
            justify="center",
            )
        self.category_combobox.grid(row=5, column=1)
        self.category_combobox.current(0)
        self.category_combobox.bind("<<ComboboxSelected>>", self.categoryComboboxSelected)
        self.category_combobox.bind("<KeyRelease>", self.validate_input)



    # When Category Combobox is selected
    def categoryComboboxSelected(self, event):
        self.selected_sub_category_id = None
        self.selected_category_id = self.category_id_list[self.category_combobox.current()]
        if not (self.selected_category_id == 0):
            data = self.queryFetchRelevantSubCategories(self.selected_category_id)
            if len(data) > 0:
                self.sub_category_name_list = self.dbValTuple(data, SUB_CATEGORY_NAME)
                # Combobx already have default value at 0 index
                self.sub_category_id_list = self.combobox_default_id + self.dbValTuple(data, SUB_CATEGORY_ID)
        else:
            self.sub_category_name_list = []
            # Combobx already have default value at 0 index
            self.sub_category_id_list = self.combobox_default_id
        
        # Redfifing Subcategory Combobox with new values
        self.sub_category_combobox = CustomCombobox(
            self,
            textvariable=self.combobox_data_2,
            valueList=self.sub_category_name_list, 
            defaultvalue=self.combobox_default_sub_category,
            width=60,
            font=("TkdefaultFont", 10, "bold"),
            style="ShowProduct.TCombobox",
            state="readonly",
            justify="center",
            )
        self.sub_category_combobox.grid(row=6, column=1)
        self.sub_category_combobox.current(0)
        self.sub_category_combobox.bind("<<ComboboxSelected>>", self.subCategoryComboboxSelected)
        self.sub_category_combobox.bind("<KeyRelease>", self.validate_input)
        self.validate_input()
    
    
    
    # When Sub-Category Combobox is selected
    def subCategoryComboboxSelected(self, event):
        self.selected_sub_category_id = self.sub_category_id_list[self.sub_category_combobox.current()]
        self.validate_input()
    
    
    
    # Submit Product
    def commandSubmitProduct(self):
        self.button.configure(state="disabled")
        
        query = f"SELECT * FROM {DATABASE_NAME}.{PRODUCT_TABLE_NAME} WHERE {PRODUCT_NAME} = %(data)s"
        # Check for Duplicates Entry
        product = self.executeFetchSqlQuery(PRODUCT_TABLE_NAME, query, {"data": self.name_data.get().strip()})
        # If Duplicates present
        if len(product) > 0:
            self.validateGui(
                None,
                None,
                "disabled",
                1,
                "ErrorLoginRegisterLabel.TLabel",
                f"Product with same name already exist as follow:\nProduct Id: {product[0][PRODUCT_ID]}\nProduct Name: {product[0][PRODUCT_NAME]}",
                error_label_grid_row=9
                )
        # If Duplicates not present
        else:
            try:
                # Saving Product to Database
                query = f"""INSERT INTO `{DATABASE_NAME}`.`{PRODUCT_TABLE_NAME}` 
                (`{PRODUCT_NAME}`, `{PRODUCT_PRICE}`, `{PRODUCT_QUANTITY}`,
                `{PRODUCT_REORDER_QUANTITY}`, `{PRODUCT_DESCRIPTION}`,
                `{PRODUCT_FOREIGNKEY_CATEGORY_ID}`, `{PRODUCT_FOREIGNKEY_SUB_CATEGORY_ID}`) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                query_parameters = (
                    self.name_data.get().strip(),
                    round(float(self.price_data.get().strip()), 2),
                    self.quantity_data.get().strip(),
                    self.reorder_data.get().strip(),
                    self.description_entry.get(1.0, "end-1c").strip(),
                    self.selected_category_id,
                    self.selected_sub_category_id
                    )
                # Saving Product and getting new product id
                product_id = self.executeCommitSqlQuery(PRODUCT_TABLE_NAME, query, query_parameters)
                # Creating Log for Product
                self.queryInsertProductLog("Product registered successfully.", product_id)
                
                # After Saving
                self.validateGui(
                    None,
                    None,
                    "disabled",
                    1,
                    "SuccessfulLoginRegisterLabel.TLabel", 
                    "Product registered successfully",
                    error_label_grid_row=9
                    )
                
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
                    error_label_grid_row=9
                    )
                print(f"Development Error (Storing Product Name): {error}")
                ErrorModal("Something went wrong while registring new product, please contact software developer.")
           
           
     # Validating all entries      
    def validate_input(self, event=None):
        category_name_index = 0 if self.category_combobox.current() == 0 else self.category_combobox.current()-1
        sub_category_name_index = 0 if self.sub_category_combobox.current() == 0 else self.sub_category_combobox.current()-1
        # If after pressing submit button, self.after() active then terminates
        self.terminateAfter(self, self.thread_flag, self.after_id)
        
        quantity_regex = r"^([0-9]){1,4}$"
        price_regex = r"^[-+]?[0-9]*\.?[0-9]+$"
        
        if self.name_data.get() == "" or self.name_data.get().isspace():
            self.validateGui(
                self.product_name_entry,
                "ErrorEntry.TEntry",
                "disabled",
                1,
                "ErrorLoginRegisterLabel.TLabel",
                "Product name cannot be empty.",
                error_label_grid_row=9
                )
        elif len(self.name_data.get()) >= 1 and len(self.name_data.get())  > 75:
            self.validateGui(
                self.product_name_entry,
                "ErrorEntry.TEntry",
                "disabled",
                1,
                "ErrorLoginRegisterLabel.TLabel",
                "Product name must be less than 75 characters.",
                error_label_grid_row=9
                )
        elif self.quantity_data.get() == "" or self.quantity_data.get().isspace():
            self.validateGui(
                None,
                None,
                "disabled",
                1,
                "ErrorLoginRegisterLabel.TLabel",
                "Quantity of cannot be empty.",
                error_label_grid_row=9
                )
            self.quantity_entry.configure(highlightcolor="red")
        elif (not re.fullmatch(quantity_regex, self.quantity_data.get())):
            self.validateGui(
                None,
                None,
                "disabled",
                1,
                "ErrorLoginRegisterLabel.TLabel",
                "Invalid value for Quantity, must be value from 0 to 9999",
                error_label_grid_row=9
                )
            self.quantity_entry.configure(highlightcolor="red")
        elif self.reorder_data.get() == "" or self.reorder_data.get().isspace():
            self.validateGui(
                None,
                None,
                "disabled",
                1,
                "ErrorLoginRegisterLabel.TLabel",
                "Reorder quantity of product cannot be empty.",
                error_label_grid_row=9
                )
            self.reorder_entry.configure(highlightcolor="red")
        elif (not re.fullmatch(quantity_regex, self.reorder_data.get())):
            self.validateGui(
                None,
                None,
                "disabled",
                1,
                "ErrorLoginRegisterLabel.TLabel",
                "Invalid value for Reorder, must be value from 0 to 9999",
                error_label_grid_row=9
                )
            self.reorder_entry.configure(highlightcolor="red")
        elif self.price_data.get() == "" or self.price_data.get().isspace():
            self.validateGui(
                self.price_entry,
                "ErrorEntry.TEntry",
                "disabled",
                1,
                "ErrorLoginRegisterLabel.TLabel",
                "Price of product cannot be empty.",
                error_label_grid_row=9
                )
        elif (not re.fullmatch(price_regex, self.price_data.get())):
            self.validateGui(
                self.price_entry,
                "ErrorEntry.TEntry",
                "disabled",
                1,
                "ErrorLoginRegisterLabel.TLabel",
                "Invalid value for Price.",
                error_label_grid_row=9
                )
        elif self.selected_category_id == "" or self.selected_category_id == 0 or type(self.selected_category_id) == None.__class__:
            self.validateGui(
                None,
                None,
                "disabled",
                1,
                "ErrorLoginRegisterLabel.TLabel",
                "Category for product is mandatory.",
                error_label_grid_row=9
                )
        elif not (self.combobox_data_1.get() == self.category_name_list[category_name_index]):
            self.validateGui(
                None,
                None,
                "disabled",
                1,
                "ErrorLoginRegisterLabel.TLabel",
                "Invalid Category.",
                error_label_grid_row=9
                )
        elif self.selected_sub_category_id == "" or self.selected_sub_category_id == 0 or type(self.selected_sub_category_id) == None.__class__:
            self.validateGui(
                None,
                None,
                "disabled",
                1,
                "ErrorLoginRegisterLabel.TLabel",
                "Sub-Category for product is mandatory.",
                error_label_grid_row=9
                )
        elif not (self.combobox_data_2.get() == self.sub_category_name_list[sub_category_name_index]):
            self.validateGui(
                None,
                None,
                "disabled",
                1,
                "ErrorLoginRegisterLabel.TLabel",
                "Invalid Sub-Category.",
                error_label_grid_row=9
                )
        elif len(self.description_entry.get(1.0, "end-1c")) >= 1 and len(self.description_entry.get(1.0, "end-1c"))  > 500:
            self.validateGui(
                None,
                None,
                "disabled",
                1, 
                "ErrorLoginRegisterLabel.TLabel", 
                "Description must be less than 500 characters.",
                error_label_grid_row=9
                )
            self.description_entry.configure(highlightcolor="red")
        else:
            self.validateGui(
                None,
                None,
                "normal",
                0, 
                "SuccessfulLoginRegisterLabel.TLabel", 
                "Product registered successfully",
                error_label_grid_row=9
                ) 
            
            
             
    # Resetting the Page
    def customReset(self):
        self.validateGui(
            None,
            None,
            "disabled",
            0,
            "SuccessfulLoginRegisterLabel.TLabel", 
            "Product registered successfully",
            error_label_grid_row=9
            )
        # Data Reset
        self.name_data.set("")
        self.quantity_data.set(0)
        self.reorder_data.set(0)
        self.price_data.set("")
        self.description_entry.delete(1.0, "end-1c")
        self.combobox_data_1.set("")
        self.category_combobox.current(0)
        self.combobox_data_2.set("")
        self.sub_category_combobox.current(0)
        self.category_name_list = list()
        self.category_id_list = list()
        self.sub_category_name_list = list()
        self.sub_category_id_list = list()
        self.selected_category_id = ""
        self.selected_sub_category_id = ""
        self.thread_flag = False
        self.after_id = 0
        self.fetchCategory()


        
        

    