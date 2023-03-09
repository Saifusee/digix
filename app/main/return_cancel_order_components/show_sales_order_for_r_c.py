import tkinter as tk
from app.base import Base
from app.main.order_components.show_sales_order import ShowSalesOrder
from app.main.order_components.record_sales_order import RecordSalesOrder
from os import path
from CONSTANT.application_setting_constants import PATH_TO_IMAGES, FILE_APP_LOGO, FILE_APP_DEFAULT_LOGO

class ShowSalesOrderForReturnCancel(tk.Toplevel, Base):
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
        
        self.show_sales_order_frame = ShowSalesOrder(self, mysql, user, is_r_c_page)

        # Define Buttons below Table
        self.show_sales_order_frame.definePaginateButtons(
            refreshedTableMethod=lambda: self.show_sales_order_frame.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.show_sales_order_frame.queryFetchPaginatedSalesOrder(
                    offset=self.show_sales_order_frame.offset,
                    limit=self.show_sales_order_frame.limit,
                    from_date=self.show_sales_order_frame.from_date_data.get(),
                    to_date=self.show_sales_order_frame.to_date_data.get(),
                    radio_data=self.show_sales_order_frame.radio_value.get(),
                    query_data=self.show_sales_order_frame.search_data.get()
                    )
                ),
            searchedRefreshTableMethod=lambda: self.show_sales_order_frame.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.show_sales_order_frame.queryFetchPaginatedSalesOrder(
                    offset=self.show_sales_order_frame.offset,
                    limit=self.show_sales_order_frame.limit,
                    from_date=self.show_sales_order_frame.from_date_data.get(),
                    to_date=self.show_sales_order_frame.to_date_data.get(),
                    radio_data=self.show_sales_order_frame.radio_value.get(),
                    query_data=self.show_sales_order_frame.search_data.get()
                    )
                ),
            second_functionality_button_text="Select Sales Order",
            second_functionality_switch="add_record_id",
            is_single_button_functionality_needed=True
            )

        # Define Other Search Options such as check box and combobox above Table
        self.show_sales_order_frame.defineParticularSearchesWidgets(self.show_sales_order_frame.above_frame, is_r_c_page)
        
        # Insert Data
        self.show_sales_order_frame.insertDataInTree(
            tableRowFetchAndRenderMethod=lambda: self.show_sales_order_frame.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.show_sales_order_frame.queryFetchPaginatedSalesOrder(
                    offset=self.show_sales_order_frame.offset,
                    limit=self.show_sales_order_frame.limit,
                    from_date=self.show_sales_order_frame.from_date_data.get(),
                    to_date=self.show_sales_order_frame.to_date_data.get(),
                    radio_data=self.show_sales_order_frame.radio_value.get(),
                    query_data=self.show_sales_order_frame.search_data.get()
                    )
                )
            )
        
        # Defining Key and Mouse Bindings on Table  
        self.show_sales_order_frame.definingEventBindings(
            refreshTableMethod=lambda: self.show_sales_order_frame.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.show_sales_order_frame.queryFetchPaginatedSalesOrder(
                    offset=self.show_sales_order_frame.offset,
                    limit=self.show_sales_order_frame.limit,
                    from_date=self.show_sales_order_frame.from_date_data.get(),
                    to_date=self.show_sales_order_frame.to_date_data.get(),
                    radio_data=self.show_sales_order_frame.radio_value.get(),
                    query_data=self.show_sales_order_frame.search_data.get()
                    )
                ),
            RecordPopupClass=lambda: RecordSalesOrder(
                container=self.show_sales_order_frame,
                mysql=self.show_sales_order_frame.mysql,
                user=self.show_sales_order_frame.current_user,
                sales_order_id=self.show_sales_order_frame.tree.item(self.show_sales_order_frame.tree.focus())["values"][1]
                )
            )


        self.show_sales_order_frame.grid(row=0, column=0, sticky="nsew")