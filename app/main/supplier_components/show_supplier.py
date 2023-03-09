import tkinter as tk
from tkinter import ttk
from CONSTANT.index import *
from app.main.supplier_components.edit_supplier import EditSupplier
from app.main.supplier_components.record_supplier import RecordSupplier
from app.main.external_files.export_supplier_data import ExportSupplierData
from app.main.tree_essentials import TreeEssentials

class ShowSupplier(tk.Canvas, TreeEssentials):
    
    def __init__(self, container, mysql, user, is_invoice_page=False):
        
        self.container = container # useful when treeview for supplier addition need toplevel instance to destroy
        self.offset = 0
        self.limit = 15
        self.is_invoice_page = is_invoice_page
        
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
            page_heading="Show All Registered Suppliers:",
            refreshedTableMethod=lambda: self.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.queryFetchPaginatedSuppliers(self.offset, self.limit)
                ),
            searchedRefreshTableMethod=lambda: self.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.queryFetchSearchedData(offset=self.offset,
                limit=self.limit,
                query_data=self.search_data.get(),
                selectable_columns_from_table_query=self.saved_query_supplier,
                table_name=SUPPLIER_TABLE_NAME,
                sort_column=SUPPLIER_NAME)
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
        
        # If For Invoice then don't call this methods
        if self.is_invoice_page:
            pass
        else:
            # Define Buttons below Table
            self.definePaginateButtons(
                refreshedTableMethod=lambda: self.definingRowsOfParticularTree(
                    dataFetchingMethod=lambda: self.queryFetchPaginatedSuppliers(
                        self.offset,
                        self.limit
                        )
                    ),
                searchedRefreshTableMethod=lambda: self.definingRowsOfParticularTree(
                    dataFetchingMethod=lambda: self.queryFetchSearchedData(
                        offset=self.offset, 
                        limit=self.limit,
                        query_data=self.search_data.get(),
                        selectable_columns_from_table_query=self.saved_query_supplier,
                        table_name=SUPPLIER_TABLE_NAME,
                        sort_column=SUPPLIER_NAME
                        )
                    ),
                firstFunctionalityMethod=lambda: EditSupplier(
                    container=self,
                    mysql=self.mysql,
                    user=self.current_user,
                    supplier_id=self.tree.item(self.tree.focus())["values"][1],
                    refreshedTableMethod=lambda: self.insertDataInTree(
                        tableRowFetchAndRenderMethod=lambda: self.definingRowsOfParticularTree(
                            dataFetchingMethod=lambda: self.queryFetchPaginatedSuppliers(offset=self.offset, limit=self.limit)
                            )
                        )
                    ),
                secondFunctionalityMethod=self.queryToggleSupplierStatus,
                second_functionality_button_text="Active/Inactive Supplier",
                second_functionality_switch="toggle_supplier_status",
                third_functionality_switch="download",
                third_functionality_button_text="Download Records",
                thirdFunctionalityMethod=lambda: ExportSupplierData(
                    lambda: self.queryFetchPaginatedSuppliers(
                        self.offset,
                        self.limit,
                        export=True
                        ),
                    container=self
                    ),
                is_triple_button_functionality_needed=True
                )
            
            # Insert Data
            self.insertDataInTree(
                tableRowFetchAndRenderMethod=lambda: self.definingRowsOfParticularTree(
                    dataFetchingMethod=lambda: self.queryFetchPaginatedSuppliers(offset=self.offset, limit=self.limit))
                )
            
            # Defining Key and Mouse Bindings on Table  
            self.definingEventBindings(
                refreshTableMethod=lambda: self.definingRowsOfParticularTree(
                    dataFetchingMethod=lambda: self.queryFetchPaginatedSuppliers(offset=self.offset, limit=self.limit)
                    ),
                RecordPopupClass=lambda: RecordSupplier(
                    container=self,
                    mysql=self.mysql,
                    user=self.current_user,
                    supplier_id=self.tree.item(self.tree.focus())["values"][1],
                    refreshedTableMethod=lambda: self.insertDataInTree(
                        tableRowFetchAndRenderMethod=lambda: self.definingRowsOfParticularTree(
                            dataFetchingMethod=lambda: self.queryFetchPaginatedSuppliers(
                                offset=self.offset,
                                limit=self.limit
                                )
                            )
                        )
                    ),
                secondFunctionalityMethod=self.queryToggleSupplierStatus,
                second_functionality_switch="toggle_supplier_status"
                )

        
        
    # Create Rows of Particular Tree with data from database   
    def definingRowsOfParticularTree(self, dataFetchingMethod):
        data = dataFetchingMethod()

        # when download button not needed
        if self.is_invoice_page:
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
                supplier_name = self.morphText(data[i][SUPPLIER_NAME])
                supplier_contact_1 = self.morphText(data[i][SUPPLIER_CONTACT_1])          
                supplier_contact_2 = self.morphText(data[i][SUPPLIER_CONTACT_2])
                active_state = "Active" if data[i][SUPPLIER_ACTIVE_STATE] == 1 else "Inactive"
                supplier_address = self.morphText(data[i][SUPPLIER_ADDRESS])
                supplier_org_name = self.morphText(data[i][SUPPLIER_ORGANIZATION_NAME])
                supplier_org_contact_1 = self.morphText(data[i][SUPPLIER_ORGANIZATION_CONTACT_1])
                supplier_org_contact_2 = self.morphText(data[i][SUPPLIER_ORGANIZATION_CONTACT_2])
                supplier_org_address = self.morphText(data[i][SUPPLIER_ORGANIZATION_ADDRESS])
                supplier_description = self.morphText(data[i][SUPPLIER_DESCRIPTION])
                
                val = (s_no_count+1, data[i][SUPPLIER_ID], supplier_name, active_state, supplier_contact_1,
                       supplier_contact_2, supplier_address, data[i][SUPPLIER_GSTIN], supplier_description, supplier_org_name, supplier_org_contact_1,
                       supplier_org_contact_2, supplier_org_address, data[i][CREATED_AT])
                
                tag_value = tuple()
                if count % 2 != 0:
                    tag_value = ("inactive_supplier_odd_rows",) if data[i][SUPPLIER_ACTIVE_STATE] == 0 else ("odd_row",)
                else:
                    tag_value = ("inactive_supplier_even_rows",) if data[i][SUPPLIER_ACTIVE_STATE] == 0 else ("even_row",)

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
        columnTuple = ("s_no", SUPPLIER_ID, SUPPLIER_NAME, SUPPLIER_ACTIVE_STATE, SUPPLIER_CONTACT_1,
                       SUPPLIER_CONTACT_2, SUPPLIER_ADDRESS, SUPPLIER_GSTIN, SUPPLIER_DESCRIPTION, SUPPLIER_ORGANIZATION_NAME,
                       SUPPLIER_ORGANIZATION_CONTACT_1, SUPPLIER_ORGANIZATION_CONTACT_2, SUPPLIER_ORGANIZATION_ADDRESS, CREATED_AT)
        
        self.tree = ttk.Treeview(self, columns=columnTuple, show="headings", style="Tree.Treeview")
        
        # Defining Column Name 
        self.tree.heading("s_no", text="S. No.")
        self.tree.heading(SUPPLIER_ID, text="Supplier ID")
        self.tree.heading(SUPPLIER_NAME, text="Name")
        self.tree.heading(SUPPLIER_ACTIVE_STATE, text="Status")
        self.tree.heading(SUPPLIER_CONTACT_1, text="Primary Contact")
        self.tree.heading(SUPPLIER_CONTACT_2, text="Secondary Contact")
        self.tree.heading(SUPPLIER_ADDRESS, text="Address")
        self.tree.heading(SUPPLIER_GSTIN, text="Supplier GSTIN")
        self.tree.heading(SUPPLIER_DESCRIPTION, text="Description")
        self.tree.heading(SUPPLIER_ORGANIZATION_NAME, text="Organization")
        self.tree.heading(SUPPLIER_ORGANIZATION_CONTACT_1, text="Organization Contact")
        self.tree.heading(SUPPLIER_ORGANIZATION_CONTACT_2, text="Organization Contact")
        self.tree.heading(SUPPLIER_ORGANIZATION_ADDRESS, text="Organization Address")
        self.tree.heading(CREATED_AT, text="Registered on")
        
        
        # Defining Configuration for Columns
        self.tree.column("s_no", anchor="center", stretch=tk.NO, width=100)
        self.tree.column(SUPPLIER_ID, anchor="center", stretch=tk.NO, width=100)
        self.tree.column(SUPPLIER_NAME, anchor="center")
        self.tree.column(SUPPLIER_ACTIVE_STATE, anchor="center")
        self.tree.column(SUPPLIER_CONTACT_1, anchor="center")
        self.tree.column(SUPPLIER_CONTACT_2, anchor="center")
        self.tree.column(SUPPLIER_ADDRESS, anchor="center")
        self.tree.column(SUPPLIER_GSTIN, anchor="center")
        self.tree.column(SUPPLIER_DESCRIPTION, anchor="center")
        self.tree.column(SUPPLIER_ORGANIZATION_NAME, anchor="center")
        self.tree.column(SUPPLIER_ORGANIZATION_CONTACT_1, anchor="center")
        self.tree.column(SUPPLIER_ORGANIZATION_CONTACT_2, anchor="center")
        self.tree.column(SUPPLIER_ORGANIZATION_ADDRESS, anchor="center")
        self.tree.column(CREATED_AT, anchor="center")
        
        # Giving Striped Rows Style
        self.tree.tag_configure("even_row", background="lightblue")
        self.tree.tag_configure("odd_row", background="white")
        self.tree.tag_configure("inactive_supplier_even_rows", background="#ffe6e6")
        self.tree.tag_configure("inactive_supplier_odd_rows", background="#ffcccc")
        
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
                dataFetchingMethod=lambda: self.queryFetchPaginatedSuppliers(offset=self.offset, limit=self.limit)
                )
            )