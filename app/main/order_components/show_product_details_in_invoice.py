import tkinter as tk
from tkinter import ttk
from CONSTANT.index import *
from app.main.tree_essentials import TreeEssentials

class ShowProductDetailsInInvoice(tk.Canvas, TreeEssentials):
    
    def __init__(self, container, mysql, user, type, removeProductFromShowProductDetailsInInvoiceMethod):
        
        self.offset = 0
        self.limit = 15
        self.callback = lambda: removeProductFromShowProductDetailsInInvoiceMethod()
        
        # Note: when we call, instance.method(), method automatically take instance as first argument which we define as self
        # when we call, Class.method(), method need instance manually as first argument bcz it doesn't know which one to take
        tk.Canvas.__init__(self, container)
        
        # Configuration for Frame
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=95)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=4)


        # Create Tree
        self.createTreeAndConfiguration(type)
        
        # Rendering Scrollbar
        self.renderScrollbar()
        
        # Initiliazing Tree essentials method and components
        TreeEssentials.__init__(self, mysql=mysql, user=user, tree_instance=self.tree)
        
        # Define Frames below Table
        self.defineBelowFrames(container=self)
        
        # Define Buttons below Table
        self.definePaginateButtons(
            refreshedTableMethod=lambda: self.definingRowsOfParticularTree(),
            searchedRefreshTableMethod=lambda: self.definingRowsOfParticularTree(),
            second_functionality_button_text="Remove Selected",
            second_functionality_switch="remove_product_from_invoice",
            secondFunctionalityMethod=self.callback,
            is_pagination_needed=False,
            is_single_button_functionality_needed=True
            )
        
        # Insert Data
        self.insertDataInTree(tableRowFetchAndRenderMethod=lambda: self.definingRowsOfParticularTree())
        

        
        
    # Create Rows of Particular Tree with data from database   
    def definingRowsOfParticularTree(self):
        # Do Nothing here
        # Insertion of Rows Take Place in CreateSalesOrder class
        # If no rows available
        pass
        
        
       
    # Create Tree Instance and set its Configuration 
    def createTreeAndConfiguration(self, type):

        # Tuple of Tree Columns
        if type == "ReturnCancelOrder":
            columnTuple = ("s_no", PRODUCT_NAME, PRODUCT_ID, CANCELLED_QUANTITY, RETURNED_QUANTITY, REFUNDED_AMOUNT)
        else:
            columnTuple = ("s_no", PRODUCT_NAME, PRODUCT_ID, PRODUCT_PRICE, PRODUCT_QUANTITY, "total")
        
        
        self.tree = ttk.Treeview(self, columns=columnTuple, show="headings", selectmode="extended", style="SelectedProductInInvoiceTree.Treeview")
        
        # Defining Column Name 
        self.tree.heading("s_no", text="")
        self.tree.heading(PRODUCT_NAME, text="Product Name")
        self.tree.heading(PRODUCT_ID, text="ID")
        if type == "ReturnCancelOrder":
            self.tree.heading(CANCELLED_QUANTITY, text="Cancel")
            self.tree.heading(RETURNED_QUANTITY, text="Return")
            self.tree.heading(REFUNDED_AMOUNT, text="Refund (\u20B9)")
        else:
            self.tree.heading(PRODUCT_PRICE, text="Buying Price") if type == "PurchaseOrder" else self.tree.heading(PRODUCT_PRICE, text="Price")
            self.tree.heading(PRODUCT_QUANTITY, text="Quantity")
            self.tree.heading("total", text="Total")
        
        
        # Defining Configuration for Columns
        self.tree.column("s_no", anchor="center", stretch=tk.NO, width=15)
        self.tree.column(PRODUCT_NAME, anchor="center")
        self.tree.column(PRODUCT_ID, anchor="center", stretch=tk.NO, width=75)
        if type == "ReturnCancelOrder":
            self.tree.column(CANCELLED_QUANTITY, anchor="center", stretch=tk.NO, width=55)
            self.tree.column(RETURNED_QUANTITY, anchor="center", stretch=tk.NO, width=55)
            self.tree.column(REFUNDED_AMOUNT, anchor="center", stretch=tk.NO, width=80)
        else:
            self.tree.column(PRODUCT_PRICE, anchor="center", stretch=tk.NO, width=80)
            self.tree.column(PRODUCT_QUANTITY, anchor="center", stretch=tk.NO, width=55)
            self.tree.column("total", anchor="center", stretch=tk.NO, width=75)


        # Giving Striped Rows Style
        self.tree.tag_configure("odd_row", background="white")
        
        # Rendering Tree
        self.tree.grid(row=1, column=0, sticky="nsew")



    # Reset Page
    def customReset(self):
        self.insertDataInTree(tableRowFetchAndRenderMethod=lambda: self.definingRowsOfParticularTree())