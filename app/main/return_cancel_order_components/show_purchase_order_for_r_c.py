import tkinter as tk
from app.base import Base
from app.main.order_components.show_purchase_order import ShowPurchaseOrder
from app.main.order_components.record_purchase_order import RecordPurchaseOrder
from os import path
from CONSTANT.application_setting_constants import PATH_TO_IMAGES, FILE_APP_LOGO, FILE_APP_DEFAULT_LOGO

class ShowPurchaseOrderForReturnCancel(tk.Toplevel, Base):
    def __init__(self, container, mysql, user, is_r_c_page=True):
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
        
        self.grab_set()
        self.state('zoomed') # Open App fullscreen in maximize window  
        self.selected_purchase_order_id = ""


        self.show_purchase_order_frame = ShowPurchaseOrder(self, mysql, user, is_r_c_page)

        # Define Buttons below Table
        self.show_purchase_order_frame.definePaginateButtons(
            refreshedTableMethod=lambda: self.show_purchase_order_frame.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.show_purchase_order_frame.queryFetchPaginatedPurchaseOrder(
                    offset=self.show_purchase_order_frame.offset,
                    limit=self.show_purchase_order_frame.limit,
                    from_date=self.show_purchase_order_frame.from_date_data.get(),
                    to_date=self.show_purchase_order_frame.to_date_data.get(),
                    radio_data=self.show_purchase_order_frame.radio_value.get(),
                    query_data=self.show_purchase_order_frame.search_data.get()
                    )
                ),
            searchedRefreshTableMethod=lambda: self.show_purchase_order_frame.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.show_purchase_order_frame.queryFetchPaginatedPurchaseOrder(
                    offset=self.show_purchase_order_frame.offset,
                    limit=self.show_purchase_order_frame.limit,
                    from_date=self.show_purchase_order_frame.from_date_data.get(),
                    to_date=self.show_purchase_order_frame.to_date_data.get(),
                    radio_data=self.show_purchase_order_frame.radio_value.get(),
                    query_data=self.show_purchase_order_frame.search_data.get()
                    )
                ),
            second_functionality_button_text="Select Purchase Order",
            second_functionality_switch="add_record_id",
            is_single_button_functionality_needed=True
            )

        # Define Other Search Options such as check box and combobox above Table
        self.show_purchase_order_frame.defineParticularSearchesWidgets(self.show_purchase_order_frame.above_frame)
        
        # Insert Data
        self.show_purchase_order_frame.insertDataInTree(
            tableRowFetchAndRenderMethod=lambda: self.show_purchase_order_frame.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.show_purchase_order_frame.queryFetchPaginatedPurchaseOrder(
                    offset=self.show_purchase_order_frame.offset,
                    limit=self.show_purchase_order_frame.limit,
                    from_date=self.show_purchase_order_frame.from_date_data.get(),
                    to_date=self.show_purchase_order_frame.to_date_data.get(),
                    radio_data=self.show_purchase_order_frame.radio_value.get(),
                    query_data=self.show_purchase_order_frame.search_data.get()
                    )
                )
            )
        
        # Defining Key and Mouse Bindings on Table  
        self.show_purchase_order_frame.definingEventBindings(
            refreshTableMethod=lambda: self.show_purchase_order_frame.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.show_purchase_order_frame.queryFetchPaginatedPurchaseOrder(
                    offset=self.show_purchase_order_frame.offset,
                    limit=self.show_purchase_order_frame.limit,
                    from_date=self.show_purchase_order_frame.from_date_data.get(),
                    to_date=self.show_purchase_order_frame.to_date_data.get(),
                    radio_data=self.show_purchase_order_frame.radio_value.get(),
                    query_data=self.show_purchase_order_frame.search_data.get()
                    )
                ),
            RecordPopupClass=lambda: RecordPurchaseOrder(
                container=self.show_purchase_order_frame,
                mysql=self.show_purchase_order_frame.mysql,
                user=self.show_purchase_order_frame.current_user,
                purchase_order_id=self.show_purchase_order_frame.tree.item(self.show_purchase_order_frame.tree.focus())["values"][1]
                )
            )



        self.show_purchase_order_frame.grid(row=0, column=0, sticky="nsew")



    # Selecting ID
    def addId(self, event):
        print("Hello")
        if event.widget == self:
            if len(self.tree.item(self.tree.focus())["values"]) > 0:
                self.selected_purchase_order_id = self.tree.item(self.tree.focus())["values"][1]