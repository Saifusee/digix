import tkinter as tk
from tkinter import ttk
from CONSTANT.index import *
from app.base import Base
from error import ErrorModal
from app.main.order_components.show_product_details_in_invoice import ShowProductDetailsInInvoice
from app.main.return_cancel_order_components.show_products_in_order_toplevel import ShowProductsInOrderToplevel
from app.main.return_cancel_order_components.show_sales_order_for_r_c import ShowSalesOrderForReturnCancel
from app.main.return_cancel_order_components.show_purchase_order_for_r_c import ShowPurchaseOrderForReturnCancel
from app.main.external_files.create_invoice import GenerateInvoice

class CreateReturnCancelOrder(ttk.Frame, Base):
    def __init__(self, container, mysql, user):
        # Note: when we call, instance.method(), method automatically take instance as first argument which we define as self
        # when we call, Class.method(), method need instance manually as first argument bcz it doesn't know whic one to take
        ttk.Frame.__init__(self, container)
        Base.__init__(self, mysql, user)
                
        self.radio_value = tk.IntVar()
        self.sales_order_id = 0
        self.purchase_order_id = 0
        self.selected_records = list()
        self.s_no = 1
        self.total_refunded_amount = 0
        self.is_product_created = False
        self.purchase_order_delivery_status = ""

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
        headlb = ttk.Label(self, text="Create Return/Cancel Order", style="ApplicationLabel1.TLabel", anchor="center")
        headlb.grid(row=0, column=0, columnspan=2, sticky="ew")

        # Render Form 
        self.renderLeftFrame()
        # Render Invoice Details
        self.renderRightFrame()

    
    
    def renderLeftFrame(self):
        self.frame_left.columnconfigure(1, weight=1)

        # Radio Button for type of order selection
        lb = ttk.Label(self.frame_left, text="Order Type: ", style="LoginLabel.TLabel")
        lb.grid(row=0, column=0, sticky="w")
        f = ttk.Frame(self.frame_left)
        f.grid(row=0, column=1, sticky="nsew")
        f.columnconfigure(0, weight=1)
        f.columnconfigure(1, weight=1)
        f.rowconfigure(0, weight=1)


        self.radio_button_1 = ttk.Radiobutton(f, text="Purchase Order", variable=self.radio_value, value=0, style="OrderRadiobutton.TRadiobutton")
        self.radio_button_1.grid(row=0, column=0, sticky="e", padx=(0, 20))
        self.radio_button_2 = ttk.Radiobutton(f, text="Sales Order", variable=self.radio_value, value=1, style="OrderRadiobutton.TRadiobutton")
        self.radio_button_2.grid(row=0, column=1, sticky="w", padx=(20,0))
        self.radio_button_2.invoke()

        # Add Order Button
        self.gb_label = ttk.Label(self.frame_left, text="Add Order: ", style="LoginLabel.TLabel")
        self.gb_label.grid(row=1, column=0, sticky="w")
        self.add_order_button = ttk.Button(self.frame_left, text="Select Order", command=self.commandAddOrder, style="SelectSupplierButton.TButton")
        self.add_order_button.grid(row=1, column=1, sticky="ew", pady=(15))
        
        # Frame Showing Order Details
        self.sales_order_frame = ttk.Frame(self.frame_left, style="a.TFrame")
        self.purchase_order_frame = ttk.Frame(self.frame_left, style="a.TFrame")


        # Sales Order Details
        rf_lb_0 = ttk.Label(self.sales_order_frame, text="------------------- Sales Order Details --------------------", style="InvoiceDetailsPageHeadLabel.TLabel")
        rf_lb_0.grid(row=0, column=0, columnspan=2, sticky="ew")

        lb = ttk.Label(self.sales_order_frame, text="Order Id: ", style="LoginLabel.TLabel")
        lb.grid(row=1, column=0, sticky="w")
        self.s_o_id_label = ttk.Label(self.sales_order_frame, style="SupplierLabels.TLabel")
        self.s_o_id_label.grid(row=1, column=1, sticky="ew")

        lb = ttk.Label(self.sales_order_frame, text="Customer Name: ", style="LoginLabel.TLabel")
        lb.grid(row=2, column=0, sticky="w")
        self.s_o_customer_name_label = ttk.Label(self.sales_order_frame, style="SupplierLabels.TLabel")
        self.s_o_customer_name_label.grid(row=2, column=1, sticky="ew")

        lb = ttk.Label(self.sales_order_frame, text="Customer Mobile: ", style="LoginLabel.TLabel")
        lb.grid(row=3, column=0, sticky="w")
        self.s_o_customer_mobile_label = ttk.Label(self.sales_order_frame, style="SupplierLabels.TLabel")
        self.s_o_customer_mobile_label.grid(row=3, column=1, sticky="ew")

        lb = ttk.Label(self.sales_order_frame, text="Customer E-Mail: ", style="LoginLabel.TLabel")
        lb.grid(row=4, column=0, sticky="w")
        self.s_o_customer_email_label = ttk.Label(self.sales_order_frame, style="SupplierLabels.TLabel")
        self.s_o_customer_email_label.grid(row=4, column=1, sticky="ew")

        lb = ttk.Label(self.sales_order_frame, text="Order Details: ", style="LoginLabel.TLabel")
        lb.grid(row=5, column=0, sticky="w")
        self.s_o_details_label = ttk.Label(self.sales_order_frame, style="SupplierLabels.TLabel")
        self.s_o_details_label.grid(row=5, column=1, sticky="ew")

        lb = ttk.Label(self.sales_order_frame, text="Order Amount (\u20B9): ", style="LoginLabel.TLabel")
        lb.grid(row=6, column=0, sticky="w")
        self.s_o_amount_label = ttk.Label(self.sales_order_frame, style="SupplierLabels.TLabel")
        self.s_o_amount_label.grid(row=6, column=1, sticky="ew")

        lb = ttk.Label(self.sales_order_frame, text="Generated By: ", style="LoginLabel.TLabel")
        lb.grid(row=7, column=0, sticky="w")
        self.s_o_user_label = ttk.Label(self.sales_order_frame, style="SupplierLabels.TLabel")
        self.s_o_user_label.grid(row=7, column=1, sticky="ew")

        lb = ttk.Label(self.sales_order_frame, text="Creation Date: ", style="LoginLabel.TLabel")
        lb.grid(row=8, column=0, sticky="w")
        self.s_o_date_label = ttk.Label(self.sales_order_frame, style="SupplierLabels.TLabel")
        self.s_o_date_label.grid(row=8, column=1, sticky="ew")


        # Purchase Order Details
        rf_lb_0 = ttk.Label(self.purchase_order_frame, text="------------------- Purchase Order Details --------------------", style="InvoiceDetailsPageHeadLabel.TLabel")
        rf_lb_0.grid(row=0, column=0, columnspan=2, sticky="ew")

        lb = ttk.Label(self.purchase_order_frame, text="Order Id: ", style="LoginLabel.TLabel")
        lb.grid(row=1, column=0, sticky="w")
        self.p_o_id_label = ttk.Label(self.purchase_order_frame, style="SupplierLabels.TLabel")
        self.p_o_id_label.grid(row=1, column=1, sticky="ew")

        lb = ttk.Label(self.purchase_order_frame, text="Supplier Name: ", style="LoginLabel.TLabel")
        lb.grid(row=2, column=0, sticky="w")
        self.p_o_supplier_name_label = ttk.Label(self.purchase_order_frame, style="SupplierLabels.TLabel")
        self.p_o_supplier_name_label.grid(row=2, column=1, sticky="ew")

        lb = ttk.Label(self.purchase_order_frame, text="Supplier's Contact: ", style="LoginLabel.TLabel")
        lb.grid(row=3, column=0, sticky="w")
        self.p_o_supplier_contact_label = ttk.Label(self.purchase_order_frame, style="SupplierLabels.TLabel")
        self.p_o_supplier_contact_label.grid(row=3, column=1, sticky="ew")

        lb = ttk.Label(self.purchase_order_frame, text="Supplier's Organization: ", style="LoginLabel.TLabel")
        lb.grid(row=4, column=0, sticky="w")
        self.p_o_org_label = ttk.Label(self.purchase_order_frame, style="SupplierLabels.TLabel")
        self.p_o_org_label.grid(row=4, column=1, sticky="ew")

        lb = ttk.Label(self.purchase_order_frame, text="Order Details: ", style="LoginLabel.TLabel")
        lb.grid(row=5, column=0, sticky="w")
        self.p_o_details_label = ttk.Label(self.purchase_order_frame, style="SupplierLabels.TLabel")
        self.p_o_details_label.grid(row=5, column=1, sticky="ew")

        lb = ttk.Label(self.purchase_order_frame, text="Order Amount (\u20B9): ", style="LoginLabel.TLabel")
        lb.grid(row=6, column=0, sticky="w")
        self.p_o_amount_label = ttk.Label(self.purchase_order_frame, style="SupplierLabels.TLabel")
        self.p_o_amount_label.grid(row=6, column=1, sticky="ew")

        lb = ttk.Label(self.purchase_order_frame, text="Generated By: ", style="LoginLabel.TLabel")
        lb.grid(row=7, column=0, sticky="w")
        self.p_o_user_label = ttk.Label(self.purchase_order_frame, style="SupplierLabels.TLabel")
        self.p_o_user_label.grid(row=7, column=1, sticky="ew")

        lb = ttk.Label(self.purchase_order_frame, text="Creation Date: ", style="LoginLabel.TLabel")
        lb.grid(row=8, column=0, sticky="w")
        self.p_o_date_label = ttk.Label(self.purchase_order_frame, style="SupplierLabels.TLabel")
        self.p_o_date_label.grid(row=8, column=1, sticky="ew")

        # Reset Button
        self.reset_button = ttk.Button(self.frame_left, text="New", command=self.customReset, style="ResetCancelButton.TButton")
        self.reset_button.grid(row=3, column=0, sticky="nsw", pady=(15))

        # Modify Order Details Button
        self.product_button = ttk.Button(
            self.frame_left, 
            text="Modify Order Details", 
            command=self.commandAddModifiedProduct, 
            style="SignButton.TButton",
            state="disabled"
            )
        self.product_button.grid(row=3, column=1, sticky="nse", pady=(15))
        
        self.lbsuc = ttk.Label(self.frame_left, justify="center", anchor="center", wraplength=500)
        
        # RadioButton Command added here last because radioButtonSelect() method have widget which declared after RadioButtons
        self.radio_button_1.configure(command=self.radioButtonSelect)
        self.radio_button_2.configure(command=self.radioButtonSelect)



    # Radio Button changes value
    def radioButtonSelect(self):
        self.customReset()



    # Configure Supplier Details
    def configureOrderDetails(self, toggle_frame=0, record_details=None):
        if type(record_details) == None.__class__:
            pass
        else:
            details_text = f"Total Products = {record_details[PRODUCT_COUNT]}\nTotal Units = {record_details[UNIT_COUNT]}"
            # Configure Text
            if toggle_frame == "PurchaseOrder":
                self.p_o_id_label.configure(text=record_details[PURCHASE_ORDER_ID])
                self.p_o_supplier_name_label.configure(text=f"{record_details[SUPPLIER_NAME]}\nSupplier Id = {record_details[PURCHASE_ORDER_FOREIGNKEY_SUPPLIER_ID]}")
                self.p_o_supplier_contact_label.configure(text=record_details[SUPPLIER_CONTACT_1])
                self.p_o_org_label.configure(text=record_details[SUPPLIER_ORGANIZATION_NAME])
                self.p_o_details_label.configure(text=details_text)
                self.p_o_amount_label.configure(text=record_details[PURCHASE_ORDER_TOTAL_PRICE])
                self.p_o_user_label.configure(text=record_details[USERNAME])
                self.p_o_date_label.configure(text=record_details[CREATED_AT])
                self.purchase_order_delivery_status = record_details[PURCHASE_ORDER_DELIVERY_STATUS]
            elif toggle_frame == "SalesOrder":
                self.s_o_id_label.configure(text=record_details[SALES_ORDER_ID])
                self.s_o_customer_name_label.configure(text=record_details[SALES_ORDER_C_NAME])
                self.s_o_customer_mobile_label.configure(text=record_details[SALES_ORDER_C_MOBILE])
                self.s_o_customer_email_label.configure(text=record_details[SALES_ORDER_C_EMAIL])
                self.s_o_details_label.configure(text=details_text)
                self.s_o_amount_label.configure(text=record_details[SALES_ORDER_TOTAL_PRICE])
                self.s_o_user_label.configure(text=record_details[USERNAME])
                self.s_o_date_label.configure(text=record_details[CREATED_AT])

        self.purchase_order_frame.grid_forget()
        self.sales_order_frame.grid_forget()
        if toggle_frame == "PurchaseOrder":
            self.gb_label.grid_forget()
            self.add_order_button.grid_forget()
            self.purchase_order_frame.grid(row=2, column=0, columnspan=2, sticky="ns", pady=(5,0))
        elif toggle_frame == "SalesOrder":
            self.gb_label.grid_forget()
            self.add_order_button.grid_forget()
            self.sales_order_frame.grid(row=2, column=0, columnspan=2, sticky="ns", pady=(5,0))

 

    def renderRightFrame(self):
        self.frame_right.columnconfigure(0, weight=1)

        rf_lb_0 = ttk.Label(self.frame_right, text="------------------- Selected Details --------------------", style="InvoiceDetailsPageHeadLabel.TLabel")
        rf_lb_0.grid(row=0, column=0, sticky="ew")

        self.product_detail_in_invoice_instance = ShowProductDetailsInInvoice(self.frame_right, self.mysql, self.current_user, "ReturnCancelOrder", lambda: self.deleteProductFromInvoice())
        self.product_detail_in_invoice_instance.grid(row=1, column=0, sticky="ns")

        self.total_refunded_amount_label = ttk.Label(
            self.frame_right,
            text=f"Total: {self.formatINR(self.total_refunded_amount)}",
            font=("TkDefaultFont", 10, "bold")
         )
        self.total_refunded_amount_label.grid(row=2, column=0, sticky="e", padx=(0,50))

        self.button = ttk.Button(self.frame_right,
                            text="Submit",
                            command=self.commandSubmitReturnCancelOrder,
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
            refunded_price = self.formatReverseINR(self.product_detail_in_invoice_instance.tree.item(focused_record_id)["values"][5])

            for stored_product in self.selected_records:
                if product_id == stored_product["product_id"]:
                    self.selected_records.remove(stored_product)
                    self.total_refunded_amount = round(self.total_refunded_amount - refunded_price, 2)
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
    def commandAddOrder(self):
        order_type = self.radio_value.get()

        # Purchase Order
        if order_type == 0:
            show_purchase_order_instance = ShowPurchaseOrderForReturnCancel(self, self.mysql, self.current_user, is_r_c_page=True)
            show_purchase_order_instance.bind("<Destroy>", lambda e: [self.commandAddPurchaseOrder(e, show_purchase_order_instance), self.validate_input()])

        # Sales Order
        elif order_type == 1:
            show_sales_order_instance = ShowSalesOrderForReturnCancel(self, self.mysql, self.current_user, is_r_c_page=True)
            show_sales_order_instance.bind("<Destroy>", lambda e: [self.commandAddSalesOrder(e, show_sales_order_instance), self.validate_input()])
        # Nothing
        else:
            pass




    # When A Purchase Order is selected
    def commandAddPurchaseOrder(self, event, toplevel_treeview_instance):
        # Child Widget destroy event ignored
        if event.widget == toplevel_treeview_instance:
            self.purchase_order_id = toplevel_treeview_instance.show_purchase_order_frame.selected_id

            if self.purchase_order_id == 0 or self.purchase_order_id == "" or type(self.purchase_order_id) == None.__class__:
                pass
            else:
                # Getting saved query
                queryy =  self.saved_query_purchase_order_morphed
                # Making modification in query for total bought product and total units in order column
                add_on_query = f""" , 
                (SELECT COUNT(*) FROM `{DATABASE_NAME}`.`{PURCHASE_ORDER_PRODUCT_TABLE_NAME}` 
                WHERE `{P_O_P_FOREIGNKEY_PURCHASE_ORDER_ID}` = {self.purchase_order_id}) as {PRODUCT_COUNT} ,
                (SELECT SUM(`{PRODUCT_QUANTITY}`) FROM `{DATABASE_NAME}`.`{PURCHASE_ORDER_PRODUCT_TABLE_NAME}`
                WHERE `{P_O_P_FOREIGNKEY_PURCHASE_ORDER_ID}` = {self.purchase_order_id}) as {UNIT_COUNT} 
                FROM `{DATABASE_NAME}`.`{PURCHASE_ORDER_TABLE_NAME}` AS A
                """
                # Updating modification in query
                queryy = queryy.replace(f"FROM `{DATABASE_NAME}`.`{PURCHASE_ORDER_TABLE_NAME}` AS A", add_on_query)
                purchase_order = self.queryFetchSinglePurchaseOrder(self.purchase_order_id, custom_query=queryy)  

                # Configuring Label Details
                self.configureOrderDetails(toggle_frame="PurchaseOrder", record_details=purchase_order[0])     



    # When A Sales Order is selected
    def commandAddSalesOrder(self, event, toplevel_treeview_instance):
        # Child Widget destroy event ignored
        if event.widget == toplevel_treeview_instance:
            self.sales_order_id = toplevel_treeview_instance.show_sales_order_frame.selected_id

            if self.sales_order_id == 0 or self.sales_order_id == "" or type(self.sales_order_id) == None.__class__:
                pass
            else:
            # Getting saved query
                queryy =  self.saved_query_sales_order_morphed
                # Making modification in query for total bought product and total units in order column
                add_on_query = f""" , 
                (SELECT COUNT(*) FROM `{DATABASE_NAME}`.`{SALES_ORDER_PRODUCT_TABLE_NAME}` 
                WHERE `{S_O_P_FOREIGNKEY_SALES_ORDER_ID}` = {self.sales_order_id}) as {PRODUCT_COUNT} ,
                (SELECT SUM(`{PRODUCT_QUANTITY}`) FROM `{DATABASE_NAME}`.`{SALES_ORDER_PRODUCT_TABLE_NAME}`
                WHERE `{S_O_P_FOREIGNKEY_SALES_ORDER_ID}` = {self.sales_order_id}) as {UNIT_COUNT} 
                FROM `{DATABASE_NAME}`.`{SALES_ORDER_TABLE_NAME}` AS A
                """
                # Updating modification in query
                queryy = queryy.replace(f"FROM `{DATABASE_NAME}`.`{SALES_ORDER_TABLE_NAME}` AS A", add_on_query)
                sales_order = self.queryFetchSingleSalesOrder(self.sales_order_id, custom_query=queryy)  
                # Configuring Label Details
                self.configureOrderDetails(toggle_frame="SalesOrder", record_details=sales_order[0])   



    # When Add Product Button clicked
    def commandAddModifiedProduct(self):
        if self.radio_value.get() == 0:
            type_for_treeview =  "PurchaseOrder"
            order_id = self.purchase_order_id
        else:
            type_for_treeview =  "SalesOrder"
            order_id = self.sales_order_id
            
        show_products_in_order_instance =  ShowProductsInOrderToplevel(self, self.mysql, self.current_user, order_id=order_id, type=type_for_treeview)
        show_products_in_order_instance.bind("<Destroy>", lambda e: [self.modifyOrderProductList(e, show_products_in_order_instance), self.validate_input()])
            



    # Modify Product list
    def modifyOrderProductList(self, event, toplevel_treeview_instance):
        # <Destroy> event calls for n times for all widget and sub-widget inside, so to avoid we only do functionality when widget is main widget
        if event.widget == toplevel_treeview_instance:
            self.total_refunded_amount = 0
            length_of_old_selected_records = len(self.selected_records)
            old_selected_data = self.selected_records
            new_selected_data = toplevel_treeview_instance.show_product_for_invoice_instance.selected_data

            # Iteration of new selected product
            for new_data in new_selected_data:
                # If this is first time selection
                if length_of_old_selected_records == 0:
                    self.selected_records.append(dict(new_data))  
                # If there's already some selected and tried again for selection 
                elif length_of_old_selected_records > 0:
                    # If selected new_data not in previous list, add it
                    # New product can be in old product list with different quantity so we still append it and make a copy
                    if not (new_data in old_selected_data):
                        self.selected_records.append(dict(new_data))

                    # Now deleting product whose quantity is change and new appended but already in old product list with previous quantity
                    for old_data in old_selected_data:
                        if int(new_data["order_product_id"]) == int(old_data["order_product_id"]) and not (old_data == new_data):
                            index = self.selected_records.index(dict(old_data))
                            self.selected_records.pop(index)

            # Refreshing Table
            if len(self.selected_records) == 0:
                pass
            else:
                self.insertRowsInShowProductDetailsInInvoice()
                                                
                                                

    # Insert Rows in ShowProductDetailsInInvoice class instance to show product details in invoice
    def insertRowsInShowProductDetailsInInvoice(self, flag=True):
        self.s_no = 1
        self.product_detail_in_invoice_instance.deleteWholeTree()
        for record in self.selected_records:
            cancel_quantity = record["cancelled_quantity"]
            return_quantity = record["returned_quantity"]
            refund_amount = record["refunded_amount"]
            product_id = record["product_id"]
            product_name = record["product_name"]

            # If Modification in total not needed
            if flag : self.total_refunded_amount = self.total_refunded_amount + float(refund_amount)
            values = (
                self.s_no, # S.No.
                self.product_detail_in_invoice_instance.morphText(product_name, 36), # Product Name 
                product_id, # Product Id
                f"x {cancel_quantity}", # Product Price
                f"x {return_quantity}", # Selected Quantity
                self.formatINR(refund_amount)
            )
            # Delete whole rows
            self.product_detail_in_invoice_instance.tree.insert("", tk.END, values=values)
            self.product_detail_in_invoice_instance.tree.configure(selectmode="extended")
            self.s_no = self.s_no + 1 
        self.total_refunded_amount_label.configure(text=f"Total Refunded Amount: {self.formatINR(self.total_refunded_amount)}")
           

           
     # Validating all entries      
    def validate_input(self, event=None):

        if self.sales_order_id == 0 and self.purchase_order_id == 0:
         self.validateGui(
            None,
            None,
            "disabled",
            1,
            "ErrorLoginRegisterLabel.TLabel", 
            "No Order Selected",
            error_label_grid_row=4
            )
        elif len(self.selected_records) <= 0:
         self.validateGui(
            None,
            None,
            "disabled",
            1,
            "ErrorLoginRegisterLabel.TLabel", 
            "No Product is selected for cancellation or modification.",
            error_label_grid_row=4
            )
        else:
         self.validateGui(
            None,
            None,
            "normal",
            0,
            "SuccessfulLoginRegisterLabel.TLabel", 
            "Return/Cancel Order generated successfully",
            error_label_grid_row=4
            )



    # Submit Product
    def commandSubmitReturnCancelOrder(self):
        self.button.configure(state="disabled")
        self.validateGui(None, None, "disabled", 1, "SuccessfulLoginRegisterLabel.TLabel", "Order generation initiated ....", error_label_grid_row=4)

        try:
            # Generation of Return/Cancel Order
            if self.sales_order_id == 0 or self.sales_order_id == "" or type(self.sales_order_id) == None.__class__:
                self.sales_order_id = None
            elif self.purchase_order_id == 0 or self.purchase_order_id == "" or type(self.purchase_order_id) == None.__class__:
                self.purchase_order_id = None
            query = f""" INSERT INTO `{DATABASE_NAME}`.`{RETURN_CANCEL_ORDER_TABLE_NAME}`
            (`{RETURN_CANCEL_ORDER_FOREIGNKEY_SALES_ORDER_ID}` , `{RETURN_CANCEL_ORDER_FOREIGNKEY_PURCHASE_ORDER_ID}` ,
            `{RETURN_CANCEL_ORDER_TOTAL_REFUND_AMOUNT}` , `{RETURN_CANCEL_ORDER_FOREIGNKEY_USER_ID}`)
            VALUES (%s, %s, %s, %s);"""
            query_params = (
                self.sales_order_id,
                self.purchase_order_id,
                self.total_refunded_amount,
                self.current_user[USER_ID]
            )
            return_cancel_order_id = self.executeCommitSqlQuery(RETURN_CANCEL_ORDER_TABLE_NAME, query, query_params)



            # Generation of relevant products and their details in Return/Cancel Order
            query_2 = f""" INSERT INTO `{DATABASE_NAME}`.`{RETURN_CANCEL_ORDER_PRODUCT_TABLE_NAME}`
            (`{R_C_O_P_FOREIGNKEY_RETURN_CANCEL_ORDER_ID}` , `{R_C_O_P_FOREIGNKEY_PRODUCT_ID}` , `{PRODUCT_NAME}` ,
             `{R_C_O_P_PRODUCT_REFUND_AMOUNT}` , `{R_C_O_P_PRODUCT_CANCEL_QUANTITY}` , `{R_C_O_P_PRODUCT_RETURN_QUANTITY}` , `{R_C_O_P_REASON}`)
            VALUES (%s, %s, %s, %s, %s, %s, %s);"""

            query_params_2 = list()
            for data in self.selected_records:
                query_params_2.append((
                    return_cancel_order_id,
                    data["product_id"],
                    data["product_name"],
                    data["refunded_amount"],
                    data["cancelled_quantity"],
                    data["returned_quantity"],
                    data["reason"]
                ))
            self.mysql.query.executemany(query_2, query_params_2)
            self.mysql.db_connection.commit()


            # Updating Cancelled and Returned quantities in Sales and Purchase Order's Product Table
            for data in self.selected_records:
                cancelled_quantity = int(data["already_cancelled_quantity"]) + int(data["cancelled_quantity"])
                returned_quantity = int(data["already_returned_quantity"]) + int(data["returned_quantity"])
                refunded_amount = float(data["already_refunded_amount"])  + float(data["refunded_amount"])

                # If Sales Order is selected
                if self.radio_value.get() == 1:
                    query_3 = f"""UPDATE `{DATABASE_NAME}`.`{SALES_ORDER_PRODUCT_TABLE_NAME}` SET
                    `{CANCELLED_QUANTITY}` = '{cancelled_quantity}' ,
                    `{RETURNED_QUANTITY}` = '{returned_quantity}' ,
                    `{REFUNDED_AMOUNT}` = '{refunded_amount}'
                    WHERE `{S_O_P_ID}` = {data["order_product_id"]};"""
                    self.executeCommitSqlQuery(SALES_ORDER_PRODUCT_TABLE_NAME, query_3)

                    # Create Sales Order Log
                    if not (int(data["returned_quantity"]) == 0) and not (int(data["cancelled_quantity"]) == 0):
                        a = f"x {data['cancelled_quantity']} and x {data['returned_quantity']} units of "
                        b = f"'{data['product_name']}' marked for cancellation and return in this order respectively."
                        log_data_1 = a+b
                    elif not (int(data["returned_quantity"]) == 0):
                        log_data_1 = f"x {data['returned_quantity']} units of '{data['product_name']}' marked for return in this order."
                    elif not (int(data["cancelled_quantity"]) == 0):
                        log_data_1 = f"x {data['cancelled_quantity']} units of '{data['product_name']}' marked for cancellation in this order."
                    query_4 = f"""INSERT INTO `{DATABASE_NAME}`.`{SALES_ORDER_LOGS_TABLE_NAME}` 
                    (`{SALES_ORDER_LOGS_LOG}` , `{SALES_ORDER_LOGS_FOREIGNKEY_SALES_ORDER_ID}` , `{SALES_ORDER_LOGS_FOREIGNKEY_USER_ID}`)
                    VALUES (%s , %s , %s) ;"""
                    query_4_logs_parameters  = (log_data_1, self.sales_order_id, self.current_user[USER_ID])
                    self.executeCommitSqlQuery(SALES_ORDER_LOGS_TABLE_NAME, query_4, query_4_logs_parameters)

                    # If Order already delivered then update quantity of product in inventory.
                    query_fetch_product_qunatity = f"SELECT `{PRODUCT_QUANTITY}` FROM `{DATABASE_NAME}`.`{PRODUCT_TABLE_NAME}` WHERE `{PRODUCT_ID}` = {data['product_id']}"
                    available_stock_quantity = self.executeFetchSqlQuery(PRODUCT_TABLE_NAME, query_fetch_product_qunatity)[0][PRODUCT_QUANTITY]
                    effective_new_product_quantity = (int(available_stock_quantity) +  int(data["cancelled_quantity"])) +  int(data["returned_quantity"])
                    query_5 = f"""UPDATE `{DATABASE_NAME}`.`{PRODUCT_TABLE_NAME}` 
                    SET `{PRODUCT_QUANTITY}` = '{effective_new_product_quantity}'
                    WHERE `{PRODUCT_ID}` = {data['product_id']}""" 
                    self.executeCommitSqlQuery(PRODUCT_TABLE_NAME, query_5)

                    # Add inventory addition log to product_log table
                    if not (int(data["returned_quantity"]) == 0) and not (int(data["cancelled_quantity"]) == 0):
                        a = f"x {data['cancelled_quantity']} and x {data['returned_quantity']} units are "
                        b = f"added back to inventory via Return/Cancel Order Id = {return_cancel_order_id} because they are marked for "
                        c = f"cancellation and return in Sales Order Id = {self.sales_order_id}."
                        log_data_0 = a + b + c
                    elif not (int(data["returned_quantity"]) == 0):
                        a = f"x {data['returned_quantity']} units are added back to inventory via Return/Cancel Order Id = {return_cancel_order_id} "
                        b = f"because they are marked for return in Sales Order Id = {self.sales_order_id}."
                        log_data_0 = a + b
                    elif not (int(data["cancelled_quantity"]) == 0):
                        a = f"x {data['cancelled_quantity']} units are added back to inventory via Return/Cancel Order Id = {return_cancel_order_id} "
                        b = f"because they are marked for cancellation in Sales Order Id = {self.sales_order_id}."
                        log_data_0 = a + b
                    query_6 = f"""INSERT INTO `{DATABASE_NAME}`.`{PRODUCT_LOGS_TABLE_NAME}`
                    ( 
                        `{PRODUCT_LOGS_LOG}`, `{PRODUCT_LOGS_FOREIGNKEY_PRODUCT_ID}`, `{PRODUCT_LOGS_FOREIGNKEY_USER_ID}`
                    )
                    VALUES (%(log)s, %(p_o_id)s, %(user_id)s)"""

                    query_6_logs_parameters = {
                        "log": log_data_0,
                        "p_o_id": data['product_id'],
                        "user_id": self.current_user[USER_ID]
                    }
                    self.executeCommitSqlQuery(PRODUCT_LOGS_TABLE_NAME, query_6, query_6_logs_parameters)
                    

                # If Purchase Order is selected
                elif self.radio_value.get() == 0:
                    # Updating Return and Cancel Quantity in PURCHASE_ORDER_PRODUCT
                    query_3 = f"""UPDATE `{DATABASE_NAME}`.`{PURCHASE_ORDER_PRODUCT_TABLE_NAME}` SET
                    `{CANCELLED_QUANTITY}` = '{cancelled_quantity}' ,
                    `{RETURNED_QUANTITY}` = '{returned_quantity}' ,
                    `{REFUNDED_AMOUNT}` = '{refunded_amount}'
                    WHERE `{P_O_P_ID}` = {data["order_product_id"]};"""
                    self.executeCommitSqlQuery(PURCHASE_ORDER_PRODUCT_TABLE_NAME, query_3)

                    # Create Purchase Order Log
                    if not (int(data["returned_quantity"]) == 0) and not (int(data["cancelled_quantity"]) == 0):
                        a = f"x {data['cancelled_quantity']} and x {data['returned_quantity']} units of "
                        b = f"'{data['product_name']}' marked for cancellation and return in this order respectively."
                        log_data_1 = a+b
                    elif not (int(data["returned_quantity"]) == 0):
                        log_data_1 = f"x {data['returned_quantity']} units of '{data['product_name']}' marked for return in this order."
                    elif not (int(data["cancelled_quantity"]) == 0):
                        log_data_1 = f"x {data['cancelled_quantity']} units of '{data['product_name']}' marked for cancellation in this order."
                    query_4 = f"""INSERT INTO `{DATABASE_NAME}`.`{PURCHASE_ORDER_LOGS_TABLE_NAME}` 
                    (`{PURCHASE_ORDER_LOGS_LOG}` , `{PURCHASE_ORDER_LOGS_FOREIGNKEY_PURCHASE_ORDER_ID}` , `{PURCHASE_ORDER_LOGS_FOREIGNKEY_USER_ID}`)
                    VALUES (%s , %s , %s) ;"""
                    query_4_logs_parameters  = (log_data_1, self.purchase_order_id, self.current_user[USER_ID])
                    self.executeCommitSqlQuery(PURCHASE_ORDER_LOGS_TABLE_NAME, query_4, query_4_logs_parameters)

                    # If Order already delivered then update quantity of product in inventory and create product logs.
                    if self.purchase_order_delivery_status == DELIVERED:
                        # If Order already delivered then update quantity of product in inventory.
                        query_fetch_product_qunatity = f"SELECT `{PRODUCT_QUANTITY}` FROM `{DATABASE_NAME}`.`{PRODUCT_TABLE_NAME}` WHERE `{PRODUCT_ID}` = {data['product_id']}"
                        available_stock_quantity = self.executeFetchSqlQuery(PRODUCT_TABLE_NAME, query_fetch_product_qunatity)[0][PRODUCT_QUANTITY]
                        effective_new_product_quantity = (int(available_stock_quantity) -  int(data["cancelled_quantity"])) -  int(data["returned_quantity"])
                        query_5 = f"""UPDATE `{DATABASE_NAME}`.`{PRODUCT_TABLE_NAME}` 
                        SET `{PRODUCT_QUANTITY}` = '{effective_new_product_quantity}'
                        WHERE `{PRODUCT_ID}` = {data['product_id']}""" 
                        self.executeCommitSqlQuery(PRODUCT_TABLE_NAME, query_5)

                        # Add inventory addition log to product_log table
                        if not (int(data["returned_quantity"]) == 0) and not (int(data["cancelled_quantity"]) == 0):
                            a = f"x {data['cancelled_quantity']} and x {data['returned_quantity']} units are removed "
                            b = f"from inventory via Return/Cancel Order Id = {return_cancel_order_id} because they are marked for "
                            c = f"cancellation and return in Purchase Order Id = {self.purchase_order_id}."
                            log_data_2 = a + b + c
                        elif not (int(data["returned_quantity"]) == 0):
                            a = f"x {data['returned_quantity']} units are removed from inventory via Return/Cancel Order Id = {return_cancel_order_id} "
                            b = f"because they are marked for return in Purchase Order Id = {self.purchase_order_id}."
                            log_data_2 = a + b
                        elif not (int(data["cancelled_quantity"]) == 0):
                            a = f"x {data['cancelled_quantity']} units are removed from inventory via Return/Cancel Order Id = {return_cancel_order_id} "
                            b = f"because they are marked for cancellation in Purchase Order Id = {self.purchase_order_id}."
                            log_data_2 = a + b
                        query_6 = f"""INSERT INTO `{DATABASE_NAME}`.`{PRODUCT_LOGS_TABLE_NAME}`
                        ( 
                            `{PRODUCT_LOGS_LOG}`, `{PRODUCT_LOGS_FOREIGNKEY_PRODUCT_ID}`, `{PRODUCT_LOGS_FOREIGNKEY_USER_ID}`
                        )
                        VALUES (%(log)s, %(p_o_id)s, %(user_id)s)"""

                        query_6_logs_parameters = {
                            "log": log_data_2,
                            "p_o_id": data['product_id'],
                            "user_id": self.current_user[USER_ID]
                        }
                        self.executeCommitSqlQuery(PRODUCT_LOGS_TABLE_NAME, query_6, query_6_logs_parameters)
                        
                        

            # Modify Order Status
            # If Sales Order is selected
            if self.radio_value.get() == 1:
                query_7 = f"""SELECT SUM(`{S_O_P_PRODUCT_QUANTITY}`) AS  {S_O_P_PRODUCT_QUANTITY} , SUM(`{RETURNED_QUANTITY}`) AS {RETURNED_QUANTITY} , 
                SUM(`{CANCELLED_QUANTITY}`) AS {CANCELLED_QUANTITY} FROM `{DATABASE_NAME}`.`{SALES_ORDER_PRODUCT_TABLE_NAME}`
                WHERE `{S_O_P_FOREIGNKEY_SALES_ORDER_ID}` = {self.sales_order_id};"""
                fetched_data = self.executeFetchSqlQuery(SALES_ORDER_PRODUCT_TABLE_NAME, query_7)
                order_quantity = int(fetched_data[0][S_O_P_PRODUCT_QUANTITY])
                returned_quantity = int(fetched_data[0][RETURNED_QUANTITY])
                cancelled_quantity = int(fetched_data[0][CANCELLED_QUANTITY])
                order_status = None
                # If all quantities are returned then order_status = returned
                if order_quantity == returned_quantity:
                        order_status = ORDER_RETURNED
                # If all quantities are cancelled + returned, then order_status = cancelled
                elif order_quantity == (cancelled_quantity + returned_quantity):
                    order_status = ORDER_CANCELLED
                # Update Order Status
                if not (order_status == "") and not (type(order_status) == None.__class__):
                    query_8 = f"""UPDATE `{DATABASE_NAME}`.`{SALES_ORDER_TABLE_NAME}` SET `{SALES_ORDER_STATUS}` = '{order_status}'
                    WHERE `{SALES_ORDER_ID}` = {self.sales_order_id};"""
                    self.executeCommitSqlQuery(SALES_ORDER_TABLE_NAME, query_8)

                
            # If Purchase Order is selected
            elif self.radio_value.get() == 0:
                query_7 = f"""SELECT SUM(`{P_O_P_PRODUCT_QUANTITY}`) AS {P_O_P_PRODUCT_QUANTITY} , SUM(`{RETURNED_QUANTITY}`) AS {RETURNED_QUANTITY} ,
                SUM(`{CANCELLED_QUANTITY}`) AS {CANCELLED_QUANTITY} FROM `{DATABASE_NAME}`.`{PURCHASE_ORDER_PRODUCT_TABLE_NAME}`
                WHERE `{P_O_P_FOREIGNKEY_PURCHASE_ORDER_ID}` = {self.purchase_order_id};"""
                fetched_data = self.executeFetchSqlQuery(PURCHASE_ORDER_PRODUCT_TABLE_NAME, query_7)
                order_quantity = int(fetched_data[0][P_O_P_PRODUCT_QUANTITY])
                returned_quantity = int(fetched_data[0][RETURNED_QUANTITY])
                cancelled_quantity = int(fetched_data[0][CANCELLED_QUANTITY])
                order_status = None
                # If all quantities are returned then order_status = returned
                if order_quantity == returned_quantity:
                        order_status = ORDER_RETURNED
                # If all quantities are cancelled + returned, then order_status = cancelled
                elif order_quantity == (cancelled_quantity + returned_quantity):
                    order_status = ORDER_CANCELLED
                # Update Order Status
                if not (order_status == "") and not (type(order_status) == None.__class__):
                    query_8 = f"""UPDATE `{DATABASE_NAME}`.`{PURCHASE_ORDER_TABLE_NAME}` SET `{PURCHASE_ORDER_STATUS}` = '{order_status}'
                    WHERE `{PURCHASE_ORDER_ID}` = {self.purchase_order_id};"""
                    self.executeCommitSqlQuery(SALES_ORDER_TABLE_NAME, query_8)


            self.validateGui(
                None,
                None,
                "disabled",
                1,
                "SuccessfulLoginRegisterLabel.TLabel", 
                "Return/Cancel Order generated successfully",
                error_label_grid_row=4
                )
            self.radio_button_1.configure(state="disabled")
            self.radio_button_2.configure(state="disabled")
            self.product_button.configure(state="disabled")
            self.add_order_button.configure(state="disabled")
            self.product_detail_in_invoice_instance.second_functionality_button.configure(state="disabled")
            self.button.grid_forget()
            self.print_button.configure(command=lambda: GenerateInvoice(return_cancel_order_id=return_cancel_order_id))
            self.print_button.grid(row=8, column=0, columnspan=2, sticky="ew", pady=(15))

        except Exception as error:
            print(f"Development Error (While Creating Return Cancel Order: {error}")
            ErrorModal("Something went wrong while generation Return/Cancel Order, please contact the software developer.")

        

    # Resetting the Page
    def customReset(self):
        self.sales_order_id = 0
        self.purchase_order_id = 0
        self.gb_label.grid(row=1, column=0, sticky="w")
        self.add_order_button.grid(row=1, column=1, sticky="ew", pady=(15))
        self.radio_button_1.configure(state="normal")
        self.radio_button_2.configure(state="normal")
        self.product_button.configure(state="normal")
        self.add_order_button.configure(state="normal")
        self.product_detail_in_invoice_instance.second_functionality_button.configure(state="normal")
        self.validateGui(
            None,
            None,
            "disabled",
            0,
            "SuccessfulLoginRegisterLabel.TLabel", 
            "Return/Cancel Order generated successfully",
            error_label_grid_row=4
            )
        # Data Reset
        self.selected_records = list()
        self.s_no = 1
        self.total_refunded_amount = 0
        self.is_product_created = False
        self.purchase_order_delivery_status = ""
        self.button.grid(row=8, column=0, columnspan=2, sticky="ew", pady=(15))
        self.print_button.grid_forget()
        # Hide Order Details Frame
        self.configureOrderDetails()
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