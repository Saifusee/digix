import tkinter as tk
from tkinter import ttk
from CONSTANT.index import *
from app.base import Base
from error import ErrorModal
from app.main.other_components.custom_combobx import CustomCombobox
from app.main.order_components.show_product_details_in_invoice import ShowProductDetailsInInvoice
from app.main.order_components.show_product_for_invoice import ShowProductForInvoice
from app.main.external_files.create_invoice import GenerateInvoice
import re

class CreateSalesOrder(ttk.Frame, Base):
    def __init__(self, container, mysql, user):
        # Note: when we call, instance.method(), method automatically take instance as first argument which we define as self
        # when we call, Class.method(), method need instance manually as first argument bcz it doesn't know whic one to take
        ttk.Frame.__init__(self, container)
        Base.__init__(self, mysql, user)
                
        self.customer_name_data = tk.StringVar()
        self.customer_mobile_data = tk.StringVar()
        self.customer_email_data = tk.StringVar()
        self.payment_mode_data = tk.StringVar()
        self.payment_mode_option_list = S_O_PAYMENT_MODE_OPTIONS
        self.selected_products = list()
        self.s_no = 1
        self.total_price = 0
        self.is_product_created = False

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        

        self.frame_left = ttk.Frame(self)
        self.frame_left.grid(row=1, column=0, sticky="nsew", pady=(15), padx=(20))
        self.frame_right = ttk.Frame(self, width=600)
        self.frame_right.grid(row=1, column=1, sticky="nsew", pady=(15), padx=(20))
        self.frame_right.grid_propagate (False)
        
        # Page Heading
        headlb = ttk.Label(self, text="Create Customer Invoice", style="ApplicationLabel1.TLabel", anchor="center")
        headlb.grid(row=0, column=0, columnspan=2, sticky="ew")

        # Render Form 
        self.renderLeftFrame()
        # Render Invoice Details
        self.renderRightFrame()

    
    
    def renderLeftFrame(self):

        lb_1 = ttk.Label(self.frame_left, text="Customer Name: {}".format(self.superscript("*")), style="LoginLabel.TLabel")
        lb_1.grid(row=1, column=0, sticky="w")
        
        self.customer_name_entry = ttk.Entry(self.frame_left, width=50,  textvariable=self.customer_name_data, font=("TkdefaultFont", 10, "bold"))
        self.customer_name_entry.grid(row=1, column=1, padx=(10,10), pady=(10,10))
        self.bindFormFields(self.customer_name_entry, self.validate_input)
        
        lb_2 = ttk.Label(self.frame_left, text="Customer Mobile Number: {}".format(self.superscript("*")), style="LoginLabel.TLabel")
        lb_2.grid(row=2, column=0, sticky="w")
        
        self.customer_mobile_entry = ttk.Entry(self.frame_left, width=50,  textvariable=self.customer_mobile_data, font=("TkdefaultFont", 10, "bold"))
        self.customer_mobile_entry.grid(row=2, column=1, padx=(10,10), pady=(10,10))
        self.bindFormFields(self.customer_mobile_entry, self.validate_input)

        lb_3 = ttk.Label(self.frame_left, text="Customer E-mail: ", style="LoginLabel.TLabel")
        lb_3.grid(row=3, column=0, sticky="w")
        
        self.customer_email_entry = ttk.Entry(self.frame_left, width=50,  textvariable=self.customer_email_data, font=("TkdefaultFont", 10, "bold"))
        self.customer_email_entry.grid(row=3, column=1, padx=(10,10), pady=(10,10))
        self.bindFormFields(self.customer_email_entry, self.validate_input)

        lb_4 = ttk.Label(self.frame_left, text="Payment Mode: ", style="LoginLabel.TLabel")
        lb_4.grid(row=4, column=0, sticky="w")
        
        self.payment_mode_entry = CustomCombobox(
            self.frame_left,
            textvariable=self.payment_mode_data,
            valueList=self.payment_mode_option_list, 
            width=50,
            font=("TkdefaultFont", 10, "bold"),
            justify="center",
            style="ShowProduct.TCombobox",
            state="readonly",
            )
        self.payment_mode_entry.grid(row=4, column=1)
        self.payment_mode_entry.current(1)
        
        # Product Button
        self.reset_button = ttk.Button(self.frame_left, text="New Invoice", command=self.customReset, style="ResetCancelButton.TButton")
        self.reset_button.grid(row=5, column=0, sticky="nsw", pady=(15))

        # # Discount Button
        # discount_button = ttk.Button(self.frame_left, text="Add Discount", command=lambda: print("Add Discount"), style="SignButton.TButton")
        # discount_button.grid(row=5, column=1, sticky="nsw", pady=(15))

        # Product Button
        self.product_button = ttk.Button(self.frame_left, text="Add Product", command=self.commandAddProduct, style="SignButton.TButton")
        self.product_button.grid(row=5, column=1, sticky="nse", pady=(15))
        
        self.lbsuc = ttk.Label(self.frame_left, justify="center", anchor="center", wraplength=500)


 
    def renderRightFrame(self):
        self.frame_right.columnconfigure(0, weight=1)

        rf_lb_0 = ttk.Label(self.frame_right, text="------------------- Invoice Details --------------------", style="InvoiceDetailsPageHeadLabel.TLabel")
        rf_lb_0.grid(row=0, column=0, sticky="ew")

        self.product_detail_in_invoice_instance = ShowProductDetailsInInvoice(self.frame_right, self.mysql, self.current_user, "SalesOrder", lambda: self.deleteProductFromInvoice())
        self.product_detail_in_invoice_instance.grid(row=1, column=0, sticky="ns")

        self.total_price_label = ttk.Label(
            self.frame_right,
            text=f"Total: {self.formatINR(self.total_price)}",
            font=("TkDefaultFont", 10, "bold")
         )
        self.total_price_label.grid(row=2, column=0, sticky="e", padx=(0,50))

        self.button = ttk.Button(self.frame_right,
                            text="Submit",
                            command=self.commandSubmitSalesOrder,
                            style="SignButton.TButton",
                            state="disabled"
                            )
        self.button.grid(row=8, column=0, columnspan=2, sticky="ew", pady=(15))

        self.print_button = ttk.Button(self.frame_right, text="Print Invoice", style="SignButton.TButton")



    def deleteProductFromInvoice(self):
        # list of Treeview Unique id instance for selected row
        focused_record_id = self.product_detail_in_invoice_instance.tree.focus()
        # If nothing selected do nothing
        if len(focused_record_id) >= 1:
            product_id = self.product_detail_in_invoice_instance.tree.item(focused_record_id)["values"][2]
            total_price_of_product = self.formatReverseINR(self.product_detail_in_invoice_instance.tree.item(focused_record_id)["values"][5])

            for stored_product in self.selected_products:
                if product_id == stored_product[1]:
                    self.selected_products.remove(stored_product)
                    self.total_price = round(self.total_price - total_price_of_product, 2)
            # Insert Selected Product in Invoice Details
            self.insertRowsInShowProductDetailsInInvoice(flag=False)

            # If no rows available
            if len(self.product_detail_in_invoice_instance.tree.get_children()) < 1:
                values = (
                    "",
                    "---", 
                    "---", 
                    "---",
                    "---",
                    "---"
                )
                # Delete whole rows
                self.product_detail_in_invoice_instance.tree.insert("", tk.END, values=values)
                self.product_detail_in_invoice_instance.tree.configure(selectmode="none")
        if not (self.is_product_created): self.validate_input()



    # Reset Entries
    def resetEntries(self):
        self.customer_name_entry.configure(style="TEntry")
        self.customer_mobile_entry.configure(style="TEntry")
        self.customer_email_entry.configure(style="TEntry")



    # When Add Product Button clicked
    def commandAddProduct(self):
        show_product_for_invoice_instance =  ShowProductForInvoice(self, self.mysql, self.current_user, type="SalesOrder")
        show_product_for_invoice_instance.bind("<Destroy>", lambda e: [self.modifyInvoiceProductList(e, show_product_for_invoice_instance), self.validate_input()])



    # Modify Product list
    def modifyInvoiceProductList(self, event, toplevel_treeview_instance):
        self.total_price = 0
        # <Destroy> event calls for n times for all widget and sub-widget inside, so to avoid we only do functionality when widget is main widget
        if event.widget == toplevel_treeview_instance:
            length_of_old_product_list = len(self.selected_products)
            old_product_list = self.selected_products
            new_product_list = toplevel_treeview_instance.show_product_frame.selected_products_for_invoice

            # Iteration of new selected product
            for new_product in new_product_list:
                # If this is first time selection
                if length_of_old_product_list == 0:
                    self.selected_products.append(list(new_product))  
                # If there's already some selected and tried again for selection 
                elif length_of_old_product_list > 0:
                    # If selected new_product not in previous list, add it
                    # New product can be in old product list with different quantity so we still append it and make a copy
                    if not (new_product in old_product_list):
                        self.selected_products.append(list(new_product))

                    # Now deleting product whose quantity is change and new appended but already in old product list with previous quantity
                    for old_product in old_product_list:
                        if int(new_product[1]) == int(old_product[1]) and not (old_product == new_product):
                            index = self.selected_products.index(list(old_product))
                            self.selected_products.pop(index)
            
            # Refreshing Table
            if len(self.selected_products) == 0:
                pass
            else:
                self.insertRowsInShowProductDetailsInInvoice()
                                                
                                                

    # Insert Rows in ShowProductDetailsInInvoice class instance to show product details in invoice
    def insertRowsInShowProductDetailsInInvoice(self, flag=True):  
        self.s_no = 1
        self.product_detail_in_invoice_instance.deleteWholeTree()
        for product in self.selected_products:
            quantity = int(product[4][2:]) # Removing prefix of x 1 from quantity
            price = self.formatReverseINR(product[3]) # Removing Prefix of Rupee Character
            total_unit_price = round(price * quantity, 2)
            # If Modification in total not needed
            if flag : self.total_price = self.total_price + total_unit_price
            values = (
                self.s_no, # S.No.
                self.product_detail_in_invoice_instance.morphText(product[2], 36), # Product Name 
                product[1], # Product Id
                product[3], # Product Price
                product[4], # Selected Quantity
                f"{self.formatINR(total_unit_price)}" # Total price for product with its quantity
            )
            # Delete whole rows
            self.product_detail_in_invoice_instance.tree.insert("", tk.END, values=values)
            self.product_detail_in_invoice_instance.tree.configure(selectmode="extended")
            self.s_no = self.s_no + 1 
        self.total_price_label.configure(text=f"Total: {self.formatINR(self.total_price)}")
           

           
     # Validating all entries      
    def validate_input(self, event=None):
        
        contact_regex = r"^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})?[-. ]*(\d{4})(?: *x(\d+))?\s*$"
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z]+\.[A-Z|a-z]{2,}\b'

        if self.customer_name_data.get() == "" or self.customer_name_data.get().isspace():
         self.validateGui(
            self.customer_name_entry,
            "ErrorEntry.TEntry",
            "disabled",
            1,
            "ErrorLoginRegisterLabel.TLabel", 
            "Customer name is empty",
            error_label_grid_row=8
            )
        elif len(self.customer_name_data.get().strip()) > 80:
         self.validateGui(
            self.customer_name_entry,
            "ErrorEntry.TEntry",
            "disabled",
            1,
            "ErrorLoginRegisterLabel.TLabel", 
            "Customer name should be less than 80 characters.",
            error_label_grid_row=8
            )
        elif self.customer_mobile_data.get() == "" or self.customer_mobile_data.get().isspace():
         self.validateGui(
            self.customer_mobile_entry,
            "ErrorEntry.TEntry",
            "disabled",
            1,
            "ErrorLoginRegisterLabel.TLabel", 
            "Customer mobile details are not provided.",
            error_label_grid_row=8
            )
        elif not (re.fullmatch(contact_regex, self.customer_mobile_data.get().strip())):
         self.validateGui(
            self.customer_mobile_entry,
            "ErrorEntry.TEntry",
            "disabled",
            1,
            "ErrorLoginRegisterLabel.TLabel", 
            "Invalid mobile details.",
            error_label_grid_row=8
            )
        elif len(self.customer_email_data.get()) >= 1 and  not (re.fullmatch(email_regex, self.customer_email_data.get().strip())):
         self.validateGui(
            self.customer_email_entry,
            "ErrorEntry.TEntry",
            "disabled",
            1,
            "ErrorLoginRegisterLabel.TLabel", 
            "Invalid email.",
            error_label_grid_row=8
            )
        elif len(self.selected_products) <= 0:
         self.validateGui(
            None,
            None,
            "disabled",
            1,
            "ErrorLoginRegisterLabel.TLabel", 
            "No Product is selected.",
            error_label_grid_row=8
            )
        else:
            self.validateGui(
                None,
                None,
                "normal",
                0,
                "SuccessfulLoginRegisterLabel.TLabel", 
                "Invoice generated successfully",
                error_label_grid_row=8
                )



    # Submit Product
    def commandSubmitSalesOrder(self):
        self.button.configure(state="disabled")
        self.validateGui(None, None, "disabled", 1, "SuccessfulLoginRegisterLabel.TLabel", "Invoice generation initiated ....", error_label_grid_row=8)
        flag = True
        # Ensuring no changes made in product details while transaction
        for i in range(len(self.selected_products)):
            price = self.formatReverseINR(self.selected_products[i][3]) # Removing Prefix of Rupee Character
            quantity = int(self.selected_products[i][4][2:]) # Removing prefix of x 1 from quantity
            id = self.selected_products[i][1]
            query_fetch = f"SELECT `{PRODUCT_NAME}`, `{PRODUCT_PRICE}`, `{PRODUCT_QUANTITY}` FROM `{DATABASE_NAME}`.`{PRODUCT_TABLE_NAME}` WHERE `{PRODUCT_ID}` = {id};"
            response = self.executeFetchSqlQuery(PRODUCT_TABLE_NAME, query_fetch)
            if not ((response[0][PRODUCT_PRICE]) == price):
                self.validateGui(
                    None,
                    None,
                    "disabled",
                    1,
                    "ErrorLoginRegisterLabel.TLabel",
                    f"'{response[0][PRODUCT_NAME]}' prices modified from {self.formatINR(price)} to {self.formatINR(response[0][PRODUCT_PRICE])}, please check modified prices",
                    error_label_grid_row=8
                    )
                flag = False
            if int(response[0][PRODUCT_QUANTITY]) < int(self.selected_products[i][5][2:]):
                self.validateGui(
                    None,
                    None,
                    "disabled",
                    1,
                    "ErrorLoginRegisterLabel.TLabel",
                    f"{response[0][PRODUCT_QUANTITY]} stocks left for product '{response[0][PRODUCT_NAME]}'",
                    error_label_grid_row=8
                    )
                flag = False
        
        if flag:
            # Creating  Sales order id and inserting it to database
            try:
                query = f"""INSERT INTO `{DATABASE_NAME}`.`{SALES_ORDER_TABLE_NAME}`
                ( `{SALES_ORDER_C_NAME}`, `{SALES_ORDER_C_MOBILE}`, `{SALES_ORDER_C_EMAIL}`,
                `{SALES_ORDER_PAYMENT_MODE}`, `{SALES_ORDER_FOREIGNKEY_USER_ID}`, `{SALES_ORDER_TOTAL_PRICE}`)
                VALUES (%(c_name)s, %(c_mobile)s, %(c_email)s, %(payment_mode)s, %(user)s, %(total)s)"""

                query_parameters = {
                    "c_name": self.customer_name_data.get().strip(),
                    "c_mobile": self.customer_mobile_data.get().strip(),
                    "c_email": self.customer_email_data.get().strip(),
                    "payment_mode": self.payment_mode_data.get(),
                    "user": self.current_user[USER_ID],
                    "total": self.total_price
                }
                order_id = self.executeCommitSqlQuery(SALES_ORDER_TABLE_NAME, query, query_parameters)
            except Exception as error:
                print(f"Development Error (While Creating Sales Order): {error}")
                ErrorModal("Something went wrong while creating sales order, please contact developer.", self)



            # Creating sales_order_log
            try:
                query_logs = f"""INSERT INTO `{DATABASE_NAME}`.`{SALES_ORDER_LOGS_TABLE_NAME}`
                ( 
                    `{SALES_ORDER_LOGS_LOG}`, `{SALES_ORDER_LOGS_FOREIGNKEY_SALES_ORDER_ID}`, `{SALES_ORDER_LOGS_FOREIGNKEY_USER_ID}`
                )
                VALUES (%(log)s, %(p_o_id)s, %(user_id)s)"""

                query_logs_parameters = {
                    "log": 'Order generated successfully.',
                    "p_o_id": order_id,
                    "user_id": self.current_user[USER_ID]
                }
                self.executeCommitSqlQuery(SALES_ORDER_LOGS_TABLE_NAME, query_logs, query_logs_parameters)
            except Exception as error:
                print(f"Development Error (While Creating Sales_Order_Logs): {error}")
                ErrorModal("Something went wrong while creating purchase order, please contact developer.", self)


            # After complete sales order update product quantity in iventory and their respective logs
            try:
                for data in self.selected_products:
                    product_id = int(data[1])
                    bought_quantity = int(data[4][2:])
                    availbale_quantity = int(data[5][2:])
                    query_product_quantity = f"""UPDATE `{DATABASE_NAME}`.`{PRODUCT_TABLE_NAME}` 
                    SET `{PRODUCT_QUANTITY}` = '{availbale_quantity - bought_quantity}'
                    WHERE `{PRODUCT_ID}` = {product_id}""" 
                    self.executeCommitSqlQuery(PRODUCT_TABLE_NAME, query_product_quantity)

                    # Add inventory addition log to product_log table
                    query_product_logs = f"""INSERT INTO `{DATABASE_NAME}`.`{PRODUCT_LOGS_TABLE_NAME}`
                    ( 
                        `{PRODUCT_LOGS_LOG}`, `{PRODUCT_LOGS_FOREIGNKEY_PRODUCT_ID}`, `{PRODUCT_LOGS_FOREIGNKEY_USER_ID}`
                    )
                    VALUES (%(log)s, %(p_o_id)s, %(user_id)s)"""

                    query_logs_parameters_2 = {
                        "log": f'x {bought_quantity} unit sold from inventory via Sales Order Id = {order_id}.',
                        "p_o_id": product_id,
                        "user_id": self.current_user[USER_ID]
                    }
                    self.executeCommitSqlQuery(PRODUCT_LOGS_TABLE_NAME, query_product_logs, query_logs_parameters_2)
            except Exception as error:
                print(f"Development Error (While updating quantity in product and creating a respective log): {error}")
                ErrorModal("Something went wrong while creating purchase order, please contact developer.", self) 

            
            # Inserting Product relevant to particular sales order id
            try:
                query_parameters_2 = list()
                for i in range(len(self.selected_products)):
                    product_id = self.selected_products[i][1]
                    price = self.formatReverseINR(self.selected_products[i][3]) # Removing Prefix of Rupee Character
                    quantity = int(self.selected_products[i][4][2:]) # Removing prefix of x 1 from quantity
                    query_parameters_2.append((order_id, product_id, self.selected_products[i][2], price, quantity,  round(price * quantity, 2))) 

                query_2 = f"""INSERT INTO `{DATABASE_NAME}`.`{SALES_ORDER_PRODUCT_TABLE_NAME}`
                (
                `{S_O_P_FOREIGNKEY_SALES_ORDER_ID}`,
                `{S_O_P_FOREIGNKEY_PRODUCT_ID}` ,
                `{PRODUCT_NAME}` ,
                `{S_O_P_PRODUCT_PRICE}` ,
                `{S_O_P_PRODUCT_QUANTITY}` ,
                `{S_O_P_PRODUCT_TOTAL_AMOUNT}`
                )  
                VALUES (%s, %s, %s, %s, %s, %s)"""
                
                self.mysql.query.executemany(query_2, query_parameters_2)
                self.mysql.db_connection.commit()
                self.validateGui(
                    None,
                    None,
                    "disabled",
                    1,
                    "SuccessfulLoginRegisterLabel.TLabel", 
                    "Invoice generated successfully",
                    error_label_grid_row=8
                    )
                self.customer_name_entry.configure(state="disabled")
                self.customer_mobile_entry.configure(state="disabled")
                self.customer_email_entry.configure(state="disabled")
                self.payment_mode_entry.configure(state="disabled")
                self.product_button.configure(state="disabled")
                self.product_detail_in_invoice_instance.second_functionality_button.configure(state="disabled")
                self.is_product_created = True
                self.button.grid_forget()
                self.print_button.configure(command=lambda: GenerateInvoice(sales_order_id=order_id))
                self.print_button.grid(row=8, column=0, columnspan=2, sticky="ew", pady=(15))

            except Exception as error:
                print(f"Development Error (While Creating Sales_Order_Product): {error}")
                ErrorModal("Something went wrong while creating sales order, please contact developer.", self)



    # Resetting the Page
    def customReset(self):
        self.customer_name_entry.configure(state="normal")
        self.customer_mobile_entry.configure(state="normal")
        self.customer_email_entry.configure(state="normal")
        self.payment_mode_entry.configure(state="readonly")
        self.product_button.configure(state="normal")
        self.product_detail_in_invoice_instance.second_functionality_button.configure(state="normal")
        self.validateGui(
            None,
            None,
            "disabled",
            0,
            "SuccessfulLoginRegisterLabel.TLabel", 
            "Invoice generated successfully",
            error_label_grid_row=8
            )
        # Data Reset
        self.customer_name_data.set("")
        self.customer_mobile_data.set("")
        self.customer_email_data.set("")
        self.payment_mode_data.set("")
        self.payment_mode_entry.current(1)
        self.selected_products = list()
        self.s_no = 1
        self.total_price = 0
        self.is_product_created = False
        self.button.grid(row=8, column=0, columnspan=2, sticky="ew", pady=(15))
        self.print_button.grid_forget()
        # Refreshing Table
        self.insertRowsInShowProductDetailsInInvoice()
        values = (
            "",
            "---", 
            "---", 
            "---",
            "---",
            "---"
        )
        self.product_detail_in_invoice_instance.tree.configure(selectmode="none")
        # Delete whole rows
        self.product_detail_in_invoice_instance.tree.insert("", tk.END, values=values)