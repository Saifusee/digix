
import tkinter as tk
from tkinter import ttk
from CONSTANT.index import *
from modal import Modal

class SidebarButton():
    def __init__(self, app_window, frame, main_page_instance, user):
        
        self.user_authority = user[USER_AUTHORITY]

        # SideBar Button Frame 
        frame.columnconfigure(0, weight=1)
        
        # Disabled Button for Design
        self.header_button = tk.Button(frame, state="disabled")
        self.header_button.grid(sticky="ew")
        
        # Dashboard Button
        self.messages_button = tk.Button(
            frame,
            text="Notifications",
            command=main_page_instance.commandRenderDashboard,
            wraplength=SIDEBAR_BUTTON_TEXT_WRAP_VALUE,
            background=SIDEBAR_BUTTON_BACKGROUND,
            activebackground=SIDEBAR_BUTTON_ACTIVE_BACKGROUND,
            activeforeground=SIDEBAR_BUTTON_ACTIVE_FOREGROUND,
            font=SIDEBAR_BUTTON_FONT
        )
        self.messages_button.bind("<Button-1>", self.toggleButtonColor)
        
        # Product Button
        self.product_button = tk.Button(
            frame,
            text="Inventory",
            command=main_page_instance.commandRenderProduct,
            wraplength=SIDEBAR_BUTTON_TEXT_WRAP_VALUE,
            background=SIDEBAR_BUTTON_BACKGROUND,
            activebackground=SIDEBAR_BUTTON_ACTIVE_BACKGROUND,
            activeforeground=SIDEBAR_BUTTON_ACTIVE_FOREGROUND,
            font=SIDEBAR_BUTTON_FONT
        )
        self.product_button.bind("<Button-1>", self.toggleButtonColor)

        # Sales Order Button
        self.sales_order_button = tk.Button(
            frame,
            text="Sales Orders",
            command=main_page_instance.commandRenderSalesOrder,
            wraplength=SIDEBAR_BUTTON_TEXT_WRAP_VALUE,
            background=SIDEBAR_BUTTON_BACKGROUND,
            activebackground=SIDEBAR_BUTTON_ACTIVE_BACKGROUND,
            activeforeground=SIDEBAR_BUTTON_ACTIVE_FOREGROUND,
            font=SIDEBAR_BUTTON_FONT
        )
        self.sales_order_button.bind("<Button-1>", self.toggleButtonColor)

        # Purchase Order Button
        self.purchase_order_button = tk.Button(
            frame,
            text="Purchase Orders",
            command=main_page_instance.commandRenderPurchaseOrder,
            wraplength=SIDEBAR_BUTTON_TEXT_WRAP_VALUE,
            background=SIDEBAR_BUTTON_BACKGROUND,
            activebackground=SIDEBAR_BUTTON_ACTIVE_BACKGROUND,
            activeforeground=SIDEBAR_BUTTON_ACTIVE_FOREGROUND,
            font=SIDEBAR_BUTTON_FONT
        )
        self.purchase_order_button.bind("<Button-1>", self.toggleButtonColor)

        # Return/Cancel Order Button
        self.return_cancel_order_button = tk.Button(
            frame,
            text="Return/Cancel Orders",
            command=main_page_instance.commandRenderReturnCancelOrder,
            wraplength=SIDEBAR_BUTTON_TEXT_WRAP_VALUE,
            background=SIDEBAR_BUTTON_BACKGROUND,
            activebackground=SIDEBAR_BUTTON_ACTIVE_BACKGROUND,
            activeforeground=SIDEBAR_BUTTON_ACTIVE_FOREGROUND,
            font=SIDEBAR_BUTTON_FONT
        )
        self.return_cancel_order_button.bind("<Button-1>", self.toggleButtonColor)
        
        # Suppliers Button
        self.supplier_button = tk.Button(
            frame,
            text="Registered Suppliers",
            command=main_page_instance.commandRenderSupplier,
            wraplength=SIDEBAR_BUTTON_TEXT_WRAP_VALUE,
            background=SIDEBAR_BUTTON_BACKGROUND,
            activebackground=SIDEBAR_BUTTON_ACTIVE_BACKGROUND,
            activeforeground=SIDEBAR_BUTTON_ACTIVE_FOREGROUND,
            font=SIDEBAR_BUTTON_FONT
        )
        self.supplier_button.bind("<Button-1>", self.toggleButtonColor)
    
        # Categories Button
        self.category_button = tk.Button(
            frame,
            text="Product Categories",
            command=main_page_instance.commandRenderCategory,
            wraplength=SIDEBAR_BUTTON_TEXT_WRAP_VALUE,
            background=SIDEBAR_BUTTON_BACKGROUND,
            activebackground=SIDEBAR_BUTTON_ACTIVE_BACKGROUND,
            activeforeground=SIDEBAR_BUTTON_ACTIVE_FOREGROUND,
            font=SIDEBAR_BUTTON_FONT
        )
        self.category_button.bind("<Button-1>", self.toggleButtonColor)
        
        # User Button
        self.user_button = tk.Button(
            frame,
            text="User",
            command=main_page_instance.commandRenderUser,
            wraplength=SIDEBAR_BUTTON_TEXT_WRAP_VALUE,
            background=SIDEBAR_BUTTON_BACKGROUND,
            activebackground=SIDEBAR_BUTTON_ACTIVE_BACKGROUND,
            activeforeground=SIDEBAR_BUTTON_ACTIVE_FOREGROUND,
            font=SIDEBAR_BUTTON_FONT
        )
        self.user_button.bind("<Button-1>", self.toggleButtonColor)

        # Profile Button
        self.user_profile_button = tk.Button(
            frame,
            text="Profile",
            command=main_page_instance.commandRenderUserProfile,
            wraplength=SIDEBAR_BUTTON_TEXT_WRAP_VALUE,
            background=SIDEBAR_BUTTON_BACKGROUND,
            activebackground=SIDEBAR_BUTTON_ACTIVE_BACKGROUND,
            activeforeground=SIDEBAR_BUTTON_ACTIVE_FOREGROUND,
            font=SIDEBAR_BUTTON_FONT
        )
        self.user_profile_button.bind("<Button-1>", self.toggleButtonColor)

        # Profile Button
        self.shop_profile_button = tk.Button(
            frame,
            text="Organization's Profile",
            command=main_page_instance.commandRenderShopProfile,
            wraplength=SIDEBAR_BUTTON_TEXT_WRAP_VALUE,
            background=SIDEBAR_BUTTON_BACKGROUND,
            activebackground=SIDEBAR_BUTTON_ACTIVE_BACKGROUND,
            activeforeground=SIDEBAR_BUTTON_ACTIVE_FOREGROUND,
            font=SIDEBAR_BUTTON_FONT
        )
        self.shop_profile_button.bind("<Button-1>", self.toggleButtonColor)

        # By Default Show Sales Order Components
        self.user_profile_button.invoke()
        self.user_profile_button.configure(background=SIDEBAR_BUTTON_ACTIVE_BACKGROUND, foreground=SIDEBAR_BUTTON_ACTIVE_FOREGROUND)

        
        self.messages_button.grid(sticky="ew")
        if self.user_authority == AUTHORITY_PRIMARY or self.user_authority == AUTHORITY_SECONDARY: self.product_button.grid(sticky="ew")
        self.sales_order_button.grid(sticky="ew")
        if self.user_authority == AUTHORITY_PRIMARY or self.user_authority == AUTHORITY_SECONDARY: self.purchase_order_button.grid(sticky="ew")
        if self.user_authority == AUTHORITY_PRIMARY or self.user_authority == AUTHORITY_SECONDARY: self.return_cancel_order_button.grid(sticky="ew")
        if self.user_authority == AUTHORITY_PRIMARY or self.user_authority == AUTHORITY_SECONDARY: self.supplier_button.grid(sticky="ew")
        if self.user_authority == AUTHORITY_PRIMARY or self.user_authority == AUTHORITY_SECONDARY: self.category_button.grid(sticky="ew")
        if self.user_authority == AUTHORITY_PRIMARY or self.user_authority == AUTHORITY_SECONDARY: self.user_button.grid(sticky="ew")
        if self.user_authority == AUTHORITY_PRIMARY: self.shop_profile_button.grid(sticky="ew")
        self.user_profile_button.grid(sticky="ew")
        
        # Disabled Button for Design
        self.footer_button = tk.Button(frame, state="disabled")
        self.footer_button.grid(sticky="ew",)
        
        # Logout Button
        self.logout_button = ttk.Button(
            frame,
            text="Logout",
            command=lambda: Modal(app_window, "Are you sure you want to log out ?", lambda: self.commandLogout(app_window)),
            style="ResetCancelButton.TButton"
        )
        self.logout_button.grid(sticky="ew")
        

    def commandButton(self):
        pass

    def toggleButtonColor(self, event):
        # Resets all buttons colors
        self.messages_button.configure(background=SIDEBAR_BUTTON_BACKGROUND, foreground="black")
        self.product_button.configure(background=SIDEBAR_BUTTON_BACKGROUND, foreground="black")
        self.sales_order_button.configure(background=SIDEBAR_BUTTON_BACKGROUND, foreground="black")
        self.purchase_order_button.configure(background=SIDEBAR_BUTTON_BACKGROUND, foreground="black")
        self.return_cancel_order_button.configure(background=SIDEBAR_BUTTON_BACKGROUND, foreground="black")
        self.supplier_button.configure(background=SIDEBAR_BUTTON_BACKGROUND, foreground="black")
        self.category_button.configure(background=SIDEBAR_BUTTON_BACKGROUND, foreground="black")
        self.user_button.configure(background=SIDEBAR_BUTTON_BACKGROUND, foreground="black")
        self.user_profile_button.configure(background=SIDEBAR_BUTTON_BACKGROUND, foreground="black")
        self.shop_profile_button.configure(background=SIDEBAR_BUTTON_BACKGROUND, foreground="black")

        # change selected button color
        event.widget.configure(background=SIDEBAR_BUTTON_ACTIVE_BACKGROUND, foreground=SIDEBAR_BUTTON_ACTIVE_FOREGROUND)



    def commandLogout(self, app_window):
        app_window.destroy()
        
