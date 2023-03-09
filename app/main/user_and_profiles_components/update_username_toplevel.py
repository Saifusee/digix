import tkinter as tk
from tkinter import ttk
from CONSTANT.index import *
from os import path

class UpdateUsername(tk.Toplevel):
    def __init__(self, container, user_id, mysql, *args, **kwargs) -> None:
        super().__init__(container, *args, **kwargs)

        self.configure(background=TTK_FRAME_DEFAULT_BG_COLOR)
        self.grab_set()
        try:
            self.image = path.join(PATH_TO_IMAGES, FILE_APP_LOGO)
            self.iconbitmap(self.image)
        except Exception:
            self.image = path.join(PATH_TO_IMAGES, FILE_APP_DEFAULT_LOGO)
            self.iconbitmap(self.image)
            
        centerTkinterToplevel(container, self, dx=600, dy=200)
        self.geometry("400x200")
        self.resizable(False, False)

        self.columnconfigure(0, weight=1)
        self.input_data = tk.StringVar()

        lb0 = ttk.Label(self, text="Change Username", style="ChangeOrderStatusTitle.TLabel")
        lb0.grid(row=0, column=0, sticky="nsew")
        entry = ttk.Entry(self, textvariable=self.input_data, font=("TkdefaultFont", 10, "bold"))
        entry.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        button = ttk.Button(self, text="Update Username", command=lambda: self.submitCommand(user_id, mysql), style="SignButton.TButton")
        button.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        self.er_lb = ttk.Label(self, style="ErrorLoginRegisterLabel.TLabel")



    def submitCommand(self, user_id, mysql):
        self.er_lb.configure(style="ErrorLoginRegisterLabel.TLabel")
        if len(self.input_data.get().strip()) == 0:
            self.er_lb.configure(text="Field cannot be empty")
            self.er_lb.grid(row=3, column=0, sticky="nsew")
        elif not self.input_data.get().strip().isalnum():
            self.er_lb.configure(text="Username should be consist of alphanumeric values")
            self.er_lb.grid(row=3, column=0, sticky="nsew")
        else:
            qu_duplicate = f"SELECT `{USER_ID}` FROM `{DATABASE_NAME}`.`{USER_TABLE_NAME}` WHERE `{USERNAME}` = %s;"
            mysql.query.execute(qu_duplicate, (self.input_data.get().strip().lower(),))
            response = mysql.query.fetchall()
            # If duplicate usernames
            if len(response) > 0:
                if len(response) == 1:
                    if response[0][USER_ID] == int(user_id):
                        self.er_lb.configure(text="Given username is same as your current username")
                        self.er_lb.grid(row=3, column=0, sticky="nsew")
                    else:
                        self.er_lb.configure(text="Username already in used by other account")
                        self.er_lb.grid(row=3, column=0, sticky="nsew")
                else:
                    self.er_lb.configure(text="Username already in used by other account")
                    self.er_lb.grid(row=3, column=0, sticky="nsew")
            else: 
                # Update Username
                qu_main = f"UPDATE `{DATABASE_NAME}`.`{USER_TABLE_NAME}` SET `{USERNAME}` = %s WHERE `{USER_ID}` = {user_id};"
                mysql.query.execute(qu_main, (self.input_data.get().strip().lower(),))
                mysql.db_connection.commit()
                self.er_lb.configure(text="Username updated successfully, please relaunch application to see changes.", style="SuccessfulLoginRegisterLabel.TLabel")
                self.er_lb.grid(row=3, column=0, sticky="nsew")
