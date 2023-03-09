import tkinter as tk
from tkinter import ttk
from CONSTANT.index import *
from app.base import Base
from error import ErrorModal
from app.main.order_components.show_product_details_in_invoice import ShowProductDetailsInInvoice
from app.main.order_components.show_product_for_invoice import ShowProductForInvoice
from app.main.order_components.show_supplier_for_invoice import ShowSupplierForInvoice
from app.main.external_files.create_invoice import GenerateInvoice

class CreatePurchaseOrder(ttk.Frame, Base):
    def __init__(self, container, mysql, user):
        # Note: when we call, instance.method(), method automatically take instance as first argument which we define as self
        # when we call, Class.method(), method need instance manually as first argument bcz it doesn't know whic one to take
        ttk.Frame.__init__(self, container)
        Base.__init__(self, mysql, user)
                
        self.payment_mode_data = tk.StringVar()
        self.payment_status_data = tk.StringVar()
        self.delivery_status_data = tk.StringVar()
        self.supplier_id = 0
        self.payment_mode_option_list = P_O_PAYMENT_MODE_OPTIONS
        self.payment_status_option_list = P_O_PAYMENT_STATUS_OPTIONS
        self.delivery_status_option_list = P_O_DELIVERY_STATUS_OPTIONS
        self.selected_products = list()
        self.s_no = 1
        self.total_price = 0
        self.is_product_created = False

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        

        self.frame_left = ttk.Frame(self, width=300)
        self.frame_left.grid(row=1, column=0, sticky="nsew", pady=(15), padx=(20))
        self.frame_right = ttk.Frame(self, width=300)
        self.frame_right.grid(row=1, column=1, sticky="nsew", pady=(15), padx=(20))
        self.frame_left.grid_propagate (False)
        self.frame_right.grid_propagate (False)
        
        # Page Heading
        headlb = ttk.Label(self, text="Create Purchase Order", style="ApplicationLabel1.TLabel", anchor="center")
        headlb.grid(row=0, column=0, columnspan=2, sticky="ew")

        # Render Form 
        self.renderLeftFrame()
        # Render Invoice Details
        self.renderRightFrame()

    
    
    def renderLeftFrame(self):
        self.frame_left.columnconfigure(1, weight=1)


        # Add Supplier Button
        lb = ttk.Label(self.frame_left, text="Add Supplier: ", style="LoginLabel.TLabel")
        lb.grid(row=0, column=0, sticky="w")
        self.add_supplier_button = ttk.Button(self.frame_left, text="Select Supplier", command=self.commandAddSupplier, style="SelectSupplierButton.TButton")
        self.add_supplier_button.grid(row=0, column=1, sticky="ew", pady=(15))

        # Frame Showing Supplier Details
        self.supplier_frame = ttk.Frame(self.frame_left, style="a.TFrame")

        # Supplier Details
        lb = ttk.Label(self.supplier_frame, text="Supplier's Name: ", style="LoginLabel.TLabel")
        lb.grid(row=0, column=0, sticky="w")
        self.name_label = ttk.Label(self.supplier_frame, style="SupplierLabels.TLabel")
        self.name_label.grid(row=0, column=1, sticky="ew")

        lb = ttk.Label(self.supplier_frame, text="Supplier's Id: ", style="LoginLabel.TLabel")
        lb.grid(row=1, column=0, sticky="w")
        self.id_label = ttk.Label(self.supplier_frame, style="SupplierLabels.TLabel")
        self.id_label.grid(row=1, column=1, sticky="ew")

        lb = ttk.Label(self.supplier_frame, text="Contact: ", style="LoginLabel.TLabel")
        lb.grid(row=2, column=0, sticky="w")
        self.contact_1_label = ttk.Label(self.supplier_frame, style="SupplierLabels.TLabel")
        self.contact_1_label.grid(row=2, column=1, sticky="ew")

        lb = ttk.Label(self.supplier_frame, text="Address: ", style="LoginLabel.TLabel")
        lb.grid(row=3, column=0, sticky="w")
        self.address_label = ttk.Label(self.supplier_frame, style="SupplierLabels.TLabel")
        self.address_label.grid(row=3, column=1, sticky="ew")

        lb = ttk.Label(self.supplier_frame, text="Supplier's organization: ", style="LoginLabel.TLabel")
        lb.grid(row=4, column=0, sticky="w")
        self.org_name_label = ttk.Label(self.supplier_frame, style="SupplierLabels.TLabel")
        self.org_name_label.grid(row=4, column=1, sticky="ew")

        self.org_contact_1_label = ttk.Label(self.supplier_frame, style="SupplierLabels.TLabel") # Hidden Label
        self.gst_label = ttk.Label(self.supplier_frame, style="SupplierLabels.TLabel") # Hidden Label

        lb = ttk.Label(self.supplier_frame, text="Organization's Address: ", style="LoginLabel.TLabel")
        lb.grid(row=6, column=0, sticky="w")
        self.org_address_label = ttk.Label(self.supplier_frame, style="SupplierLabels.TLabel")
        self.org_address_label.grid(row=6, column=1, sticky="ew")


        lb = ttk.Label(self.supplier_frame, text="Payment Method: ", style="LoginLabel.TLabel")
        lb.grid(row=7, column=0, sticky="w")
        self.payment_mode_entry = ttk.Combobox(
            self.supplier_frame,
            textvariable=self.payment_mode_data,
            values=self.payment_mode_option_list, 
            width=50,
            font=("TkdefaultFont", 10, "bold"),
            justify="center",
            style="ShowProduct.TCombobox",
            state="readonly",
            )
        self.payment_mode_entry.current(2)
        self.payment_mode_entry.grid(row=7, column=1, sticky="ew")

        lb = ttk.Label(self.supplier_frame, text="Payment Status: ", style="LoginLabel.TLabel")
        lb.grid(row=8, column=0, sticky="w")
        self.payment_status_entry = ttk.Combobox(
            self.supplier_frame,
            textvariable=self.payment_status_data,
            values=self.payment_status_option_list, 
            width=50,
            font=("TkdefaultFont", 10, "bold"),
            justify="center",
            style="ShowProduct.TCombobox",
            state="readonly",
            )
        self.payment_status_entry.current(0)
        self.payment_status_entry.grid(row=8, column=1, sticky="ew")

        lb = ttk.Label(self.supplier_frame, text="Delivery Status: ", style="LoginLabel.TLabel")
        lb.grid(row=9, column=0, sticky="w")
        self.delivery_status_entry = ttk.Combobox(
            self.supplier_frame,
            textvariable=self.delivery_status_data,
            values=self.delivery_status_option_list, 
            width=25,
            font=("TkdefaultFont", 10, "bold"),
            justify="center",
            style="ShowProduct.TCombobox",
            state="readonly",
            )
        self.delivery_status_entry.current(0)
        self.delivery_status_entry.grid(row=9, column=1, sticky="ew")
        
        # Product Button
        self.reset_button = ttk.Button(self.frame_left, text="New Invoice", command=self.customReset, style="ResetCancelButton.TButton")
        self.reset_button.grid(row=2, column=0, sticky="nsw", pady=(15))

        # # Discount Button
        # discount_button = ttk.Button(self.frame_left, text="Add Discount", command=lambda: print("Add Discount"), style="SignButton.TButton")
        # discount_button.grid(row=2, column=1, sticky="nsw", pady=(15))

        # Product Button
        self.product_button = ttk.Button(self.frame_left, text="Add Product", command=self.commandAddProduct, style="SignButton.TButton")
        self.product_button.grid(row=2, column=1, sticky="nse", pady=(15))
        
        self.lbsuc = ttk.Label(self.frame_left, justify="center", anchor="center", wraplength=500)



    # Configure Supplier Details
    def configureSupplierDetails(self, supplier=None, toggle_supplier_frame=0):
        if type(supplier) == None.__class__:
            pass
        else:
            # Configure Text
            self.id_label.configure(text=supplier[SUPPLIER_ID])
            self.name_label.configure(text=supplier[SUPPLIER_NAME])
            self.contact_1_label.configure(text=supplier[SUPPLIER_CONTACT_1])
            self.gst_label.configure(text=supplier[SUPPLIER_GSTIN])
            self.address_label.configure(text=supplier[SUPPLIER_ADDRESS])
            self.org_name_label.configure(text=supplier[SUPPLIER_ORGANIZATION_NAME])
            self.org_contact_1_label.configure(text=supplier[SUPPLIER_ORGANIZATION_CONTACT_1])
            self.org_address_label.configure(text=supplier[SUPPLIER_ORGANIZATION_ADDRESS])

        if toggle_supplier_frame == 1:
            self.supplier_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        else:
            self.supplier_frame.grid_forget()

        

    def renderRightFrame(self):
        self.frame_right.columnconfigure(0, weight=1)

        rf_lb_0 = ttk.Label(self.frame_right, text="------------------- Invoice Details --------------------", style="InvoiceDetailsPageHeadLabel.TLabel")
        rf_lb_0.grid(row=0, column=0, sticky="ew")

        self.product_detail_in_invoice_instance = ShowProductDetailsInInvoice(self.frame_right, self.mysql, self.current_user, "PurchaseOrder", lambda: self.deleteProductFromInvoice())
        self.product_detail_in_invoice_instance.grid(row=1, column=0, sticky="ns")

        self.total_price_label = ttk.Label(
            self.frame_right,
            text=f"Total: {self.formatINR(self.total_price)}",
            font=("TkDefaultFont", 10, "bold")
         )
        self.total_price_label.grid(row=2, column=0, sticky="e", padx=(0,50))

        self.button = ttk.Button(self.frame_right,
                            text="Submit",
                            command=self.commandSubmitPurchaseOrder,
                            style="SignButton.TButton",
                            state="disabled"
                            )
        self.button.grid(row=8, column=0, columnspan=2, sticky="ew", pady=(15))

        self.print_button = ttk.Button(self.frame_right,
                            text="Print Invoice",
                            command=lambda: print("Print Invoice"),
                            style="SignButton.TButton"
                            )



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
        pass



    # Add Supplier Details to invoice
    def commandAddSupplier(self):
        show_supplier_for_invoice = ShowSupplierForInvoice(self, self.mysql, self.current_user)
        show_supplier_for_invoice.bind("<Destroy>", lambda e: [self.modifySupplierDetailsInInvoice(e, show_supplier_for_invoice), self.validate_input()])



    # When Add Product Button clicked
    def commandAddProduct(self):
        show_product_for_invoice_instance =  ShowProductForInvoice(self, self.mysql, self.current_user, type="PurchaseOrder")
        show_product_for_invoice_instance.bind("<Destroy>", lambda e: [self.modifyInvoiceProductList(e, show_product_for_invoice_instance), self.validate_input()])



    # Add and Modify Supplier Details
    def modifySupplierDetailsInInvoice(self, event, toplevel_treeview_instance):
        # <Destroy> event calls for n times for all widget and sub-widget inside, so to avoid we only do functionality when widget is main widget
        if event.widget == toplevel_treeview_instance:
            self.supplier_id = toplevel_treeview_instance.show_supplier_frame.selected_id
            try:
                if self.supplier_id == 0:
                    pass
                else:
                    query = f"SELECT * FROM `{DATABASE_NAME}`.`{SUPPLIER_TABLE_NAME}` WHERE `{SUPPLIER_ID}` = {self.supplier_id};"
                    supplier_details = self.executeFetchSqlQuery(SUPPLIER_TABLE_NAME, query)
                    self.configureSupplierDetails(supplier_details[0], toggle_supplier_frame=1)

            except Exception as error:
                print(f"Development Error (While fetching details of Supplier for Purchase Order): {error}")
                ErrorModal("Something went wrong while selecting supplier, please contact software developer.")
            



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
            quantity = int(product[5][2:]) # Removing prefix of x 1 from quantity
            price = self.formatReverseINR(product[4]) # Removing Prefix of Rupee Character
            total_unit_price = round(price * quantity, 2)
            # If Modification in total not needed
            if flag : self.total_price = self.total_price + total_unit_price
            values = (
                self.s_no, # S.No.
                self.product_detail_in_invoice_instance.morphText(product[2], 36), # Product Name 
                product[1], # Product Id
                product[4], # Product Price
                product[5], # Selected Quantity
                f"{self.formatINR(total_unit_price)}" # Total price for product with its quantity
            )
            # Delete whole rows
            self.product_detail_in_invoice_instance.tree.insert("", tk.END, values=values)
            self.product_detail_in_invoice_instance.tree.configure(selectmode="extended")
            self.s_no = self.s_no + 1 
        self.total_price_label.configure(text=f"Total: {self.formatINR(self.total_price)}")
           

           
     # Validating all entries      
    def validate_input(self, event=None):

        if self.supplier_id == 0:
         self.validateGui(
            None,
            None,
            "disabled",
            1,
            "ErrorLoginRegisterLabel.TLabel", 
            "No Supplier Selected",
            error_label_grid_row=3
            )
        elif len(self.selected_products) <= 0:
         self.validateGui(
            None,
            None,
            "disabled",
            1,
            "ErrorLoginRegisterLabel.TLabel", 
            "No Product Selected",
            error_label_grid_row=3
            )
        else:
         self.validateGui(
            None,
            None,
            "normal",
            0,
            "SuccessfulLoginRegisterLabel.TLabel", 
            "Invoice generated successfully",
            error_label_grid_row=3
            )



    # Submit Product
    def commandSubmitPurchaseOrder(self):
        self.button.configure(state="disabled")
        self.validateGui(None, None, "disabled", 1, "SuccessfulLoginRegisterLabel.TLabel", "Invoice generation initiated ....", error_label_grid_row=3)
        
        # Creating Purchase order id and inserting it to database
        try:
            query = f"""INSERT INTO `{DATABASE_NAME}`.`{PURCHASE_ORDER_TABLE_NAME}`
            ( 
                `{PURCHASE_ORDER_FOREIGNKEY_SUPPLIER_ID}`, `{SUPPLIER_NAME}`, `{SUPPLIER_CONTACT_1}`, `{SUPPLIER_ADDRESS}`, `{SUPPLIER_GSTIN}`, `{SUPPLIER_ORGANIZATION_NAME}`,
                `{SUPPLIER_ORGANIZATION_CONTACT_1}`, `{SUPPLIER_ORGANIZATION_ADDRESS}`, `{PURCHASE_ORDER_PAYMENT_MODE}`, `{PURCHASE_ORDER_STATUS}`, 
                `{PURCHASE_ORDER_TOTAL_PRICE}`, `{PURCHASE_ORDER_PAYMENT_STATUS}`, `{PURCHASE_ORDER_DELIVERY_STATUS}`, `{PURCHASE_ORDER_FOREIGNKEY_USER_ID}`
            )
            VALUES (%(s_id)s, %(s_name)s, %(s_contact)s, %(s_address)s, %(s_gstin)s, %(s_org)s, %(s_org_contact)s, %(s_org_address)s, %(payment_mode)s, %(order_status)s, %(total)s, %(payment_status)s, %(delivery_status)s, %(user)s)"""

            query_parameters = {
                "s_id": self.id_label["text"],
                "s_name": self.name_label["text"],
                "s_contact": self.contact_1_label["text"],
                "s_address": self.address_label["text"],
                "s_gstin": self.gst_label["text"],
                "s_org": self.org_name_label["text"],
                "s_org_contact": self.org_contact_1_label["text"], 
                "s_org_address": self.org_address_label["text"],
                "payment_mode": self.payment_mode_data.get(),
                "order_status":  ORDER_COMPLETED if (self.payment_status_data.get() == PAYMENT_COMPLETED) and (self.delivery_status_data.get() == DELIVERED) else ORDER_PENDING,
                "total": self.total_price,
                "payment_status": self.payment_status_data.get(), 
                "delivery_status": self.delivery_status_data.get(),  
                "user": self.current_user[USER_ID], 
            }
            order_id = self.executeCommitSqlQuery(PURCHASE_ORDER_TABLE_NAME, query, query_parameters)
        except Exception as error:
            print(f"Development Error (While Creating Purchase Order): {error}")
            ErrorModal("Something went wrong while creating purchase order, please contact developer.", self)


        # Creating Purchase_order_log
        try:
            query_logs = f"""INSERT INTO `{DATABASE_NAME}`.`{PURCHASE_ORDER_LOGS_TABLE_NAME}`
            ( 
                `{PURCHASE_ORDER_LOGS_LOG}`, `{PURCHASE_ORDER_LOGS_FOREIGNKEY_PURCHASE_ORDER_ID}`, `{PURCHASE_ORDER_LOGS_FOREIGNKEY_USER_ID}`
            )
            VALUES (%(log)s, %(p_o_id)s, %(user_id)s)"""

            query_logs_parameters = {
                "log": 'Order generated successfully.',
                "p_o_id": order_id,
                "user_id": self.current_user[USER_ID]
            }
            self.executeCommitSqlQuery(PURCHASE_ORDER_LOGS_TABLE_NAME, query_logs, query_logs_parameters)
        except Exception as error:
            print(f"Development Error (While Creating Purchase_Order_Logs): {error}")
            ErrorModal("Something went wrong while creating purchase order, please contact developer.", self)

        # Inserting Product relevant to particular purchase order id
        try:
            query_parameters_2 = list()
            for i in range(len(self.selected_products)):
                product_id = self.selected_products[i][1]
                price = self.formatReverseINR(self.selected_products[i][4]) # Removing Prefix of Rupee Character
                quantity = int(self.selected_products[i][5][2:]) # Removing prefix of x 1 from quantity
                already_available_quantity = int(self.selected_products[i][6][2:]) # Removing prefix of x 1 from quantity
                query_parameters_2.append((order_id, product_id, self.selected_products[i][2], price, quantity,  round(price * quantity, 2)))

                # If product already delivered increase product quantities in inventory
                if self.delivery_status_data.get() == DELIVERED:
                    query_product_quantity = f"""UPDATE `{DATABASE_NAME}`.`{PRODUCT_TABLE_NAME}` 
                    SET `{PRODUCT_QUANTITY}` = '{already_available_quantity + quantity}'
                    WHERE `{PRODUCT_ID}` = {product_id}""" 
                    self.executeCommitSqlQuery(PRODUCT_TABLE_NAME, query_product_quantity)

                    # Add inventory addition log to product_log table
                    query_logs_2 = f"""INSERT INTO `{DATABASE_NAME}`.`{PRODUCT_LOGS_TABLE_NAME}`
                    ( 
                        `{PRODUCT_LOGS_LOG}`, `{PRODUCT_LOGS_FOREIGNKEY_PRODUCT_ID}`, `{PRODUCT_LOGS_FOREIGNKEY_USER_ID}`
                    )
                    VALUES (%(log)s, %(p_o_id)s, %(user_id)s)"""

                    query_logs_parameters_2 = {
                        "log": f'x {quantity} unit added to inventory via Purchase Order Id = {order_id}.',
                        "p_o_id": product_id,
                        "user_id": self.current_user[USER_ID]
                    }
                    self.executeCommitSqlQuery(PRODUCT_LOGS_TABLE_NAME, query_logs_2, query_logs_parameters_2)

            query_2 = f"""INSERT INTO `{DATABASE_NAME}`.`{PURCHASE_ORDER_PRODUCT_TABLE_NAME}`
            (
            `{P_O_P_FOREIGNKEY_PURCHASE_ORDER_ID}`,
            `{P_O_P_FOREIGNKEY_PRODUCT_ID}` ,
            `{PRODUCT_NAME}` ,
            `{P_O_P_PRODUCT_PRICE}` ,
            `{P_O_P_PRODUCT_QUANTITY}` ,
            `{P_O_P_PRODUCT_TOTAL_AMOUNT}`
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
                error_label_grid_row=3
                )

            self.payment_mode_entry.configure(state="disabled")
            self.payment_status_entry.configure(state="disabled")
            self.delivery_status_entry.configure(state="disabled")
            self.product_button.configure(state="disabled")
            self.add_supplier_button.configure(state="disabled")
            self.product_detail_in_invoice_instance.second_functionality_button.configure(state="disabled")
            self.is_product_created = False
            self.button.grid_forget()
            self.print_button.configure(command=lambda: GenerateInvoice(purchase_order_id=order_id))
            self.print_button.grid(row=8, column=0, columnspan=2, sticky="ew", pady=(15))

        except Exception as error:
            print(f"Development Error (While Creating Purchase_Order_Product): {error}")
            ErrorModal("Something went wrong while creating purchase order, please contact developer.", self)



    # Resetting the Page
    def customReset(self):
        self.payment_mode_entry.configure(state="readonly")
        self.payment_status_entry.configure(state="readonly")
        self.delivery_status_entry.configure(state="readonly")
        self.product_button.configure(state="normal")
        self.add_supplier_button.configure(state="normal")
        self.product_detail_in_invoice_instance.second_functionality_button.configure(state="normal")
        self.payment_mode_entry.current(2)
        self.payment_status_entry.current(0)
        self.delivery_status_entry.current(0)
        self.validateGui(
            None,
            None,
            "disabled",
            0,
            "SuccessfulLoginRegisterLabel.TLabel", 
            "Invoice generated successfully",
            error_label_grid_row=3
            )
        # Data Reset
        self.selected_products = list()
        self.supplier_id = 0
        self.s_no = 1
        self.total_price = 0
        self.is_product_created = False
        self.button.grid(row=8, column=0, columnspan=2, sticky="ew", pady=(15))
        self.print_button.grid_forget()
        # Hide Supplier Details Frame
        self.configureSupplierDetails()
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