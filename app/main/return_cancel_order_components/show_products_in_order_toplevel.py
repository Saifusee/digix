import tkinter as tk
from app.base import Base
from app.main.return_cancel_order_components.show_products_in_order_frame import ShowProductsInOrderFrame
from os import path
from CONSTANT.application_setting_constants import PATH_TO_IMAGES, FILE_APP_LOGO, FILE_APP_DEFAULT_LOGO

class ShowProductsInOrderToplevel(tk.Toplevel, Base):
    def __init__(self, container, mysql, user, order_id, type):
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
        self.grab_set()
        self.state('zoomed') # Open App fullscreen in maximize window  
        self.show_product_for_invoice_instance =  ShowProductsInOrderFrame(self, self.mysql, self.current_user, order_id=order_id, type=type)
        self.show_product_for_invoice_instance.grid(row=0, column=0, sticky="nsew")