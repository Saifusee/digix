import tkinter as tk
from tkinter import ttk
from custom_styles import CustomStyle
from PIL import Image, ImageTk
from os import path
from CONSTANT.index import *

# Toplevel error modal
class ErrorModal(tk.Toplevel):
    def __init__(self, error_message, container=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        CustomStyle(self)
        self.title("ERROR!")
        self.geometry("450x150")
        self.resizable(False, False)
        try:
            self.image = path.join(PATH_TO_IMAGES, FILE_APP_LOGO)
            self.iconbitmap(self.image)
        except Exception:
            self.image = path.join(PATH_TO_IMAGES, FILE_APP_DEFAULT_LOGO)
            self.iconbitmap(self.image)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        
        self.grab_set()
        
        path_to_error_logo = path.join(PATH_TO_ROOT, "assets", FILE_ERROR_LOGO)
        _error_image = Image.open(path_to_error_logo)
        self.error_image_tk = ImageTk.PhotoImage(_error_image)
        
        # Creating Frames
        self._put_frames()
        
        # Renedering Labels in Frames
        self._render_labels(error_message)
        
        # Destroy the container
        if not (type(container) == None.__class__):
            container.destroy()
        else:
            pass
        
    def _put_frames(self):
        # Frames
        self.top_frame =ttk.Frame(self)
        self.top_frame.grid(row=0, column=0, sticky="nsew")
        self.top_frame.columnconfigure(0, weight=1)
        self.bottom_frame =ttk.Frame(self)
        self.bottom_frame.grid(row=1, column=0, sticky="nsew")
        self.bottom_frame.columnconfigure(0, weight=1)
        
    def _render_labels (self, message):
        # Labels
        self.label = ttk.Label(self.top_frame, image=self.error_image_tk, style="Errorlabel.TLabel")
        self.label.grid(row=0, column=0, sticky="nsew")
        self.label = ttk.Label(self.bottom_frame, text=message, style="Errorlabel.TLabel", wraplength=400)
        self.label.grid(row=1, column=0, sticky="nsew")
