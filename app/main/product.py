import tkinter as tk
from tkinter import ttk
from CONSTANT.index import *
from app.main.product_components.create_product import CreateProduct
from app.main.product_components.show_product import ShowProduct



# Note: We're not rendering this frame on grid until in main.py it was needed to
class Product(ttk.Frame):
    def __init__(self, main_page_frame, mysql, user, *args, **kwargs):
        super().__init__(main_page_frame, *args, **kwargs)
        
        # Category Frame Grid Cofiguration
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=9)
        self.columnconfigure(0, weight=1)
        self.user = user
        
        # Rendering Frames
        self.renderFrames()
        
        # Rendering Contents of Top Frame
        self.contentForTopFrame()
        
        # Rendering Contents of Top Frame
        self.contentForBottomFrame(mysql)


    def renderFrames(self):
        # Top Frame for Tabs
        self.top_frame = ttk.Frame(self, padding=10)
        self.top_frame.columnconfigure(0, weight=1)
        self.top_frame.columnconfigure(1, weight=1)
        self.top_frame.rowconfigure(0, weight=1)
        self.top_frame.grid(row=0, column=0, sticky="nsew") 
        
        # Bottom Frame for Tab's Content
        self.bottom_frame = ttk.Frame(self)
        self.bottom_frame.columnconfigure(0, weight=1)
        self.bottom_frame.rowconfigure(0, weight=1)
        self.bottom_frame.grid(row=1, column=0, sticky="nsew")  
        


    def contentForTopFrame(self):
        # Tabs for Top Frame
        # Products
        self.show_product_tab = tk.Button(self.top_frame,
                                             text="Show Inventory",
                                             command=self.commandShowProduct,
                                             background=CATEGORY_PAGE_TAB_BUTTON_BACKGROUND,
                                             activebackground=SIDEBAR_BUTTON_ACTIVE_BACKGROUND,
                                             activeforeground=SIDEBAR_BUTTON_ACTIVE_FOREGROUND,
                                             font=CATEGORY_PAGE_TAB_BUTTON_FONT
                                             )
        self.show_product_tab.grid(row=0, column=0, sticky="ew")
        
        self.create_product_tab = tk.Button(self.top_frame,
                                           text="Create New Product",
                                           command=self.commandCreateProduct,
                                            background=CATEGORY_PAGE_TAB_BUTTON_BACKGROUND,
                                            activebackground=SIDEBAR_BUTTON_ACTIVE_BACKGROUND,
                                            activeforeground=SIDEBAR_BUTTON_ACTIVE_FOREGROUND,
                                            font=CATEGORY_PAGE_TAB_BUTTON_FONT
                                             )
        self.create_product_tab.grid(row=0, column=1, sticky="ew")
        
    def contentForBottomFrame(self, mysql):
        self.create_product_instance = CreateProduct(self.bottom_frame, mysql, self.user)
        self.show_product_instance = ShowProduct(self.bottom_frame, mysql, self.user)
        self.show_product_instance.grid(row=0, column=0, sticky="nsew")

        
    def commandCreateProduct(self):
        self.customReset()
        self.show_product_instance.grid_forget()
        self.create_product_instance.grid(row=0, column=0, sticky="ns")
    
    def commandShowProduct(self):
        self.customReset()
        self.create_product_instance.grid_forget()
        self.show_product_instance.grid(row=0, column=0, sticky="nsew")
        
    # Reset Page
    def customReset(self):
        self.show_product_instance.customReset()
        self.create_product_instance.customReset()
        
        