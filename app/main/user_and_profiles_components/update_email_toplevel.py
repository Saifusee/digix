import tkinter as tk
from tkinter import ttk
from CONSTANT.index import *
import mail.mail as mail
import threading
from random import randint
from os import path
import re
from error import ErrorModal

class UpdateEmail(tk.Toplevel):
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
        self.geometry("500x275")
        self.resizable(False, False)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.email_data = tk.StringVar()
        self.otp_data = tk.StringVar()
        self.otp_gen = ""
        self.otp_ref = ""

        lb0 = ttk.Label(self, text="Change E-Mail", style="ChangeOrderStatusTitle.TLabel")
        lb0.grid(row=0, column=0, columnspan=2, sticky="nsew")

        lb = ttk.Label(self, text="E-Mail: ", font=("TkdefaultFont", 10, "bold"), anchor="w")
        lb.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.email_entry = ttk.Entry(self, textvariable=self.email_data, font=("TkdefaultFont", 10, "bold"))
        self.email_entry.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        lb = ttk.Label(self, text="OTP: ", font=("TkdefaultFont", 10, "bold"), anchor="w")
        lb.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        self.otp_entry = ttk.Entry(self, textvariable=self.otp_data, state="disabled", font=("TkdefaultFont", 10, "bold"))
        self.otp_entry.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)
        self.button = ttk.Button(self, text="Submit E-Mail", command=lambda: self.submitEmail(user_id, mysql), style="SignButton.TButton")
        self.button.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        self.resend_button = ttk.Button(self, text="Resend E-Mail", command=lambda: self.submitEmail(user_id, mysql, snd_or_rsnd="again"), style="SignButton.TButton")

        self.er_lb = ttk.Label(self, style="ErrorLoginRegisterLabel.TLabel")


    # When submit Email
    def submitEmail(self, user_id, mysql, snd_or_rsnd=""):
        self.er_lb.configure(style="ErrorLoginRegisterLabel.TLabel")
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z]+\.[A-Z|a-z]{2,}\b'

        if len(self.email_data.get().strip()) == 0:
            self.er_lb.configure(text="E-Mial field cannot be empty")
            self.er_lb.grid(row=5, column=0, columnspan=2, sticky="nsew")
        elif (not re.fullmatch(email_regex, self.email_data.get().strip().lower())):
            self.er_lb.configure(text="Invalid E-Mail Syntax. Example = example123@gmail.com")
            self.er_lb.grid(row=5, column=0, columnspan=2, sticky="nsew")
        else:
            try:
                qu_duplicate = f"SELECT `{USER_ID}` FROM `{DATABASE_NAME}`.`{USER_TABLE_NAME}` WHERE `{EMAIL}` = %s;"
                mysql.query.execute(qu_duplicate, (self.email_data.get().strip().lower(),))
                response = mysql.query.fetchall()

                # If duplicate email
                if len(response) > 0:
                    if len(response) == 1:
                        if response[0][USER_ID] == int(user_id):
                            self.er_lb.configure(text="Given email is same as your current email")
                            self.er_lb.grid(row=5, column=0, columnspan=2, sticky="nsew")
                        else:
                            self.er_lb.configure(text="E-Mail already registered to other account")
                            self.er_lb.grid(row=5, column=0, columnspan=2, sticky="nsew")
                    else:
                        self.er_lb.configure(text="E-Mail already registered to other account")
                        self.er_lb.grid(row=5, column=0, columnspan=2, sticky="nsew")
                else:
                    self.email_entry.configure(state="disabled")
                    self.otp_entry.configure(state="normal")
                    # generate otp and save in database
                    self.otp_gen = randint(11111111, 99999999)
                    self.otp_ref = f"{self.otp_gen}{self.email_data.get().strip().lower()}{self.otp_gen}"
                    mysql.query.execute(f"""INSERT INTO {DATABASE_NAME}.{OTP_TABLE_NAME}
                                        ({OTP_REFERENCE}, {OTP_VALUE}) 
                                        VALUE (%s, %s)""", (self.otp_ref, self.otp_gen))
                    mysql.db_connection.commit()

                    # Send mail with OTP
                    message = f"Greetings from {getShopDetails()[SHOP_NAME]}, the OTP for E-Mail update verification is = {self.otp_gen}"
                    t_hread = threading.Thread(target=lambda: mail.DigixMail(self.email_data.get().strip().lower(), f"E-Mail Verification: {getShopDetails()[SHOP_NAME]}", message), name="SendOTPMailThread")
                    t_hread.start()

                    self.er_lb.configure(text=f"OTP sent successfully {snd_or_rsnd}. OTP is valid for next 5 minutes", style="SuccessfulLoginRegisterLabel.TLabel")
                    self.er_lb.grid(row=5, column=0, columnspan=2, sticky="nsew")
                    curent_otp_ref = self.otp_ref
                    # Delete OTP after 5 minutes
                    timer = threading.Timer(300, lambda: self.deleteOTP(mysql, curent_otp_ref))
                    timer.start()
                    self.button.configure(text="Submit OTP", command=lambda: self.submitOTP(user_id, mysql))
                    self.resend_button.grid(row=4, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

            except Exception as error:
                print(f"Development Error (Submiting  E-Mail and generating OTP): {error}")
                ErrorModal("Something went wrong, please contact the software developer")



    # When submit OTP
    def submitOTP(self, user_id, mysql):
        self.er_lb.configure(style="ErrorLoginRegisterLabel.TLabel")
        
        if len(self.otp_data.get().strip()) == 0:
            self.er_lb.configure(text="Field cannot be empty")
            self.er_lb.grid(row=5, column=0, columnspan=2, sticky="nsew")
        elif not self.otp_data.get().strip().isdigit():
            self.er_lb.configure(text="OTP is a numeric value")
            self.er_lb.grid(row=5, column=0, columnspan=2, sticky="nsew")
        else:
            try:
                otp_value = int(self.otp_data.get().strip())
                q = f"SELECT * FROM {DATABASE_NAME}.{OTP_TABLE_NAME} WHERE {OTP_REFERENCE} LIKE '{self.otp_ref}'"
                mysql.query.execute(q)
                otp_data = mysql.query.fetchone()

                # If OTP expires or not exist
                if type(otp_data) == None.__class__:                        
                    self.er_lb.configure(text="OTP expires or invalid, please try again.")
                    self.er_lb.grid(row=5, column=0, columnspan=2, sticky="nsew")
                else:
                    # If OTP is correct
                    if (otp_data["otp"] == otp_value):
                        # Update E-Mail
                        qu_main = f"UPDATE `{DATABASE_NAME}`.`{USER_TABLE_NAME}` SET `{EMAIL}` = %s WHERE `{USER_ID}` = {user_id};"
                        mysql.query.execute(qu_main, (self.email_data.get().strip().lower(),))
                        mysql.db_connection.commit()
                        self.er_lb.configure(text="E-Mail updated successfully, please relaunch application to see changes.", style="SuccessfulLoginRegisterLabel.TLabel")
                        self.er_lb.grid(row=5, column=0, columnspan=2, sticky="nsew")
                        self.otp_entry.configure(state="disabled")
                        self.button.configure(state="disabled")
                        self.resend_button.configure(state="disabled")

                        # Delete OTP
                        self.deleteOTP(mysql)

                    else:
                        self.er_lb.configure(text="Invalid OTP")
                        self.er_lb.grid(row=5, column=0, columnspan=2, sticky="nsew")
            except Exception as error:
                print(f"Development Error (Verifying OTP and updating E-Mail): {error}")
                ErrorModal("Something went wrong, please contact the software developer")



    # Delete OTP
    def deleteOTP(self, mysql, otp_ref):
        # Deleting the OTP from Database
        qw = f"DELETE FROM {DATABASE_NAME}.{OTP_TABLE_NAME} WHERE {OTP_REFERENCE} = %s"
        mysql.query.execute(qw, (otp_ref,))
        mysql.db_connection.commit()