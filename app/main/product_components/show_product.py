import tkinter as tk
from tkinter import ttk
from CONSTANT.index import *
from app.main.product_components.edit_product import EditProduct
from app.main.product_components.record_product import RecordProduct
from app.main.tree_essentials import TreeEssentials
from app.main.external_files.export_product_data import ExportProductData
from app.main.other_components.custom_combobx import CustomCombobox
from error import ErrorModal

class ShowProduct(tk.Canvas, TreeEssentials):
    
    def __init__(self, container, mysql, user, is_invoice_page=False):

        self.container = container # useful when treeview for product addition need toplevel instance to destroy
        self.offset = 0
        self.limit = 15
        self.default_sub_category_combobox_value = ["-------- Search Sub-Category --------"]
        self.default_category_combobox_value = ["-------- Search Category --------"]
        self.default_combobox_id = [0]
        self.sub_category_value = tk.StringVar()
        self.category_value = tk.StringVar()
        self.category_name_list = list()
        self.category_id_list = list()
        self.sub_category_name_list = list()
        
        self.sub_category_id_list = list()

        
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
            page_heading="Inventory:",
            refreshedTableMethod=lambda: self.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.queryFetchPaginatedProducts(self.offset, self.limit)
                ),
            searchedRefreshTableMethod=self.definingRowsOfParticularTree,
            is_product_table=1
            )
        
        # Create Tree
        self.createTreeAndConfiguration()
        
        # Rendering Scrollbar
        self.renderScrollbar()
        
        # Initiliazing Tree essentials method and components
        TreeEssentials.__init__(self, mysql=mysql, user=user, tree_instance=self.tree)
        
        
        # Define Frames below Table
        self.defineBelowFrames(container=self)
        
    
        # If For Invoice then don't call this methods
        if is_invoice_page:
            pass
        else:
            # Define Buttons below Table
            self.definePaginateButtons(
                refreshedTableMethod=lambda: self.definingRowsOfParticularTree(
                    dataFetchingMethod=lambda: self.queryFetchPaginatedProducts(
                        self.offset,
                        self.limit
                        )
                    ),
                searchedRefreshTableMethod=self.definingRowsOfParticularTree,
                firstFunctionalityMethod=EditProduct,
                second_functionality_switch="toggle_product_delete_status",
                second_functionality_button_text="Delete Record",
                secondFunctionalityMethod=self.queryToggleProductDeleteStatus,
                third_functionality_switch="download",
                third_functionality_button_text="Download Records",
                thirdFunctionalityMethod=lambda: ExportProductData(
                    lambda: self.queryFetchPaginatedProducts(
                        self.offset,
                        self.limit,
                        self.radio_value.get(),
                        self.category_id_selected,
                        self.sub_category_id_selected,
                        self.search_data.get(),
                        export=True
                        ),
                    container=self
                    ),
                is_product_table=1,
                is_triple_button_functionality_needed=True
                )
        
            # Define Other Search Options such as check box and combobox above Table
            self.defineParticularSearchesWidgets(self.above_frame)
        
            # Fetch Categories and Sub Categories for Products
            self.fetchCategoriesForProduct()
            
            # Insert Data
            self.insertDataInTree(
                tableRowFetchAndRenderMethod=lambda: self.definingRowsOfParticularTree(
                    dataFetchingMethod=lambda: self.queryFetchPaginatedProducts(offset=self.offset, limit=self.limit))
                )
            
            # Defining Key and Mouse Bindings on Table  
            self.definingEventBindings(
                refreshTableMethod=self.definingRowsOfParticularTree,
                RecordPopupClass=RecordProduct,
                secondFunctionalityMethod=self.queryToggleProductDeleteStatus,
                second_functionality_switch="toggle_product_delete_status",
                is_product_table=1
                )

        
        
    # Create Rows of Particular Tree with data from database 
    # Also used as refreshedTableMethod or searchedRefreshTableMethod  
    def definingRowsOfParticularTree(self, dataFetchingMethod, type=None):
        data = dataFetchingMethod()
        # Inserting Data In Tree
        if len(data) >= 1:
            count = 0
            s_no_count = self.offset
            for i in range(len(data)):
                
                product_name = self.morphText(data[i][PRODUCT_NAME], 50)
                product_description = self.morphText(data[i][PRODUCT_DESCRIPTION])   
                category_name = self.morphText(data[i][CATEGORY_NAME], 40)
                sub_category_name = self.morphText(data[i][SUB_CATEGORY_NAME], 40)
                price = self.formatINR(data[i][PRODUCT_PRICE])
                
                # If Product Treeview is for product selection for invoice and for sales order
                if self.is_product_table_for_invoice_product_selection == 1 and type == "SalesOrder":
                    val = (s_no_count+1, data[i][PRODUCT_ID], product_name, price, "x 0", f"x {data[i][PRODUCT_QUANTITY]}",
                        product_description, category_name, sub_category_name, data[i][PRODUCT_REORDER_QUANTITY],
                        data[i][PRODUCT_PRICE_UPDATE_DATETIME], data[i][UPDATED_AT], data[i][CREATED_AT])
                # If Product Treeview is for product selection for invoice and for purchase order
                elif self.is_product_table_for_invoice_product_selection == 1 and type == "PurchaseOrder":
                    val = (s_no_count+1, data[i][PRODUCT_ID], product_name, price, self.formatINR(0.00),
                         "x 0", f"x {data[i][PRODUCT_QUANTITY]}", product_description, category_name, sub_category_name, data[i][PRODUCT_REORDER_QUANTITY],
                        data[i][PRODUCT_PRICE_UPDATE_DATETIME], data[i][UPDATED_AT], data[i][CREATED_AT])
                else:
                    val = (s_no_count+1, data[i][PRODUCT_ID], product_name, price, f"x {data[i][PRODUCT_QUANTITY]}",
                        product_description, category_name, sub_category_name, data[i][PRODUCT_REORDER_QUANTITY],
                        data[i][PRODUCT_PRICE_UPDATE_DATETIME], data[i][UPDATED_AT], data[i][CREATED_AT])

                # In invoice selection if the product id is selected then this tag is applied to it row 
                if data[i][PRODUCT_ID] in self.mapped_tag_data.keys():
                    tag_val = ("selected_for_invoice",)
                # if product_id is deleted
                elif data[i][PRODUCT_IS_DELETED] == 1:
                    if count % 2 != 0:
                        tag_val = ("deleted_even_row",)
                    else:
                        tag_val = ("deleted_odd_row",)
                # if product_id is low in stock
                elif data[i][PRODUCT_QUANTITY] <= data[i][PRODUCT_REORDER_QUANTITY]:
                    if count % 2 != 0:
                        tag_val = ("low_stock_even_row",)
                    else:
                        tag_val = ("low_stock_odd_row",)
                else:
                    if count % 2 != 0:
                        tag_val = ("odd_row",)
                    else:
                        tag_val = ("even_row",)
                    
                self.tree.insert(
                    "",
                    tk.END,
                    values=val,
                    tags=tag_val
                    )
                count = count + 1
                s_no_count = s_no_count + 1
                self.tree.configure(selectmode="extended")
        else:
            # If Product Treeview is for product selection for invoice
            if self.is_product_table_for_invoice_product_selection == 0:
                val = ("No Reco....", "No Reco....", "No Records Found", "No Records Found", "No Reco....", "No Records Found",
                 "No Records Found", "No Records Found",  "No Reco....", "No Records Found", "No Records Found", "No Records Found")
            else:
                val = ("No Reco....", "No Reco....", "No Records Found", "No Records Found", "No Records Found", "No Reco....", "No Records Found",
                 "No Records Found", "No Records Found",  "No Reco....", "No Records Found", "No Records Found", "No Records Found")

            self.tree.insert("",
                             tk.END,
                             values=val,
                             tags=("odd_row",)
                             )
            
            self.tree.configure(selectmode="none")

        
       
    # Create Tree Instance and set its Configuration 
    def createTreeAndConfiguration(self, type=None, product_treeview_for_invoice_modification=False):
        # If Product Treeview is for product selection for invoice
        if product_treeview_for_invoice_modification and type == "PurchaseOrder":
            # Tuple of Tree Columns
            columnTuple = ("s_no", PRODUCT_ID, PRODUCT_NAME, PRODUCT_PRICE, "bought_price", "selected_quantity", PRODUCT_QUANTITY, PRODUCT_DESCRIPTION,
                        PRODUCT_FOREIGNKEY_CATEGORY_ID, PRODUCT_FOREIGNKEY_SUB_CATEGORY_ID, PRODUCT_REORDER_QUANTITY,
                        PRODUCT_PRICE_UPDATE_DATETIME, UPDATED_AT, CREATED_AT)
        elif product_treeview_for_invoice_modification and type == "SalesOrder":
            # Tuple of Tree Columns
            columnTuple = ("s_no", PRODUCT_ID, PRODUCT_NAME, PRODUCT_PRICE, "selected_quantity", PRODUCT_QUANTITY, PRODUCT_DESCRIPTION,
                        PRODUCT_FOREIGNKEY_CATEGORY_ID, PRODUCT_FOREIGNKEY_SUB_CATEGORY_ID, PRODUCT_REORDER_QUANTITY,
                        PRODUCT_PRICE_UPDATE_DATETIME, UPDATED_AT, CREATED_AT)
        else:
            # Tuple of Tree Columns
            columnTuple = ("s_no", PRODUCT_ID, PRODUCT_NAME, PRODUCT_PRICE, PRODUCT_QUANTITY, PRODUCT_DESCRIPTION,
                        PRODUCT_FOREIGNKEY_CATEGORY_ID, PRODUCT_FOREIGNKEY_SUB_CATEGORY_ID, PRODUCT_REORDER_QUANTITY,
                        PRODUCT_PRICE_UPDATE_DATETIME, UPDATED_AT, CREATED_AT)
            
        
        self.tree = ttk.Treeview(self, columns=columnTuple, show="headings", selectmode="extended", style="Tree.Treeview")
        
        # Defining Column Name 
        self.tree.heading("s_no", text="S. No.")
        self.tree.heading(PRODUCT_ID, text="Product ID")
        self.tree.heading(PRODUCT_NAME, text="Product Name")
        self.tree.heading(PRODUCT_PRICE, text="Price (\u20B9)")
        self.tree.heading(PRODUCT_QUANTITY, text="Quantity")
        self.tree.heading(PRODUCT_DESCRIPTION, text="Description")
        self.tree.heading(PRODUCT_FOREIGNKEY_CATEGORY_ID, text="Category")
        self.tree.heading(PRODUCT_FOREIGNKEY_SUB_CATEGORY_ID, text="Sub-Category")
        self.tree.heading(PRODUCT_REORDER_QUANTITY, text="Reorder Quantity")
        self.tree.heading(PRODUCT_PRICE_UPDATE_DATETIME, text="Price Updated At")
        self.tree.heading(UPDATED_AT, text="Updated At")
        self.tree.heading(CREATED_AT, text="Created At")
        
        
        # Defining Configuration for Columns
        self.tree.column("s_no", anchor="center", stretch=tk.NO, width=100)
        self.tree.column(PRODUCT_ID, anchor="center", stretch=tk.NO, width=100)
        self.tree.column(PRODUCT_NAME, anchor="center", stretch=tk.NO, width=500)
        self.tree.column(PRODUCT_PRICE, anchor="center")
        self.tree.column(PRODUCT_QUANTITY, anchor="center", stretch=tk.NO, width=100)
        self.tree.column(PRODUCT_DESCRIPTION, anchor="center")
        self.tree.column(PRODUCT_FOREIGNKEY_CATEGORY_ID, anchor="center", stretch=tk.NO, width=400)
        self.tree.column(PRODUCT_FOREIGNKEY_SUB_CATEGORY_ID, anchor="center", stretch=tk.NO, width=400)
        self.tree.column(PRODUCT_REORDER_QUANTITY, anchor="center")
        self.tree.column(PRODUCT_PRICE_UPDATE_DATETIME, anchor="center")
        self.tree.column(UPDATED_AT, anchor="center")
        self.tree.column(CREATED_AT, anchor="center")

        # If Product Treeview is for product selection for invoice and SalesOrder
        if product_treeview_for_invoice_modification and type == "SalesOrder":
            self.tree.heading("selected_quantity", text="Selected Quantity")
            self.tree.column("selected_quantity", anchor="center")

        # If Product Treeview is for product selection for invoice and PurchaseOrder
        if product_treeview_for_invoice_modification and type == "PurchaseOrder":
            self.tree.heading("selected_quantity", text="Selected Quantity")
            self.tree.column("selected_quantity", anchor="center")
            self.tree.heading("bought_price", text="Bought Price")
            self.tree.column("bought_price", anchor="center")
            self.tree.heading(PRODUCT_PRICE, text="Selling Price")
            self.tree.column(PRODUCT_PRICE, anchor="center")

        # Giving Striped Rows Style
        self.tree.tag_configure("even_row", background="lightblue")
        self.tree.tag_configure("odd_row", background="white")
        self.tree.tag_configure("low_stock_even_row", background="#ffffe6")
        self.tree.tag_configure("low_stock_odd_row", background="#ffffcc")
        self.tree.tag_configure("deleted_even_row", background="#ffe6e6")
        self.tree.tag_configure("deleted_odd_row", background="#ffcccc")
        self.tree.tag_configure("selected_for_invoice", background="#66ff66")
        
        # Rendering Tree
        self.tree.grid(row=1, column=0, sticky="nsew")

        
    
    # Frame Configurations for Search above Tables
    def defineAboveFrames(self):
        self.above_frame = ttk.Frame(self, padding=(10,0,10,0))
        self.above_frame.grid(row=0, column=0, sticky="nsew")


    # Define Widgets Above TreeView for Searching Purposes of Product
    def defineParticularSearchesWidgets(self, frame):

        # Frame for Combobox 
        self.c_frame = ttk.Frame(frame)
        self.c_frame.pack(side="right", fill="y", padx=(0, 30), pady=(0, 10))
        
        # Frame for Radio Buttons
        r_frame = ttk.Frame(frame)
        r_frame.pack(side="left", fill="y", padx=10)
        
        # Combobox
        combo_label_1 = ttk.Label(self.c_frame, text="Category:", font=("TkDefaulFont", 9, "bold"))
        combo_label_1.grid(row=0, column=0, sticky="ns", pady=(0, 5))
        combo_label_2 = ttk.Label(self.c_frame, text="Sub-Category:", font=("TkDefaulFont", 9, "bold"))
        combo_label_2.grid(row=1, column=0, sticky="ns", pady=(5, 5))
        
        # Dummy Comboxbox Structues with no value
        self.category_combobox = CustomCombobox(
            self.c_frame,
            width=50,
            textvariable=self.category_value,
            valueList=self.category_name_list,
            defaultvalue=self.default_category_combobox_value,
            state="readonly",
            justify="center",
            font=("TkDefaultFont", 10, "bold"),
            style="ShowProduct.TCombobox"
        )
        self.category_combobox.grid(row=0, column=1, sticky="ns", padx=(5, 0), pady=(0, 5))
        self.category_combobox.bind("<<ComboboxSelected>>", self.categoryComboboxSelect)
        
        self.sub_category_combobox = CustomCombobox(
            self.c_frame,
            width=50,
            textvariable=self.sub_category_value,
            valueList=self.sub_category_name_list,
            defaultvalue=self.default_sub_category_combobox_value,
            state="readonly",
            justify="center",
            font=("TkDefaultFont", 10, "bold"),
            style="ShowProduct.TCombobox"
        )
        self.sub_category_combobox.grid(row=1, column=1, sticky="ns", padx=(5, 0), pady=(5, 5))
        self.sub_category_combobox.current(0)
        

        
        
        # Radiobuttons
        self.radio_1 = ttk.Radiobutton(r_frame, text="All Products", variable=self.radio_value, value=0, command=self.radioButtonSelect, style="TreeRadiobutton.TRadiobutton")
        self.radio_2 = ttk.Radiobutton(r_frame, text="Active Products", variable=self.radio_value, value=1, command=self.radioButtonSelect, style="TreeRadiobutton.TRadiobutton")
        self.radio_3 = ttk.Radiobutton(r_frame, text="Deleted", variable=self.radio_value, value=2, command=self.radioButtonSelect, style="TreeRadiobutton.TRadiobutton")
        self.radio_4 = ttk.Radiobutton(r_frame, text="Low Stock", variable=self.radio_value, value=3, command=self.radioButtonSelect, style="TreeRadiobutton.TRadiobutton")
        self.radio_2.invoke()
        self.radio_4.pack(side="right", fill="x", padx=5)
        self.radio_3.pack(side="right", fill="x", padx=5) if self.is_product_table_for_invoice_product_selection == 0 else 0
        self.radio_2.pack(side="right", fill="x", padx=5)
        self.radio_1.pack(side="right", fill="x", padx=5) if self.is_product_table_for_invoice_product_selection == 0 else 0
        
        
    # Fetching Categories for Combobox  
    def fetchCategoriesForProduct(self):
        try:
            category_data = self.queryFetchAllCategories()  
            
            self.category_name_list = self.dbValTuple(category_data, CATEGORY_NAME) # Extracting Categories values from query fetched dictionaries
            self.category_id_list = self.default_combobox_id + self.dbValTuple(category_data, CATEGORY_ID) # Extracting Categories values from query fetched dictionaries 
            # Rendering new category combobx with values
            self.category_combobox = CustomCombobox(
                self.c_frame,
                width=50,
                textvariable=self.category_value,
                valueList=self.category_name_list,
                defaultvalue=self.default_category_combobox_value,
                state="readonly",
                justify="center",
                font=("TkDefaultFont", 10, "bold"),
                style="ShowProduct.TCombobox"
            )
            self.category_combobox.current(0)
            self.category_combobox.grid(row=0, column=1, sticky="ns", padx=(5, 0), pady=(0, 5))
            self.category_combobox.bind("<<ComboboxSelected>>", self.categoryComboboxSelect)

        except Exception as error:
            print(f"Development Error (Fetching Categories and Sub Categories for Show Product Treeview): {error}")
            ErrorModal("Something went wrong, please contact software developer.")
            
            
            
    # When Category Combobox is selected
    def categoryComboboxSelect(self, event):
        self.offset = 0
        self.category_id_selected = self.category_id_list[self.category_combobox.current()]
        self.sub_category_id_selected = None

        # Setting New Values to Sub Category Combobox
        sub_category_data = self.queryFetchRelevantSubCategories(self.category_id_selected)
        self.sub_category_name_list = self.dbValTuple(sub_category_data, SUB_CATEGORY_NAME) # Extracting Categories values from query fetched dictionaries
        self.sub_category_id_list = self.default_combobox_id + self.dbValTuple(sub_category_data, SUB_CATEGORY_ID) # Extracting Categories values from query fetched dictionaries
        # If No category selected
        if self.category_id_selected <= 0:
          self.category_id_selected = None  
        self.insertDataInTree(
                            tableRowFetchAndRenderMethod=lambda: self.definingRowsOfParticularTree(
                                dataFetchingMethod=lambda: self.queryFetchPaginatedProducts(
                                    self.offset,
                                    self.limit,
                                    self.radio_value.get(),
                                    self.category_id_selected,
                                    self.sub_category_id_selected,
                                    self.search_data.get()
                                    )
                                )
                            )
        
        # Rendering new sub-category combobx with values
        self.sub_category_combobox = CustomCombobox(
            self.c_frame,
            width=50,
            textvariable=self.sub_category_value,
            valueList=self.sub_category_name_list,
            defaultvalue=self.default_sub_category_combobox_value,
            state="readonly",
            justify="center",
            font=("TkDefaultFont", 10, "bold"),
            style="ShowProduct.TCombobox"
        )
        self.sub_category_combobox.current(0)
        self.sub_category_combobox.grid(row=1, column=1, sticky="ns", padx=(5, 0), pady=(5, 5))
        self.sub_category_combobox.bind("<<ComboboxSelected>>", self.subCategoryComboboxSelect)
        
        
        
    # When Sub-Category Combobox is selected
    def subCategoryComboboxSelect(self, event):
        self.offset = 0
        self.sub_category_id_selected = self.sub_category_id_list[self.sub_category_combobox.current()]
        # If No sub-category selected
        if (self.sub_category_id_selected <= 0):
            self.sub_category_id_selected = None
        self.insertDataInTree(
                            tableRowFetchAndRenderMethod=lambda: self.definingRowsOfParticularTree(
                                dataFetchingMethod=lambda: self.queryFetchPaginatedProducts(
                                    self.offset,
                                    self.limit,
                                    self.radio_value.get(),
                                    self.category_id_selected,
                                    self.sub_category_id_selected,
                                    self.search_data.get()
                                    )
                                )
                            )
        
        
        
    # When Radio Buttons Selected
    def radioButtonSelect(self):
        self.offset = 0
        # If Product Treeview is for adding product to invoice then not override delete button text
        if self.is_product_table_for_invoice_product_selection == 1:
            pass
        else:
            if self.radio_value.get() == 2:
                self.second_functionality_button.configure(text="Restore")
            else:
                self.second_functionality_button.configure(text="Delete")

        self.insertDataInTree(
                            tableRowFetchAndRenderMethod=lambda: self.definingRowsOfParticularTree(
                                dataFetchingMethod=lambda: self.queryFetchPaginatedProducts(
                                    self.offset,
                                    self.limit,
                                    self.radio_value.get(),
                                    self.category_id_selected,
                                    self.sub_category_id_selected,
                                    self.search_data.get()
                                    )
                                )
                            )
                
          
                
    # Reset Page
    def customReset(self):
        self.offset = 0
        self.second_functionality_button.configure(text="Delete")
        # Fetch Categories and Sub Categories for Products
        self.fetchCategoriesForProduct()
        # Reset Sub Category Combobx conditions
        self.sub_category_combobox.configure(values=self.default_sub_category_combobox_value,)
        self.sub_category_combobox.current(0)
        # Setting Radio Buttons Default Values
        self.radio_2.invoke()
        # Fetching Data for Treeview
        self.insertDataInTree(
            tableRowFetchAndRenderMethod=lambda: self.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.queryFetchPaginatedProducts(offset=self.offset, limit=self.limit)
                )
            )





