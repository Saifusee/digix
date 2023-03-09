import tkinter as tk
from app.base import Base
from app.main.product_components.show_product import ShowProduct
from app.main.order_components.s_o_quantity_entry import SalesOrderQuantityEntry
from app.main.order_components.p_o_quantity_and_price_entry import PurchaseOrderQuantityAndPriceEntry
from CONSTANT.application_setting_constants import PATH_TO_IMAGES, FILE_APP_LOGO, FILE_APP_DEFAULT_LOGO
from os import path

class ShowProductForInvoice(tk.Toplevel, Base):
    def __init__(self, container, mysql, user, is_invoice_page=True, type="SalesOrder"):
        tk.Toplevel.__init__(self, container)
        Base.__init__(self, mysql, user)
        try:
            self.image = path.join(PATH_TO_IMAGES, FILE_APP_LOGO)
            self.iconbitmap(self.image)
        except Exception:
            self.image = path.join(PATH_TO_IMAGES, FILE_APP_DEFAULT_LOGO)
            self.iconbitmap(self.image)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.type = type
        self.quantity = ""
        self.price = ""
        self.quantity_popup_instance = None
        self.quantity_and_price_popup_instance = None

        
        self.grab_set()
        self.state('zoomed') # Open App fullscreen in maximize window  
        self.show_product_frame = ShowProduct(self, mysql, user, is_invoice_page)
        self.show_product_frame.is_product_table_for_invoice_product_selection = 1
        self.show_product_frame.createTreeAndConfiguration(type=self.type, product_treeview_for_invoice_modification=True)
        self.show_product_frame.renderScrollbar()
        
        
        
        self.show_product_frame.tree.bind("<Double-Button-1>", self.selectInvoiceRow)
        self.show_product_frame.definePaginateButtons(
            refreshedTableMethod=lambda: self.show_product_frame.definingRowsOfParticularTree(type=self.type, 
                dataFetchingMethod=lambda: self.queryFetchPaginatedProducts(
                    self.show_product_frame.offset,
                    self.show_product_frame.limit
                    )
                ),
            searchedRefreshTableMethod=self.show_product_frame.definingRowsOfParticularTree,
            firstFunctionalityMethod=None,
            secondFunctionalityMethod=self.queryToggleProductDeleteStatus,
            second_functionality_button_text="Add Selected Product",
            second_functionality_switch="add_record",
            is_product_table=1,
            is_single_button_functionality_needed=True,
            )

        # Define Other Search Options such as check box and combobox above Table
        self.show_product_frame.defineParticularSearchesWidgets(self.show_product_frame.above_frame)
    
        # Fetch Categories and Sub Categories for Products
        self.show_product_frame.fetchCategoriesForProduct()
        
        # Insert Data
        self.show_product_frame.insertDataInTree(
            tableRowFetchAndRenderMethod=lambda: self.show_product_frame.definingRowsOfParticularTree(type=self.type, 
                dataFetchingMethod=lambda: self.queryFetchPaginatedProducts(offset=self.show_product_frame.offset, limit=self.show_product_frame.limit))
            )

            
        self.show_product_frame.grid(row=0, column=0, sticky="nsew")
        # When this toplevel destroyed Destroy event in parent class catch selected product id list as follow:
        # toplevel_treeview_instance.show_product_frame.selected_products_id_list




    # Select Invoice
    def selectInvoiceRow(self, event):

        if len(self.show_product_frame.tree.selection()) >= 1:
            for selected_row in self.show_product_frame.tree.selection():
                selected_row_instance = self.show_product_frame.tree.item(selected_row)
                
                if self.type == "SalesOrder":
                    self.quantity_popup_instance = SalesOrderQuantityEntry(
                        self,
                        selected_row_instance["values"],
                        selected_row_instance["tags"][0]
                        )
                    self.quantity_popup_instance.bind("<Destroy>", lambda event: self.assignQuantity(event, selected_row))
                elif self.type == "PurchaseOrder":
                    self.quantity_and_price_popup_instance = PurchaseOrderQuantityAndPriceEntry(
                        self,
                        selected_row_instance["values"],
                        selected_row_instance["tags"][0]
                        )
                    self.quantity_and_price_popup_instance.bind("<Destroy>", lambda event: self.assignQuantity(event, selected_row))




    def assignQuantity(self, event, selected_row):
        # Changing Tag to show green color row
        selected_product_row_instance = self.show_product_frame.tree.item(selected_row)
        selected_product = selected_product_row_instance["values"]

        # If Sales Order Quantity Pop Up Causes Event
        if event.widget == self.quantity_popup_instance:

            self.quantity = int(self.quantity_popup_instance.quantity.get().strip())

            # If selected quantity is validated then true    
            if self.quantity_popup_instance.acceptable_quantity:
                
                selected_product[4] = f"x {self.quantity}"
                # Updating selected quantity in treeview
                self.show_product_frame.tree.item(selected_row, values=tuple(selected_product))                
                # If already product is selected an now deselecting
                if selected_product_row_instance["tags"][0] == "selected_for_invoice" and self.quantity == 0:
                    self.show_product_frame.tree.item(selected_row, tags=self.show_product_frame.mapped_tag_data[selected_product[1]])

                    # Finding index of deselected product in selected product list
                    p_id = selected_product[1]
                    index = None
                    for element in self.show_product_frame.selected_products_for_invoice:
                        if element[1] == p_id:
                            index = self.show_product_frame.selected_products_for_invoice.index(element)
                            break

                    # Removing product, selected for deselection
                    self.show_product_frame.selected_products_for_invoice.pop(index)
                    self.show_product_frame.selected_products_id_for_invoice.pop(index)
                    # Deleteing tag_value of row which we no longer needed for selection
                    del self.show_product_frame.mapped_tag_data[selected_product[1]]

                # When Product is selected
                if not (selected_product_row_instance["tags"][0] == "selected_for_invoice") and not (self.quantity == 0):
                    # ProductID = Key, TagValue = Value of dictionary, where tagvalue is previous tag value of row mapped with respective id
                    self.show_product_frame.mapped_tag_data[selected_product[1]] = selected_product_row_instance["tags"][0]
                    # Adding new tag to selected row
                    self.show_product_frame.tree.item(selected_row, tags='selected_for_invoice')
                    # Appending selected product and its respective id
                    self.show_product_frame.selected_products_for_invoice.append(selected_product)
                    self.show_product_frame.selected_products_id_for_invoice.append(selected_product[1])
                
                # Deselecting or losing focus from row after double clicking it
                for row_instance_item in self.show_product_frame.tree.selection():
                    self.show_product_frame.tree.selection_remove(row_instance_item)


        # If Purchase Order Quantity Pop Up Causes Event
        if event.widget == self.quantity_and_price_popup_instance:

            self.quantity = int(self.quantity_and_price_popup_instance.quantity.get().strip())
            self.price = self.quantity_and_price_popup_instance.price.get().strip()
            self.price = round(float(self.price), 2) if len(self.price) > 0 else self.price
            # We can do above 2 line in 1 but float conversion on empty string gives error

            # If selected quantity is validated then true    
            if self.quantity_and_price_popup_instance.acceptable_input:
                
                selected_product[5] = f"x {self.quantity}"
                selected_product[4] = self.formatINR(self.price)
                # Updating selected quantity in treeview
                self.show_product_frame.tree.item(selected_row, values=tuple(selected_product))                
                # If already product is selected an now deselecting
                if selected_product_row_instance["tags"][0] == "selected_for_invoice" and self.quantity == 0:
                    self.show_product_frame.tree.item(selected_row, tags=self.show_product_frame.mapped_tag_data[selected_product[1]])

                    # Finding index of deselected product in selected product list
                    p_id = selected_product[1]
                    index = None
                    for element in self.show_product_frame.selected_products_for_invoice:
                        if element[1] == p_id:
                            index = self.show_product_frame.selected_products_for_invoice.index(element)
                            break

                    # Removing product, selected for deselection
                    self.show_product_frame.selected_products_for_invoice.pop(index)
                    self.show_product_frame.selected_products_id_for_invoice.pop(index)
                    # Deleteing tag_value of row which we no longer needed for selection
                    del self.show_product_frame.mapped_tag_data[selected_product[1]]

                # When Product is selected
                if not (selected_product_row_instance["tags"][0] == "selected_for_invoice") and not (self.quantity == 0):
                    # ProductID = Key, TagValue = Value of dictionary, where tagvalue is previous tag value of row mapped with respective id
                    self.show_product_frame.mapped_tag_data[selected_product[1]] = selected_product_row_instance["tags"][0]
                    # Adding new tag to selected row
                    self.show_product_frame.tree.item(selected_row, tags='selected_for_invoice')
                    # Appending selected product and its respective id
                    self.show_product_frame.selected_products_for_invoice.append(selected_product)
                    self.show_product_frame.selected_products_id_for_invoice.append(selected_product[1])
                
                # Deselecting or losing focus from row after double clicking it
                for row_instance_item in self.show_product_frame.tree.selection():
                    self.show_product_frame.tree.selection_remove(row_instance_item)



        
