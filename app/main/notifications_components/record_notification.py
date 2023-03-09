import tkinter as tk
from tkinter import ttk
from CONSTANT.index import *
from app.main.other_components.record_base import RecordBase, CLabel


# Sub Category Single Record Display
class RecordNotification(tk.Toplevel, RecordBase):
    def __init__(self, container, mysql, record_dictionary, second_label_heading, *args, **kwargs):
        
        # Inheriting tk.Toplevel Class
        super().__init__(container, *args, **kwargs)
        self.grab_set()
        # Inheriting RecordBase Class
        # Class.contructor(instance_or_object) is right syntax
        RecordBase.__init__(self, mysql, None, POPUP_TITLE="Notification Details", button_2_text=None) # Class.contructor(instance or object) is right syntax

        # Render Contents inside Canvas 
        self.renderLabels(self.POPUP_TITLE, record_dictionary, second_label_heading)

        
        
        
    def renderLabels(self, record_table_name, record_dictionary, second_label_heading):
        # Heading Label
        heading_label = ttk.Label(self.frame, text=record_table_name, anchor="center", style="PageHeadingLabel.TLabel")
        heading_label.grid(row=0, column=0, columnspan=2, sticky="ew")
        
        # Contents to Display in Canvas
        lb_1 = CLabel(self.frame, text="Message: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_1.grid(row=1, column=0, sticky="nsew")
        
        self.log_label = CLabel(self.frame, text=record_dictionary["B"], font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.log_label.grid(row=1, column=1, sticky="nsew")
        
        
        lb_2 = CLabel(self.frame, text=second_label_heading, font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_2.grid(row=2, column=0, sticky="nsew")
        
        self.date_label = CLabel(self.frame, text=record_dictionary["C"], font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.date_label.grid(row=2, column=1, sticky="nsew")
        
        
