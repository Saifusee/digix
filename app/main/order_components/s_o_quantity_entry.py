import tkinter as tk
from tkinter import ttk
from CONSTANT.application_setting_constants import TTK_FRAME_DEFAULT_BG_COLOR, centerTkinterToplevel, PATH_TO_IMAGES, FILE_APP_LOGO, FILE_APP_DEFAULT_LOGO
import re
from os import path

class SalesOrderQuantityEntry(tk.Toplevel):
    def __init__(self, container, product_attributes_tuple, tag_value):
        super().__init__(container)
        self.columnconfigure(0, weight=1)
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
        self.acceptable_quantity = False
        self.in_stock_quantity = int(product_attributes_tuple[5][2:]) # Quantity
        product_name = product_attributes_tuple[2] # Quantity

        # Title Label
        label_1 = ttk.Label(self, text=f'Select Quantity for "{product_name}"',  style="QuantityPopUpLabel.TLabel")
        label_1.grid(row=0, column=0, sticky="ns", pady=(10))
        # Input Spinbox
        self.quantity_entry = tk.Spinbox(
            self,
            width=4,
            wrap=True,
            from_=0,
            to=9999,
            textvariable=self.quantity,
            font=("TkDefaultFont", 15, "bold"),
            justify="center"
            )
        self.quantity_entry.invoke("buttonup")
        self.quantity_entry.grid(row=1, column=0, sticky="ns", pady=(10))
        self.quantity_entry.bind("<KeyPress>", lambda e: self.submitQuantity)
        # Submit Button
        button = ttk.Button(self, text="Enter", style="SignButton.TButton", command=self.submitQuantity)
        button.grid(row=2, column=0, sticky="ns", pady=(10))
        # Error Label
        self.label_2 = ttk.Label(self, style="ErrorLoginRegisterLabel.TLabel")



    def submitQuantity(self):
        quantity_regex = r"^([0-9]){1,4}$"
        if (not re.fullmatch(quantity_regex, self.quantity.get().strip())):
            self.acceptable_quantity = False
            self.label_2.configure(text=f"Invalid Input")
            self.label_2.grid(row=3, column=0, sticky="ns", pady=(10))
        elif int(self.quantity.get()) == 0 and not (self.tag_value == "selected_for_invoice"):
            self.acceptable_quantity = False
            self.label_2.configure(text=f"No stock selected")
            self.label_2.grid(row=3, column=0, sticky="ns", pady=(10))
        elif int(self.quantity.get()) > self.in_stock_quantity:
            self.acceptable_quantity = False
            self.label_2.configure(text=f"Only {self.in_stock_quantity} units available in inventory")
            self.label_2.grid(row=3, column=0, sticky="ns", pady=(10))
        else:
            self.acceptable_quantity = True
            self.destroy()