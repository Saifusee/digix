from tkinter import ttk
from CONSTANT.index import *
from app.main.user_and_profiles_components.show_user import ShowUser


# Note: We're not rendering this frame on grid until in main.py it was needed to
class User(ttk.Frame):
    def __init__(self, main_page_frame, mysql, user, *args, **kwargs):
        super().__init__(main_page_frame, *args, **kwargs)
        
        self.user = user
        
        # Category Frame Grid Cofiguration
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=9)
        self.columnconfigure(0, weight=1)
        
        # Rendering Frames
        self.renderFrame()
        
        # Rendering Contents of Top Frame
        self.contentForTreeviewFrame(mysql)



    def renderFrame(self):
        # Bottom Frame for Tab's Content
        self.bottom_frame = ttk.Frame(self)
        self.bottom_frame.columnconfigure(0, weight=1)
        self.bottom_frame.rowconfigure(0, weight=1)
        self.bottom_frame.grid(row=0, column=0, sticky="nsew")  


        
    def contentForTreeviewFrame(self, mysql):
        self.show_user_instance = ShowUser(self.bottom_frame, mysql, self.user)
        self.show_user_instance.grid(row=0, column=0, sticky="nsew")



    # Reset Page
    def customReset(self):
        self.show_user_instance.customReset()
        