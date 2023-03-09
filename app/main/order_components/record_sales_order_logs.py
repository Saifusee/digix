import tkinter as tk
from tkinter import ttk
from CONSTANT.index import *
from app.main.other_components.record_base import RecordBase, CLabel


# Sub Category Single Record Display
class RecordSalesOrderLog(tk.Toplevel, RecordBase):
    def __init__(self, container, mysql, user, sales_order_id, *args, **kwargs):
        
        # Inheriting tk.Toplevel Class
        super().__init__(container, *args, **kwargs)
        self.grab_set()
        # Inheriting RecordBase Class
        # Class.contructor(instance_or_object) is right syntax
        RecordBase.__init__(self, mysql, user, POPUP_TITLE="Sales Order Log's Description", button_2_text=None) # Class.contructor(instance or object) is right syntax
        
        # necessary instance variable for particular class
        self.sales_order_id = sales_order_id

        # Render Contents inside Canvas 
        self.renderLabels(record_table_name = self.POPUP_TITLE)
        
        # Fetch and show data
        self.fetchDataAndRender()
        
        
        
    def renderLabels(self, record_table_name):
        # Heading Label
        heading_label = ttk.Label(self.frame, text=record_table_name, anchor="center", style="PageHeadingLabel.TLabel")
        heading_label.grid(row=0, column=0, columnspan=2, sticky="ew")
        
        # Contents to Display in Canvas
        lb_1 = CLabel(self.frame, text="Log Data: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_1.grid(row=1, column=0, sticky="nsew")
        
        self.log_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.log_label.grid(row=1, column=1, sticky="nsew")
        
        
        lb_2 = CLabel(self.frame, text="Date: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_2.grid(row=2, column=0, sticky="nsew")
        
        self.date_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.date_label.grid(row=2, column=1, sticky="nsew")
        
        
        lb_3 = CLabel(self.frame, text="Time: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_3.grid(row=3, column=0, sticky="nsew")
        
        self.time_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.time_label.grid(row=3, column=1, sticky="nsew")
        
        lb_4 = CLabel(self.frame, text="Sales Order Id: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_4.grid(row=4, column=0, sticky="nsew")
        
        self.sales_order_id_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.sales_order_id_label.grid(row=4, column=1, sticky="nsew")
        
        
        lb_6 = CLabel(self.frame, text="Done by (username): ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_6.grid(row=6, column=0, sticky="nsew")
        
        self.username_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.username_label.grid(row=6, column=1, sticky="nsew")
        
        lb_7 = CLabel(self.frame, text="User ID: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_7.grid(row=7, column=0, sticky="nsew")
        
        self.username_id_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.username_id_label.grid(row=7, column=1, sticky="nsew")
        
        
        
    # Fetch Data from Database of Record and display it    
    def fetchDataAndRender(self):
        # Fetch Data
        data = self.queryFetchSingleSalesOrderLog(self.sales_order_id)
        # Display Data
        self.log_label.configure(text=data[0][SALES_ORDER_LOGS_LOG])
        self.date_label.configure(text=data[0][CREATED_AT].strftime("%Y-%m-%d"))
        self.time_label.configure(text=data[0][CREATED_AT].strftime("%H:%M:%S"))
        self.sales_order_id_label.configure(text=data[0][SALES_ORDER_LOGS_FOREIGNKEY_SALES_ORDER_ID])
        self.username_label.configure(text=data[0][USERNAME])
        self.username_id_label.configure(text=data[0][SALES_ORDER_LOGS_FOREIGNKEY_USER_ID])
        
     # Refreshing the Widget   
    def customReset(self):
        self.fetchDataAndRender()
