import tkinter as tk
from tkinter import ttk
from CONSTANT.index import *
from app.base import Base
from os import path


class RecordBase(Base):
    def __init__(self, mysql, user, POPUP_TITLE, button_1_text="Edit", button_2_text="Delete", is_zero_button_needed=False):
        super().__init__(mysql, user)
        
        # Tk.Toplevel Configuration and Main Frame overlapping it completely
        self.mainAndItsConfiguration(mysql, POPUP_TITLE)
        
        # Rendering and configuring frame and its content above  
        self.buttonAndItsConfiguration(button_1_text, button_2_text, is_zero_button_needed)
        
        # Frame configuration for Canvas, Scrollbar and its contents
        self.canvasScrollbarAndItsConfiguration()
        
        
        
    # Toplevel and Main Frame Basic Configuration  
    def mainAndItsConfiguration(self,mysql, POPUP_TITLE):
        # SQL Instance
        self.mysql = mysql
        # Popup Title Constant 
        self.POPUP_TITLE = POPUP_TITLE
        # Toplevel Grid Configuration
        self.title(self.POPUP_TITLE)
        
        try:
            self.image = path.join(PATH_TO_IMAGES, FILE_APP_LOGO)
            self.iconbitmap(self.image)
        except Exception:
            self.image = path.join(PATH_TO_IMAGES, FILE_APP_DEFAULT_LOGO)
            self.iconbitmap(self.image)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        # Frame to overlap Toplevel Completely
        self.popup_background_frame = tk.Frame(self, background=SINGLE_RECORD_DISPLAY_BACKGROUND, padx=(10), pady=(10))
        self.popup_background_frame.rowconfigure(0, weight=1)
        self.popup_background_frame.rowconfigure(1, weight=99)
        self.popup_background_frame.columnconfigure(0, weight=1)
        self.popup_background_frame.grid(row=0, column=0, sticky="nsew")
    
    
    
    # Rendering and configuring frame and its content above    
    def buttonAndItsConfiguration(self, button_1_text, button_2_text, is_zero_button_needed):
        if type(button_2_text) == None.__class__:
            pass
        else:
            # Frame above Canvas
            button_frame = tk.Frame(self.popup_background_frame, background=SINGLE_RECORD_DISPLAY_LABEL_FOREGROUND, padx=(10), pady=(10))
            button_frame.columnconfigure(0, weight=1)
            button_frame.columnconfigure(1, weight=1)
            button_frame.grid(row=0, column=0, sticky="nsew")
            # Edit and Delete Buttons
            # When no buttons needed
            if is_zero_button_needed:
                pass
            # When buttons needed
            else:
                self.button_1 = ttk.Button(button_frame, text=button_1_text, command=self.commandButton1, style="LoginRegisterButton.TButton")
                self.button_2 = ttk.Button(button_frame, text=button_2_text, command=self.commandButton2, style="ResetCancelButton.TButton")
                self.button_1.grid(row=0, column=0, sticky="ns")
                self.button_2.grid(row=0, column=1, sticky="ns")
        
        
        
    # Frame configuration for Canvas, Scrollbar and its contents
    def canvasScrollbarAndItsConfiguration(self):
        
        # Frame to render Canvas on it
        canvas_background_frame = tk.Frame(self.popup_background_frame, background="black", padx=(10), pady=(10))
        canvas_background_frame.rowconfigure(0, weight=1)
        canvas_background_frame.grid(row=1, column=0, sticky="ns")
        
        # Canvas, so we can add scrollbar
        self.canvas = tk.Canvas(canvas_background_frame, width=SINGLE_RECORD_DISPLAY_LABEL_WRAPLENGTH+250)
        self.canvas.columnconfigure(0, weight=1)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        
        # Vertical Scrollbar
        self.vscroll = ttk.Scrollbar(canvas_background_frame, orient="vertical", command=self.canvas.yview)
        self.vscroll.grid(row=0, column=1, sticky="ns")
        self.canvas.config(yscrollcommand=self.vscroll.set)
        
        # Frame to overlap Canvas completely
        self.frame = tk.Frame(self.canvas)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        # Scrollbar works if Frame Rendered with create_window method of canvas
        self.canvas.create_window((0,0), window=self.frame, anchor="nw", tags="self.frame")
        
        ## Event Bindings on Frame
        # self.frame.grid(sticky="nsew") equivalent, bcz create_window doesn't alllow us to use sticky
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig("self.frame", width=e.width))
        # Making Frame Scrollable inside canvas region
        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        # Mouse Scroll above Toplevel contents
        self.bind("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1*(e.delta/120)), "units"))    
    
    

    
# CLabel Class for Custom Label for Single Record Display    
class CLabel(tk.Label):
    def __init__(self, container, wrap=SINGLE_RECORD_DISPLAY_LABEL_WRAPLENGTH, *args, **kwargs):
        """tk.Label class with pre-defined styling for single record display,
        because ttk.Label doesn't have wraplength we are using this. 
        styles includes:-
            foreground,
            background,
            font,
            pady,
            padx,
            wraplength,
        """
        
        # Styling for tk.Label
        super().__init__(
            container,
            foreground=SINGLE_RECORD_DISPLAY_LABEL_FOREGROUND, 
            background=SINGLE_RECORD_DISPLAY_BACKGROUND,
            pady=(10),
            padx=(10),
            wraplength=wrap,
            borderwidth=5,
            relief="sunken",
            *args,
            **kwargs
            )