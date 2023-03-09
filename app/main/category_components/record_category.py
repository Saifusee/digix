import tkinter as tk
from tkinter import ttk
from CONSTANT.index import *
from modal import Modal
from app.main.category_components.edit_category import EditCategory
from app.main.category_components.edit_sub_category import EditSubCategory
from app.main.other_components.record_base import RecordBase, CLabel
from app.main.category_components.show_category_wise_sub_category import ShowCategoryWiseSubCategory

# Category Single Record Display
class RecordCategory(tk.Toplevel, RecordBase):
    def __init__(self, container, mysql, user, category_id, refreshedTableMethod=None, *args, **kwargs):
        
        # Inheriting tk.Toplevel Class
        super().__init__(container, *args, **kwargs)
        self.grab_set()
        # Inheriting RecordBase Class
        # Class.contructor(instance_or_object) is right syntax
        RecordBase.__init__(self, mysql, user, POPUP_TITLE="Category Detail") # Class.contructor(instance or object) is right syntax
        
        # necessary instance variable for particular class
        self.category_id = category_id
        self.refreshedTableMethod = lambda: refreshedTableMethod()

        # Render Contents inside Canvas 
        self.renderLabels(record_table_name = self.POPUP_TITLE)
        
        # Fetch and show data
        self.fetchDataAndRender()
        
        
        
    def renderLabels(self, record_table_name):
        # Heading Label
        heading_label = ttk.Label(self.frame, text=record_table_name, anchor="center", style="PageHeadingLabel.TLabel")
        heading_label.grid(row=0, column=0, columnspan=2, sticky="ew")
        
        # Contents to Display in Canvas
        lb_1 = CLabel(self.frame, text="Category ID: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_1.grid(row=1, column=0, sticky="nsew")
        self.category_id_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.category_id_label.grid(row=1, column=1, sticky="nsew")
        
        lb_2 = CLabel(self.frame, text="Category Name: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_2.grid(row=2, column=0, sticky="nsew")
        self.category_name_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.category_name_label.grid(row=2, column=1, sticky="nsew")
        
        self.show_sub_category_button = ttk.Button(
            self.frame,
            text="Show all Sub-Categories",
            command= lambda: ShowCategoryWiseSubCategory(
                self,
                self.mysql,
                self.current_user,
                self.category_id,
                RecordSubCategoryClass=RecordSubCategory
                ),
            style="SingleRecordLinkButton.TButton"
            )
        self.show_sub_category_button.grid(row=4, column=0, columnspan=2, sticky="ew")
        
        
        
    # Fetch Data from Database of Record and display it    
    def fetchDataAndRender(self):
        # Fetch Data
        data = self.queryFetchSingleCategory(self.category_id)
        # Display Data
        self.category_id_label.configure(text=data[0][CATEGORY_ID])
        self.category_name_label.configure(text=data[0][CATEGORY_NAME])
        
        
        
    # Edit Record    
    def commandButton1(self):
        # Edit Record
        EditCategory(
            self,
            self.mysql,
            self.current_user,
            self.category_id,
            lambda: [self.refreshedTableMethod(), self.customReset()]
        )
        # Refresh Details in Popup
        self.fetchDataAndRender()
        
        
        
    # Delete record
    def commandButton2(self):
        # If user confirm -> Delete Record, refresh table and destroy popup
        Modal(self,
              f"Are you sure to delete this record permanently ?",
              lambda: [
                  self.queryDeleteCategory(self.category_id),
                  self.refreshedTableMethod(),
                  self.destroy(),
                  ]
              )
        
        
     # Refreshing the Widget   
    def customReset(self):
        self.fetchDataAndRender()
        
        
        
        
        
        
        
        


# Sub Category Single Record Display
class RecordSubCategory(tk.Toplevel, RecordBase):
    def __init__(self, container, mysql, user, sub_category_id, refreshedTableMethod=None, *args, **kwargs):
        
        # Inheriting tk.Toplevel Class
        super().__init__(container, *args, **kwargs)
        self.grab_set()
        # Inheriting RecordBase Class
        # Class.contructor(instance_or_object) is right syntax
        RecordBase.__init__(self, mysql, user, POPUP_TITLE="Sub-Category Detail") # Class.contructor(instance or object) is right syntax
        
        # necessary instance variable for particular class
        self.sub_category_id = sub_category_id
        self.refreshedTableMethod = lambda: refreshedTableMethod()

        # Render Contents inside Canvas 
        self.renderLabels(record_table_name = self.POPUP_TITLE)
        
        # Fetch and show data
        self.fetchDataAndRender()
        
        
        
    def renderLabels(self, record_table_name):
        # Heading Label
        heading_label = ttk.Label(self.frame, text=record_table_name, anchor="center", style="PageHeadingLabel.TLabel")
        heading_label.grid(row=0, column=0, columnspan=2, sticky="ew")
        
        # Contents to Display in Canvas
        lb_1 = CLabel(self.frame, text="Sub-Category ID: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_1.grid(row=1, column=0, sticky="nsew")
        
        self.sub_category_id_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.sub_category_id_label.grid(row=1, column=1, sticky="nsew")
        
        
        lb_2 = CLabel(self.frame, text="Sub-Category Name: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_2.grid(row=2, column=0, sticky="nsew")
        
        self.sub_category_name_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.sub_category_name_label.grid(row=2, column=1, sticky="nsew")
        
        
        lb_3 = CLabel(self.frame, text="Category Name: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_3.grid(row=3, column=0, sticky="nsew")
        
        self.category_name_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.category_name_label.grid(row=3, column=1, sticky="nsew")
        
        
        
    # Fetch Data from Database of Record and display it    
    def fetchDataAndRender(self):
        # Fetch Data
        data = self.queryFetchSingleSubCategory(self.sub_category_id)
        # Display Data
        self.sub_category_id_label.configure(text=data[0][SUB_CATEGORY_ID])
        self.sub_category_name_label.configure(text=data[0][SUB_CATEGORY_NAME])
        self.category_name_label.configure(text=data[0][CATEGORY_NAME])
        
        
        
    # Edit Record    
    def commandButton1(self):
        # Edit Record
        EditSubCategory(
            self,
            self.mysql,
            self.current_user,
            self.sub_category_id,
            lambda: [self.refreshedTableMethod(), self.customReset()]
        )
        # Refresh Details in Popup
        self.fetchDataAndRender()
        
        
        
    # Delete record
    def commandButton2(self):
        # If user confirm -> Delete Record, refresh table and destroy popup
        Modal(self,
              f"Are you sure to delete this record permanently ?",
              lambda: [
                  self.queryDeleteSubCategory(self.sub_category_id),
                  self.refreshedTableMethod(),
                  self.destroy(),
                  ]
              )
        
        
        
     # Refreshing the Widget   
    def customReset(self):
        self.fetchDataAndRender()
