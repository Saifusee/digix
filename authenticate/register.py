import re
import tkinter as tk
from tkinter import StringVar, ttk
from authenticate.authenticate_base import AuthenticateBase
from CONSTANT.index import *
import mysql.connector as db
import mail.mail as mail
from random import randint
import threading
from error import ErrorModal


class Register(ttk.Frame, AuthenticateBase):
    def __init__(self, container, mysql, raise_login_frame, window_instance, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        self.errors = StringVar()
        self.c_email = bool(False)
        self.c_username = bool(False)
        self.c_password = bool(False)
        self.c_otp = bool(False)
        self.username_value = tk.StringVar()
        self.email_value = tk.StringVar()
        self.password_value = tk.StringVar()
        self.otp_value = tk.StringVar()
        self.show_p_value = tk.IntVar()
        self.otp_ref = ""
        self.thread_flag = False
        self.after_id = 0
        self.mysql = mysql
        self.window_instance = window_instance
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        #FRAMES
        top_frame = ttk.Frame(self, padding=10)
        top_frame.grid(row=0, column=0)
        middle_frame = ttk.Frame(self, padding=10)
        middle_frame.grid(row=1, column=0)
        bottom_frame = ttk.Frame(self, padding=10)
        bottom_frame.grid(row=2, column=0)
        self.bottom_error_frame = ttk.Frame(self, height=1000)
        self.bottom_error_frame.grid(row=3, column=0)
        
        #Error Frame and its content
        self.bottom_error_frame.columnconfigure(0, weight=1)
        self.bottom_error_frame.rowconfigure(0, weight=1)
        self.error_label = ttk.Label(self.bottom_error_frame, textvariable=self.errors, wraplength=350, style="ErrorLoginRegisterLabel.TLabel")
        self.error_label.grid()

        #PAGE HEADING
        page_label = ttk.Label(top_frame, padding=10, text="REGISTER PAGE", style="PageHeadingLabel.TLabel", anchor="center")
        page_label.grid(rowspan=2, sticky="ew")
        
        #PUTTING LABEL AND FIELD
        self.put_labels_and_fields(middle_frame)

        #PUTTING BUTTONS
        self.put_buttons(bottom_frame, raise_login_frame)

    def put_labels_and_fields(self, frame):
        
        #EMAIL LABEL AND FIELD
        self.email_label = ttk.Label(frame, text="E-Mail: ", style="LoginLabel.TLabel")
        self.email_label.grid(row=0, column=0, sticky="w")
        self.email_entry = ttk.Entry(frame, width=40, textvariable=self.email_value, font=('TkDefaultFont', 10))
        self.email_entry.grid(row=0, column=1, padx=(10,10), pady=(10,10))
        self.email_entry.bind("<KeyRelease>", self.validate_email)
        self.email_entry.bind("<FocusOut>", self.validate_email)
        
        #OTP LABEL AND FIELD
        self.otp = ttk.Label(frame, text="OTP: ", style="LoginLabel.TLabel")
        self.otp_entry = ttk.Entry(frame, width=40, textvariable=self.otp_value, font=('TkDefaultFont', 10))
        self.otp_entry.bind("<KeyRelease>", self.validate_otp)
        self.otp_entry.bind("<FocusOut>", self.validate_otp)
        
        #OTP Button
        self.email_otp_button = ttk.Button(frame, text="Submit E-Mail for OTP", command=self.submit_only_email)
        self.otp_otp_button = ttk.Button(frame, text="Submit OTP", command=self.submit_only_otp)
        self.edit_email_button = ttk.Button(frame, text="Edit Email", command=self.edit_email_again)
        self.email_otp_button["state"] = "disabled"
        self.otp_otp_button["state"] = "disabled"
        self.email_otp_button.grid(row=2, column=0, columnspan=2, sticky="nsew")
        
        # USERNAME LABEL AND FIELD
        self.username_label = ttk.Label(frame, text="Username: ", style="LoginLabel.TLabel")
        self.username_label.grid(row=3, column=0, sticky="w")
        self.username_entry = ttk.Entry(frame, width=40, textvariable=self.username_value, font=('TkDefaultFont', 10))
        self.username_entry.grid(row=3, column=1, padx=(10,10), pady=(10,10))
        self.username_entry["state"] = "disabled"
        self.username_entry.bind("<KeyRelease>", self.validate_username)
        self.username_entry.bind("<FocusOut>", self.validate_username)
        
        
        # PASSWORD LABEL AND FIELD
        self.password = ttk.Label(frame, text="Password: ", style="LoginLabel.TLabel")
        self.password.grid(row=4, column=0, sticky="w")
        self.password_entry = ttk.Entry(frame, width=40, show="*", textvariable=self.password_value, font=('TkDefaultFont', 10))
        self.password_entry.grid(row=4, column=1, padx=(10,10), pady=(10,10))
        self.password_entry["state"] = "disabled"
        self.password_entry.bind("<KeyRelease>", self.validate_password)
        self.password_entry.bind("<FocusOut>", self.validate_password)

        # Show Password Checkbutton
        self.show_password_checkbox = ttk.Checkbutton(
            frame,
            text="Show Password",
            variable=self.show_p_value,
            style="ShowPasswordCheckButton.TCheckbutton",
            command=lambda: self.toggleCheckButton(self.show_p_value.get(), self.password_entry),
            state="disabled"
            )
        self.show_password_checkbox.grid(row=5, column=0, sticky="w", padx=(10, 10), pady=(5, 10))


    def put_buttons(self, frame, raise_login_frame):
        #SUBMIT BUTTON
        self.submit_button = ttk.Button(frame, text="Submit", command=self.submit_function, style="LoginRegisterButton.TButton")
        self.submit_button.grid(row=0, column=0, padx=(10,10))
        self.submit_button["state"] = "disabled"
        
        #RESET BUTTON
        self.reset_button = ttk.Button(frame, text="Reset", command=self.reset_field_data, style="ResetCancelButton.TButton")
        self.reset_button.grid(row=0, column=1, padx=(10,10))
        
        #TOGGLE BUTTON FOR SIGNUP AND SIGNIN
        self.toggle_frame_button = ttk.Button(frame, text="Sign In", command=lambda: [raise_login_frame(), self.reset_field_data()], style="SignButton.TButton")
        self.toggle_frame_button.grid(row=0, column=2, padx=(10,10))
        

    # Toggle to show/hide password value to user
    def toggleCheckButton(self, check_value, entry_instance):
        match check_value:
            case 1:
                entry_instance.configure(show="")
            case 0:
                entry_instance.configure(show="*")
            case _:
                entry_instance.configure(show="*")


    def reset_field_data(self):
        # self.otp_otp_button.grid_forget()
        self.email_value.set("")
        self.password_value.set("")
        self.username_value.set("")
        self.otp_value.set("")
        self.errors.set("")
        self.show_p_value.set(0)
        self.username_entry["style"] = "TEntry"
        self.email_entry["style"] = "TEntry"
        self.password_entry["style"] = "TEntry"
        self.otp_entry["style"] = "TEntry"
        self.email_entry["state"] = "normal"
        self.username_entry["state"] = "disabled"
        self.password_entry["state"] = "disabled"
        self.show_password_checkbox.configure(state="disabled")
        self.email_otp_button["state"] = "disabled"
        self.otp_otp_button["state"] = "disabled"
        self.submit_button["state"] = "disabled"
        self.otp.grid_forget()
        self.otp_entry.grid_forget()
        self.otp_otp_button.grid_forget()
        self.edit_email_button.grid_forget()
        self.email_otp_button.grid(row=2, column=0, columnspan=2, sticky="nsew")
        self.error_label["style"]="ErrorLoginRegisterLabel.TLabel"
        
    def edit_email_again(self): # Edit Email Again after otp send
        self.otp_value.set("")
        self.otp.grid_forget()
        self.otp_entry.grid_forget()
        self.otp_otp_button.grid_forget()
        self.edit_email_button.grid_forget()
        self.errors.set("")
        self.email_otp_button.grid(row=2, column=0, columnspan=2, sticky="nsew")
        self.email_entry["state"] = "normal"
        
        
    def validate_email(self, event):
        # Terminating After Method if active
        if self.thread_flag:
            self.after_cancel(self.after_id)
            
        email_value = self.email_value.get().strip()
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z]+\.[A-Z|a-z]{2,}\b'
        parameter_false_tuple = ("email", False, self.email_entry, "ErrorEntry.TEntry", self.on_invalid)
        parameter_true_tuple = ("email", True, self.email_entry, "TEntry", self.enable_submit_button)
        self.error_label["style"] = "ErrorLoginRegisterLabel.TLabel"
        if (email_value == ""):
            self._validation_fail("E-Mail field cannot be empty", *parameter_false_tuple)
            self.email_otp_button["state"] = "disabled"
        elif (not re.fullmatch(email_regex, email_value)):
            self._validation_fail("Invalid E-Mail Syntax. Example = example123@gmail.com", *parameter_false_tuple)
            self.email_otp_button["state"] = "disabled"
        else:
            self.email_otp_button["state"] = "normal"
            self._validation_fail("", *parameter_true_tuple)
        return
        
    def validate_username(self, event):
        # Terminating After Method if active
        if self.thread_flag:
            self.after_cancel(self.after_id)
            
        username_value = self.username_value.get().strip()
        parameter_false_tuple = ("username", False, self.username_entry, "ErrorEntry.TEntry", self.on_invalid)
        parameter_true_tuple = ("username", True, self.username_entry, "TEntry", self.enable_submit_button)
        if (username_value == ""):
            self._validation_fail("Username field cannot be empty", *parameter_false_tuple)
        elif (not username_value.isalnum()):
            self._validation_fail("Username can only contain alphanumeric characters", *parameter_false_tuple)
        else:
            self._validation_fail("", *parameter_true_tuple)
        return
    
    def validate_password(self, event):
        # Terminating After Method if active
        if self.thread_flag:
            self.after_cancel(self.after_id)
            
        password_value = self.password_value.get().strip()
        password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,15}$"
        parameter_false_tuple = ("password", False, self.password_entry, "ErrorEntry.TEntry", self.on_invalid)
        parameter_true_tuple = ("password", True, self.password_entry, "TEntry", self.enable_submit_button)
        if (password_value == ""):
            self._validation_fail("Password field cannot be empty", *parameter_false_tuple)
        elif (not re.fullmatch(password_regex, password_value)):
            p_e_text = "Password must contain 8-15 characters, uppercase letter, lowercase letter, number and special symbold (@$!%*?&).)"
            self._validation_fail(p_e_text, *parameter_false_tuple)
        else:
            self._validation_fail("", *parameter_true_tuple)
        return   
    
    def submit_only_email(self): # When EMAIL submit for OTP
        try: 
            # enable and diable relevant fields
            self.email_entry["state"] = "disabled"
            
            self.otp.grid(row=1, column=0, sticky="w")
            self.otp_entry.grid(row=1, column=1, padx=(10,10), pady=(10,10))
            self.email_otp_button.grid_forget()
            self.otp_otp_button.grid(row=2, column=1, sticky="nsew")
            self.edit_email_button.grid(row=2, column=0, sticky="nsew")
            
            # generate otp and save in database
            self.otp_gen = randint(11111111, 99999999)
            self.otp_ref = f"{self.otp_gen}{self.email_value.get().strip()}{self.otp_gen}"
            self.mysql.query.execute(f"""INSERT INTO {DATABASE_NAME}.{OTP_TABLE_NAME}
                                ({OTP_REFERENCE}, {OTP_VALUE}) 
                                VALUE (%s, %s)""", (self.otp_ref, self.otp_gen))
            self.mysql.db_connection.commit()
        except Exception as errors:
            print(f"Development Error (Inserting OTP in Database): {errors}")
            ErrorModal("Something went wrong, please try again.", self.window_instance)
        
        # send email with otp
        try:
            message = f"Welcome to {getShopDetails()[SHOP_NAME]}, the OTP for E-Mail verification is = {self.otp_gen}"
            t_hread =threading.Thread(target=lambda: mail.DigixMail(self.email_value.get().strip(), f"E-Mail Verification: {getShopDetails()[SHOP_NAME]}", message), name="SendOTPMailThread")
            t_hread.start()
            self.error_label["style"] = "SuccessfulLoginRegisterLabel.TLabel"
            self.errors.set("OTP sent successfully, OTP is valid for next 5 minutes")
            curent_otp_ref = self.otp_ref
            # Delete OTP after 5 minutes
            timer = threading.Timer(300, lambda: self.deleteOTP(curent_otp_ref))
            timer.start()
        except Exception as errors:
            print(f"Development Error (Sending Email with OTP): {errors}")
            ErrorModal("Something went wrong, please try again.", self.window_instance)

    def submit_only_otp(self): # When OTP submit for EMAIL verification
        try:
            otp_value = int(self.otp_value.get().strip())
            query = f"SELECT * FROM {DATABASE_NAME}.{OTP_TABLE_NAME} WHERE {OTP_REFERENCE} LIKE '{self.otp_ref}'"
            self.mysql.query.execute(query)
            otp_data = self.mysql.query.fetchone()
            
            # If otp is deleted or missing
            if type(otp_data) == None.__class__:
                self.errors.set("OTP expired or invalid.")
            else:
                if (otp_data["otp"] == otp_value):
                    self.otp.grid_forget()
                    self.otp_entry.grid_forget()
                    self.otp_otp_button.grid_forget()
                    self.edit_email_button.grid_forget()
                    self.username_entry["state"] = "normal"
                    self.password_entry["state"] = "normal"
                    self.show_password_checkbox.configure(state="normal")
                else:
                    self.errors.set("Incorrect OTP")
        except Exception as errors:
            print(f"Development Error: {errors}")
            ErrorModal("Something went wrong, please try again.", self.window_instance)
            
    def validate_otp (self, event):
        # Terminating After Method if active
        if self.thread_flag:
            self.after_cancel(self.after_id)
            
        otp_value = self.otp_value.get().strip()
        otp_regex = r"^([0-9]){8}$" #for exact 8 digit numbers
        self.error_label["style"] = "ErrorLoginRegisterLabel.TLabel"
        parameter_false_tuple = ("otp", False, self.otp_entry, "ErrorEntry.TEntry", self.on_invalid)
        parameter_true_tuple = ("otp", True, self.otp_entry, "TEntry", self.enable_submit_button)
        if (otp_value == ""):
            self._validation_fail("OTP field cannot be empty", *parameter_false_tuple)
            self.otp_otp_button["state"] = "disabled"
        elif (not re.fullmatch(otp_regex, otp_value)):
            o_e_text = "OTP must be 8 digit numeric value"
            self._validation_fail(o_e_text, *parameter_false_tuple)
            self.otp_otp_button["state"] = "disabled"
        else:
            self._validation_fail("", *parameter_true_tuple)
            self.otp_otp_button["state"] = "normal"
        return
        
    def on_invalid(self):
        self.submit_button["state"] = "disabled"

    def enable_submit_button(self):
        if (self.c_email and self.c_username and self.c_password and self.c_otp):
            self.submit_button["state"] = "normal"

    def deleteOTP(self, otp_ref):
        query2 = f"DELETE FROM {DATABASE_NAME}.{OTP_TABLE_NAME} WHERE {OTP_REFERENCE} = %s"
        self.mysql.query.execute(query2, (otp_ref,))
        self.mysql.db_connection.commit()
            
    def submit_function(self):
        try: 
            email_value = self.email_value.get().strip().lower()
            username = self.username_value.get().strip().lower()
            password = self.password_value.get().strip()
            query = f"""INSERT INTO {DATABASE_NAME}.{USER_TABLE_NAME}
                    ({EMAIL}, {USERNAME}, {PASSWORD}) 
                    VALUES (%s, %s, %s)"""
            self.mysql.query.execute(query, (email_value, username, password))
            self.mysql.db_connection.commit()
            
            otp_ref = self.otp_ref
            self.deleteOTP(otp_ref)
            
            self.errors.set("Registration Successful.")
            self.submit_button["state"] = "disabled"
            self.error_label["style"] = "SuccessfulLoginRegisterLabel.TLabel"
            self.after_id = self.after(5000, self.reset_field_data)
            self.thread_flag = True
        except db.Error as error:
            if(error.msg == f"Duplicate entry '{self.email_value.get().strip()}' for key 'email'"):
                self.errors.set("E-Mail already registerd with another user.")
            elif(error.msg == f"Duplicate entry '{self.username_value.get().strip()}' for key 'username'"):
                self.errors.set("Username already registerd with another user.")
            else:
                self.errors.set("Error: Something went wrong. Try again later.")
            print("Development Error: ",error)
            ErrorModal("Something went wrong, please try again.", self.window_instance)
            
            
            