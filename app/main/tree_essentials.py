import tkinter as tk
from tkinter import ttk
from CONSTANT.index import *
from app.base import Base
from modal import Modal
from PIL import Image, ImageTk
from os import path


class TreeEssentials(Base):
    def __init__(self, mysql, user, tree_instance,  *args, **kwargs):
        super().__init__(mysql, user)
        self.tree = tree_instance
        self.totalRecordsCount = 0
        self.radio_value = tk.IntVar()
        self.category_value = tk.StringVar()
        self.sub_category_value = tk.StringVar()
        self.category_id_selected = None
        self.sub_category_id_selected = None
        self.is_product_table = 0
        self.selected_products_for_invoice = list()
        self.selected_products_id_for_invoice = list()
        self.selected_id = int()
        self.is_product_table_for_invoice_product_selection = 0
        # Keys = ProductId, Values = Tag_value given to row of respective product_id
        self.mapped_tag_data = dict() 

         
        
    
    ##############################################
    #########   Data Insertion in Tree   #########
    ##############################################
        
    # Insert Data in Tree from Databasessss
    def insertDataInTree(self, tableRowFetchAndRenderMethod):
        
        # Deletinig whole tree
        self.deleteWholeTree()
        # Fetching Data from Database and constructing rows of tree
        tableRowFetchAndRenderMethod()
        
        first_record_no_in_page = 0 if self.totalRecordsCount == 0 else (self.offset + 1)
        last_record_no_in_page = self.totalRecordsCount if (self.offset + self.limit) > self.totalRecordsCount else self.offset + self.limit
        st = f"Total Records found: {first_record_no_in_page} - {last_record_no_in_page} / {self.totalRecordsCount}"
        self.lb.configure(text=st)
        
        # Toggle Pagination Buttons
        self.togglePaginationButtonState()
        
        
     # Disable or Enable Paginate Buttons   
    def togglePaginationButtonState(self):
        # Disabling or Enabling Next Button as per records available
        if self.offset + self.limit >= self.totalRecordsCount:
            self.next_button.configure(state="disabled")
        elif self.offset + self.limit < self.totalRecordsCount:
            self.next_button.configure(state="normal")
        else:
            self.next_button.configure(state="disabled")
        
        # Disabling or Enabling Previous Button as per records available
        if self.offset <= 0:
            self.previous_button.configure(state="disabled")
        else:
            self.previous_button.configure(state="normal")
        
        
        
    ##############################################
    ########  Search field and its methods  ######
    ##############################################
        
     # Defining Icon-Button Widget for Search Bar   
    def imageForSearchButton(self):
        path_to_image = path.join(PATH_TO_ROOT, "assets", FILE_TABLE_SEARCH_BUTTON)
        _s_i_ = Image.open(path_to_image)
        _s_i_ = _s_i_.resize((20,20))
        self.imig = ImageTk.PhotoImage(_s_i_)
        return self.imig
        
        
        
    # Defining Search field and button above table   
    def defineSearchButtons(self, frame, page_heading, refreshedTableMethod=None, searchedRefreshTableMethod=None, is_product_table=0):
        self.search_data = tk.StringVar()

        # If no searching functionality needed
        if type(refreshedTableMethod) == None.__class__ and type(searchedRefreshTableMethod) == None.__class__:
            pass
        else:
            # Mechanism is different for product table search system
            if is_product_table == 1:
                self.is_product_table = 1
                call_search_data = lambda: self.searchData(
                    refreshedTableMethod=lambda: refreshedTableMethod(),
                    searchedRefreshTableMethod=searchedRefreshTableMethod
                    )
            else:
                call_search_data = lambda: self.searchData(
                    refreshedTableMethod=lambda: refreshedTableMethod(),
                    searchedRefreshTableMethod=lambda: searchedRefreshTableMethod()
                    )
            
        self.title_label = ttk.Label(frame, text=page_heading, style="TreeviewTitleLabel.TLabel")
        self.title_label.pack(side="top", fill="x")

        # If no searching functionality needed
        if type(refreshedTableMethod) == None.__class__ and type(searchedRefreshTableMethod) == None.__class__:
            pass
        else:
            self.search_button = tk.Button(frame,
                                        width=40,
                                        height=18,
                                        image=self.imageForSearchButton(),
                                        command=lambda: call_search_data()
            )
            
            self.search_button.pack(side="right")
            self.search_entry = ttk.Entry(frame,
                                    textvariable=self.search_data,
                                    width=30,
                                    justify="center",
                                    font=("TkdefaultFont", 12, "bold")
                                    )
            self.search_entry.pack(side="right")
            # Search Box Bindings
            self.search_entry.bind("<Return>", lambda e: call_search_data())
            self.search_entry.bind("<KeyRelease>", lambda e: call_search_data())
            self.search_entry.bind("<FocusOut>", lambda e: call_search_data())
        
        
        
    # Search data in Table
    def searchData(self, refreshedTableMethod, searchedRefreshTableMethod):

        # Mechanism is different for Product Table Search System
        if self.is_product_table == 1:
            self.insertDataInTree(
                tableRowFetchAndRenderMethod=lambda : searchedRefreshTableMethod(
                    lambda: self.queryFetchPaginatedProducts(
                        self.offset,
                        self.limit,
                        self.radio_value.get(),
                        self.category_id_selected,
                        self.sub_category_id_selected,
                        self.search_data.get()
                        )
                    )
                )
        # For All Other Tables
        elif self.search_data.get() == "":
            self.insertDataInTree(tableRowFetchAndRenderMethod=lambda : refreshedTableMethod())
        else:
            self.offset=0
            self.insertDataInTree(tableRowFetchAndRenderMethod=lambda: searchedRefreshTableMethod())
            
            
            
    ##############################################
    #######  Pagination and its components  ######
    ##############################################
        
    # Frame Configurations for Button below Tables
    def defineBelowFrames(self, container):
        bottom_frame = ttk.Frame(container, padding=10)
        bottom_frame.grid(row=3, column=0, sticky="nsew")
        bottom_frame.rowconfigure(0, weight=1)
        bottom_frame.columnconfigure(0, weight=1)
        bottom_frame.columnconfigure(1, weight=1)
        
        self.sub_bottom_frame_1 = ttk.Frame(bottom_frame)
        self.sub_bottom_frame_1.grid(row=0, column=0, sticky="nsew")
        self.sub_bottom_frame_1.rowconfigure(0, weight=1)
        
        self.sub_bottom_frame_2 = ttk.Frame(bottom_frame)
        self.sub_bottom_frame_2.grid(row=0, column=1, sticky="nsew")
        self.sub_bottom_frame_2.rowconfigure(0, weight=1)
        
        
        
    # Define Paginate Buttons, Delete and Edit Records Button
    def definePaginateButtons(
        self, refreshedTableMethod, searchedRefreshTableMethod,
        first_functionality_switch="edit", first_functionality_button_text="Edit Record", firstFunctionalityMethod=None,
        second_functionality_switch="delete", second_functionality_button_text="Delete Record", secondFunctionalityMethod=None, 
        third_functionality_switch="download", third_functionality_button_text=None, thirdFunctionalityMethod=None, 
        is_zero_button_functionality_needed=False, is_single_button_functionality_needed=False, 
        is_triple_button_functionality_needed=False, is_pagination_needed=True, is_product_table=0, is_dashboard_table=0
        ):
        
        # Combobox for toggling no of records in table
        self.new_limit = tk.StringVar()
        t_lis = [5, 10, 15, 25, 50, 100]
        self.toggle_records_combobox = ttk.Combobox(
            self.sub_bottom_frame_1, 
            textvariable=self.new_limit, 
            values=t_lis, state="readonly", 
            width=5, style="TreeviewLimit.TCombobox", 
            justify="center", 
            font=("TkDefaultFont", 10, "bold")
            )
        self.toggle_records_combobox.current(t_lis.index(self.limit))
         
        # Setting up separate mechanism for Product Table especially
        if is_product_table == 1:
            self.is_product_table = 1
            # Command for Delete Button
            commandForSecondFunctionalityButton = lambda: self.commandSecondFunctionality(
                second_functionality_switch, 
                searchedRefreshTableMethod, 
                secondFunctionalityMethod
                )
            # Command for Delete Button
            commandForFirstFunctionalityButton = lambda: self.commandFirstFunctionality(
                first_functionality_switch, 
                firstFunctionalityMethod, 
                searchedRefreshTableMethod
                )
        else:
            commandForSecondFunctionalityButton = lambda: self.commandSecondFunctionality(
                second_functionality_switch, 
                lambda: refreshedTableMethod(), 
                secondFunctionalityMethod
                )
            commandForFirstFunctionalityButton = lambda: self.commandFirstFunctionality(
                first_functionality_switch, 
                lambda: firstFunctionalityMethod()
                )

        # When no button needed
        if is_zero_button_functionality_needed:
            pass
        else:
            # If Treeview don't need Edit and Delete functionality,  while it need something different
            if is_single_button_functionality_needed:
                self.second_functionality_button = ttk.Button(
                    self.sub_bottom_frame_1, 
                    text=second_functionality_button_text, 
                    command=lambda: commandForSecondFunctionalityButton(), 
                    style="TreeviewPaginateButtons.TButton"
                    )
                self.second_functionality_button.pack(side="left", padx=(30,30))
            else:
                # Buttons Definition Below Tables

                self.first_functionality_button = ttk.Button(
                    self.sub_bottom_frame_1, 
                    text=first_functionality_button_text, 
                    command=lambda: commandForFirstFunctionalityButton(), 
                    style="TreeviewPaginateButtons.TButton"
                    )
                self.first_functionality_button.pack(side="left", padx=(30,30))
                
                self.second_functionality_button = ttk.Button(
                    self.sub_bottom_frame_1, 
                    text=second_functionality_button_text, 
                    command=lambda: commandForSecondFunctionalityButton(), 
                    style="TreeviewPaginateButtons.TButton"
                    )
                self.second_functionality_button.pack(side="left", padx=(30,30))

            # If three button needed
            if is_triple_button_functionality_needed:
                self.third_functionality_button = ttk.Button(
                    self.sub_bottom_frame_1,
                    text=third_functionality_button_text, 
                    command=lambda: self.commandThirdFunctionality(
                        third_functionality_switch, 
                        lambda: thirdFunctionalityMethod(),
                        lambda: refreshedTableMethod()
                        ), 
                    style="TreeviewPaginateButtons.TButton"
                    )
                self.third_functionality_button.pack(side="left", padx=(30,30))
        
        # Setting up separate mechanism for Product Table especially
        if is_product_table == 1:
            self.is_product_table = 1
            # Command for Next Button
            commandForNextButton = lambda: self.commandNextRecord(
                lambda: refreshedTableMethod(), 
                searchedRefreshTableMethod
                )
            # Command for Previous Button
            commandForPreviousButton = lambda: self.commandPreviousRecord(
                lambda: refreshedTableMethod(), 
                searchedRefreshTableMethod
                )
            # Command for Changing Limit of treeview
            commandChangeLimitMethod = lambda: self.changeLimitOfRecords(t_lis, searchedRefreshTableMethod)
        else:
            commandForNextButton = lambda: self.commandNextRecord(
                lambda: refreshedTableMethod(), 
                lambda: searchedRefreshTableMethod()
                )
            commandForPreviousButton = lambda: self.commandPreviousRecord(
                lambda: refreshedTableMethod(), 
                lambda: searchedRefreshTableMethod()
                )
            commandChangeLimitMethod = lambda: self.changeLimitOfRecords(
                t_lis, lambda: 
                refreshedTableMethod()
                )   
          
        # Event Binding for Record Limit Combobox in bottom-left corner 
        self.toggle_records_combobox.bind("<<ComboboxSelected>>", lambda e: commandChangeLimitMethod()) 
        

        # Pagination Buttons
        # Next Button Instance
        self.next_button = ttk.Button(
            self.sub_bottom_frame_2, 
            text="Next Record", 
            command=lambda: commandForNextButton(),
            style="TreeviewPaginateButtons.TButton"
            )
        # Previous Button Instance
        self.previous_button = ttk.Button(
            self.sub_bottom_frame_2,
             text="Previous Record", 
             command=lambda: commandForPreviousButton(), 
             style="TreeviewPaginateButtons.TButton"
             )
         # Total Record Count Label Instance   
        self.lb = ttk.Label(self.sub_bottom_frame_2, font=("TkDefaultFont", 10, "bold"))

        if not is_pagination_needed:
            pass
        else:
            self.next_button.pack(side="right", padx=(30,30))
            self.previous_button.pack(side="right", padx=(30,30))
            self.lb.pack(side="left",  pady=(12,12))
            self.toggle_records_combobox.pack(side="left", padx=(30,30), anchor="center")
            
        
    
    # Change limit of records in a table
    def changeLimitOfRecords(self, t_lis, refreshedTableMethod):
        self.limit = int(t_lis[self.toggle_records_combobox.current()])
        self.offset = 0
        # Different Mechanism for Product Table
        if self.is_product_table == 1:
            self.insertDataInTree(
                tableRowFetchAndRenderMethod=lambda : refreshedTableMethod(
                    lambda: self.queryFetchPaginatedProducts(
                        self.offset,
                        self.limit,
                        self.radio_value.get(),
                        self.category_id_selected,
                        self.sub_category_id_selected,
                        self.search_data.get()
                        )
                    )
                )
        else:
            self.insertDataInTree(tableRowFetchAndRenderMethod=lambda : refreshedTableMethod())
        


    # First Button different mechanisms
    def commandFirstFunctionality(self, first_functionality_switch, firstFunctionalityMethod=None, refreshTableMethod=None):
        match first_functionality_switch:
            case "edit":
                count = len(self.tree.selection())
                # If nothing selected
                if count == 0:
                    pass
                else:
                    # Separate Mechanism for Product Table
                    if self.is_product_table == 1:
                        firstFunctionalityMethod(
                        self,
                        self.mysql,
                        self.current_user,
                        self.tree.item(self.tree.focus())["values"][1],
                        lambda: self.insertDataInTree(
                            tableRowFetchAndRenderMethod=lambda: refreshTableMethod(
                                lambda: self.queryFetchPaginatedProducts(
                                    self.offset,
                                    self.limit,
                                    self.radio_value.get(),
                                    self.category_id_selected,
                                    self.sub_category_id_selected,
                                    self.search_data.get()
                                    )
                                )
                            )
                        )
                    else:
                        firstFunctionalityMethod()
            case "download":
                if not (len(self.tree.get_children()) == 0):
                    firstFunctionalityMethod()
        


    # Second Button different mechanisms
    def commandSecondFunctionality(self, second_functionality_switch, refreshedTableMethod, secondFunctionalityMethod):
        count = len(self.tree.selection())
        # Switch Statement in Python
        match second_functionality_switch:
            # Generally to delete selected element
            case "delete":
                s1 = f"Are you sure to delete selected record permanently ?"
                s2 = f"Are you sure to delete {count} records permanently ?"
                # If nothing selected
                if count == 0:
                    pass
                else:
                    Modal(
                        container = self,
                        modal_message = s1 if count == 1 else s2, 
                        confirmationMethod = lambda : self.deleteRecordFromTree(
                            secondFunctionalityMethod, 
                            lambda: self.insertDataInTree(tableRowFetchAndRenderMethod=lambda : refreshedTableMethod())
                            )
                        )
            # Change Supplier Status Active/Inactive
            case "toggle_supplier_status":
                # Toggle Active/Inactive Status of Supplier
                # If nothing selected
                if count == 0:
                    pass
                else:
                    data = self.selectTreeRow()
                    Modal(
                        container = self,
                        modal_message =f"Are you sure to change active/inactive status of supplier {data[0][2]}", 
                        confirmationMethod = lambda : [
                            secondFunctionalityMethod(data[0][1]),
                            self.insertDataInTree(tableRowFetchAndRenderMethod=lambda : refreshedTableMethod())
                            ]
                        )
            # Delete Product not from database but mark it generally deleted
            case "toggle_product_delete_status":
                # If nothing selected
                if count == 0:
                    pass
                else:
                    data = self.selectTreeRow()
                    if self.second_functionality_button["text"] == "Delete":
                        question = f"Delete the selected product, you can restore it back again? (Product Id = {data[0][1]})"
                    else:
                        question = f"Restore the selected product back to inventory again? (Product Id = {data[0][1]})"
                    Modal(
                        container = self,
                        modal_message = question, 
                        confirmationMethod = lambda : [
                            secondFunctionalityMethod(data[0][1]),
                            self.insertDataInTree(
                                tableRowFetchAndRenderMethod=lambda : refreshedTableMethod(
                                    lambda: self.queryFetchPaginatedProducts(
                                        self.offset,
                                        self.limit,
                                        self.radio_value.get(),
                                        self.category_id_selected,
                                        self.sub_category_id_selected,
                                        self.search_data.get()
                                        )
                                    )
                                )
                            ]
                        )
            # # To add product to invoice
            case "add_record":
                self.container.destroy()
            # # To add supplier to invoice
            # To remove product from invoice      
            case "remove_product_from_invoice":
                secondFunctionalityMethod()
            case "add_record_id":
                if len(self.tree.focus()) > 0:
                    self.selected_id = self.tree.item(self.tree.focus())["values"][1]
                    self.container.destroy()
            case "call_passed_method_directly":
                if len(self.tree.focus()) > 0:
                    # Call the class or method passed as parameter
                    secondFunctionalityMethod()
            case "download":
                if not (len(self.tree.get_children()) == 0):
                    secondFunctionalityMethod()
            case _:
                pass
       


    # Third Button different mechanisms
    def commandThirdFunctionality(self, third_functionality_switch, thirdFunctionalityMethod=None, refreshTableMethod=None):
        match third_functionality_switch:
            case "call_passed_method_directly":
                if len(self.tree.focus()) > 0:
                    # Call the class for change order status passed as parameter
                    thirdFunctionalityMethod()
            case "download":
                if not (len(self.tree.get_children()) == 0):
                    thirdFunctionalityMethod()

       

    # Single Record Popup       
    def commandSingleRecord(self, RecordClass, refreshTableMethod=None):
        count = len(self.tree.selection())
        # If nothing selected
        if count == 0:
            pass
        else:
            # Separate Mechanism for Product Table
            if self.is_product_table == 1:
                RecordClass(
                    self,
                    self.mysql,
                    self.current_user,
                    self.tree.item(self.tree.focus())["values"][1],
                    lambda: self.insertDataInTree(
                        tableRowFetchAndRenderMethod=lambda: refreshTableMethod(
                            lambda: self.queryFetchPaginatedProducts(
                                self.offset,
                                self.limit,
                                self.radio_value.get(),
                                self.category_id_selected,
                                self.sub_category_id_selected,
                                self.search_data.get()
                                )
                            )
                        )
                    )
            else:
                RecordClass()
              
              
              
    # Move to Next Records            
    def commandNextRecord(self, refreshedTableMethod, searchedRefreshTableMethod):
        self.offset = self.offset + self.limit
        # Mechanism is different for Product Table Search System
        if self.is_product_table == 1:
            self.insertDataInTree(
                tableRowFetchAndRenderMethod=lambda : searchedRefreshTableMethod(
                    lambda: self.queryFetchPaginatedProducts(
                        self.offset,
                        self.limit,
                        self.radio_value.get(),
                        self.category_id_selected,
                        self.sub_category_id_selected,
                        self.search_data.get()
                        )
                    )
                )
        # For All Other Tables
        elif self.search_data.get() == "":
            self.insertDataInTree(tableRowFetchAndRenderMethod=lambda : refreshedTableMethod())
        else:
            self.insertDataInTree(tableRowFetchAndRenderMethod=lambda : searchedRefreshTableMethod())

    
    
    # Move back to Previous Records           
    def commandPreviousRecord(self, refreshedTableMethod, searchedRefreshTableMethod):
        self.offset = self.offset - self.limit
        # Mechanism is different for Product Table Search System
        if self.is_product_table == 1:
            self.insertDataInTree(
                tableRowFetchAndRenderMethod=lambda : searchedRefreshTableMethod(
                    lambda: self.queryFetchPaginatedProducts(
                        self.offset,
                        self.limit,
                        self.radio_value.get(),
                        self.category_id_selected,
                        self.sub_category_id_selected,
                        self.search_data.get()
                        )
                    )
                )
        # For All Other Tables
        elif self.search_data.get() == "":
            self.insertDataInTree(tableRowFetchAndRenderMethod=lambda : refreshedTableMethod())
        else:
            self.insertDataInTree(tableRowFetchAndRenderMethod=lambda : searchedRefreshTableMethod())
        
        
        
    ##############################################
    #######       Deletion of Records       ######
    ############################################## 

    # Delete whole tree
    def deleteWholeTree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
            
            
    # Delete Particular Records from Tree    
    def deleteRecordFromTree(self, queryDeleteMethod, refreshTableMethod):
        selectedRecords = self.selectTreeRow()
        if len(selectedRecords) > 1:
            for row in selectedRecords:
                queryDeleteMethod(row[1])      
        else:
            queryDeleteMethod(selectedRecords[0][1])
        self.search_data.set("")
        refreshTableMethod()
        
        
        
    ##############################################
    #########           Others           #########
    ############################################## 
    
    # Defining Horizontal ScrollBar and its configuration
    def renderScrollbar(self):
        # Horizontal Scrollbar
        self.horizontal_srollbar = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.horizontal_srollbar.grid(row=1, column=0, sticky="sew")
        self.tree.configure(xscrollcommand=self.horizontal_srollbar.set)
        # Vertical Scrollbar
        self.vertical_scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.vertical_scrollbar.grid(row=1, column=0, sticky="nse")
        self.tree.configure(yscrollcommand=self.vertical_scrollbar.set)
        
        
        
    # From TreeView Tables this method return selected rows values as tuples inside list
    def selectTreeRow(self):
        # tree_instance.selection() = Return Unique Id for selected row in tree in form of tuple   ->   ("I001", "I002")
        # tree_instance.item() = Return Dictionary with row value and options below is example for that unique id
        #            {'text': '', 'image': '', 'values': [3, 'Saiful', 'Khan'], 'open': 0, 'tags': ''}
        # return tuple(tree_instance.item(tree_instance.focus())["values"])   ->     [(1, "Data1"), (2, "Data2")] 
        ne_l = list()
        for n in range(len(self.tree.selection())):
            ne_l.append(tuple(tuple(self.tree.item(self.tree.selection()[n])["values"])))
        return ne_l
    
    
    
    # Defining Key and Mouse Bindings on Table  
    def definingEventBindings(
        self, refreshTableMethod, RecordPopupClass, secondFunctionalityMethod=None, 
        second_functionality_switch="delete", is_product_table=0
        ):
        # If the treeview don't need deletion feature
        if type(secondFunctionalityMethod) == None.__class__:
            pass
        else:
            
            # If the treeview is for product table
            if is_product_table == 1:
                commandForDeleting = lambda: self.commandSecondFunctionality(
                    second_functionality_switch, 
                    refreshTableMethod, 
                    secondFunctionalityMethod
                    )
                commandForRecordPopUpClass = lambda: self.commandSingleRecord(RecordPopupClass, refreshTableMethod)
            else:
                commandForDeleting = lambda: self.commandSecondFunctionality(
                    second_functionality_switch, 
                    lambda: refreshTableMethod(), 
                    secondFunctionalityMethod
                    )
                commandForRecordPopUpClass = lambda: self.commandSingleRecord(lambda: RecordPopupClass())
            # Delete Button Press 
            self.tree.bind("<Delete>", lambda e: commandForDeleting())
            
        # If the treeview is for product table
        if is_product_table == 1:
            commandForRecordPopUpClass = lambda: self.commandSingleRecord(RecordPopupClass, refreshTableMethod)
        else:
            commandForRecordPopUpClass = lambda: self.commandSingleRecord(lambda: RecordPopupClass())
        # Double Click for Edit Pop-Up 
        self.tree.bind("<Double-Button-1>", lambda e: commandForRecordPopUpClass())
        
        
        
    # Row Text Formatting
    def morphText(self, data, char_limit=22):
        """Take data of field from Tree Row and format it for better display

        Args:
            data (str): should be string

        Returns:
            str: _formatted string
        """
        s = ""
        
        if data == None:
            pass
        else:            
            if len(data) > char_limit:
                s = data[0:char_limit-4] + "...." 
            else:
                s = data
        return s