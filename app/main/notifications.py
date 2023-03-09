import tkinter as tk
from tkinter import ttk
from CONSTANT.index import *
from app.main.notifications_components.record_notification import RecordNotification
from app.main.tree_essentials import TreeEssentials

class Notifications(tk.Canvas, TreeEssentials):
    
    def __init__(self, container, mysql, user):
        
        self.offset = 0
        self.limit = 15
        self.messages_list = list()
        self.second_label_head = ""
        # Note: when we call, instance.method(), method automatically take instance as first argument which we define as self
        # when we call, Class.method(), method need instance manually as first argument bcz it doesn't know which one to take
        tk.Canvas.__init__(self, container)
        
        # Configuration for Frame
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=95)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=4)

        # Define Frames above Table
        self.defineAboveFrames()
        
        # Define Search above Table
        self.defineSearchButtons(
            frame=self.above_frame,
            page_heading="Home Page - Important Notifications"
            )
        
        # Create Tree
        self.createTreeAndConfiguration()
        
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
            is_zero_button_functionality_needed=True,
            is_dashboard_table=1
            )
        
        # Insert Data
        self.insertDataInTree(
            tableRowFetchAndRenderMethod=lambda: self.definingRowsOfParticularTree()
            )
        
        # Defining Key and Mouse Bindings on Table  
        self.tree.bind("<Double-Button-1>", self.mouseDoubleClicked)


        # Radio Buttons
        self.radio_1 = ttk.Radiobutton(self.above_frame, text="Products", variable=self.radio_value, value=0, command=self.radioButtonSelect, style="TreeRadiobutton.TRadiobutton")
        self.radio_2 = ttk.Radiobutton(self.above_frame, text="Purchase Orders", variable=self.radio_value, value=1, command=self.radioButtonSelect, style="TreeRadiobutton.TRadiobutton")
        self.radio_3 = ttk.Radiobutton(self.above_frame, text="Users", variable=self.radio_value, value=2, command=self.radioButtonSelect, style="TreeRadiobutton.TRadiobutton")
        self.radio_3.pack(side="right", fill="x", padx=5)
        self.radio_2.pack(side="right", fill="x", padx=5)
        self.radio_1.pack(side="right", fill="x", padx=5)
        self.radio_1.invoke()

        

    # When Radio Button Selected
    def radioButtonSelect(self):
        self.messages_list = []
        self.offset = 0
        self.tree.heading("A", text="S. No.")
        # Products
        if self.radio_value.get() == 0:

            # Modifying Column names for tree
            self.tree.heading("B", text="Messages related to Inventory")
            self.second_label_head = "Product ID"
            self.tree.heading("C", text=self.second_label_head)

            # Fetching Data
            queryy = f"""SELECT * FROM `{DATABASE_NAME}`.`{PRODUCT_TABLE_NAME}` WHERE (`{PRODUCT_QUANTITY}` <= `{PRODUCT_REORDER_QUANTITY}`)
            AND (`{PRODUCT_IS_DELETED}` <> 1);"""
            response = self.executeFetchSqlQuery(PRODUCT_TABLE_NAME, queryy)

            # Creating Rows
            for s_no, record in enumerate(response):
                if record[PRODUCT_QUANTITY] == 0:
                    message = f"'{record[PRODUCT_NAME]}' is out of stock, please refill the stock."
                else:
                    message = f"Only x {record[PRODUCT_QUANTITY]} quantities of '{record[PRODUCT_NAME]}' left in inventory, please refill the stock."
                self.messages_list.append({"A": s_no, "B": message, "C": record[PRODUCT_ID]})

        # Purchase Orders
        elif self.radio_value.get() == 1:
            # Modifying Column names for tree
            self.tree.heading("B", text="Messages related to Purchase Orders")
            self.second_label_head = "Purchase Order Id"
            self.tree.heading("C", text=self.second_label_head)

            # Fetching Data
            queryy = f"""SELECT * FROM `{DATABASE_NAME}`.`{PURCHASE_ORDER_TABLE_NAME}` WHERE (`{PURCHASE_ORDER_DELIVERY_STATUS}` <> '{DELIVERED}'
            OR `{PURCHASE_ORDER_PAYMENT_STATUS}` <> '{PAYMENT_COMPLETED}') 
            AND (`{PURCHASE_ORDER_STATUS}` <> '{ORDER_CANCELLED}' OR `{PURCHASE_ORDER_STATUS}` <> '{ORDER_RETURNED}');"""
            response = self.executeFetchSqlQuery(PURCHASE_ORDER_TABLE_NAME, queryy)

            # Creating Rows
            for s_no, record in enumerate(response):
                if not (record[PURCHASE_ORDER_DELIVERY_STATUS] == DELIVERED):
                    if record[PURCHASE_ORDER_DELIVERY_STATUS] == DISPATCHED:
                        message = f"This order is dispatched and is on the way for delivery by supplier '{record[SUPPLIER_NAME]}' (Supplier Id = {record[PURCHASE_ORDER_FOREIGNKEY_SUPPLIER_ID]})."
                    elif record[PURCHASE_ORDER_DELIVERY_STATUS] == NOT_DISPATCHED:
                        message = f"This order is not dispatched for delivery yet by supplier '{record[SUPPLIER_NAME]}' (Supplier Id = {record[PURCHASE_ORDER_FOREIGNKEY_SUPPLIER_ID]})."
                    self.messages_list.append({"A": s_no, "B": message, "C": record[PURCHASE_ORDER_ID]})
                if record[PURCHASE_ORDER_PAYMENT_STATUS] == PAYMENT_PENDING:
                    message = f"Payment for this order is due to supplier '{record[SUPPLIER_NAME]}' (Supplier Id = {record[PURCHASE_ORDER_FOREIGNKEY_SUPPLIER_ID]})."
                    self.messages_list.append({"A": s_no, "B": message, "C": record[PURCHASE_ORDER_ID]})
            

        # Users
        elif self.radio_value.get() == 2:
            # Modifying Column names for tree
            self.tree.heading("B", text="Messages related to Active Users/Employees")
            self.second_label_head = "Username"
            self.tree.heading("C", text=self.second_label_head)
            
            # Fetching Data
            queryy = f"""SELECT * FROM `{DATABASE_NAME}`.`{USER_TABLE_NAME}` WHERE (`{EMPLOYMENT_STATUS}` = '{EMPLOYED}')
            AND (`{USER_CONTACT_1}` IS NULL OR `{USER_ADDRESS}` IS NULL);"""
            response = self.executeFetchSqlQuery(USER_TABLE_NAME, queryy)

            # Creating Rows
            for s_no, record in enumerate(response):
                if (type(record[USER_CONTACT_1]) == None.__class__ or record[USER_CONTACT_1] == "") and (type(record[USER_ADDRESS]) == None.__class__ or record[USER_ADDRESS] == ""):
                    message = f"Primary contact and address of user '{record[USERNAME]}' (User Id = {record[USER_ID]}) is not updated."
                else:
                    if type(record[USER_CONTACT_1]) == None.__class__ or record[USER_CONTACT_1] == "":
                        message = f"Primary contact of user '{record[USERNAME]}' (User Id = {record[USER_ID]}) is not updated."
                    if type(record[USER_ADDRESS]) == None.__class__ or record[USER_ADDRESS] == "":
                        message = f"Address of user '{record[USERNAME]}' (User Id = {record[USER_ID]}) is not updated."
                self.messages_list.append({"A": s_no, "B": message, "C": record[USERNAME]})

        # Modify Tree with new data
        self.insertDataInTree(
            tableRowFetchAndRenderMethod=lambda: self.definingRowsOfParticularTree()
            )



    # When Double-Button-1 event launched on Treeview
    def mouseDoubleClicked(self, event):
        index_of_record_in_messages_list = (self.tree.item(self.tree.focus())["values"][0])-1 # s_no-1 is index
        RecordNotification(self, None, self.messages_list[index_of_record_in_messages_list], self.second_label_head)

        

    # Create Rows of Particular Tree with data from database   
    def definingRowsOfParticularTree(self):
        # Setting total number of records for pagination functionality to work properly
        self.totalRecordsCount = len(self.messages_list)
        start_index = self.offset
        last_index = self.offset + self.limit
        # Getting Data
        data = self.messages_list[start_index:last_index]

        # Inserting Data In Tree
        if len(data) >= 1:
            count = 0
            s_no_count = self.offset
            for i in range(len(data)):       
                
                val = (s_no_count+1, self.morphText(data[i]["B"], 124), self.morphText(str(data[i]["C"])))

                if count % 2 != 0:
                    self.tree.insert(
                        "",
                        tk.END,
                        values=val,
                        tags=("odd_row",)
                        )
                else:
                    self.tree.insert("",
                                     tk.END,
                                     values=val,
                                     tags=("even_row",)
                                    )
                count = count + 1
                s_no_count = s_no_count + 1
                self.tree.configure(selectmode="extended")
        else:
            if self.radio_value.get() == 0:
                val = ("",  "No messages related to inventory.", "")
            elif self.radio_value.get() == 1:
                val = ("",  "No messages related to purchase orders.", "")
            elif self.radio_value.get() == 2:
                val = ("",  "No messages related to user accounts.", "")
            else:
                val = ("",  "Nothing to show here.", "")
            self.tree.insert("",
                             tk.END,
                             values=val,
                             tags=("odd_row",)
                             )
            
            self.tree.configure(selectmode="none")


        
       
    # Create Tree Instance and set its Configuration 
    def createTreeAndConfiguration(self):
        
        # Tuple of Tree Columns
        columnTuple = ("A", "B", "C")
        
        self.tree = ttk.Treeview(self, columns=columnTuple, show="headings", selectmode="extended", style="Tree.Treeview")
        
        # Defining Configuration for Columns
        self.tree.column("A", anchor="center", stretch=tk.NO, width=100)
        self.tree.column("B", anchor="center")
        self.tree.column("C", anchor="center", stretch=tk.NO, width=250)
        
        # Giving Striped Rows Style
        self.tree.tag_configure("even_row", background="#f2e6ff")
        self.tree.tag_configure("odd_row", background="#e6ccff")
        
        # Rendering Tree
        self.tree.grid(row=1, column=0, sticky="nsew")

        
    
    # Frame Configurations for Search above Tables
    def defineAboveFrames(self):
        self.above_frame = ttk.Frame(self, padding=15)
        self.above_frame.grid(row=0, column=0, sticky="nsew")



    # Reset Page
    def customReset(self):
        self.offset = 0
        self.radio_1.invoke()
        self.insertDataInTree(
            tableRowFetchAndRenderMethod=lambda: self.definingRowsOfParticularTree()
            )