
from tkinter import ttk
from CONSTANT.index import *
from CONSTANT.index import EMAIL, USERNAME
from PIL import Image, ImageTk

class SidebarProfile():
    def __init__(self, app_window, frame, user):
        
        self.user = user
        frame.columnconfigure(0, weight=1)
        
        try:
            app_logo_image = Image.open(path.join(PATH_TO_IMAGES, FILE_APP_LOGO))
        except Exception:
            app_logo_image = Image.open(path.join(PATH_TO_IMAGES, FILE_APP_DEFAULT_LOGO))
        
        resized_app_logo_image = app_logo_image.resize((90,90)) #90, 75
        path_to_app_logo = ImageTk.PhotoImage(resized_app_logo_image)
        
        self.logo_label = ttk.Label(
            frame,
            image=path_to_app_logo,
        )
        self.logo_label.image =path_to_app_logo
        self.logo_label.grid()
        
        self.profile_label_1 = ttk.Label(
            frame,
            text=f"{self.user[USERNAME]}",
            style="SidebarProfileLabel.TLabel",
            font=("TkDefaultFont", 15, "bold")
        )
        self.profile_label_1.grid()
        
        self.profile_label_2 = ttk.Label(
            frame,
            text=f"({self.user[EMAIL]})",
            style="SidebarProfileLabel.TLabel",
            font=("TkDefaultFont", 10)
        )
        self.profile_label_2.grid()

        
        
