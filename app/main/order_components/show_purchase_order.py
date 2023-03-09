import tkinter as tk
from tkinter import ttk
from CONSTANT.index import *
from app.main.order_components.record_purchase_order import RecordPurchaseOrder
from app.main.tree_essentials import TreeEssentials
from datetime import *
from tkcalendar import DateEntry
from app.main.order_components.p_o_status_change_toplevel import POStatusChangeEntry
from app.main.external_files.export_purchase_order_data import ExportPurchaseOrderData
from app.main.external_files.create_invoice import GenerateInvoice

class ShowPurchaseOrder(tk.Canvas, TreeEssentials):
    
    def __init__(self, container, mysql, user, is_r_c_page=False, product_id=None, supplier_id=None):
        
        self.offset = 0
        self.limit = 15
        self.container = container
        self.is_r_c_page = is_r_c_page
        # Data Set for Default from and today
        self.from_date_data = tk.StringVar()
        self.to_date_data = tk.StringVar()
        today_date = date.today()
        self.from_date_data.set(today_date)
        self.to_date_data.set(today_date)


        if not type(product_id) == None.__class__:
            # Product wise Purchase Orders
            added_query = f""" WHERE `{PURCHASE_ORDER_ID}` IN 
            ((SELECT `{P_O_P_FOREIGNKEY_PURCHASE_ORDER_ID}` FROM `{DATABASE_NAME}`.`{PURCHASE_ORDER_PRODUCT_TABLE_NAME}`
             WHERE `{P_O_P_FOREIGNKEY_PRODUCT_ID}` = {product_id})) """
            self.dataFetchingMethod = lambda export_bool=False: self.queryFetchPaginatedPurchaseOrder(
                offset=self.offset,
                limit=self.limit,
                from_date=self.from_date_data.get(),
                to_date=self.to_date_data.get(),
                radio_data=self.radio_value.get(),
                query_data=self.search_data.get(),
                query_add_on=added_query,
                export=export_bool
                )
        elif not type(supplier_id) == None.__class__:
            # Supplier wise Purchase Orders
            added_query = f""" WHERE `{PURCHASE_ORDER_ID}` IN 
            ((SELECT `{PURCHASE_ORDER_ID}` FROM `{DATABASE_NAME}`.`{PURCHASE_ORDER_TABLE_NAME}`
             WHERE `{PURCHASE_ORDER_FOREIGNKEY_SUPPLIER_ID}` = {supplier_id})) """
            self.dataFetchingMethod = lambda export_bool=False: self.queryFetchPaginatedPurchaseOrder(
                offset=self.offset,
                limit=self.limit,
                from_date=self.from_date_data.get(),
                to_date=self.to_date_data.get(),
                radio_data=self.radio_value.get(),
                query_data=self.search_data.get(),
                query_add_on=added_query,
                export=export_bool
                )
        else:
            self.dataFetchingMethod = lambda export_bool=False: self.queryFetchPaginatedPurchaseOrder(
                offset=self.offset,
                limit=self.limit,
                from_date=self.from_date_data.get(),
                to_date=self.to_date_data.get(),
                radio_data=self.radio_value.get(),
                query_data=self.search_data.get(),
                export=export_bool
                )

        
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

        if self.is_r_c_page:
            page_head = "Select Purchase Orders:"
        elif not type(product_id) == None.__class__:
            page_head = f"Purchase Orders for Product Id = {product_id}:"
        elif not type(supplier_id) == None.__class__:
            page_head = f"Purchase Orders from this Supplier Id = {supplier_id}:"
        else:
            page_head = "Purchase Orders:"

        # Define Search above Table
        self.defineSearchButtons(
            frame=self.above_frame,
            page_heading=page_head,
            refreshedTableMethod=lambda: self.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.dataFetchingMethod()
                ),
            searchedRefreshTableMethod=lambda: self.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.dataFetchingMethod()
                )
            )
        
        # Create Tree
        self.createTreeAndConfiguration()
        
        # Rendering Scrollbar
        self.renderScrollbar()
        
        # Initiliazing Tree essentials method and components
        TreeEssentials.__init__(self, mysql=mysql, user=user, tree_instance=self.tree)
        
        # Define Frames below Table
        self.defineBelowFrames(container=self)

        # If its for create_return_cancel order 
        if self.is_r_c_page:
            pass
        else:            
            # Define Buttons below Table
            self.definePaginateButtons(
                refreshedTableMethod=lambda: self.definingRowsOfParticularTree(
                    dataFetchingMethod=lambda: self.dataFetchingMethod()
                    ),
                searchedRefreshTableMethod=lambda: self.definingRowsOfParticularTree(
                    dataFetchingMethod=lambda: self.dataFetchingMethod()
                    ),
                first_functionality_switch="download",
                first_functionality_button_text="Download Record",
                firstFunctionalityMethod=lambda: ExportPurchaseOrderData(
                    lambda: self.dataFetchingMethod(export_bool=True),
                    container=self
                    ),
                second_functionality_switch="call_passed_method_directly",
                second_functionality_button_text="Change Status",
                secondFunctionalityMethod=lambda: POStatusChangeEntry(
                    self,
                    self.mysql,
                    self.current_user,
                    self.tree.item(self.tree.focus())["values"][1],
                    lambda: self.insertDataInTree(
                        tableRowFetchAndRenderMethod=lambda: self.definingRowsOfParticularTree(
                            dataFetchingMethod=lambda: self.dataFetchingMethod()
                            )
                        )
                    ),
                third_functionality_switch="call_passed_method_directly",
                third_functionality_button_text="Print Invoice",
                thirdFunctionalityMethod=lambda: GenerateInvoice(purchase_order_id=self.tree.item(self.tree.focus())["values"][1]),
                is_triple_button_functionality_needed=True
                )

            # Define Other Search Options such as check box and combobox above Table
            self.defineParticularSearchesWidgets(self.above_frame)
            
            # Insert Data
            self.insertDataInTree(
                tableRowFetchAndRenderMethod=lambda: self.definingRowsOfParticularTree(
                    dataFetchingMethod=lambda: self.dataFetchingMethod()
                    )
                )
            
            # Defining Key and Mouse Bindings on Table  
            self.definingEventBindings(
                refreshTableMethod=lambda: self.definingRowsOfParticularTree(
                    dataFetchingMethod=lambda: self.dataFetchingMethod()
                    ),
                RecordPopupClass=lambda: RecordPurchaseOrder(
                    container=self,
                    mysql=self.mysql,
                    user=self.current_user,
                    purchase_order_id=self.tree.item(self.tree.focus())["values"][1]
                    )
                )
        

        
        
    # Create Rows of Particular Tree with data from database   
    def definingRowsOfParticularTree(self, dataFetchingMethod):
        data = dataFetchingMethod()

        # When donwload button not needed
        if self.is_r_c_page:
            pass
        else:
            # If no record then disable download record button
            if len(data) == 0:
                self.first_functionality_button.configure(state="disabled")
                self.second_functionality_button.configure(state="disabled")
                self.third_functionality_button.configure(state="disabled")
            else:
                self.first_functionality_button.configure(state="normal")
                self.second_functionality_button.configure(state="normal")
                self.third_functionality_button.configure(state="normal")

        # Inserting Data In Tree
        if len(data) >= 1:
            count = 0
            s_no_count = self.offset
            for i in range(len(data)):
                s_name = self.morphText(data[i][SUPPLIER_NAME])
                user_name = self.morphText(data[i][USERNAME])   
                order_status = data[i][PURCHASE_ORDER_STATUS]
                price = self.formatINR(data[i][PURCHASE_ORDER_TOTAL_PRICE])       

                
                val = (s_no_count+1, data[i][PURCHASE_ORDER_ID], price, data[i][PURCHASE_ORDER_PAYMENT_MODE],
                    order_status, data[i][PURCHASE_ORDER_PAYMENT_STATUS], data[i][PURCHASE_ORDER_DELIVERY_STATUS],
                    data[i][SUPPLIER_ID], s_name, user_name, data[i][CREATED_AT])
                
                tag_value = tuple()
                if count % 2 != 0:
                    if order_status == ORDER_PENDING:
                        tag_value = ("pending_odd_rows",)
                    elif order_status == ORDER_CANCELLED or order_status == ORDER_RETURNED:
                        tag_value = ("cancelled_odd_rows",)
                    else:
                        tag_value = ("odd_rows",)
                else:
                    if order_status == ORDER_PENDING:
                        tag_value = ("pending_even_rows",)
                    elif order_status == ORDER_CANCELLED or order_status == ORDER_RETURNED:
                        tag_value = ("cancelled_even_rows",)
                    else:
                        tag_value = ("even_rows",)

                self.tree.insert("",
                                tk.END,
                                values=val,
                                tags=tag_value
                                )
                count = count + 1
                s_no_count = s_no_count + 1
                self.tree.configure(selectmode="extended")
        else:
            self.tree.insert("",
                             tk.END,
                             values=(
                                 "No Records Found",
                                 "No Records Found", 
                                 "No Records Found",
                                 "No Records Found",
                                 "No Records Found",
                                 "No Records Found", 
                                 "No Records Found",
                                 "No Records Found",
                                 "No Records Found",
                                 "No Records Found",
                                 "No Records Found", 
                                 ),
                             tags=("odd_row",)
                             )
            
            self.tree.configure(selectmode="none")

        
       
    # Create Tree Instance and set its Configuration 
    def createTreeAndConfiguration(self):
        
        # Tuple of Tree Columns
        columnTuple = ("s_no", PURCHASE_ORDER_ID, PURCHASE_ORDER_TOTAL_PRICE, PURCHASE_ORDER_PAYMENT_MODE, PURCHASE_ORDER_STATUS, PURCHASE_ORDER_PAYMENT_STATUS,
        PURCHASE_ORDER_DELIVERY_STATUS,  SUPPLIER_ID, SUPPLIER_NAME, USERNAME, CREATED_AT)
        
        self.tree = ttk.Treeview(self, columns=columnTuple, show="headings", style="Tree.Treeview")
        
        # Defining Column Name 
        self.tree.heading("s_no", text="S. No.")
        self.tree.heading(PURCHASE_ORDER_ID, text="Order ID")
        self.tree.heading(PURCHASE_ORDER_TOTAL_PRICE, text="Total (\u20B9)")
        self.tree.heading(PURCHASE_ORDER_PAYMENT_MODE, text="Payment Mode")
        self.tree.heading(PURCHASE_ORDER_STATUS, text="Order Status")
        self.tree.heading(PURCHASE_ORDER_PAYMENT_STATUS, text="Payment Status")
        self.tree.heading(PURCHASE_ORDER_DELIVERY_STATUS, text="Delivery Status")
        self.tree.heading(SUPPLIER_ID, text="Supplier ID")
        self.tree.heading(SUPPLIER_NAME, text="Supplier's Name")
        self.tree.heading(USERNAME, text="Generated By")
        self.tree.heading(CREATED_AT, text="Date")
        
        
        # Defining Configuration for Columns
        self.tree.column("s_no", anchor="center")
        self.tree.column(PURCHASE_ORDER_ID, anchor="center")
        self.tree.column(PURCHASE_ORDER_TOTAL_PRICE, anchor="center")
        self.tree.column(PURCHASE_ORDER_PAYMENT_MODE, anchor="center")
        self.tree.column(PURCHASE_ORDER_STATUS, anchor="center")
        self.tree.column(PURCHASE_ORDER_PAYMENT_STATUS, anchor="center")
        self.tree.column(PURCHASE_ORDER_DELIVERY_STATUS, anchor="center")
        self.tree.column(SUPPLIER_ID, anchor="center")
        self.tree.column(SUPPLIER_NAME, anchor="center")
        self.tree.column(USERNAME, anchor="center")
        self.tree.column(CREATED_AT, anchor="center")
        
        # Giving Striped Rows Style
        self.tree.tag_configure("even_rows", background="#ccffcc")
        self.tree.tag_configure("odd_rows", background="#99ff99")
        self.tree.tag_configure("pending_even_rows", background="#ffffcc")
        self.tree.tag_configure("pending_odd_rows", background="#ffff80")
        self.tree.tag_configure("cancelled_even_rows", background="#ffd6cc")
        self.tree.tag_configure("cancelled_odd_rows", background="#ffad99")
        
        # Rendering Tree
        self.tree.grid(row=1, column=0, sticky="nsew")

        
    
    # Frame Configurations for Search above Tables
    def defineAboveFrames(self):
        self.above_frame = ttk.Frame(self, padding=15)
        self.above_frame.grid(row=0, column=0, sticky="nsew")

    # Define Widgets Above TreeView for Searching Purposes of Product
    def defineParticularSearchesWidgets(self, frame):
        
        # Frame for Radio Buttons
        t_frame = ttk.Frame(frame)
        t_frame.pack(side="top", anchor="w", pady=5)
        # Frame for Calendar Buttons
        from_date_frame = tk.Frame(frame, background="white")
        from_date_frame.pack(side="left", anchor="w", pady=5, padx=5)
        to_date_frame = tk.Frame(frame, background="white")
        to_date_frame.pack(side="left", anchor="w", pady=5, padx=5)
        

        # Radiobuttons
        self.radio_0 = ttk.Radiobutton(t_frame, text="All", variable=self.radio_value, value=0, command=self.radioButtonSelect, style="TreeRadiobutton.TRadiobutton")
        self.radio_0_in_r_c_page = ttk.Radiobutton(t_frame, text="All", variable=self.radio_value, value=100, command=self.radioButtonSelect, style="TreeRadiobutton.TRadiobutton")
        self.radio_1 = ttk.Radiobutton(t_frame, text="Completed", variable=self.radio_value, value=1, command=self.radioButtonSelect, style="TreeRadiobutton.TRadiobutton")
        self.radio_2 = ttk.Radiobutton(t_frame, text="Pending", variable=self.radio_value, value=2, command=self.radioButtonSelect, style="TreeRadiobutton.TRadiobutton")
        self.radio_3 = ttk.Radiobutton(t_frame, text="Cancelled", variable=self.radio_value, value=3, command=self.radioButtonSelect, style="TreeRadiobutton.TRadiobutton")
        self.radio_4 = ttk.Radiobutton(t_frame, text="Returned", variable=self.radio_value, value=4, command=self.radioButtonSelect, style="TreeRadiobutton.TRadiobutton")
        self.radio_5 = ttk.Radiobutton(t_frame, text="Payment Pending", variable=self.radio_value, value=5, command=self.radioButtonSelect, style="TreeRadiobutton.TRadiobutton")
        self.radio_6 = ttk.Radiobutton(t_frame, text="Payment Completed", variable=self.radio_value, value=6, command=self.radioButtonSelect, style="TreeRadiobutton.TRadiobutton")
        self.radio_7 = ttk.Radiobutton(t_frame, text="In Transit", variable=self.radio_value, value=7, command=self.radioButtonSelect, style="TreeRadiobutton.TRadiobutton")
        self.radio_8 = ttk.Radiobutton(t_frame, text="Delivered", variable=self.radio_value, value=8, command=self.radioButtonSelect, style="TreeRadiobutton.TRadiobutton")
    
        self.radio_0_in_r_c_page.invoke() if self.is_r_c_page else self.radio_0.invoke()

        self.radio_8.pack(side="right", fill="x", padx=5)
        self.radio_7.pack(side="right", fill="x", padx=5)
        self.radio_6.pack(side="right", fill="x", padx=5)
        self.radio_5.pack(side="right", fill="x", padx=5)
        if not (self.is_r_c_page): self.radio_4.pack(side="right", fill="x", padx=5)
        if not (self.is_r_c_page): self.radio_3.pack(side="right", fill="x", padx=5)
        self.radio_2.pack(side="right", fill="x", padx=5)
        self.radio_1.pack(side="right", fill="x", padx=5)
        if not (self.is_r_c_page): self.radio_0.pack(side="right", fill="x", padx=5)
        if self.is_r_c_page: self.radio_0_in_r_c_page.pack(side="right", fill="x", padx=5)
        # if its for return_cancel page then "ALL" means ORDER_STATUS other than cancel and return

        # Calendars
        from_label = ttk.Label(from_date_frame, text="From:", style="CalendarLabel.TLabel")
        from_label.pack(side="left", fill="x", padx=5)
        self.from_calendar = DateEntry(
            from_date_frame,
            textvariable=self.from_date_data,
            justify="center",
            font=("TkDefaultFont", 8, "bold"),
            date_pattern="y-mm-d",
            maxdate=date.today(),
            showothermonthdays=False,
            showweeknumbers=False,
            weekendbackground="white",
            weekendforeground="black"
            )
        self.from_calendar.pack(side="left", fill="x", padx=5)
        self.from_calendar.bind("<<DateEntrySelected>>", self.dateChanged)
        


        to_label = ttk.Label(to_date_frame, text="To:", style="CalendarLabel.TLabel")
        to_label.pack(side="left", fill="x", padx=5)
        self.to_calendar = DateEntry(
            to_date_frame,
            textvariable=self.to_date_data,
            justify="center",
            font=("TkDefaultFont", 8, "bold"),
            date_pattern="y-mm-d",
            maxdate=date.today(),
            showothermonthdays=False,
            showweeknumbers=False,
            weekendbackground="white",
            weekendforeground="black"
            )
        self.to_calendar.pack(side="left", fill="x", padx=5)
        self.to_calendar.bind("<<DateEntrySelected>>", self.dateChanged)
        


    # Change Date
    def dateChanged(self, event):
        self.offset = 0
        self.insertDataInTree(
            tableRowFetchAndRenderMethod=lambda: self.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.dataFetchingMethod()
                )
            )



    # When Radio Button is selected
    def radioButtonSelect(self):
        self.offset = 0
        self.insertDataInTree(
            tableRowFetchAndRenderMethod=lambda: self.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.dataFetchingMethod()
                )
            )
        

        
    # Reset Page
    def customReset(self):
        self.offset = 0
        self.radio_0_in_r_c_page.invoke() if self.is_r_c_page else self.radio_0.invoke()
        today_date= date.today()
        self.from_date_data.set(today_date)
        self.to_date_data.set(today_date)
        self.insertDataInTree(
            tableRowFetchAndRenderMethod=lambda: self.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.dataFetchingMethod()
                )
            )