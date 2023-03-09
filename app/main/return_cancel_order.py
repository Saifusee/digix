import tkinter as tk
from tkinter import ttk
from CONSTANT.index import *
from app.main.return_cancel_order_components.create_return_cancel_order import CreateReturnCancelOrder
from app.main.return_cancel_order_components.show_return_cancel_order import ShowReturnCancelOrder



# Note: We're not rendering this frame on grid until in main.py it was needed to
class ReturnCancelOrder(ttk.Frame):
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
        self.create_return_cancel_order_tab = tk.Button(self.top_frame,
                                             text="Create Return/Cancel Order",
                                             command=self.commandCreateReturnCancelOrder,
                                             background=CATEGORY_PAGE_TAB_BUTTON_BACKGROUND,
                                             activebackground=SIDEBAR_BUTTON_ACTIVE_BACKGROUND,
                                             activeforeground=SIDEBAR_BUTTON_ACTIVE_FOREGROUND,
                                             font=CATEGORY_PAGE_TAB_BUTTON_FONT
                                             )
        self.create_return_cancel_order_tab.grid(row=0, column=0, sticky="ew")
        
        self.show_return_cancel_order_tab = tk.Button(self.top_frame,
                                           text="Show Return/Cancel Order",
                                           command=self.commandShowReturnCancelOrder,
                                            background=CATEGORY_PAGE_TAB_BUTTON_BACKGROUND,
                                            activebackground=SIDEBAR_BUTTON_ACTIVE_BACKGROUND,
                                            activeforeground=SIDEBAR_BUTTON_ACTIVE_FOREGROUND,
                                            font=CATEGORY_PAGE_TAB_BUTTON_FONT
                                             )
        self.show_return_cancel_order_tab.grid(row=0, column=1, sticky="ew")
        
        
    def contentForBottomFrame(self, mysql):
        self.create_return_cancel_order_instance = CreateReturnCancelOrder(self.bottom_frame, mysql, self.user)
        self.show_return_cancel_order_instance = ShowReturnCancelOrder(self.bottom_frame, mysql, self.user)
        # By Default open create new sales order
        self.create_return_cancel_order_tab.invoke()

    def commandCreateReturnCancelOrder(self):
        self.customReset()
        self.show_return_cancel_order_instance.grid_forget()
        self.create_return_cancel_order_instance.grid(row=0, column=0, sticky="nsew")
    
    def commandShowReturnCancelOrder(self):
        self.customReset()
        self.create_return_cancel_order_instance.grid_forget()
        self.show_return_cancel_order_instance.grid(row=0, column=0, sticky="nsew")
        
    # Reset Page
    def customReset(self):
        self.create_return_cancel_order_instance.customReset()
        self.show_return_cancel_order_instance.customReset()