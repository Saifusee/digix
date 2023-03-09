import tkinter as tk
from tkinter import ttk
from CONSTANT.index import *
from app.main.return_cancel_order_components.record_return_cancel_order import RecordReturnCancelOrder
from app.main.tree_essentials import TreeEssentials
from datetime import *
from tkcalendar import DateEntry
from app.main.external_files.export_return_cancel_order_data import ExportReturnCancelOrderData
from app.main.external_files.create_invoice import GenerateInvoice

class ShowReturnCancelOrder(tk.Canvas, TreeEssentials):
    
    def __init__(self, container, mysql, user):
        
        self.offset = 0
        self.limit = 15
        self.container = container
        # Data Set for Default from and today
        self.from_date_data = tk.StringVar()
        self.to_date_data = tk.StringVar()
        today_date = date.today()
        self.from_date_data.set(today_date)
        self.to_date_data.set(today_date)
        
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
            page_heading="Show Return/Cancel Orders:",
            refreshedTableMethod=lambda: self.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.queryFetchPaginatedReturnCancelOrder(
                    offset=self.offset,
                    limit=self.limit,
                    from_date=self.from_date_data.get(),
                    to_date=self.to_date_data.get(),
                    radio_data=self.radio_value.get(),
                    query_data=self.search_data.get()
                    )
                ),
            searchedRefreshTableMethod=lambda: self.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.queryFetchPaginatedReturnCancelOrder(
                    offset=self.offset,
                    limit=self.limit,
                    from_date=self.from_date_data.get(),
                    to_date=self.to_date_data.get(),
                    radio_data=self.radio_value.get(),
                    query_data=self.search_data.get()
                    )
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

        # Define Buttons below Table
        self.definePaginateButtons(
            refreshedTableMethod=lambda: self.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.queryFetchPaginatedReturnCancelOrder(
                    offset=self.offset,
                    limit=self.limit,
                    from_date=self.from_date_data.get(),
                    to_date=self.to_date_data.get(),
                    radio_data=self.radio_value.get(),
                    query_data=self.search_data.get()
                    )
                ),
            searchedRefreshTableMethod=lambda: self.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.queryFetchPaginatedReturnCancelOrder(
                    offset=self.offset,
                    limit=self.limit,
                    from_date=self.from_date_data.get(),
                    to_date=self.to_date_data.get(),
                    radio_data=self.radio_value.get(),
                    query_data=self.search_data.get()
                    )
                ),
            first_functionality_switch="download",
            first_functionality_button_text="Download Record",
            firstFunctionalityMethod=lambda: ExportReturnCancelOrderData(
                lambda: self.queryFetchPaginatedReturnCancelOrder(
                    offset=self.offset,
                    limit=self.limit,
                    from_date=self.from_date_data.get(),
                    to_date=self.to_date_data.get(),
                    radio_data=self.radio_value.get(),
                    query_data=self.search_data.get(),
                    export=True
                    ),
                container=self
                ),
            second_functionality_switch="call_passed_method_directly",
            second_functionality_button_text="Print Invoice",
            secondFunctionalityMethod=lambda: GenerateInvoice(return_cancel_order_id=self.tree.item(self.tree.focus())["values"][1]),
            )

        # Define Other Search Options such as check box and combobox above Table
        self.defineParticularSearchesWidgets(self.above_frame)
        
        # Insert Data
        self.insertDataInTree(
            tableRowFetchAndRenderMethod=lambda: self.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.queryFetchPaginatedReturnCancelOrder(
                    offset=self.offset,
                    limit=self.limit,
                    from_date=self.from_date_data.get(),
                    to_date=self.to_date_data.get(),
                    radio_data=self.radio_value.get(),
                    query_data=self.search_data.get()
                    )
                )
            )
        
        # Defining Key and Mouse Bindings on Table  
        self.definingEventBindings(
            refreshTableMethod=lambda: self.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.queryFetchPaginatedReturnCancelOrder(
                    offset=self.offset,
                    limit=self.limit,
                    from_date=self.from_date_data.get(),
                    to_date=self.to_date_data.get(),
                    radio_data=self.radio_value.get(),
                    query_data=self.search_data.get()
                    )
                ),
            RecordPopupClass=lambda: RecordReturnCancelOrder(
                container=self,
                mysql=self.mysql,
                user=self.current_user,
                return_cancel_order_id=self.tree.item(self.tree.focus())["values"][1]
                )
            )

        
        
    # Create Rows of Particular Tree with data from database   
    def definingRowsOfParticularTree(self, dataFetchingMethod):
        data = dataFetchingMethod()

        # If no record then disable download record button
        if len(data) == 0:
            self.first_functionality_button.configure(state="disabled")
            self.second_functionality_button.configure(state="disabled")
        else:
            self.first_functionality_button.configure(state="normal")
            self.second_functionality_button.configure(state="normal")

        # Inserting Data In Tree
        if len(data) >= 1:
            count = 0
            s_no_count = self.offset
            for i in range(len(data)):
                user_name = self.morphText(data[i][USERNAME])   
                order_status = data[i][RETURN_CANCEL_ORDER_STATUS]
                price = self.formatINR(data[i][RETURN_CANCEL_ORDER_TOTAL_REFUND_AMOUNT]) 

                if not (type(data[i][RETURN_CANCEL_ORDER_FOREIGNKEY_SALES_ORDER_ID]) == None.__class__):
                    order_type = "Sales Order"
                    sales_order_id = data[i][RETURN_CANCEL_ORDER_FOREIGNKEY_SALES_ORDER_ID]
                    purchase_order_id = "--"
                elif not (type(data[i][RETURN_CANCEL_ORDER_FOREIGNKEY_PURCHASE_ORDER_ID]) == None.__class__):
                    order_type = "Purchase Order"
                    sales_order_id = "--"
                    purchase_order_id = data[i][RETURN_CANCEL_ORDER_FOREIGNKEY_PURCHASE_ORDER_ID]
                else:
                    order_type = "Not Mentioned"
                    sales_order_id = "--"
                    purchase_order_id = "--"

                
                val = (s_no_count+1, data[i][RETURN_CANCEL_ORDER_ID], order_type, sales_order_id, 
                purchase_order_id, order_status, price, user_name, data[i][CREATED_AT])
                
                tag_value = tuple()
                if count % 2 != 0:
                    if order_status == ORDER_CANCELLED:
                        tag_value = ("cancelled_odd_rows",)
                    else:
                        tag_value = ("odd_rows",)
                else:
                    if order_status == ORDER_CANCELLED:
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
                                 "No Recor....",
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
        columnTuple = ("s_no", RETURN_CANCEL_ORDER_ID, "order_type", RETURN_CANCEL_ORDER_FOREIGNKEY_SALES_ORDER_ID, 
        RETURN_CANCEL_ORDER_FOREIGNKEY_PURCHASE_ORDER_ID, RETURN_CANCEL_ORDER_STATUS, RETURN_CANCEL_ORDER_TOTAL_REFUND_AMOUNT,
        RETURN_CANCEL_ORDER_FOREIGNKEY_USER_ID, CREATED_AT)
        
        self.tree = ttk.Treeview(self, columns=columnTuple, show="headings", style="Tree.Treeview")
        
        # Defining Column Name 
        self.tree.heading("s_no", text="S. No.")
        self.tree.heading(RETURN_CANCEL_ORDER_ID, text="R/C ID")
        self.tree.heading("order_type", text="Order Type")
        self.tree.heading(RETURN_CANCEL_ORDER_FOREIGNKEY_SALES_ORDER_ID, text="Sales Order Id")
        self.tree.heading(RETURN_CANCEL_ORDER_FOREIGNKEY_PURCHASE_ORDER_ID, text="Purchase Order Id")
        self.tree.heading(RETURN_CANCEL_ORDER_STATUS, text="Order Status")
        self.tree.heading(RETURN_CANCEL_ORDER_TOTAL_REFUND_AMOUNT, text="Total Refund (\u20B9)")
        self.tree.heading(RETURN_CANCEL_ORDER_FOREIGNKEY_USER_ID, text="Generated By")
        self.tree.heading(CREATED_AT, text="Created At")
        
        
        # Defining Configuration for Columns
        self.tree.column("s_no", anchor="center", stretch=tk.NO, width=100)
        self.tree.column(RETURN_CANCEL_ORDER_ID, anchor="center")
        self.tree.column("order_type", anchor="center")
        self.tree.column(RETURN_CANCEL_ORDER_FOREIGNKEY_SALES_ORDER_ID, anchor="center")
        self.tree.column(RETURN_CANCEL_ORDER_FOREIGNKEY_PURCHASE_ORDER_ID, anchor="center")
        self.tree.column(RETURN_CANCEL_ORDER_STATUS, anchor="center")
        self.tree.column(RETURN_CANCEL_ORDER_TOTAL_REFUND_AMOUNT, anchor="center")
        self.tree.column(RETURN_CANCEL_ORDER_FOREIGNKEY_USER_ID, anchor="center")
        self.tree.column(CREATED_AT, anchor="center")
        
        # Giving Striped Rows Style
        self.tree.tag_configure("even_rows", background="#ccffcc")
        self.tree.tag_configure("odd_rows", background="#99ff99")
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
        self.radio_1 = ttk.Radiobutton(t_frame, text="Cancelled", variable=self.radio_value, value=1, command=self.radioButtonSelect, style="TreeRadiobutton.TRadiobutton")
        self.radio_2 = ttk.Radiobutton(t_frame, text="Purchase Orders", variable=self.radio_value, value=2, command=self.radioButtonSelect, style="TreeRadiobutton.TRadiobutton")
        self.radio_3 = ttk.Radiobutton(t_frame, text="Sales Order", variable=self.radio_value, value=3, command=self.radioButtonSelect, style="TreeRadiobutton.TRadiobutton")
    
        self.radio_0.invoke()

        self.radio_3.pack(side="right", fill="x", padx=5)
        self.radio_2.pack(side="right", fill="x", padx=5)
        self.radio_1.pack(side="right", fill="x", padx=5)
        self.radio_0.pack(side="right", fill="x", padx=5)

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
        


    # When Date Change
    def dateChanged(self, event):
        self.offset = 0
        self.insertDataInTree(
            tableRowFetchAndRenderMethod=lambda: self.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.queryFetchPaginatedReturnCancelOrder(
                    offset=self.offset,
                    limit=self.limit,
                    from_date=self.from_date_data.get(),
                    to_date=self.to_date_data.get(),
                    radio_data=self.radio_value.get(),
                    query_data=self.search_data.get()
                    )
                )
            )


    def radioButtonSelect(self):
        self.offset = 0
        self.insertDataInTree(
            tableRowFetchAndRenderMethod=lambda: self.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.queryFetchPaginatedReturnCancelOrder(
                    offset=self.offset,
                    limit=self.limit,
                    from_date=self.from_date_data.get(),
                    to_date=self.to_date_data.get(),
                    radio_data=self.radio_value.get(),
                    query_data=self.search_data.get()
                    )
                )
            )
        
    # Reset Page
    def customReset(self):
        self.offset = 0
        self.radio_0.invoke()
        today_date= date.today()
        self.from_date_data.set(today_date)
        self.to_date_data.set(today_date)
        self.insertDataInTree(
            tableRowFetchAndRenderMethod=lambda: self.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.queryFetchPaginatedReturnCancelOrder(
                    offset=self.offset,
                    limit=self.limit,
                    from_date=self.from_date_data.get(),
                    to_date=self.to_date_data.get(),
                    radio_data=self.radio_value.get(),
                    query_data=self.search_data.get()
                )
                )
            )