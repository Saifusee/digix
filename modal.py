import tkinter as tk
from tkinter import ttk
from custom_styles import CustomStyle
from os import path
from CONSTANT.index import *

# Toplevel class help in making multilevel popup and require parent window
class Modal(tk.Toplevel):
    def __init__(self, container, modal_message, confirmationMethod=None, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        # Freezing all other windows until Modal is close
        self.grab_set()
        
        CustomStyle(self)

        if type(container) == None.__class__:
            pass
        else:
            centerTkinterToplevel(container, self)

        if confirmationMethod != None:
            # Method to call when user press confirm button
            self.confirmationMethod = confirmationMethod
        else:
            self.confirmationMethod = None
        
        # Two Rows of App Window cover whole area one for label and other for button
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        
        # App Window Configuration
        self.title(getShopDetails()[SHOP_NAME])
        self.geometry("450x100")
        self.resizable(False, False)
        try:
            self.image = path.join(PATH_TO_IMAGES, FILE_APP_LOGO)
            self.iconbitmap(self.image)
        except Exception:
            self.image = path.join(PATH_TO_IMAGES, FILE_APP_DEFAULT_LOGO)
            self.iconbitmap(self.image)
        self.columnconfigure(0, weight=1)
        
        # Declaring and configuring all frames
        self.putFrames()

        # Rendering Modal Message Label
        self.putLabels(modal_message)
        
        # Rendering Modal Buttons
        self.putButtons()
        
        
        self.mainloop()

    def putFrames(self):
        # Frame for Modal Message
        self.top_frame =ttk.Frame(self)
        self.top_frame.grid(row=0, column=0, sticky="nsew")
        self.top_frame.columnconfigure(0, weight=1)
        
        # Frame for Buttons
        self.bottom_frame =ttk.Frame(self)
        self.bottom_frame.grid(row=1, column=0, sticky="nsew")
        self.bottom_frame.columnconfigure(0, weight=1)
        self.bottom_frame.columnconfigure(1, weight=1)
        
    def putLabels(self, modal_message):
        # Modal Message Label
        self.modal_label = ttk.Label(self.top_frame, text=modal_message, style="Errorlabel.TLabel", wraplength=300)
        self.modal_label.grid(row=0, column=0, sticky="nsew")
        
    def putButtons(self):
        if type(self.confirmationMethod) == None.__class__:
            pass
        else:
            # Confirm Button
            self.confirm_button = ttk.Button(self.bottom_frame, text="Confirm", command=self.commandConfirmModal, style="SignButton.TButton")
            self.confirm_button.grid(row=0, column=0)
            
            # Cancel Button
            self.cancel_button = ttk.Button(self.bottom_frame, text="Cancel", command=self.commandCancelModal, style="ResetCancelButton.TButton")
            self.cancel_button.grid(row=0, column=1)

    def commandCancelModal(self):
        # Unfreezing all other windows
        self.grab_release()
        self.destroy()

    def commandConfirmModal(self):
        # Unfreezing all other windows
        self.grab_release()
        # First Destroy Modal
        self.destroy()
        
        if self.confirmationMethod != None:
            self.confirmationMethod()