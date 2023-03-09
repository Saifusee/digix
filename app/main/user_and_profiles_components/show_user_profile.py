import tkinter as tk
from tkinter import ttk
from CONSTANT.index import *
from error import ErrorModal
from app.main.user_and_profiles_components.show_user_logs import ShowUserLogs
from database.dbconnection import Connection
from app.base import Base

class ShowUserProfile(tk.Canvas):
    
    def __init__(self, container, current_user, *args, **kwargs):
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


        try:
            logged_in_user_id = current_user[USER_ID]
            mysql = Connection()
            mysql.query.execute(f"{Base.saved_query_user_morphed} WHERE `{USER_ID}` = {logged_in_user_id};")
            logged_in_user = mysql.query.fetchall()[0]

            lb_1 = ttk.Label(self.frame_overlap, text="-------------------- User Profile --------------------", relief="raised", padding=10, style="ProfileLabels.TLabel")
            lb_1.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

            lb_1 = ttk.Label(self.frame_overlap, text="User Id: ", style="ProfileLabels.TLabel")
            lb_1.grid(row=1, column=0, pady=10, padx=10)
            lb_2 = ttk.Label(self.frame_overlap, text=self.formatNone(logged_in_user[USER_ID]), style="ProfileLabels.TLabel")
            lb_2.grid(row=1, column=1, pady=10, padx=10)

            lb_1 = ttk.Label(self.frame_overlap, text="Username: ", style="ProfileLabels.TLabel")
            lb_1.grid(row=2, column=0, pady=10, padx=10)
            lb_2 = ttk.Label(self.frame_overlap, text=self.formatNone(logged_in_user[USERNAME]), style="ProfileLabels.TLabel")
            lb_2.grid(row=2, column=1, pady=10, padx=10)

            lb_1 = ttk.Label(self.frame_overlap, text="E-Mail: ", style="ProfileLabels.TLabel")
            lb_1.grid(row=3, column=0, pady=10, padx=10)
            lb_2 = ttk.Label(self.frame_overlap, text=self.formatNone(logged_in_user[EMAIL]), style="ProfileLabels.TLabel")
            lb_2.grid(row=3, column=1, pady=10, padx=10)

            lb_1 = ttk.Label(self.frame_overlap, text="Contact 1: ", style="ProfileLabels.TLabel")
            lb_1.grid(row=4, column=0, pady=10, padx=10)
            lb_2 = ttk.Label(self.frame_overlap, text=self.formatNone(logged_in_user[USER_CONTACT_1]), style="ProfileLabels.TLabel")
            lb_2.grid(row=4, column=1, pady=10, padx=10)

            lb_1 = ttk.Label(self.frame_overlap, text="Contact 2: ", style="ProfileLabels.TLabel")
            lb_1.grid(row=5, column=0, pady=10, padx=10)
            lb_2 = ttk.Label(self.frame_overlap, text=self.formatNone(logged_in_user[USER_CONTACT_2]), style="ProfileLabels.TLabel")
            lb_2.grid(row=5, column=1, pady=10, padx=10)

            lb_1 = ttk.Label(self.frame_overlap, text="Address: ", style="ProfileLabels.TLabel")
            lb_1.grid(row=6, column=0, pady=10, padx=10)
            lb_2 = ttk.Label(self.frame_overlap, text=self.formatNone(logged_in_user[USER_ADDRESS]), style="ProfileLabels.TLabel")
            lb_2.grid(row=6, column=1, pady=10, padx=10)

            lb_1 = ttk.Label(self.frame_overlap, text="User Authority: ", style="ProfileLabels.TLabel")
            lb_1.grid(row=7, column=0, pady=10, padx=10)
            lb_2 = ttk.Label(self.frame_overlap, text=self.formatNone(logged_in_user[USER_AUTHORITY]), style="ProfileLabels.TLabel")
            lb_2.grid(row=7, column=1, pady=10, padx=10)

            lb_1 = ttk.Label(self.frame_overlap, text="Employment Status: ", style="ProfileLabels.TLabel")
            lb_1.grid(row=8, column=0, pady=10, padx=10)
            lb_2 = ttk.Label(self.frame_overlap, text=self.formatNone(logged_in_user[EMPLOYMENT_STATUS]), style="ProfileLabels.TLabel")
            lb_2.grid(row=8, column=1, pady=10, padx=10)

            lb_1 = ttk.Label(self.frame_overlap, text="Date of Joining: ", style="ProfileLabels.TLabel")
            lb_1.grid(row=9, column=0, pady=10, padx=10)
            lb_2 = ttk.Label(self.frame_overlap, text=self.formatNone(logged_in_user[DATE_OF_JOINING], is_date=True), style="ProfileLabels.TLabel")
            lb_2.grid(row=9, column=1, pady=10, padx=10)

            lb_1 = ttk.Label(self.frame_overlap, text="Date of Leaving: ", style="ProfileLabels.TLabel")
            lb_1.grid(row=10, column=0, pady=10, padx=10)
            lb_2 = ttk.Label(self.frame_overlap, text=self.formatNone(logged_in_user[DATE_OF_LEAVING], is_date=True), style="ProfileLabels.TLabel")
            lb_2.grid(row=10, column=1, pady=10, padx=10)

            lb_1 = ttk.Label(self.frame_overlap, text="Date of Rehirirng: ", style="ProfileLabels.TLabel")
            lb_1.grid(row=11, column=0, pady=10, padx=10)
            lb_2 = ttk.Label(self.frame_overlap, text=self.formatNone(logged_in_user[DATE_OF_REHIRING], is_date=True), style="ProfileLabels.TLabel")
            lb_2.grid(row=11, column=1, pady=10, padx=10)

            show_user_logs_button = ttk.Button(
                self.frame_overlap,
                text="Show User Logs",
                command= lambda: ShowUserLogs(
                    self.frame_overlap,
                    mysql,
                    current_user,
                    logged_in_user_id
                ),
                style="SingleRecordLinkButton.TButton"
                )
            show_user_logs_button.grid(row=12, column=0, columnspan=2, sticky="ew", pady=10, padx=10)



        except Exception as error:
            print(f"Development Error (While Fetching logged_in_user Details): {error}")
            ErrorModal("Something went wrong.")



    # If there's no data to show
    def formatNone(self, value, is_date=False):
        if len(str(value)) == 0 or type(value) == None.__class__:
            return "----"
        elif is_date:
            return value.strftime("%b %m, %Y %H:%M%p")
        else:
            return value
        


    # Reset Page
    def customReset(self):
        pass