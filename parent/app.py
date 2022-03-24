import tkinter as tk
from tkinter import StringVar, ttk
from cusimp.constants import *

class AppWindow(tk.Tk):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.title(ORGANIZATION_NAME) #ORGANIZATION_NAME = from constants module
        self.geometry("1000x1000")
        
        self.mainloop()