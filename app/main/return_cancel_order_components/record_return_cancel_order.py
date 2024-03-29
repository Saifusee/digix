import tkinter as tk
from tkinter import ttk
from CONSTANT.index import *
from app.main.other_components.record_base import RecordBase, CLabel
from app.main.external_files.create_invoice import GenerateInvoice


# Sub Category Single Record Display
class RecordReturnCancelOrder(tk.Toplevel, RecordBase):
    def __init__(self, container, mysql, user, return_cancel_order_id, *args, **kwargs):
        
        # Inheriting tk.Toplevel Class
        super().__init__(container, *args, **kwargs)
        self.grab_set()
        self.state('zoomed') # Open App fullscreen in maximize window  
        self.product_list = list()
        # Inheriting RecordBase Class
        # Class.contructor(instance_or_object) is right syntax
        RecordBase.__init__(self, mysql, user, POPUP_TITLE="Return/Cancel Order Details", button_2_text=None)
        
        # necessary instance variable for particular class
        self.return_cancel_order_id = return_cancel_order_id

        # Render Contents inside Canvas 
        self.renderLabels(record_table_name = self.POPUP_TITLE)
        
        # Fetch and show data
        self.fetchDataAndRender()
        
        
        
    def renderLabels(self, record_table_name):
        # Heading Label
        heading_label = ttk.Label(self.frame, text=record_table_name, anchor="center", style="PageHeadingLabel.TLabel")
        heading_label.grid(row=0, column=0, columnspan=2, sticky="ew")
        
        # Contents to Display in Canvas
        lb_1 = CLabel(self.frame, text="Return/Cancel Order Id: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_1.grid(row=1, column=0, sticky="nsew")
        
        self.order_id_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.order_id_label.grid(row=1, column=1, sticky="nsew")

        lb_1 = CLabel(self.frame, text="Return/Cancelled Order Type: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_1.grid(row=2, column=0, sticky="nsew")
        
        self.order_type_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.order_type_label.grid(row=2, column=1, sticky="nsew")

        self.order_type_head_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        self.order_type_head_label.grid(row=3, column=0, sticky="nsew")
        
        self.order_type_id_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.order_type_id_label.grid(row=3, column=1, sticky="nsew")

        lb_1 = CLabel(self.frame, text="Return/Cancel Order Status: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_1.grid(row=4, column=0, sticky="nsew")
        
        self.status_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.status_label.grid(row=4, column=1, sticky="nsew")

        lb_1 = CLabel(self.frame, text="Generated By (username): ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_1.grid(row=5, column=0, sticky="nsew")
        
        self.username_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.username_label.grid(row=5, column=1, sticky="nsew")

        lb_1 = CLabel(self.frame, text="User Id: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_1.grid(row=6, column=0, sticky="nsew")
        
        self.user_id_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.user_id_label.grid(row=6, column=1, sticky="nsew")

        lb_1 = CLabel(self.frame, text="Created At: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_1.grid(row=7, column=0, sticky="nsew")
        
        self.created_at_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.created_at_label.grid(row=7, column=1, sticky="nsew")

        self.p_frame = ttk.Frame(self.frame)
        self.p_frame.grid(row=8, column=0, columnspan=2, sticky="ew")

        self.show_logs_button = ttk.Button(
            self.frame,
            text="Cancel Order",
            command= lambda: print("Cancel Return/Cancel Order"),
            style="SingleRecordLinkButton.TButton"
            )
        self.show_logs_button.grid(row=9, column=0, columnspan=2, sticky="ew")

        self.print_button = ttk.Button(
            self.frame,
            text="Print",
            command= lambda: GenerateInvoice(return_cancel_order_id=self.return_cancel_order_id),
            style="SingleRecordLinkButton.TButton"
            )
        self.print_button.grid(row=10, column=0, columnspan=2, sticky="ew")



    # Fetch Data from Database of Record and display it    
    def fetchDataAndRender(self):
        # try:
            # Fetch Purchase Order Details
            data = self.queryFetchSingleReturnCancelOrder(self.return_cancel_order_id)

            # Display Data
            self.order_id_label.configure(text=data[0][RETURN_CANCEL_ORDER_ID])

            # Configuring either its for sales or purchase order
            if not (type(data[0][RETURN_CANCEL_ORDER_FOREIGNKEY_SALES_ORDER_ID]) == None.__class__):
                self.order_type_label.configure(text="Sales Order")
                self.order_type_head_label.configure(text="Sales Order Id")
                self.order_type_id_label.configure(text=data[0][RETURN_CANCEL_ORDER_FOREIGNKEY_SALES_ORDER_ID])
            elif not (type(data[0][RETURN_CANCEL_ORDER_FOREIGNKEY_PURCHASE_ORDER_ID]) == None.__class__):
                self.order_type_label.configure(text="Purchase Order")
                self.order_type_head_label.configure(text="Purchase Order Id")
                self.order_type_id_label.configure(text=data[0][RETURN_CANCEL_ORDER_FOREIGNKEY_PURCHASE_ORDER_ID])
            else:
                self.order_type_label.configure(text="Not Defined")
                self.order_type_head_label.configure(text="Order Id")
                self.order_type_id_label.configure(text="Not Defined")

            self.status_label.configure(text=data[0][RETURN_CANCEL_ORDER_STATUS])
            self.username_label.configure(text=data[0][USERNAME])
            self.user_id_label.configure(text=data[0][RETURN_CANCEL_ORDER_FOREIGNKEY_USER_ID])
            self.created_at_label.configure(text=data[0][CREATED_AT])

            # Fetch Products in Purchase Order Details
            self.product_list = self.queryFetchAllReturnCancelOrderProduct(self.return_cancel_order_id)

            # Render Products
            self.renderProducts(data[0][RETURN_CANCEL_ORDER_TOTAL_REFUND_AMOUNT])

        # except Exception as error:
        #     print(f"Develpoment Error (While fetching return cancel order details): {error}")
        #     ErrorModal("Something went wrong, please contact the developer.")



    def renderProducts(self, total_bill_amount):
        
        self.p_frame.columnconfigure(0, weight=1)
        self.p_frame.columnconfigure(1, weight=1)
        self.p_frame.columnconfigure(2, weight=1)

        # Headings
        h_lb = ttk.Label(self.p_frame, text="Product's unit cancellation and return details", anchor="center", style="PageHeadingLabel.TLabel")
        h_lb.grid(row=0, column=0, columnspan=4, sticky="ew")

        heading_rows = 1
        last_row = 0

        # Rendering Products
        for i in range(len(self.product_list)):
            lb_1 = CLabel(self.p_frame, text=f"{self.product_list[i][PRODUCT_NAME]}\n(Product Id = {self.product_list[i][R_C_O_P_FOREIGNKEY_PRODUCT_ID]})", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
            lb_1.grid(row=i+heading_rows, column=0, columnspan=3, sticky="nsew")
            lb_1 = CLabel(self.p_frame, text=f"Returned: x {self.product_list[i][R_C_O_P_PRODUCT_RETURN_QUANTITY]}", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
            lb_1.grid(row=i+heading_rows+1, column=0, sticky="nsew")
            lb_1 = CLabel(self.p_frame, text=f"Cancelled: x {self.product_list[i][R_C_O_P_PRODUCT_CANCEL_QUANTITY]}", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
            lb_1.grid(row=i+heading_rows+1, column=1, sticky="nsew")
            lb_1 = CLabel(self.p_frame, text=f"Refund: {self.formatINR(self.product_list[i][R_C_O_P_PRODUCT_REFUND_AMOUNT])}", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
            lb_1.grid(row=i+heading_rows+1, column=2, sticky="nsew")
            lb_1 = CLabel(self.p_frame, text=f"Reason: {self.product_list[i][R_C_O_P_REASON]}", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
            lb_1.grid(row=i+heading_rows+2, column=0, columnspan=3, sticky="nsew")

            # White separator
            h_lb = ttk.Label(self.p_frame, text=" ", anchor="center", style="EmptyLineLabel.TLabel")
            h_lb.grid(row=i+heading_rows+3, column=0, columnspan=3, sticky="ew")
            heading_rows = heading_rows + 4
            last_row = i+heading_rows+1

        lb_1 = CLabel(self.p_frame, text=f"Total Refunded Amount: {self.formatINR(total_bill_amount)}", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_1.grid(row=last_row+1, column=0, columnspan=3, sticky="nsew")



     # Refreshing the Widget   
    def customReset(self):
        self.fetchDataAndRender()