import tkinter as tk
from tkinter import ttk
from CONSTANT.index import *
from app.main.user_and_profiles_components.show_user_profile import ShowUserProfile
from app.main.user_and_profiles_components.edit_user_profile import EditUserProfile



# Note: We're not rendering this frame on grid until in main.py it was needed to
class UserProfile(ttk.Frame):
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

        # Rendering Show User Profile
        self.commandShowProfile()

    def renderFrames(self):
        # Top Frame for Tabs
        self.top_frame = ttk.Frame(self)
        self.top_frame.columnconfigure(0, weight=1)
        self.top_frame.columnconfigure(1, weight=1)
        self.top_frame.columnconfigure(2, weight=1)
        self.top_frame.columnconfigure(3, weight=1)
        self.top_frame.rowconfigure(0, weight=1)
        self.top_frame.grid(row=0, column=0, sticky="nse")  
        
        # Bottom Frame for Tab's Content
        self.bottom_frame = ttk.Frame(self)
        self.bottom_frame.columnconfigure(0, weight=1)
        self.bottom_frame.rowconfigure(0, weight=1)
        self.bottom_frame.grid(row=0, column=0, sticky="ns") 
        


    def contentForTopFrame(self):
        self.head_button = tk.Button(self.top_frame,
                                             background="#ff3333",
                                             activebackground=SIDEBAR_BUTTON_ACTIVE_BACKGROUND,
                                             activeforeground=SIDEBAR_BUTTON_ACTIVE_FOREGROUND,
                                             font=CATEGORY_PAGE_TAB_BUTTON_FONT,
                                             padx=8,
                                             pady=8
                                             )
        self.head_button.grid(row=0, column=0, columnspan=4, sticky="ne")
        
        

        
    def contentForBottomFrame(self, mysql):
        self.show_user_profile_instance = ShowUserProfile(self.bottom_frame, self.user)
        self.edit_user_profile_instance = EditUserProfile(self.bottom_frame, mysql, self.user)


        
    def commandShowProfile(self):
        self.customReset()
        # Modifying Button Settings
        self.head_button.configure(text="Edit Profile", command=self.commandEditProfile)
        self.edit_user_profile_instance.grid_forget()
        self.show_user_profile_instance.grid(row=0, column=0, sticky="ns")
    
    def commandEditProfile(self):
        self.customReset()
        # Modifying Button Settings
        self.head_button.configure(text="Profile", command=self.commandShowProfile)
        self.show_user_profile_instance.grid_forget()
        self.edit_user_profile_instance.grid(row=0, column=0, sticky="ns")
        
        
    # Reset Page
    def customReset(self):
        self.show_user_profile_instance.customReset()
        self.edit_user_profile_instance.customReset()
        