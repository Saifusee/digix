import tkinter as tk
from tkinter import ttk
import tkinter.font as font

COLOR_PRIMARY_LABEL = "#33adff"
ORGANIZATION_LABEL = "#66ff99"
LOGIN_REGISTER_PAGE_HEADING_LABEL = "#80dfff"
COLOR_PRIMARY_BUTTON = "#80b3ff"
COLOR_SECONDARY_BUTTON = "#a6a6a6"
COLOR_BUTTON_RED = "#ff3333"
COLOR_BUTTON_SIGN = "#66ff66"
COLOR_BLACK = "#000000"
COLOR_WHITE = "#ffffff"

class CustomStyle(ttk.Style):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.theme_use("clam")
        
        #LABELS
        self.configure("ApplicationLabel1.TLabel", background=COLOR_PRIMARY_LABEL, font=("TkdefaultFont", 20, "bold"))
        self.configure("OraganizationLabel1.TLabel", background=ORGANIZATION_LABEL, font=("TkdefaultFont", 10, "bold"))
        self.configure("PageHeadingLabel.TLabel", background=LOGIN_REGISTER_PAGE_HEADING_LABEL, foreground=COLOR_BLACK, font=("TkdefaultFont", 10, "bold"))
        self.configure("LoginLabel.TLabel", anchor="w", justify="left", font=("TkdefaultFont", 10, "bold"), padding=10)
        self.configure("ErrorLoginRegisterLabel.TLabel", anchor="w", justify="left", foreground="red", font=("TkdefaultFont", 10, "bold"), padding=5)
        self.configure("SuccessfulLoginRegisterLabel.TLabel", anchor="w", justify="left", foreground="green", font=("TkdefaultFont", 10, "bold"), padding=5)


        #BUTTONS
        self.configure("LoginRegisterButton.TButton", background=COLOR_PRIMARY_BUTTON, bordercolor=COLOR_BLACK, font=("TkDefaultFont",10,"bold"))
        self.map("LoginRegisterButton.TButton", background = [("active", COLOR_BLACK),], foreground = [("active", COLOR_WHITE)])
        self.configure("ResetCancelButton.TButton", background=COLOR_BUTTON_RED, bordercolor=COLOR_BLACK, font=("TkDefaultFont",10,"bold"))
        self.map("ResetCancelButton.TButton", background = [("active", COLOR_BLACK)], foreground = [("active", COLOR_WHITE)])
        self.configure("SignButton.TButton", background=COLOR_BUTTON_SIGN, bordercolor=COLOR_BLACK, font=("TkDefaultFont",10,"bold"))
        self.map("SignButton.TButton", background = [("active", COLOR_BLACK), ("pressed", "yellow"), ("disabled", "grey")], foreground = [("active", COLOR_WHITE)])
        
        #Entry
        self.configure("ErrorEntry.TEntry", bordercolor="red", highlightcolor="red")
        
