import tkinter as tk
from tkinter import ttk
from CONSTANT.index import *
from app.main.tree_essentials import TreeEssentials
from app.main.product_components.record_product_logs import RecordProductLog

class ShowProductLogs(tk.Toplevel, TreeEssentials):
    
    def __init__(self, container, mysql, user, product_id, product_name="Product Logs:"):
        
        self.offset = 0
        self.limit = 15
        
       # Get Product Table Logs with required columns with foreign key relations values
        self.saved_query_product_log_morphed = f"""
        SELECT * FROM 
        (SELECT A.{PRODUCT_LOGS_ID}, A.{PRODUCT_LOGS_LOG}, A.{PRODUCT_LOGS_FOREIGNKEY_PRODUCT_ID},
        A.{PRODUCT_LOGS_FOREIGNKEY_USER_ID}, A.{CREATED_AT},
        B.{PRODUCT_NAME} AS {PRODUCT_NAME},
        C.{USERNAME} AS {USERNAME}
        FROM {DATABASE_NAME}.{PRODUCT_LOGS_TABLE_NAME} AS A
        LEFT JOIN 
        {DATABASE_NAME}.{PRODUCT_TABLE_NAME} AS B ON A.{PRODUCT_LOGS_FOREIGNKEY_PRODUCT_ID} = B.{PRODUCT_ID}
        LEFT JOIN 
        {DATABASE_NAME}.{USER_TABLE_NAME} AS C ON A.{PRODUCT_LOGS_FOREIGNKEY_USER_ID} = C.{USER_ID}
        WHERE A.{PRODUCT_LOGS_FOREIGNKEY_PRODUCT_ID} = {product_id})
        AS merge_table"""
        
        
        # Note: when we call, instance.method(), method automatically take instance as first argument which we define as self
        # when we call, Class.method(), method need instance manually as first argument bcz it doesn't know which one to take
        tk.Toplevel.__init__(self, container)
        self.grab_set()
        self.state('zoomed') # Open App fullscreen in maximize window  
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
            page_heading=product_name,
            refreshedTableMethod=lambda: self.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.queryFetchPaginatedLogs(
                    self.offset,
                    self.limit,
                    query_to_get=self.saved_query_product_log_morphed
                    )
                ),
            searchedRefreshTableMethod=lambda: self.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.queryFetchSearchedData(offset=self.offset,
                limit=self.limit,
                query_data=self.search_data.get(),
                selectable_columns_from_table_query=self.saved_query_product_log_morphed,
                table_name=PRODUCT_LOGS_TABLE_NAME,
                sort_column=CREATED_AT,
                sort_order="DESC"
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
                dataFetchingMethod=lambda: self.queryFetchPaginatedLogs(
                    self.offset,
                    self.limit,
                    query_to_get=self.saved_query_product_log_morphed
                    )
                ),
            searchedRefreshTableMethod=lambda: self.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.queryFetchSearchedData(
                    offset=self.offset, 
                    limit=self.limit,
                    query_data=self.search_data.get(),
                    selectable_columns_from_table_query=self.saved_query_product_log_morphed,
                    table_name=PRODUCT_LOGS_TABLE_NAME,
                    sort_column=CREATED_AT,
                    sort_order="DESC"
                    )
                ),
                is_zero_button_functionality_needed=True
            )
        
        # Insert Data
        self.insertDataInTree(
            tableRowFetchAndRenderMethod=lambda: self.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.queryFetchPaginatedLogs(
                    offset=self.offset,
                    limit=self.limit,
                    query_to_get=self.saved_query_product_log_morphed
                    )
                )
            )
        
        # Defining Key and Mouse Bindings on Table  
        self.definingEventBindings(
            refreshTableMethod=lambda: self.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.queryFetchPaginatedLogs(
                    offset=self.offset,
                    limit=self.limit,
                    query_to_get=self.saved_query_product_log_morphed
                    )
                ),
            RecordPopupClass=lambda: RecordProductLog(
                container=self,
                mysql=self.mysql,
                user=self.current_user,
                product_log_id=self.tree.item(self.tree.focus())["values"][-1]
                )
            )

        
        
    # Create Rows of Particular Tree with data from database   
    def definingRowsOfParticularTree(self, dataFetchingMethod):
        data = dataFetchingMethod()
        # Inserting Data In Tree
        if len(data) >= 1:
            count = 0
            for i in range(len(data)):
                
                log = self.morphText(data[i][PRODUCT_LOGS_LOG], 144)        
                user = self.morphText(data[i][USERNAME])
                date = data[i][CREATED_AT].strftime("%Y-%m-%d") 
                time = data[i][CREATED_AT].strftime("%H:%M:%S") 
                
                if count % 2 != 0:
                    tag_value = ("odd_row",)
                else:
                    tag_value = ("even_row",)
                    
                self.tree.insert("",
                                    tk.END,
                                    values=(
                                    date,
                                    time,
                                    log,
                                    user,
                                    data[i][PRODUCT_LOGS_ID]
                                    ),
                                    tags=tag_value
                                    )
                count = count + 1
                self.tree.configure(selectmode="extended")
        else:
            self.tree.insert("",
                             tk.END,
                             values=(
                                 "No Records Found",
                                 "No Records Found", 
                                 "No Records Found",
                                 "No Records Found"
                                 ),
                             tags=("odd_row",)
                             )
            
            self.tree.configure(selectmode="none")

        
       
    # Create Tree Instance and set its Configuration 
    def createTreeAndConfiguration(self):
        
        # Tuple of Tree Columns
        columnTuple = ("DATE", "TIME", PRODUCT_LOGS_LOG, USERNAME)
        
        self.tree = ttk.Treeview(self, columns=columnTuple, show="headings", selectmode="extended", style="Tree.Treeview")
        
        # Defining Column Name 
        self.tree.heading("DATE", text="Date")
        self.tree.heading("TIME", text="Time")
        self.tree.heading(PRODUCT_LOGS_LOG, text="Logs")
        self.tree.heading(USERNAME, text="User")
        
        
        # Defining Configuration for Columns
        self.tree.column("DATE", anchor="center", stretch=tk.NO, width=100) # Automatically set to shortest width
        self.tree.column("TIME", anchor="center", stretch=tk.NO, width=100)
        self.tree.column(PRODUCT_LOGS_LOG, anchor="center", stretch=tk.YES, width=100)
        self.tree.column(USERNAME, anchor="center", stretch=tk.NO, width=200)

        # Giving Striped Rows Style
        self.tree.tag_configure("even_row", background="#dadaf1")
        self.tree.tag_configure("odd_row", background="#c7c7eb")
        
        # Rendering Tree
        self.tree.grid(row=1, column=0, sticky="nsew")

        
    
    # Frame Configurations for Search above Tables
    def defineAboveFrames(self):
        self.above_frame = ttk.Frame(self, padding=15)
        self.above_frame.grid(row=0, column=0, sticky="nsew")



    # Reset Page
    def customReset(self):
        self.offset = 0
        self.insertDataInTree(
            tableRowFetchAndRenderMethod=lambda: self.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.queryFetchPaginatedLogs(
                    offset=self.offset,
                    limit=self.limit,
                    query_to_get=self.saved_query_product_log_morphed
                    )
                )
            )