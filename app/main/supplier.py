import tkinter as tk
from tkinter import ttk
from CONSTANT.index import *
from app.main.supplier_components.create_supplier import CreateSupplier
from app.main.supplier_components.show_supplier import ShowSupplier



# Note: We're not rendering this frame on grid until in main.py it was needed to
class Supplier(ttk.Frame):
    def __init__(self, main_page_frame, mysql, user, *args, **kwargs):
        super().__init__(main_page_frame, padding=10, *args, **kwargs)
        
        self.user = user
        
        # Category Frame Grid Cofiguration
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=9)
        self.columnconfigure(0, weight=1)
        
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
        # Suppliers
        self.create_supplier_tab = tk.Button(self.top_frame,
                                             text="Create New Supplier Profile",
                                             command=self.commandCreateSupplier,
                                             background=CATEGORY_PAGE_TAB_BUTTON_BACKGROUND,
                                             activebackground=SIDEBAR_BUTTON_ACTIVE_BACKGROUND,
                                             activeforeground=SIDEBAR_BUTTON_ACTIVE_FOREGROUND,
                                             font=CATEGORY_PAGE_TAB_BUTTON_FONT
                                             )
        self.create_supplier_tab.grid(row=0, column=0, sticky="ew")
        
        self.show_supplier_tab = tk.Button(self.top_frame,
                                           text="Show All Suppliers List",
                                           command=self.commandShowSupplier,
                                            background=CATEGORY_PAGE_TAB_BUTTON_BACKGROUND,
                                            activebackground=SIDEBAR_BUTTON_ACTIVE_BACKGROUND,
                                            activeforeground=SIDEBAR_BUTTON_ACTIVE_FOREGROUND,
                                            font=CATEGORY_PAGE_TAB_BUTTON_FONT
                                             )
        self.show_supplier_tab.grid(row=0, column=1, sticky="ew")
        
        
    def contentForBottomFrame(self, mysql):
        self.create_supplier_instance = CreateSupplier(self.bottom_frame, mysql, self.user)
        self.show_supplier_instance = ShowSupplier(self.bottom_frame, mysql, self.user)
        self.show_supplier_instance.grid(row=0, column=0, sticky="nsew")

        
    def commandCreateSupplier(self):
        self.customReset()
        self.show_supplier_instance.grid_forget()
        self.create_supplier_instance.grid(row=0, column=0, sticky="ns")
    
    def commandShowSupplier(self):
        self.customReset()
        self.create_supplier_instance.grid_forget()
        self.show_supplier_instance.grid(row=0, column=0, sticky="nsew")
        
    # Reset Page
    def customReset(self):
        self.create_supplier_instance.customReset()
        self.show_supplier_instance.customReset()