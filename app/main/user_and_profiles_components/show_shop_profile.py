import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from CONSTANT.index import *
from error import ErrorModal
from database.dbconnection import Connection

class ShowShopProfile(tk.Canvas):
    
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, width=700, height=800, *args, **kwargs)

        # self.columnconfigure(0, weight=1)

        # Vertical Scrollbar
        self.vscroll = ttk.Scrollbar(container, orient="vertical", command=self.yview)
        self.vscroll.grid(row=0, column=0, sticky="nse")
        self.config(yscrollcommand=self.vscroll.set)

        self.frame_overlap = ttk.Frame(self, style="MainFrameBackgroundFrame.TFrame", relief="sunken", border=20)
        self.frame_overlap.columnconfigure(0, weight=1)
        self.frame_overlap.columnconfigure(1, weight=1)
        # self.frame_overlap.grid(row=0, column=0, sticky="nsew")
        # Scrollbar works if Frame Rendered with create_window method of canvas
        self.create_window((0,0), window=self.frame_overlap, anchor="nw", tags="self.frame")
        
        ## Event Bindings on Frame
        # self.frame.grid(sticky="nsew") equivalent, bcz create_window doesn't alllow us to use sticky
        self.bind("<Configure>", lambda e: self.itemconfig("self.frame", width=e.width))
        # Making Frame Scrollable inside canvas region
        self.frame_overlap.bind("<Configure>", lambda e: self.configure(scrollregion=self.bbox("all")))


    

        lb_1 = ttk.Label(self.frame_overlap, text="-------------------- Organization's Profile --------------------", relief="raised", padding=10, style="ProfileLabels.TLabel")
        lb_1.grid(row=0, column=0, columnspan=2, pady=10, padx=10)
        # Show Logo
        # Accessing app logo but if not exist then raise error and show default logo
        try:
            app_logo_image = Image.open(path.join(PATH_TO_IMAGES, FILE_APP_LOGO))
        except Exception:
            app_logo_image = Image.open(path.join(PATH_TO_IMAGES, FILE_APP_DEFAULT_LOGO))
            
        resized_app_logo_image = app_logo_image.resize((115,115))
        path_to_app_logo = ImageTk.PhotoImage(resized_app_logo_image)
        
        self.logo_label = ttk.Label(
            self.frame_overlap,
            image=path_to_app_logo
        )
        self.logo_label.image =path_to_app_logo
        self.logo_label.grid(row=1, column=0, columnspan=2, sticky="ns", pady=15, padx=10)

        try:
            mysql = Connection()
            mysql.query.execute(f"SELECT * FROM `{DATABASE_NAME}`.`{SHOP_TABLE_NAME}` WHERE `{SHOP_ID}` = 1;")
            shop = mysql.query.fetchall()[0]

            lb_1 = ttk.Label(self.frame_overlap, text="Organizatin's Name: ", style="ProfileLabels.TLabel")
            lb_1.grid(row=2, column=0, pady=15, padx=10)
            lb_2 = ttk.Label(self.frame_overlap, text=self.formatNone(shop[SHOP_NAME]), style="ProfileLabels.TLabel")
            lb_2.grid(row=2, column=1, pady=15, padx=10)

            lb_1 = ttk.Label(self.frame_overlap, text="Organizatin's Owner: ", style="ProfileLabels.TLabel")
            lb_1.grid(row=3, column=0, pady=15, padx=10)
            lb_2 = ttk.Label(self.frame_overlap, text=self.formatNone(shop[SHOP_OWNER_NAME]), style="ProfileLabels.TLabel")
            lb_2.grid(row=3, column=1, pady=15, padx=10)

            lb_1 = ttk.Label(self.frame_overlap, text="Organizatin's Contact 1: ", style="ProfileLabels.TLabel")
            lb_1.grid(row=4, column=0, pady=15, padx=10)
            lb_2 = ttk.Label(self.frame_overlap, text=self.formatNone(shop[SHOP_CONTACT_1]), style="ProfileLabels.TLabel")
            lb_2.grid(row=4, column=1, pady=15, padx=10)

            lb_1 = ttk.Label(self.frame_overlap, text="Organizatin's Contact 2: ", style="ProfileLabels.TLabel")
            lb_1.grid(row=5, column=0, pady=15, padx=10)
            lb_2 = ttk.Label(self.frame_overlap, text=self.formatNone(shop[SHOP_CONTACT_2]), style="ProfileLabels.TLabel")
            lb_2.grid(row=5, column=1, pady=15, padx=10)

            lb_1 = ttk.Label(self.frame_overlap, text="Organizatin's E-Mail: ", style="ProfileLabels.TLabel")
            lb_1.grid(row=6, column=0, pady=15, padx=10)
            lb_2 = ttk.Label(self.frame_overlap, text=self.formatNone(shop[SHOP_EMAIL]), style="ProfileLabels.TLabel")
            lb_2.grid(row=6, column=1, pady=15, padx=10)

            lb_1 = ttk.Label(self.frame_overlap, text="Organizatin's GSTIN: ", style="ProfileLabels.TLabel")
            lb_1.grid(row=7, column=0, pady=15, padx=10)
            lb_2 = ttk.Label(self.frame_overlap, text=self.formatNone(shop[SHOP_GST_NUMBER]), style="ProfileLabels.TLabel")
            lb_2.grid(row=7, column=1, pady=15, padx=10)

            shop_address = self.formatNone(shop[SHOP_ADDRESS]) if len(self.formatNone(shop[SHOP_ADDRESS])) < 145 else f"{self.formatNone(shop[SHOP_ADDRESS])[:145]}...."
            lb_1 = ttk.Label(self.frame_overlap, text="Organizatin's Address: ", style="ProfileLabels.TLabel")
            lb_1.grid(row=8, column=0, pady=15, padx=10)
            lb_2 = ttk.Label(self.frame_overlap, text=shop_address, style="ProfileLabels.TLabel")
            lb_2.grid(row=8, column=1, pady=15, padx=10)

        except Exception as error:
            print(f"Development Error (While Fetching Shop Details): {error}")
            ErrorModal("Something went wrong.")



    # If there's no data to show
    def formatNone(self, value):
        if len(str(value)) == 0 or type(value) == None.__class__:
            return "----"
        else:
            return value  



    # Reset Page
    def customReset(self):
        pass