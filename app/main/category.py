import tkinter as tk
from tkinter import ttk
from CONSTANT.index import *
from app.main.category_components.create_category import CreateCategory
from app.main.category_components.show_category import ShowCategory
from app.main.category_components.create_sub_category import CreateSubCategory
from app.main.category_components.show_sub_category import ShowSubCategory



# Note: We're not rendering this frame on grid until in main.py it was needed to
class Category(ttk.Frame):
    def __init__(self, main_page_frame, mysql, user, *args, **kwargs):
        super().__init__(main_page_frame, *args, **kwargs)
        
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
        self.top_frame.columnconfigure(2, weight=1)
        self.top_frame.columnconfigure(3, weight=1)
        self.top_frame.rowconfigure(0, weight=1)
        self.top_frame.grid(row=0, column=0, sticky="nsew") 
        
        # Bottom Frame for Tab's Content
        self.bottom_frame = ttk.Frame(self)
        self.bottom_frame.columnconfigure(0, weight=1)
        self.bottom_frame.rowconfigure(0, weight=1)
        self.bottom_frame.grid(row=1, column=0, sticky="nsew")  
        


    def contentForTopFrame(self):
        # Tabs for Top Frame
        # Categories
        self.create_category_tab = tk.Button(self.top_frame,
                                             text="Create New Category",
                                             command=self.commandCreateCategory,
                                             background=CATEGORY_PAGE_TAB_BUTTON_BACKGROUND,
                                             activebackground=SIDEBAR_BUTTON_ACTIVE_BACKGROUND,
                                             activeforeground=SIDEBAR_BUTTON_ACTIVE_FOREGROUND,
                                             font=CATEGORY_PAGE_TAB_BUTTON_FONT
                                             )
        self.create_category_tab.grid(row=0, column=0, sticky="ew")
        
        self.show_category_tab = tk.Button(self.top_frame,
                                           text="Show All Categories",
                                           command=self.commandShowCategory,
                                            background=CATEGORY_PAGE_TAB_BUTTON_BACKGROUND,
                                            activebackground=SIDEBAR_BUTTON_ACTIVE_BACKGROUND,
                                            activeforeground=SIDEBAR_BUTTON_ACTIVE_FOREGROUND,
                                            font=CATEGORY_PAGE_TAB_BUTTON_FONT
                                             )
        self.show_category_tab.grid(row=0, column=1, sticky="ew")
        
        # Sub-Categories
        self.create_subcategory_tab = tk.Button(self.top_frame,
                                                text="Create New Sub-Category",
                                                command=self.commandCreateSubCategory,
                                                background=CATEGORY_PAGE_TAB_BUTTON_BACKGROUND,
                                                activebackground=SIDEBAR_BUTTON_ACTIVE_BACKGROUND,
                                                activeforeground=SIDEBAR_BUTTON_ACTIVE_FOREGROUND,
                                                font=CATEGORY_PAGE_TAB_BUTTON_FONT
                                                )
        self.create_subcategory_tab.grid(row=0, column=2, sticky="ew")
        
        self.show_subcategory_tab = tk.Button(self.top_frame,
                                              text="Show All Sub-Categories",
                                              command=self.commandShowSubCategory,
                                              background=CATEGORY_PAGE_TAB_BUTTON_BACKGROUND,
                                              activebackground=SIDEBAR_BUTTON_ACTIVE_BACKGROUND,
                                              activeforeground=SIDEBAR_BUTTON_ACTIVE_FOREGROUND,
                                              font=CATEGORY_PAGE_TAB_BUTTON_FONT
                                              )
        self.show_subcategory_tab.grid(row=0, column=3, sticky="ew")
        
    def contentForBottomFrame(self, mysql):
        self.create_category_instance = CreateCategory(self.bottom_frame, mysql, self.user)
        self.show_category_instance = ShowCategory(self.bottom_frame, mysql, self.user)
        self.create_sub_category_instance = CreateSubCategory(self.bottom_frame, mysql, self.user)
        self.show_sub_category_instance = ShowSubCategory(self.bottom_frame, mysql, self.user)
        self.show_category_instance.grid(row=0, column=0, sticky="nsew")

        
    def commandCreateCategory(self):
        self.customReset()
        self.show_category_instance.grid_forget()
        self.show_sub_category_instance.grid_forget()
        self.create_sub_category_instance.grid_forget()
        self.create_category_instance.grid(row=0, column=0, sticky="ns")
    
    def commandShowCategory(self):
        self.customReset()
        self.create_category_instance.grid_forget()
        self.show_sub_category_instance.grid_forget()
        self.create_sub_category_instance.grid_forget()
        self.show_category_instance.grid(row=0, column=0, sticky="nsew")
        
    def commandCreateSubCategory(self):
        self.customReset()
        self.create_category_instance.grid_forget()
        self.show_category_instance.grid_forget()
        self.show_sub_category_instance.grid_forget()
        self.create_sub_category_instance.grid(row=0, column=0, sticky="ns")

        
    def commandShowSubCategory(self):
        self.customReset()
        self.create_category_instance.grid_forget()
        self.show_category_instance.grid_forget()
        self.create_sub_category_instance.grid_forget()
        self.show_sub_category_instance.grid(row=0, column=0, sticky="nsew")
        
    # Reset Page
    def customReset(self):
        self.create_category_instance.customReset()
        self.show_category_instance.customReset()
        self.show_sub_category_instance.customReset()
        self.create_sub_category_instance.customReset()
        