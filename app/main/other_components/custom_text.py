import tkinter as tk
from tkinter import ttk

class CustomText(tk.Text):
    def __init__(self, container, *args, **kwargs):
        self.container = container
        super().__init__(self.container, *args, **kwargs)
        

        
    def grid_scrollbar(self, row, column, rowspan=1, columnspan=1):
        """
        This method render scrollbar to Text widget horizontally and vertically
        """
        # Vertical Scrollbar
        self.vertical_scrollbar = ttk.Scrollbar(self.container, orient="vertical", command=self.yview)
        self.configure(yscrollcommand=self.vertical_scrollbar.set)
        # Horizontal Scrollbar
        self.horizontal_scrollbar = ttk.Scrollbar(self.container, orient="horizontal", command=self.xview)
        self.configure(xscrollcommand=self.horizontal_scrollbar.set)
        self.vertical_scrollbar.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky="nse")
        self.horizontal_scrollbar.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky="ews")