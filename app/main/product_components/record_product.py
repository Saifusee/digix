import tkinter as tk
from tkinter import ttk
from CONSTANT.index import *
from modal import Modal
from app.main.product_components.edit_product import EditProduct
from app.main.other_components.record_base import RecordBase, CLabel
from app.main.product_components.show_product_logs import ShowProductLogs
from app.main.product_components.show_product_wise_sales_order import ShowProductWiseSalesOrder
from app.main.product_components.show_product_wise_purchase_order import ShowProductWisePurchaseOrder


# Category Single Record Display
class RecordProduct(tk.Toplevel, RecordBase):
    def __init__(self, container, mysql, user, product_id, refreshedTableMethod=None, *args, **kwargs):
        
        # Inheriting tk.Toplevel Class
        super().__init__(container, *args, **kwargs)
        self.grab_set()
        # self.attributes('-fullscreen', True) #Gives App fullscreen view
        self.state('zoomed') # Open App fullscreen in maximize window  
        # Inheriting RecordBase Class
        # Class.contructor(instance_or_object) is right syntax
        RecordBase.__init__(self, mysql, user, POPUP_TITLE="Product Detail") # Class.contructor(instance or object) is right syntax
        
        # necessary instance variable for particular class
        self.product_id = product_id
        self.refreshedTableMethod = lambda: refreshedTableMethod()

        # Render Contents inside Canvas 
        self.renderLabels(record_table_name = self.POPUP_TITLE)
        
        # Fetch and show data
        self.fetchDataAndRender()
        
        
        
    def renderLabels(self, record_table_name):
        # Heading Label
        heading_label = ttk.Label(self.frame, text=record_table_name, anchor="center", style="PageHeadingLabel.TLabel")
        heading_label.grid(row=0, column=0, columnspan=2, sticky="ew")
        
        # Contents to Display in Canvas
        lb_1 = CLabel(self.frame, text="Product ID: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_1.grid(row=1, column=0, sticky="nsew")
        self.product_id_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.product_id_label.grid(row=1, column=1, sticky="nsew")
        
        lb_2 = CLabel(self.frame, text="Product Name: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_2.grid(row=2, column=0, sticky="nsew")
        self.product_name_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.product_name_label.grid(row=2, column=1, sticky="nsew")
        
        lb_3 = CLabel(self.frame, text="Price: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_3.grid(row=3, column=0, sticky="nsew")
        self.product_price_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.product_price_label.grid(row=3, column=1, sticky="nsew")
        
        lb_4 = CLabel(self.frame, text="Quantity availabel in inventory: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_4.grid(row=4, column=0, sticky="nsew")
        self.product_quantity_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.product_quantity_label.grid(row=4, column=1, sticky="nsew")
        
        lb_5 = CLabel(self.frame, text="Product Description: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_5.grid(row=5, column=0, sticky="nsew")
        self.product_description_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.product_description_label.grid(row=5, column=1, sticky="nsew")
        
        lb_6 = CLabel(self.frame, text="Category: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_6.grid(row=6, column=0, sticky="nsew")
        self.product_category_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.product_category_label.grid(row=6, column=1, sticky="nsew")
        
        lb_7 = CLabel(self.frame, text="Sub-Category: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_7.grid(row=7, column=0, sticky="nsew")
        self.product_sub_category_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.product_sub_category_label.grid(row=7, column=1, sticky="nsew")
        
        lb_8 = CLabel(self.frame, text="Reorder Quantity: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_8.grid(row=8, column=0, sticky="nsew")
        self.product_reorder_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.product_reorder_label.grid(row=8, column=1, sticky="nsew")
        
        lb_9 = CLabel(self.frame, text="Status: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_9.grid(row=9, column=0, sticky="nsew")
        self.product_status_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.product_status_label.grid(row=9, column=1, sticky="nsew")
        
        lb_10 = CLabel(self.frame, text="Price Updated At: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_10.grid(row=10, column=0, sticky="nsew")
        self.product_price_updated_at_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.product_price_updated_at_label.grid(row=10, column=1, sticky="nsew")
        
        lb_11 = CLabel(self.frame, text="Product Updated At: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_11.grid(row=11, column=0, sticky="nsew")
        self.product_updated_at_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.product_updated_at_label.grid(row=11, column=1, sticky="nsew")
        
        lb_12 = CLabel(self.frame, text="Product Created At: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_12.grid(row=12, column=0, sticky="nsew")
        self.product_created_at_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.product_created_at_label.grid(row=12, column=1, sticky="nsew")
        
        # Button for showing logs
        self.purchase_order = ttk.Button(
            self.frame,
            text="Show All Purchases Order",
            command= lambda: ShowProductWisePurchaseOrder(self, self.mysql, self.current_user, product_id=self.product_id,),
            style="SingleRecordLinkButton.TButton"
            )
        self.purchase_order.grid(row=13, column=0, columnspan=2, sticky="ew")
        
        # Button for showing purchase order of particular product
        self.sales_order = ttk.Button(
            self.frame,
            text="Show All Sales Order",
            command= lambda: ShowProductWiseSalesOrder(self, self.mysql, self.current_user, product_id=self.product_id,),
            style="SingleRecordLinkButton.TButton"
            )
        self.sales_order.grid(row=14, column=0, columnspan=2, sticky="ew")
        
        
        # Button for showing sales order of particular product
        self.display_log = ttk.Button(
            self.frame,
            text="Display Product Log",
            command= lambda: ShowProductLogs(
                self,
                self.mysql,
                self.current_user,
                self.product_id,
                product_name=f"Logs of '{self.product_name_label['text']}'" if len(f"Logs of '{self.product_name_label['text']}'") < 50 else f"Logs of '{self.product_name_label['text'][0:41]}....'" 
                ),
            style="SingleRecordLinkButton.TButton"
            )
        self.display_log.grid(row=15, column=0, columnspan=2, sticky="ew")
        
        
        
    # Fetch Data from Database of Record and display it    
    def fetchDataAndRender(self):
        # Fetch Data
        data = self.queryFetchSingleProduct(self.product_id)
        
        # Display Data
        self.product_id_label.configure(text=data[0][PRODUCT_ID])
        self.product_name_label.configure(text=data[0][PRODUCT_NAME])
        self.product_quantity_label.configure(text=data[0][PRODUCT_QUANTITY])
        self.product_description_label.configure(text=data[0][PRODUCT_DESCRIPTION])
        self.product_category_label.configure(text=data[0][CATEGORY_NAME])
        self.product_sub_category_label.configure(text=data[0][SUB_CATEGORY_NAME])
        self.product_reorder_label.configure(text=data[0][PRODUCT_REORDER_QUANTITY])
        self.product_price_updated_at_label.configure(text=data[0][PRODUCT_PRICE_UPDATE_DATETIME])
        self.product_updated_at_label.configure(text=data[0][UPDATED_AT])
        self.product_created_at_label.configure(text=data[0][CREATED_AT])
        self.product_price_label.configure(text=f"{self.formatINR(data[0][PRODUCT_PRICE])}")
        self.product_status_label.configure(text="x<< Currently removed from inventory >>x" if data[0][PRODUCT_IS_DELETED] == 1 else "<< Present in inventory >>")
        # Changing Delete Button Text
        if data[0][PRODUCT_IS_DELETED] == 1:
            self.button_2.configure(text="Restore")
        else:
            self.button_2.configure(text="Delete")
        
        
        
    # Edit Record    
    def commandButton1(self):
        # Edit Record
        EditProduct(
            self,
            self.mysql,
            self.current_user,
            self.product_id,
            lambda: [self.refreshedTableMethod(), self.customReset()]
        )
        # Refresh Details in Popup
        self.fetchDataAndRender()
        
        
        
    # Delete record
    def commandButton2(self):
        # If user confirm -> Delete Record, refresh table and destroy popup
        if self.button_2["text"] == "Delete":
            question = f"Delete the selected product, you can restore it back again? (Product Id = {self.product_id})"
        else:
            question = f"Restore the selected product back to inventory again? (Product Id = {self.product_id})"
        Modal(self,
              question,
              lambda: [
                  self.queryToggleProductDeleteStatus(self.product_id),
                  self.refreshedTableMethod(),
                  self.customReset()
                  ]
              )
        
        
     # Refreshing the Widget   
    def customReset(self):
        self.fetchDataAndRender()