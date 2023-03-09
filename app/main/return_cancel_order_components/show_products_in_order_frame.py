import tkinter as tk
from tkinter import ttk
from CONSTANT.index import *
from app.main.tree_essentials import TreeEssentials
from app.main.return_cancel_order_components.return_cancel_quantity_entry import ReturnCancelQuantityEntry

class ShowProductsInOrderFrame(tk.Canvas, TreeEssentials):
    
    def __init__(self, container, mysql, user, order_id, type):
        
        self.offset = 0
        self.limit = 15
        self.order_type = type
        self.order_id = order_id
        self.fetchQueryMethod = ""
        self.selected_data = list()
        self.mapped_tag_data = dict()
        self.container = container

        if self.order_type == "SalesOrder":
            self.fetchQueryMethod = self.queryFetchPaginatedSalesOrderProduct
        elif self.order_type == "PurchaseOrder":
            self.fetchQueryMethod = self.queryFetchPaginatedPurchaseOrderProduct
        
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
            page_heading="Products in Invoice:"
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
                dataFetchingMethod=lambda: self.fetchQueryMethod(
                    self.offset,
                    self.limit,
                    self.order_id
                    )
                ),
            searchedRefreshTableMethod=lambda: self.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.fetchQueryMethod(
                    self.offset,
                    self.limit,
                    self.order_id
                    )
                ),
            second_functionality_button_text="Confirm",
            second_functionality_switch="add_record",
            is_single_button_functionality_needed=True
            )

        # Bind on Double Click
        self.tree.bind("<Double-Button-1>", self.setValues)
        
        # Insert Data
        self.insertDataInTree(
            tableRowFetchAndRenderMethod=lambda: self.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.fetchQueryMethod(self.offset, self.limit, self.order_id))
            )



    # Set Cancellable and Returnable Quantuty
    def setValues(self, event):
        count = len(self.tree.selection())
        if count == 0:
            pass
        else:
            row_id = self.tree.focus()
            selected_instance = self.tree.item(row_id)
            quantity_entry = ReturnCancelQuantityEntry(self, selected_instance["values"], selected_instance["tags"][0])
            quantity_entry.bind("<Destroy>", lambda e: self.afterQuantityEntry(e, quantity_entry, row_id))



    # After Quantites selected
    def afterQuantityEntry(self, event, toplevel_instance, selcted_row_id):

        if event.widget == toplevel_instance:
            selected_row = self.tree.item(selcted_row_id)

            # Getting all input values
            cancelled_quantity = toplevel_instance.marked_cancelled_quantity.get()
            returned_quantity = toplevel_instance.marked_returned_quantity.get()
            refunded_amount = toplevel_instance.refund_amount.get()
            reason = toplevel_instance.reason

            # Storing it to list to passed to parent widget
            mapped_data = dict()
            mapped_data["order_product_id"] = selected_row["values"][1]
            mapped_data["order_id"] = self.order_id
            mapped_data["product_id"] = selected_row["values"][2]
            mapped_data["product_name"] = selected_row["values"][3]
            mapped_data["already_available_quantity_in_order"] = selected_row["values"][8][2:]
            mapped_data["cancelled_quantity"] = cancelled_quantity
            mapped_data["returned_quantity"] = returned_quantity
            mapped_data["already_cancelled_quantity"] = selected_row["values"][10][2:]
            mapped_data["already_returned_quantity"] = selected_row["values"][11][2:]
            mapped_data["already_refunded_amount"] = self.formatReverseINR(selected_row["values"][12])
            mapped_data["refunded_amount"] = refunded_amount
            mapped_data["reason"] = reason

            # Refreshing GUI after Quantities selection
            val = selected_row["values"]
            val[4] = f"x {cancelled_quantity}"
            val[5] = f"x {returned_quantity}"
            val[6] = self.formatINR(refunded_amount)
            if toplevel_instance.acceptable_quantity:
                if int(returned_quantity) == 0 and int(cancelled_quantity) == 0 and selected_row["tags"][0] == "selected":
                    self.tree.item(selcted_row_id, values=val, tags=self.mapped_tag_data[selected_row["values"][1]])
                    del self.mapped_tag_data[selected_row["values"][1]]
                    self.selected_data.remove(mapped_data)
                elif not (returned_quantity == 0) or not (cancelled_quantity == 0):
                    # If the record is selected again while show_product_in_order_toplevel is active with different values then delete the previous one
                    if len(self.selected_data) > 0:
                        for old_selected_data in self.selected_data:
                            if old_selected_data["order_product_id"] == mapped_data["order_product_id"]:
                                self.selected_data.remove(old_selected_data)
                    self.mapped_tag_data[selected_row["values"][1]] = selected_row["tags"][0]
                    self.tree.item(selcted_row_id, values=val, tags="selected")
                    self.selected_data.append(mapped_data)

            # Deselecting or losing focus from row after double clicking it
            self.tree.selection_remove(selcted_row_id)

        

        
    # Create Rows of Particular Tree with data from database   
    def definingRowsOfParticularTree(self, dataFetchingMethod):
        data = dataFetchingMethod()
        # Inserting Data In Tree
        if len(data) >= 1:
            count = 0
            s_no_count = self.offset
            for i in range(len(data)):
                
                product_name = self.morphText(data[i][PRODUCT_NAME])  
                zero_quantity = "x 0"
                cancel_quantity = f"x {data[i][CANCELLED_QUANTITY]}"
                return_quantity = f"x {data[i][RETURNED_QUANTITY]}"

                if self.order_type == "SalesOrder":
                    val = (s_no_count + 1, data[i][S_O_P_ID], data[i][PRODUCT_ID], product_name, zero_quantity, zero_quantity,
                      self.formatINR(0), self.formatINR(data[i][S_O_P_PRODUCT_PRICE]), f"x {data[i][S_O_P_PRODUCT_QUANTITY]}",
                     self.formatINR(data[i][S_O_P_PRODUCT_TOTAL_AMOUNT]), cancel_quantity, return_quantity, self.formatINR(data[i][REFUNDED_AMOUNT]))
                elif self.order_type == "PurchaseOrder":
                    val = (s_no_count + 1, data[i][P_O_P_ID], data[i][PRODUCT_ID], product_name, zero_quantity, zero_quantity,
                      self.formatINR(0), self.formatINR(data[i][P_O_P_PRODUCT_PRICE]), f"x {data[i][P_O_P_PRODUCT_QUANTITY]}",
                     self.formatINR(data[i][P_O_P_PRODUCT_TOTAL_AMOUNT]), cancel_quantity, return_quantity, self.formatINR(data[i][REFUNDED_AMOUNT]))
                
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
            self.tree.insert("",
                             tk.END,
                             values=(
                                 "No Recor....",
                                 "No Recor....", 
                                 "No Recor....", 
                                 "No Records Found",
                                 "No Records Found",
                                 "No Records Found", 
                                 "No Records Found", 
                                 "No Records Found",
                                 "No Records Found",
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
        columnTuple = ("s_no", "order_product_id", PRODUCT_ID, PRODUCT_NAME, "cancellable", "returnable",
         "amount_to_be_refunded", PRODUCT_PRICE, PRODUCT_QUANTITY, "product_total_amount",
          CANCELLED_QUANTITY, RETURNED_QUANTITY, REFUNDED_AMOUNT)
        
        self.tree = ttk.Treeview(self, columns=columnTuple, show="headings", selectmode="extended", style="Tree.Treeview")

        # Hiding order_product_id column
        columnTuple = list(columnTuple)
        columnTuple.pop(1)
        tuple(columnTuple)
        self.tree["displaycolumns"] = columnTuple
        
        # Defining Column Name 
        self.tree.heading("s_no", text="S. No.")
        self.tree.heading("order_product_id", text="Order Product Id")
        self.tree.heading(PRODUCT_ID, text="Product Id")
        self.tree.heading(PRODUCT_NAME, text="Product Name")
        self.tree.heading("cancellable", text="Mark for Cancellation")
        self.tree.heading("returnable", text="Mark for Return")
        self.tree.heading("amount_to_be_refunded", text="Mark for Refund (\u20B9)")
        self.tree.heading(CANCELLED_QUANTITY, text="Cancelled Units")
        self.tree.heading(RETURNED_QUANTITY, text="Returned Units")
        self.tree.heading(PRODUCT_PRICE, text="Product Price (\u20B9)")
        self.tree.heading(REFUNDED_AMOUNT, text="Refunded Amount (\u20B9)")
        self.tree.heading(PRODUCT_QUANTITY, text="Quantity in Order")
        self.tree.heading("product_total_amount", text="Product Total (\u20B9)")
        
        
        # Defining Configuration for Columns
        self.tree.column("s_no", anchor="center", stretch=tk.NO, width=100)
        self.tree.column("order_product_id", anchor="center")
        self.tree.column(PRODUCT_ID, anchor="center", stretch=tk.NO, width=100)
        self.tree.column(PRODUCT_NAME, anchor="center")
        self.tree.column("cancellable", anchor="center")
        self.tree.column("returnable", anchor="center")
        self.tree.column("amount_to_be_refunded", anchor="center")
        self.tree.column(CANCELLED_QUANTITY, anchor="center")
        self.tree.column(RETURNED_QUANTITY, anchor="center")
        self.tree.column(PRODUCT_PRICE, anchor="center")
        self.tree.column(REFUNDED_AMOUNT, anchor="center")
        self.tree.column(PRODUCT_QUANTITY, anchor="center")
        self.tree.column("product_total_amount", anchor="center")

        # Giving Striped Rows Style
        self.tree.tag_configure("even_row", background="lightblue")
        self.tree.tag_configure("odd_row", background="white")
        self.tree.tag_configure("selected", background="#ffd6cc")
        
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
                dataFetchingMethod=lambda: self.fetchQueryMethod(self.offset, self.limit, self.order_id)
                )
            )