import tkinter as tk
from tkinter import ttk
from CONSTANT.index import *
from modal import Modal
from app.main.supplier_components.edit_supplier import EditSupplier
from app.main.supplier_components.show_supplier_wise_purchase_order import ShowSupplierWisePurchaseOrder
from app.main.other_components.record_base import RecordBase, CLabel

# Category Single Record Display
class RecordSupplier(tk.Toplevel, RecordBase):
    def __init__(self, container, mysql, user, supplier_id, refreshedTableMethod=None, *args, **kwargs):
        
        # Inheriting tk.Toplevel Class
        super().__init__(container, *args, **kwargs)
        self.grab_set()
        # Inheriting RecordBase Class
        # Class.contructor(instance_or_object) is right syntax
        RecordBase.__init__(self, mysql, user, POPUP_TITLE="Supplier Detail", button_2_text="Active/Inactive Supplier") # Class.contructor(instance or object) is right syntax
        
        # necessary instance variable for particular class
        self.supplier_id = supplier_id
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
        lb_1 = CLabel(self.frame, text="Supplier ID: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_1.grid(row=1, column=0, sticky="nsew")
        self.supplier_id_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.supplier_id_label.grid(row=1, column=1, sticky="nsew")
        
        lb_2 = CLabel(self.frame, text="Supplier Name: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_2.grid(row=2, column=0, sticky="nsew")
        self.supplier_name_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.supplier_name_label.grid(row=2, column=1, sticky="nsew")
        
        lb_3 = CLabel(self.frame, text="Status: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_3.grid(row=3, column=0, sticky="nsew")
        self.supplier_status_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.supplier_status_label.grid(row=3, column=1, sticky="nsew")
        
        lb_4 = CLabel(self.frame, text="Primary Contact: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_4.grid(row=4, column=0, sticky="nsew")
        self.supplier_c_1_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.supplier_c_1_label.grid(row=4, column=1, sticky="nsew")
        
        lb_5 = CLabel(self.frame, text="Secondary Contact: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_5.grid(row=5, column=0, sticky="nsew")
        self.supplier_c_2_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.supplier_c_2_label.grid(row=5, column=1, sticky="nsew")
        
        lb_6 = CLabel(self.frame, text="Address: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_6.grid(row=6, column=0, sticky="nsew")
        self.supplier_address_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.supplier_address_label.grid(row=6, column=1, sticky="nsew")
        
        lb_7 = CLabel(self.frame, text="Organization Name: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_7.grid(row=7, column=0, sticky="nsew")
        self.org_name_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.org_name_label.grid(row=7, column=1, sticky="nsew")
        
        lb_8 = CLabel(self.frame, text="Organization Conatact 1: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_8.grid(row=8, column=0, sticky="nsew")
        self.org_c_1_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.org_c_1_label.grid(row=8, column=1, sticky="nsew")
        
        lb_9 = CLabel(self.frame, text="Organization Conatact 2: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_9.grid(row=9, column=0, sticky="nsew")
        self.org_c_2_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.org_c_2_label.grid(row=9, column=1, sticky="nsew")
        
        lb_10 = CLabel(self.frame, text="Organization Address: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_10.grid(row=10, column=0, sticky="nsew")
        self.org_address_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.org_address_label.grid(row=10, column=1, sticky="nsew")
        
        lb_11 = CLabel(self.frame, text="Description: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_11.grid(row=11, column=0, sticky="nsew")
        self.description_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.description_label.grid(row=11, column=1, sticky="nsew")

        lb_12 = CLabel(self.frame, text="Supplier GSTIN: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_12.grid(row=12, column=0, sticky="nsew")
        self.supplier_gst_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.supplier_gst_label.grid(row=12, column=1, sticky="nsew")
    
        lb_12 = CLabel(self.frame, text="Supplier registered on: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_12.grid(row=13, column=0, sticky="nsew")
        self.created_at_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.created_at_label.grid(row=13, column=1, sticky="nsew")
        
        
        self.show_purchases = ttk.Button(
            self.frame,
            text="Show all Purchases from this supplier",
            command= lambda: ShowSupplierWisePurchaseOrder(self, self.mysql, self.current_user, supplier_id=self.supplier_id,),
            style="SingleRecordLinkButton.TButton"
            )
        self.show_purchases.grid(row=14, column=0, columnspan=2, sticky="ew")
        
        
        
    # Fetch Data from Database of Record and display it    
    def fetchDataAndRender(self):
        # Fetch Data
        data = self.queryFetchSingleSupplier(self.supplier_id)
        
        # Display Data
        self.supplier_id_label.configure(text=data[0][SUPPLIER_ID])
        self.supplier_name_label.configure(text=data[0][SUPPLIER_NAME])
        self.supplier_c_1_label.configure(text=data[0][SUPPLIER_CONTACT_1])
        self.supplier_c_2_label.configure(text=data[0][SUPPLIER_CONTACT_2])
        self.supplier_address_label.configure(text=data[0][SUPPLIER_ADDRESS])
        self.supplier_gst_label.configure(text=data[0][SUPPLIER_GSTIN])
        self.org_name_label.configure(text=data[0][SUPPLIER_ORGANIZATION_NAME])
        self.org_c_1_label.configure(text=data[0][SUPPLIER_ORGANIZATION_CONTACT_1])
        self.org_c_2_label.configure(text=data[0][SUPPLIER_ORGANIZATION_CONTACT_2])
        self.org_address_label.configure(text=data[0][SUPPLIER_ORGANIZATION_ADDRESS])
        self.description_label.configure(text=data[0][SUPPLIER_DESCRIPTION])
        self.created_at_label.configure(text=data[0][CREATED_AT])
        self.supplier_status_label.configure(text="Active" if data[0][SUPPLIER_ACTIVE_STATE] == 1 else "Inactive")
        
        
        
    # Edit Record    
    def commandButton1(self):
        # Edit Record
        EditSupplier(
            self,
            self.mysql,
            self.current_user,
            self.supplier_id,
            lambda: [self.refreshedTableMethod(), self.customReset()]
        )
        # Refresh Details in Popup
        self.fetchDataAndRender()
        
        
        
    # Delete record
    def commandButton2(self):
        # If user confirm -> Delete Record, refresh table and destroy popup
        Modal(self,
              f"Are you sure you want to change active/inactive status of this supplier.?",
              lambda: [
                  self.queryToggleSupplierStatus(self.supplier_id),
                  self.refreshedTableMethod(),
                  self.customReset()
                  ]
              )
        
        
     # Refreshing the Widget   
    def customReset(self):
        self.fetchDataAndRender()