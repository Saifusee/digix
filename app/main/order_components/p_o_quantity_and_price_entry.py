import tkinter as tk
from tkinter import ttk
from CONSTANT.application_setting_constants import TTK_FRAME_DEFAULT_BG_COLOR, centerTkinterToplevel, PATH_TO_IMAGES, FILE_APP_LOGO, FILE_APP_DEFAULT_LOGO
import re
from os import path
from app.base import Base

class PurchaseOrderQuantityAndPriceEntry(tk.Toplevel):
    def __init__(self, container, product_attributes_tuple, tag_value):
        super().__init__(container)
        
        self.columnconfigure(1, weight=1)
        self.resizable(False, False)
        self.configure(background=TTK_FRAME_DEFAULT_BG_COLOR)
        self.grab_set()
        try:
            self.image = path.join(PATH_TO_IMAGES, FILE_APP_LOGO)
            self.iconbitmap(self.image)
        except Exception:
            self.image = path.join(PATH_TO_IMAGES, FILE_APP_DEFAULT_LOGO)
            self.iconbitmap(self.image)
        centerTkinterToplevel(container, self)
        self.tag_value = tag_value
        self.quantity = tk.StringVar()
        self.price = tk.StringVar()
        self.acceptable_input = False
        self.product_stock_price = Base.formatReverseINR(self, product_attributes_tuple[3]) # Price without rupee prefix
        product_name = product_attributes_tuple[2] # Quantity

        # Title Label
        label_1 = ttk.Label(self, text=f'"{product_name}"',  style="QuantityPopUpLabel.TLabel")
        label_1.grid(row=0, column=0, columnspan=2, sticky="ns", pady=(10), padx=(10))
        
        label_2 = ttk.Label(self, text="Bought Price",  style="QuantityPopUpLabel.TLabel")
        label_2.grid(row=1, column=0, sticky="ns", pady=(10), padx=(10))
        # Price Entry
        self.price_entry = ttk.Entry(self, width=15, textvariable=self.price, font=("TkdefaultFont", 12, "bold"))
        self.price_entry.grid(row=1, column=1, sticky="ns", pady=(10), padx=(10))


        label_3 = ttk.Label(self, text="Bought Quantity",  style="QuantityPopUpLabel.TLabel")
        label_3.grid(row=2, column=0, sticky="ns", pady=(10), padx=(10))
        # Quantity Spinbox
        self.quantity_entry = tk.Spinbox(
            self,
            width=4,
            wrap=True,
            from_=0,
            to=9999,
            textvariable=self.quantity,
            font=("TkDefaultFont", 12, "bold"),
            justify="center"
            )
        self.quantity_entry.invoke("buttonup")
        self.quantity_entry.grid(row=2, column=1, sticky="ns", pady=(10))
        self.quantity_entry.bind("<KeyPress>", lambda e: self.submitQuantity)

        # Submit Button
        button = ttk.Button(self, text="Enter", style="SignButton.TButton", command=self.submitQuantity)
        button.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(10))
        # Error Label
        self.er_label = ttk.Label(self, style="ErrorLoginRegisterLabel.TLabel")



    def submitQuantity(self):
        
        quantity_regex = r"^([0-9]){1,4}$"
        price_regex = r"^[-+]?[0-9]*\.?[0-9]+$"
        if self.price.get() == "" or self.price.get().isspace():
            self.acceptable_input = False
            self.er_label.configure(text=f"Price field cannot be empty.")
            self.er_label.grid(row=4, column=0, columnspan=2, sticky="ns", pady=(10))
        elif (not re.fullmatch(quantity_regex, self.quantity.get().strip())):
            self.acceptable_input = False
            self.er_label.configure(text=f"Invalid Quantity")
            self.er_label.grid(row=4, column=0, columnspan=2, sticky="ns", pady=(10))
        elif (not re.fullmatch(price_regex, self.price.get().strip())):
            self.acceptable_input = False
            self.er_label.configure(text=f"Invalid Price")
            self.er_label.grid(row=4, column=0, columnspan=2, sticky="ns", pady=(10))
        elif int(self.quantity.get()) == 0 and not (self.tag_value == "selected_for_invoice"):
            self.acceptable_input = False
            self.er_label.configure(text=f"Quantity must be greater than 1.")
            self.er_label.grid(row=4, column=0, columnspan=2, sticky="ns", pady=(10))
        else:
            self.acceptable_input = True
            self.destroy()