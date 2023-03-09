import tkinter as tk
from app.base import Base
from app.main.supplier_components.show_supplier import ShowSupplier
from CONSTANT.index import SUPPLIER_TABLE_NAME, SUPPLIER_NAME, PATH_TO_IMAGES, FILE_APP_LOGO, FILE_APP_DEFAULT_LOGO
from os import path

class ShowSupplierForInvoice(tk.Toplevel, Base):
    def __init__(self, container, mysql, user, is_invoice_page=True):
        tk.Toplevel.__init__(self, container)
        Base.__init__(self, mysql, user)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        try:
            self.image = path.join(PATH_TO_IMAGES, FILE_APP_LOGO)
            self.iconbitmap(self.image)
        except Exception:
            self.image = path.join(PATH_TO_IMAGES, FILE_APP_DEFAULT_LOGO)
            self.iconbitmap(self.image)

        # restrict app while this pop up is open
        self.grab_set()
        self.state('zoomed') # Open App fullscreen in maximize window  

        self.show_supplier_frame = ShowSupplier(self, mysql, user, is_invoice_page)
        self.show_supplier_frame.grid(row=0, column=0, sticky="nsew")

        # Define Buttons below Table
        self.show_supplier_frame.definePaginateButtons(
            refreshedTableMethod=lambda: self.show_supplier_frame.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.queryFetchPaginatedSuppliers(
                    self.show_supplier_frame.offset,
                    self.show_supplier_frame.limit,
                    for_invoice=True
                    )
                ),
            searchedRefreshTableMethod=lambda: self.show_supplier_frame.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.queryFetchSearchedData(
                    offset=self.show_supplier_frame.offset, 
                    limit=self.show_supplier_frame.limit,
                    query_data=self.show_supplier_frame.search_data.get(),
                    selectable_columns_from_table_query=self.saved_query_supplier,
                    table_name=SUPPLIER_TABLE_NAME,
                    sort_column=SUPPLIER_NAME
                    )
                ),
            secondFunctionalityMethod=self.queryToggleSupplierStatus,
            second_functionality_button_text="Add Selected Supplier",
            second_functionality_switch="add_record_id",
            is_single_button_functionality_needed=True
            )
        
        # Insert Data
        self.show_supplier_frame.insertDataInTree(
            tableRowFetchAndRenderMethod=lambda: self.show_supplier_frame.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.queryFetchPaginatedSuppliers(
                    offset=self.show_supplier_frame.offset,
                    limit=self.show_supplier_frame.limit,
                    for_invoice=True
                    )
                )
            )