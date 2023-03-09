import tkinter as tk
from tkinter import StringVar, ttk
from CONSTANT.index import *
from custom_styles import CustomStyle
from app.sidebar.sidebar_profile import SidebarProfile
from app.sidebar.sidebar_button import SidebarButton
from app.main.main import Main
from error import *

class AppWindow(tk.Tk):
    def __init__(self, user, mysql, *args, **kwargs):
        try:
            super().__init__(*args, **kwargs)
            
            CustomStyle(self)
            self.title(getShopDetails()[SHOP_NAME])
            self.geometry("1500x1500")
            
            try:
                self.image = path.join(PATH_TO_IMAGES, FILE_APP_LOGO)
                self.iconbitmap(self.image)
            except Exception:
                self.image = path.join(PATH_TO_IMAGES, FILE_APP_DEFAULT_LOGO)
                self.iconbitmap(self.image)

            
            # self.attributes('-fullscreen', True) #Gives App fullscreen view
            self.state('zoomed') # Open App fullscreen in maximize window  
                
            # User Detail recieved after Successful Authentication
            self.user = user
            
            # Configuration for App Grid
            self.columnconfigure(1, weight=2)
            self.rowconfigure(0, weight=1)
            
            
            # Putting Parents Frames for App
            self.put_app_frames()
            
            # Putting Main Page and its components
            self.put_main(user, mysql)
            
            # Putting Sidebar and its components
            self._put_sidebar()

            self.mainloop()
        except Exception:
            self.destroy()
            raise Exception()

        
        
    def put_app_frames(self):
        # Left hand side frame for Sidebar
        self.side_bar_frame = ttk.Frame(self, style="SideBarButtonFrame.TFrame")
        self.side_bar_frame.grid(row=0, column=0, sticky="nsew")
        
        # Right hand side frame for Main App Content
        self.main_page_frame = ttk.Frame(self, style="MainFrameBackgroundFrame.TFrame", padding=5)
        self.main_page_frame.grid(row=0, column=1, sticky="nsew")
        
        
    def put_main(self, user, mysql):
        # Main Page Background Frame  Grid Configuration
        self.main_page_frame.rowconfigure(0, weight=1)
        self.main_page_frame.columnconfigure(0, weight=1)
        self.main_page_instance = Main(self.main_page_frame, user, mysql)
        
        
    # Putting Sidebar Frame and its component
    def _put_sidebar(self):
        # Putting Sidebar Frame
        
        # Side Bar Grid Configuration
        self.side_bar_frame.columnconfigure(0, weight=1)
        self.side_bar_frame.rowconfigure(0,weight=1)
        self.side_bar_frame.rowconfigure(1,weight=99)

        # Frames for Main App Window Side Window
        # # Frame for Profile
        self.side_bar_profile_frame = ttk.Frame(self.side_bar_frame, style="SidebarProfileFrame.TFrame")
        self.side_bar_profile_frame.grid(row=0, column=0, sticky="nsew")
        
        # # Frame for Button
        self.side_bar_button_frame = ttk.Frame(self.side_bar_frame, style="SideBarButtonFrame.TFrame")
        self.side_bar_button_frame.grid(row=1, column=0, sticky="nsew")
        
        # Contents for Sidebar Profile and Buttons
        SidebarProfile(self, self.side_bar_profile_frame, self.user)
        
        SidebarButton(self, self.side_bar_button_frame, self.main_page_instance, self.user)
        