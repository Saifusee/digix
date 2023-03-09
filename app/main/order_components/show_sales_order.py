import tkinter as tk
from tkinter import ttk
from CONSTANT.index import *
from app.main.order_components.record_sales_order import RecordSalesOrder
from app.main.tree_essentials import TreeEssentials
from datetime import *
from tkcalendar import DateEntry
from app.main.external_files.create_invoice import GenerateInvoice
from app.main.external_files.export_sales_order_data import ExportSalesOrderData

class ShowSalesOrder(tk.Canvas, TreeEssentials):
    
    def __init__(self, container, mysql, user, is_r_c_page=False, product_id=None):
        
        self.offset = 0
        self.limit = 15
        self.container = container
        # Data Set for Default from and today
        self.from_date_data = tk.StringVar()
        self.to_date_data = tk.StringVar()
        today_date = date.today()
        self.from_date_data.set(today_date)
        self.to_date_data.set(today_date)
        self.is_r_c_page  = is_r_c_page


        if type(product_id) == None.__class__:
            self.dataFetchingMethod = lambda export_bool=False: self.queryFetchPaginatedSalesOrder(
                offset=self.offset,
                limit=self.limit,
                from_date=self.from_date_data.get(),
                to_date=self.to_date_data.get(),
                radio_data=self.radio_value.get(),
                query_data=self.search_data.get(),
                export=export_bool
                )
        else:
            added_query = f""" WHERE `{SALES_ORDER_ID}` IN 
            ((SELECT `{S_O_P_FOREIGNKEY_SALES_ORDER_ID}` FROM `{DATABASE_NAME}`.`{SALES_ORDER_PRODUCT_TABLE_NAME}`
             WHERE `{S_O_P_FOREIGNKEY_PRODUCT_ID}` = {product_id})) """
            self.dataFetchingMethod = lambda export_bool=False: self.queryFetchPaginatedSalesOrder(
                offset=self.offset,
                limit=self.limit,
                from_date=self.from_date_data.get(),
                to_date=self.to_date_data.get(),
                radio_data=self.radio_value.get(),
                query_data=self.search_data.get(),
                query_add_on=added_query,
                export=export_bool
                )
            # Note we add 0 before because if there's only one id return from second statemnt like 3, so it bcm (3,) which give error, but with 0 (0,3)



        
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
            page_head = "Select Sales Orders:"
        elif not type(product_id) == None.__class__:
            page_head = f"Sales Orders for Product Id = {product_id}:"
        else:
            page_head = "Sales Orders / Customer's Invoice:"
            
        
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
                firstFunctionalityMethod=lambda: ExportSalesOrderData(
                    lambda: self.dataFetchingMethod(export_bool=True),
                    container=self
                    ),
                second_functionality_switch="call_passed_method_directly",
                second_functionality_button_text="Print Invoice",
                secondFunctionalityMethod=lambda: GenerateInvoice(sales_order_id=self.tree.item(self.tree.focus())["values"][1]),
                )

            # Define Other Search Options such as check box and combobox above Table
            self.defineParticularSearchesWidgets(self.above_frame, self.is_r_c_page)
            
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
                RecordPopupClass=lambda: RecordSalesOrder(
                    container=self,
                    mysql=self.mysql,
                    user=self.current_user,
                    sales_order_id=self.tree.item(self.tree.focus())["values"][1]
                    )
                )

        
        
    # Create Rows of Particular Tree with data from database   
    def definingRowsOfParticularTree(self, dataFetchingMethod):
        data = dataFetchingMethod()

        # when download button is not needed
        if self.is_r_c_page:
            pass
        else:
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
                c_name = self.morphText(data[i][SALES_ORDER_C_NAME], 18)
                c_mobile = self.morphText(data[i][SALES_ORDER_C_MOBILE], 18)
                c_email = self.morphText(data[i][SALES_ORDER_C_EMAIL], 18)
                user_name = self.morphText(data[i][USERNAME], 18)   
                order_status = data[i][SALES_ORDER_STATUS]
                price = self.formatINR(data[i][SALES_ORDER_TOTAL_PRICE]) 

                
                val = (s_no_count+1, data[i][SALES_ORDER_ID], c_name, c_mobile, c_email,
                 order_status, data[i][SALES_ORDER_PAYMENT_MODE], price, user_name, data[i][CREATED_AT])
                
                tag_value = tuple()
                if count % 2 != 0:
                    if order_status == ORDER_CANCELLED or order_status == ORDER_RETURNED:
                        tag_value = ("cancelled_odd_rows",)
                    else:
                        tag_value = ("odd_rows",)
                else:
                    if order_status == ORDER_CANCELLED or order_status == ORDER_RETURNED:
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
                                 ),
                             tags=("odd_row",)
                             )
            
            self.tree.configure(selectmode="none")

        
       
    # Create Tree Instance and set its Configuration 
    def createTreeAndConfiguration(self):
        
        # Tuple of Tree Columns
        columnTuple = ("s_no", SALES_ORDER_ID, SALES_ORDER_C_NAME, SALES_ORDER_C_MOBILE, SALES_ORDER_C_EMAIL , SALES_ORDER_STATUS, 
        SALES_ORDER_PAYMENT_MODE, SALES_ORDER_TOTAL_PRICE,  USERNAME, CREATED_AT)
        
        self.tree = ttk.Treeview(self, columns=columnTuple, show="headings", style="Tree.Treeview")
        
        # Defining Column Name 
        self.tree.heading("s_no", text="S. No.")
        self.tree.heading(SALES_ORDER_ID, text="Order ID")
        self.tree.heading(SALES_ORDER_C_NAME, text="Customer's Name")
        self.tree.heading(SALES_ORDER_C_MOBILE, text="Mobile")
        self.tree.heading(SALES_ORDER_C_EMAIL, text="E-Mail")
        self.tree.heading(SALES_ORDER_STATUS, text="Order Status")
        self.tree.heading(SALES_ORDER_PAYMENT_MODE, text="Payment Mode")
        self.tree.heading(SALES_ORDER_TOTAL_PRICE, text="Total (\u20B9)")
        self.tree.heading(USERNAME, text="Generated By")
        self.tree.heading(CREATED_AT, text="Date")
        
        
        # Defining Configuration for Columns
        self.tree.column("s_no", anchor="center")
        self.tree.column(SALES_ORDER_ID, anchor="center")
        self.tree.column(SALES_ORDER_C_NAME, anchor="center")
        self.tree.column(SALES_ORDER_C_MOBILE, anchor="center")
        self.tree.column(SALES_ORDER_C_EMAIL, anchor="center")
        self.tree.column(SALES_ORDER_STATUS, anchor="center")
        self.tree.column(SALES_ORDER_PAYMENT_MODE, anchor="center")
        self.tree.column(SALES_ORDER_TOTAL_PRICE, anchor="center")
        self.tree.column(USERNAME, anchor="center")
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
    def defineParticularSearchesWidgets(self, frame, is_r_c_page):
        
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
        self.radio_1 = ttk.Radiobutton(t_frame, text="Completed", variable=self.radio_value, value=1, command=self.radioButtonSelect, style="TreeRadiobutton.TRadiobutton")
        self.radio_2 = ttk.Radiobutton(t_frame, text="Cancelled", variable=self.radio_value, value=2, command=self.radioButtonSelect, style="TreeRadiobutton.TRadiobutton")
        self.radio_3 = ttk.Radiobutton(t_frame, text="Returned", variable=self.radio_value, value=3, command=self.radioButtonSelect, style="TreeRadiobutton.TRadiobutton")
    
        self.radio_1.invoke()
        if not (is_r_c_page): 
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
                dataFetchingMethod=lambda: self.dataFetchingMethod()
                )
            )


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
        self.radio_1.invoke()
        today_date= date.today()
        self.from_date_data.set(today_date)
        self.to_date_data.set(today_date)
        self.insertDataInTree(
            tableRowFetchAndRenderMethod=lambda: self.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.dataFetchingMethod()
                )
            )