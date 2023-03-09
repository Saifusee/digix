import tkinter as tk
from tkinter import ttk
from CONSTANT.index import *
from app.main.other_components.record_base import RecordBase, CLabel
from error import ErrorModal
from app.main.order_components.show_purchase_order_logs import ShowPurchaseOrderLogs
from app.main.external_files.create_invoice import GenerateInvoice


# Sub Category Single Record Display
class RecordPurchaseOrder(tk.Toplevel, RecordBase):
    def __init__(self, container, mysql, user, purchase_order_id, *args, **kwargs):
        
        # Inheriting tk.Toplevel Class
        super().__init__(container, *args, **kwargs)
        self.grab_set()
        self.state('zoomed') # Open App fullscreen in maximize window  
        self.product_list = list()
        # Inheriting RecordBase Class
        # Class.contructor(instance_or_object) is right syntax
        RecordBase.__init__(self, mysql, user, POPUP_TITLE="Purchase Order Details", button_2_text=None) # Class.contructor(instance or object) is right syntax
        
        # necessary instance variable for particular class
        self.purchase_order_id = purchase_order_id

        # Render Contents inside Canvas 
        self.renderLabels(record_table_name = self.POPUP_TITLE)
        
        # Fetch and show data
        self.fetchDataAndRender()
        
        
        
    def renderLabels(self, record_table_name):
        # Heading Label
        heading_label = ttk.Label(self.frame, text=record_table_name, anchor="center", style="PageHeadingLabel.TLabel")
        heading_label.grid(row=0, column=0, columnspan=2, sticky="ew")
        
        # Contents to Display in Canvas
        lb_1 = CLabel(self.frame, text="Purchase Order Id: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_1.grid(row=1, column=0, sticky="nsew")
        
        self.order_id_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.order_id_label.grid(row=1, column=1, sticky="nsew")

        lb_1 = CLabel(self.frame, text="Supplier Id: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_1.grid(row=2, column=0, sticky="nsew")
        
        self.supplier_id_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.supplier_id_label.grid(row=2, column=1, sticky="nsew")

        lb_1 = CLabel(self.frame, text="Supplier Name: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_1.grid(row=3, column=0, sticky="nsew")
        
        self.supplier_name_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.supplier_name_label.grid(row=3, column=1, sticky="nsew")

        lb_1 = CLabel(self.frame, text="Supplier Contact: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_1.grid(row=4, column=0, sticky="nsew")
        
        self.supplier_contact_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.supplier_contact_label.grid(row=4, column=1, sticky="nsew")

        lb_1 = CLabel(self.frame, text="Supplier Address: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_1.grid(row=5, column=0, sticky="nsew")
        
        self.supplier_address_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.supplier_address_label.grid(row=5, column=1, sticky="nsew")

        lb_1 = CLabel(self.frame, text="Supplier's Organization Name: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_1.grid(row=6, column=0, sticky="nsew")
        
        self.supplier_org_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.supplier_org_label.grid(row=6, column=1, sticky="nsew")

        lb_1 = CLabel(self.frame, text="Organization's Contact: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_1.grid(row=7, column=0, sticky="nsew")
        
        self.supplier_org_contact_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.supplier_org_contact_label.grid(row=7, column=1, sticky="nsew")

        lb_1 = CLabel(self.frame, text="Organization's Address: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_1.grid(row=8, column=0, sticky="nsew")
        
        self.supplier_org_address_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.supplier_org_address_label.grid(row=8, column=1, sticky="nsew")

        lb_1 = CLabel(self.frame, text="Supplier GSTIN: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_1.grid(row=9, column=0, sticky="nsew")
        
        self.supplier_gst_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.supplier_gst_label.grid(row=9, column=1, sticky="nsew")

        lb_1 = CLabel(self.frame, text="Payment Mode: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_1.grid(row=10, column=0, sticky="nsew")
        
        self.payment_mode_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.payment_mode_label.grid(row=10, column=1, sticky="nsew")

        lb_1 = CLabel(self.frame, text="Order Status: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_1.grid(row=11, column=0, sticky="nsew")
        
        self.order_status_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.order_status_label.grid(row=11, column=1, sticky="nsew")

        lb_1 = CLabel(self.frame, text="Payment Status: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_1.grid(row=12, column=0, sticky="nsew")
        
        self.payment_status_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.payment_status_label.grid(row=12, column=1, sticky="nsew")

        lb_1 = CLabel(self.frame, text="Delivery Status: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_1.grid(row=13, column=0, sticky="nsew")
        
        self.delivery_status_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.delivery_status_label.grid(row=13, column=1, sticky="nsew")

        lb_1 = CLabel(self.frame, text="Order Generated by (User): ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_1.grid(row=14, column=0, sticky="nsew")
        
        self.user_name_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.user_name_label.grid(row=14, column=1, sticky="nsew")

        lb_1 = CLabel(self.frame, text="Order Generated by (User Id): ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_1.grid(row=15, column=0, sticky="nsew")
        
        self.user_id_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.user_id_label.grid(row=15, column=1, sticky="nsew")

        lb_1 = CLabel(self.frame, text="Created At: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_1.grid(row=16, column=0, sticky="nsew")
        
        self.created_at_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.created_at_label.grid(row=16, column=1, sticky="nsew")

        self.p_frame = ttk.Frame(self.frame)
        self.p_frame.grid(row=17, column=0, columnspan=2, sticky="ew")


        self.show_logs_button = ttk.Button(
            self.frame,
            text="Show Purchase Order Logs",
            command= lambda: ShowPurchaseOrderLogs(self, self.mysql, self.current_user, self.purchase_order_id),
            style="SingleRecordLinkButton.TButton"
            )
        self.show_logs_button.grid(row=18, column=0, columnspan=2, sticky="ew")

        self.print_button = ttk.Button(
            self.frame,
            text="Print",
            command= lambda: GenerateInvoice(purchase_order_id=self.purchase_order_id),
            style="SingleRecordLinkButton.TButton"
            )
        self.print_button.grid(row=19, column=0, columnspan=2, sticky="ew")



    # Fetch Data from Database of Record and display it    
    def fetchDataAndRender(self):
        try:
            # Fetch Purchase Order Details
            data = self.queryFetchSinglePurchaseOrder(self.purchase_order_id)
            # Display Data
            self.order_id_label.configure(text=data[0][PURCHASE_ORDER_ID])
            self.supplier_id_label.configure(text=data[0][PURCHASE_ORDER_FOREIGNKEY_SUPPLIER_ID])
            self.supplier_name_label.configure(text=data[0][SUPPLIER_NAME])
            self.supplier_contact_label.configure(text=data[0][SUPPLIER_CONTACT_1])
            self.supplier_address_label.configure(text=data[0][SUPPLIER_ADDRESS])
            self.supplier_org_label.configure(text=data[0][SUPPLIER_ORGANIZATION_NAME])
            self.supplier_org_contact_label.configure(text=data[0][SUPPLIER_ORGANIZATION_CONTACT_1])
            self.supplier_org_address_label.configure(text=data[0][SUPPLIER_ORGANIZATION_ADDRESS])
            self.supplier_gst_label.configure(text=data[0][SUPPLIER_GSTIN])
            self.payment_mode_label.configure(text=data[0][PURCHASE_ORDER_PAYMENT_MODE])
            self.order_status_label.configure(text=data[0][PURCHASE_ORDER_STATUS])
            self.payment_status_label.configure(text=data[0][PURCHASE_ORDER_PAYMENT_STATUS])
            self.delivery_status_label.configure(text=data[0][PURCHASE_ORDER_DELIVERY_STATUS])
            self.user_name_label.configure(text=data[0][USERNAME])
            self.user_id_label.configure(text=data[0][PURCHASE_ORDER_FOREIGNKEY_USER_ID])
            self.created_at_label.configure(text=data[0][CREATED_AT])

            # Fetch Products in Purchase Order Details
            self.product_list = self.queryFetchAllPurchaseOrderProduct(self.purchase_order_id)

            # Render Products
            self.renderProducts(data[0][PURCHASE_ORDER_TOTAL_PRICE])

        except Exception as error:
            print(f"Develpoment Error (While fetching purchase order details): {error}")
            ErrorModal("Something went wrong, please contact the developer.")



    def renderProducts(self, total_bill_amount):
        
        self.p_frame.columnconfigure(0, weight=1)
        self.p_frame.columnconfigure(1, weight=1)
        self.p_frame.columnconfigure(2, weight=1)

        # Headings
        h_lb = ttk.Label(self.p_frame, text="Product details in invoice", anchor="center", style="PageHeadingLabel.TLabel")
        h_lb.grid(row=0, column=0, columnspan=4, sticky="ew")


        heading_rows = 1
        last_row = 0

        # Rendering Products
        for i in range(len(self.product_list)):
            lb_1 = CLabel(self.p_frame, text=f"{self.product_list[i][PRODUCT_NAME]}\n(Product Id = {self.product_list[i][P_O_P_FOREIGNKEY_PRODUCT_ID]})", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
            lb_1.grid(row=i+heading_rows, column=0, columnspan=3, sticky="nsew")
            lb_1 = CLabel(self.p_frame, text=f"Price: {self.formatINR(self.product_list[i][P_O_P_PRODUCT_PRICE])}", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
            lb_1.grid(row=i+heading_rows+1, column=0, sticky="nsew")
            lb_1 = CLabel(self.p_frame, text=f"Quantity: x{self.product_list[i][P_O_P_PRODUCT_QUANTITY]}", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
            lb_1.grid(row=i+heading_rows+1, column=1, sticky="nsew")
            lb_1 = CLabel(self.p_frame, text=f"Total: {self.formatINR(self.product_list[i][P_O_P_PRODUCT_TOTAL_AMOUNT])}", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
            lb_1.grid(row=i+heading_rows+1, column=2, sticky="nsew")

            # Returned and Cancelled Labels
            fr = ttk.Frame(self.p_frame)
            fr.grid(row=i+heading_rows+2, column=0, columnspan=3, sticky="nsew")
            fr.columnconfigure(0, weight=1)
            fr.columnconfigure(1, weight=1)
            lb_1 = CLabel(fr, text=f"Returned Quantity: x {self.product_list[i][RETURNED_QUANTITY]}", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
            lb_1.grid(row=0, column=0, sticky="nsew")
            lb_1 = CLabel(fr, text=f"Cancelled Quantity: x {self.product_list[i][CANCELLED_QUANTITY]}", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
            lb_1.grid(row=0, column=1, sticky="nsew")
            lb_1 = CLabel(fr, text=f"Refunded Amount: {self.formatINR(self.product_list[i][REFUNDED_AMOUNT])}", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
            lb_1.grid(row=i+heading_rows+3, column=0, columnspan=3, sticky="nsew")

            # White separator
            h_lb = ttk.Label(self.p_frame, text=" ", anchor="center", style="EmptyLineLabel.TLabel")
            h_lb.grid(row=i+heading_rows+4, column=0, columnspan=3, sticky="ew")
            heading_rows = heading_rows + 5
            last_row = i+heading_rows+1

        lb_1 = CLabel(self.p_frame, text=f"Total Bill Amount: {self.formatINR(total_bill_amount)}", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_1.grid(row=last_row+1, column=0, columnspan=3, sticky="nsew")



     # Refreshing the Widget   
    def customReset(self):
        self.fetchDataAndRender()