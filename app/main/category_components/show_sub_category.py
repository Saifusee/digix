import tkinter as tk
from tkinter import ttk
from CONSTANT.index import *
from app.main.category_components.edit_sub_category import EditSubCategory
from app.main.category_components.record_category import RecordSubCategory
from app.main.tree_essentials import TreeEssentials

class ShowSubCategory(tk.Canvas, TreeEssentials):
    
    def __init__(self, container, mysql, user):
        
        self.offset = 0
        self.limit = 15
        
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
            page_heading="Show All Sub-Categories:",
            refreshedTableMethod=lambda: self.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.queryFetchPaginatedSubCategories(self.offset, self.limit)
                ),
            searchedRefreshTableMethod=lambda: self.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.queryFetchSearchedData(
                    offset=self.offset,
                    limit=self.limit,
                    query_data=self.search_data.get(),
                    selectable_columns_from_table_query=self.saved_query_sub_category_morphed,
                    table_name=SUB_CATEGORY_TABLE_NAME,
                    sort_column=f"{CATEGORY_ID}, {SUB_CATEGORY_NAME}"
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
                dataFetchingMethod=lambda: self.queryFetchPaginatedSubCategories(
                    self.offset,
                    self.limit
                    )
                ),
            searchedRefreshTableMethod=lambda: self.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.queryFetchSearchedData(
                    offset=self.offset, 
                    limit=self.limit,
                    query_data=self.search_data.get(),
                    selectable_columns_from_table_query=self.saved_query_sub_category_morphed,
                    table_name=SUB_CATEGORY_TABLE_NAME,
                    sort_column=f"{CATEGORY_ID}, {SUB_CATEGORY_NAME}"
                    )
                ),
            firstFunctionalityMethod=lambda: EditSubCategory(
                container=self,
                mysql=self.mysql,
                user=self.current_user,
                sub_category_id=self.tree.item(self.tree.focus())["values"][1], # tree.item() returns focus row data where values key is row data in tuple
                refreshedTableMethod=lambda: self.insertDataInTree(
                    tableRowFetchAndRenderMethod=lambda: self.definingRowsOfParticularTree(
                        dataFetchingMethod=lambda: self.queryFetchPaginatedSubCategories(offset=self.offset, limit=self.limit)
                        )
                    )
                ),
            secondFunctionalityMethod=self.queryDeleteSubCategory
            ) # tree.item() returns focused row data where ["values"] key is row data in tuple
        
        # Insert Data
        self.insertDataInTree(
            tableRowFetchAndRenderMethod=lambda: self.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.queryFetchPaginatedSubCategories(offset=self.offset, limit=self.limit))
            )
        
        # Defining Key and Mouse Bindings on Table  
        self.definingEventBindings(
            refreshTableMethod=lambda: self.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.queryFetchPaginatedSubCategories(offset=self.offset, limit=self.limit)
                ),
            RecordPopupClass=lambda: RecordSubCategory(
                container=self,
                mysql=self.mysql,
                user=self.current_user,
                sub_category_id=self.tree.item(self.tree.focus())["values"][1],
                refreshedTableMethod=lambda: self.insertDataInTree(
                    tableRowFetchAndRenderMethod=lambda: self.definingRowsOfParticularTree(
                        dataFetchingMethod=lambda: self.queryFetchPaginatedSubCategories(
                            offset=self.offset,
                            limit=self.limit
                            )
                        )
                    )
                ),
            secondFunctionalityMethod=self.queryDeleteSubCategory
            )

        
        
    # Create Rows of Particular Tree with data from database   
    def definingRowsOfParticularTree(self, dataFetchingMethod):
        data = dataFetchingMethod()
        # Inserting Data In Tree
        if len(data) >= 1:
            count = 0
            s_no_count = self.offset
            for i in range(len(data)):
                sub_category_name = self.morphText(data[i][SUB_CATEGORY_NAME]) 
                category_name = self.morphText(data[i][CATEGORY_NAME])          
                
                if count % 2 != 0:
                    self.tree.insert(
                        "",
                        tk.END,
                        values=(
                            f'{s_no_count+1}',
                            f'{data[i][SUB_CATEGORY_ID]}',
                            f'{sub_category_name}',
                            f'{category_name}',
                            ),
                        tags=("odd_row",)
                        )
                else:
                    self.tree.insert("",
                                     tk.END,
                                     values=(
                                        f'{s_no_count+1}',
                                        f'{data[i][SUB_CATEGORY_ID]}',
                                        f'{sub_category_name}',
                                        f'{category_name}',
                                        
                                        ),
                                     tags=("even_row",)
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
                                 "No Records Found"
                                 ),
                             tags=("odd_row",)
                             )
            
            self.tree.configure(selectmode="none")

        
       
    # Create Tree Instance and set its Configuration 
    def createTreeAndConfiguration(self):
        
        # Tuple of Tree Columns
        columnTuple = ("s_no", SUB_CATEGORY_ID, SUB_CATEGORY_NAME, SUB_CATEGORY_FOREIGNKEY_CATEGORY_ID)
        
        self.tree = ttk.Treeview(self, columns=columnTuple, show="headings", selectmode="extended", style="Tree.Treeview")
        
        # Defining Column Name 
        self.tree.heading("s_no", text="S. No.")
        self.tree.heading(SUB_CATEGORY_ID, text="Sub-Category ID")
        self.tree.heading(SUB_CATEGORY_NAME, text="Sub-Category Name")
        self.tree.heading(SUB_CATEGORY_FOREIGNKEY_CATEGORY_ID, text="Category Name")
        
        
        # Defining Configuration for Columns
        self.tree.column("s_no", anchor="center", stretch=tk.NO, width=100)
        self.tree.column(SUB_CATEGORY_ID, anchor="center", stretch=tk.NO, width=100)
        self.tree.column(SUB_CATEGORY_NAME, anchor="center")
        self.tree.column(SUB_CATEGORY_FOREIGNKEY_CATEGORY_ID, anchor="center")
        # Giving Striped Rows Style
        self.tree.tag_configure("even_row", background="lightblue")
        self.tree.tag_configure("odd_row", background="white")
        
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
                dataFetchingMethod=lambda: self.queryFetchPaginatedSubCategories(offset=self.offset, limit=self.limit)
                )
            )