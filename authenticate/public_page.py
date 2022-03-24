import tkinter as tk
from tkinter import ttk
from cusimp import constants
from authenticate import login, register
import custom_styles

class PublicPage(tk.Tk):
    def __init__(self, mysql, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.title("DigiX")
        self.geometry("700x900")
        self.user = dict()
        custom_styles.CustomStyle(self)
        
        
        #Top Frame for Labels
        self.columnconfigure(0, weight=1)
        self.top_frame = ttk.Frame(self, padding=10)
        self.top_frame.grid(row=0, column=0, columnspan=2 ,sticky="ew")
        
        #Bottom Frame for Fields and Buttons
        self.bottom_frame = ttk.Frame(self)
        self.bottom_frame.grid(row=1, column=0, padx=(10,10), pady=(10,10))
        self.bottom_frame.rowconfigure(0, weight=1)
        self.bottom_frame.columnconfigure(0, weight=1)
        
        #PUTTING TOP FRAME
        self.top_frame_contents(self.top_frame)
        
        #PUTTING BOTTOM FRAME
        self.bottom_frame_contents(self.bottom_frame, mysql)
        
        self.mainloop()        

        
    def top_frame_contents(self, frame):
        _app_name_text = "Welcome to " + constants.APPLICATION_NAME
        _organization_name_text = "Organization Name: " + constants.ORGANIZATION_NAME
        self.first_label = ttk.Label(frame, text=_app_name_text, style="ApplicationLabel1.TLabel", anchor="center", padding=5)
        self.first_label.grid(row=0, column=0, sticky="ew")
        self.middle_label = ttk.Label(frame, text=_organization_name_text, style="OraganizationLabel1.TLabel", anchor="center", padding=5)
        self.middle_label.grid(row=1, column=0, sticky="ew")
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)        
    
    def bottom_frame_contents(self, frame, mysql):
        #Register Frame
        self.register_frame = register.Register(frame, mysql, lambda: self.raise_frame("Login"))
        
        #Login Frame
        self.login_frame = login.Login(frame, mysql, lambda: self.raise_frame("Register"), self)
        
        self.raise_frame("Login")

    #Put either login or register screen
    def raise_frame(self, class_name):
        if(class_name == "Login"):
            self.register_frame.grid_forget()
            self.login_frame.grid(row=0, column=0, padx=(10,10), pady=(10,10))
        else:
            self.login_frame.grid_forget()
            self.register_frame.grid(row=0, column=0, padx=(10,10), pady=(10,10))


