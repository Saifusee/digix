import tkinter as tk
from tkinter import ttk
from CONSTANT.index import *
from os import path
import re

class UpdatePassword(tk.Toplevel):
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
        self.geometry("400x300")
        self.resizable(False, False)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.password_data = tk.StringVar()
        self.confirm_password_data = tk.StringVar()
        self.show_password_data = tk.IntVar()
        self.show_confirm_password_data = tk.IntVar()

        lb0 = ttk.Label(self, text="Change Password", style="ChangeOrderStatusTitle.TLabel")
        lb0.grid(row=0, column=0, columnspan=2, sticky="nsew")

        lb = ttk.Label(self, text="New Password: ", font=("TkdefaultFont", 10, "bold"), anchor="w")
        lb.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        entry_1 = ttk.Entry(self, textvariable=self.password_data, show="*", font=("TkdefaultFont", 10, "bold"))
        entry_1.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        # Show Password Checkbutton
        self.show_password_checkbox = ttk.Checkbutton(
            self,
            text="Show Password",
            variable=self.show_password_data,
            style="ShowPasswordCheckButton.TCheckbutton",
            command=lambda: self.toggleCheckButton(self.show_password_data.get(), entry_1)
            )
        self.show_password_checkbox.grid(row=2, column=0, sticky="w", padx=10, pady=(5,10))

        lb = ttk.Label(self, text="Confirm Password: ", font=("TkdefaultFont", 10, "bold"), anchor="w")
        lb.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)
        entry_2 = ttk.Entry(self, textvariable=self.confirm_password_data, show="*", font=("TkdefaultFont", 10, "bold"))
        entry_2.grid(row=3, column=1, sticky="nsew", padx=10, pady=10)
        # Show Password Checkbutton
        self.show_password_checkbox = ttk.Checkbutton(
            self,
            text="Show Password",
            variable=self.show_confirm_password_data,
            style="ShowPasswordCheckButton.TCheckbutton",
            command=lambda: self.toggleCheckButton(self.show_confirm_password_data.get(), entry_2)
            )
        self.show_password_checkbox.grid(row=4, column=0, sticky="w", padx=10, pady=(5,10))

        button = ttk.Button(self, text="Submit", command=lambda: self.submitCommand(user_id, mysql), style="SignButton.TButton")
        button.grid(row=5, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        self.er_lb = ttk.Label(self, style="ErrorLoginRegisterLabel.TLabel", wraplength=350)



    # Toggle to show/hide password value to user
    def toggleCheckButton(self, check_value, entry_instance):
        match check_value:
            case 1:
                entry_instance.configure(show="")
            case 0:
                entry_instance.configure(show="*")
            case _:
                entry_instance.configure(show="*")



    def submitCommand(self, user_id, mysql):
        self.er_lb.configure(style="ErrorLoginRegisterLabel.TLabel")
        password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,15}$"
        if len(self.password_data.get().strip()) == 0:
            self.er_lb.configure(text="Field 1 cannot be empty")
            self.er_lb.grid(row=6, column=0, columnspan=2, sticky="nsew")
        elif (not re.fullmatch(password_regex, self.password_data.get().strip())):
            self.er_lb.configure(text="Password in field 1 must be 8-15 characters, contain uppercase letter, lowercase letter, number and special symbold (@$!%*?&).)")
            self.er_lb.grid(row=6, column=0, columnspan=2, sticky="nsew")
        elif len(self.confirm_password_data.get().strip()) == 0:
            self.er_lb.configure(text="Field 2 cannot be empty")
            self.er_lb.grid(row=6, column=0, columnspan=2, sticky="nsew")
        elif (not re.fullmatch(password_regex, self.confirm_password_data.get().strip())):
            self.er_lb.configure(text="Password in field 2 must be 8-15 characters, contain uppercase letter, lowercase letter, number and special symbold (@$!%*?&).)")
            self.er_lb.grid(row=6, column=0, columnspan=2, sticky="nsew")
        elif not self.password_data.get().strip() == self.confirm_password_data.get().strip():
            self.er_lb.configure(text="Password didn't match")
            self.er_lb.grid(row=6, column=0, columnspan=2, sticky="nsew")
        else:
            qu_duplicate = f"SELECT `{USER_ID}` FROM `{DATABASE_NAME}`.`{USER_TABLE_NAME}` WHERE `{PASSWORD}` = %s;"
            mysql.query.execute(qu_duplicate, (self.password_data.get().strip(),))
            response = mysql.query.fetchall()

            flag = False
            for item in response:
                if int(item[USER_ID]) == int(user_id):
                    flag = True

            # If password same as old one
            if flag:
                self.er_lb.configure(text="New Password is same as old password")
                self.er_lb.grid(row=6, column=0, columnspan=2, sticky="nsew")
            else: 
                # Update Username
                qu_main = f"UPDATE `{DATABASE_NAME}`.`{USER_TABLE_NAME}` SET `{PASSWORD}` = %s WHERE `{USER_ID}` = {user_id};"
                mysql.query.execute(qu_main, (self.password_data.get().strip(),))
                mysql.db_connection.commit()
                self.er_lb.configure(text="Password changed successfully.", style="SuccessfulLoginRegisterLabel.TLabel")
                self.er_lb.grid(row=6, column=0, columnspan=2, sticky="nsew")
