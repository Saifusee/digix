import tkinter as tk
from app.main.order_components.show_sales_order import ShowSalesOrder

class ShowProductWiseSalesOrder(tk.Toplevel):
    def __init__(self, container, mysql, user, product_id, *args, **kwargs):

        super().__init__(container, *args, *kwargs)

        self.state('zoomed') # Open App fullscreen in maximize window  
        self.attributes('-alpha', 0.0) # alpha property defines transparency behaviour, set to 0
        # We making topup invisible so all widget rendered first then it will be visible

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)


        show_sales_order_frame = ShowSalesOrder(self, mysql, user, product_id=product_id)
        show_sales_order_frame.grid(row=0, column=0, sticky="nsew")
        self.after(0, self.attributes, "-alpha", 1.0) # alpha property defines transparency behaviour, set to 1
