import tkinter as tk
from tkinter import ttk
from CONSTANT.application_setting_constants import TTK_FRAME_DEFAULT_BG_COLOR, centerTkinterToplevel, PATH_TO_IMAGES, FILE_APP_LOGO, FILE_APP_DEFAULT_LOGO
from app.base import Base
from os import path
import re
from app.main.other_components.custom_text import CustomText

class ReturnCancelQuantityEntry(tk.Toplevel):
    def __init__(self, container, details_tuple, tag_value):
        super().__init__(container)
        self.columnconfigure(0, weight=1)
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
        self.tag_value = tag_value
        self.record_id = int(details_tuple[1])
        self.bought_quantity = int(details_tuple[8][2:])
        self.already_cancelled_quantity = int(details_tuple[10][2:])
        self.already_returned_quantity = int(details_tuple[11][2:])
        self.total_price = Base.formatReverseINR(self, details_tuple[9])
        self.acceptable_quantity_range = self.bought_quantity-(self.already_returned_quantity+self.already_cancelled_quantity)
        self.marked_cancelled_quantity = tk.StringVar()
        self.marked_returned_quantity = tk.StringVar()
        self.marked_cancelled_quantity.set(0)
        self.marked_returned_quantity.set(0)
        self.refund_amount = tk.StringVar()
        self.reason = ""
        self.refund_amount.set(self.total_price)
        self.acceptable_quantity = False
        product_name = details_tuple[3]

        # Title Label
        label_1 = ttk.Label(self, text=f'"{product_name}"',  style="QuantityPopUpLabel.TLabel")
        label_1.grid(row=0, column=0, columnspan=2, sticky="ns", pady=(10),  padx=(10))

        # Cancellable Quantity Spinbox
        lb = ttk.Label(self, text="Enter Cancellable Quantities: ", style="LoginLabel.TLabel")
        lb.grid(row=1, column=0, sticky="w")
        self.cancel_spinbox = tk.Spinbox(
            self,
            width=4,
            wrap=True,
            from_=0,
            to=self.acceptable_quantity_range,
            textvariable=self.marked_cancelled_quantity,
            font=("TkDefaultFont", 15, "bold"),
            justify="center"
            )
        self.cancel_spinbox.grid(row=1, column=1, sticky="ns", pady=(10),  padx=(10))
        self.cancel_spinbox.bind("<KeyPress>", lambda e: self.submitQuantity)

        # Returnable Quantity Spinbox
        lb = ttk.Label(self, text="Enter Returnable Quantities: ", style="LoginLabel.TLabel")
        lb.grid(row=2, column=0, sticky="w")
        self.return_spinbox = tk.Spinbox(
            self,
            width=4,
            wrap=True,
            from_=0,
            to=self.acceptable_quantity_range,
            textvariable=self.marked_returned_quantity,
            font=("TkDefaultFont", 15, "bold"),
            justify="center"
            )
        self.return_spinbox.grid(row=2, column=1, sticky="ns", pady=(10),  padx=(10))
        self.return_spinbox.bind("<KeyPress>", lambda e: self.submitQuantity)

        # Amount Entry
        label_2 = ttk.Label(self, text="Refunded Amount:",  style="LoginLabel.TLabel")
        label_2.grid(row=3, column=0, sticky="ns", pady=(10), padx=(10))
        # Price Entry
        self.price_entry = ttk.Entry(self, width=25, textvariable=self.refund_amount, font=("TkdefaultFont", 12, "bold"))
        self.price_entry.grid(row=3, column=1, sticky="ns", pady=(10), padx=(10))



        label_3 = ttk.Label(self, text="Reason for Return/Cancellation: ", style="LoginLabel.TLabel")
        label_3.grid(row=4, column=0, sticky="w")
        
        self.reason_entry = CustomText(
            self,
            height=5,
            width=25,
            wrap=tk.NONE,
            font=("TkdefaultFont", 10, "bold")
            )
        self.reason_entry.grid(row=4, column=1, pady=(10), padx=(10))
        self.reason_entry.grid_scrollbar(row=4, column=1)


        # Submit Button
        button = ttk.Button(self, text="Enter", style="SignButton.TButton", command=self.submitQuantity)
        button.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(10),  padx=(10))
        # Error Label
        self.label_2 = ttk.Label(self, style="ErrorLoginRegisterLabel.TLabel", wraplength=250, justify="center")


        # Disable entries if all purchased quantities already been cancelled or refunded
        if self.already_cancelled_quantity + self.already_returned_quantity >= self.bought_quantity:
            self.cancel_spinbox.configure(state="disabled")
            self.return_spinbox.configure(state="disabled")
            self.price_entry.configure(state="disabled")
            self.reason_entry.configure(state="disabled")
            button.configure(state="disabled")
            self.label_2.configure(text=f"All quantities of this product in this order already been cancelled or returned.")
            self.label_2.grid(row=6, column=0, columnspan=2, sticky="ns", pady=(10),  padx=(10))



    def submitQuantity(self):
        quantity_regex = r"^([0-9]){1,4}$"
        price_regex = r"^([0-9]){1,9}\.{,1}[0-9]{,2}$"
        if (not re.fullmatch(quantity_regex, self.marked_cancelled_quantity.get().strip())):
            self.acceptable_quantity = False
            self.label_2.configure(text=f"Invalid quantity value for cancellable quantity")
            self.label_2.grid(row=6, column=0, columnspan=2, sticky="ns", pady=(10),  padx=(10))
        elif (not re.fullmatch(quantity_regex, self.marked_returned_quantity.get().strip())):
            self.acceptable_quantity = False
            self.label_2.configure(text=f"Invalid quantity value for returnable quantity")
            self.label_2.grid(row=6, column=0, columnspan=2, sticky="ns", pady=(10),  padx=(10))
        elif (int(self.marked_cancelled_quantity.get()) == 0 and int(self.marked_returned_quantity.get()) == 0) and not (self.tag_value == "selected"):
            self.acceptable_quantity = False
            self.label_2.configure(text=f"Nothing selected for return or cancellation.")
            self.label_2.grid(row=6, column=0, columnspan=2, sticky="ns", pady=(10),  padx=(10))
        elif int(self.marked_cancelled_quantity.get()) == 0 and int(self.marked_returned_quantity.get()) > self.acceptable_quantity_range:
            self.acceptable_quantity = False
            self.label_2.configure(text=f"Only x {self.acceptable_quantity_range} unit of this product is returnable in this order.")
            self.label_2.grid(row=6, column=0, columnspan=2, sticky="ns", pady=(10),  padx=(10))
        elif int(self.marked_returned_quantity.get()) == 0 and int(self.marked_cancelled_quantity.get()) > self.acceptable_quantity_range:
            self.acceptable_quantity = False
            self.label_2.configure(text=f"Only x {self.acceptable_quantity_range} unit of this product is cancellable in this order.")
            self.label_2.grid(row=6, column=0, columnspan=2, sticky="ns", pady=(10),  padx=(10))
        elif int(self.marked_returned_quantity.get()) + int(self.marked_cancelled_quantity.get()) > self.acceptable_quantity_range:
            self.acceptable_quantity = False
            self.label_2.configure(text=f"Only x {self.acceptable_quantity_range} unit of this product is cancellable and returnable together in this order.")
            self.label_2.grid(row=6, column=0, columnspan=2, sticky="ns", pady=(10),  padx=(10))
        elif (not re.fullmatch(price_regex, self.refund_amount.get().strip())):
            self.acceptable_quantity = False
            self.label_2.configure(text=f"Invalid value for price")
            self.label_2.grid(row=6, column=0, columnspan=2, sticky="ns", pady=(10),  padx=(10))
        elif float(self.refund_amount.get()) > self.total_price:
            self.acceptable_quantity = False
            self.label_2.configure(text=f"Refunded amount is greater than total price of this product in this order.")
            self.label_2.grid(row=6, column=0, columnspan=2, sticky="ns", pady=(10),  padx=(10))
        else:
            self.acceptable_quantity = True
            self.reason = self.reason_entry.get(1.0, "end-1c").strip()
            self.destroy()
            