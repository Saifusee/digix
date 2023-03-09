from CONSTANT.index import *
import tkinter as tk
from tkinter import ttk
import mysql.connector as db
import re
from authenticate.authenticate_base import AuthenticateBase
from random import randint
from mail.mail import DigixMail
from error import ErrorModal
import threading

class Login(ttk.Frame, AuthenticateBase):
    def __init__(self, container, mysql, raise_register_frame, window_instance, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        self.username_or_email_value = tk.StringVar()
        self.password_value = tk.StringVar()
        self.otp_value = tk.StringVar()
        self.new_password_value = tk.StringVar()
        self.errors = tk.StringVar(value="")
        self.show_p_value = tk.IntVar()
        self.show_n_p_value = tk.IntVar()
        self.c_email = bool(False)
        self.c_password = bool(False)
        self.thread_flag = False
        self.after_id = 0
        self.window_instance = window_instance
        self.mysql = mysql
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
        page_label = ttk.Label(top_frame, padding=10, text="LOGIN PAGE", style="PageHeadingLabel.TLabel", anchor="center")
        page_label.grid(rowspan=2, sticky="ew")
        
        #PUTTING LABEL AND FIELD
        self.put_labels_and_fields(middle_frame)

        #PUTTING BUTTONS
        self.put_buttons(bottom_frame, raise_register_frame)

    def put_labels_and_fields(self, frame):
        #USERNAME LABEL AND FIELD
        self.username_or_email_label = ttk.Label(frame, text="Username or E-Mail: ", style="LoginLabel.TLabel")
        self.username_or_email_label.grid(row=0, column=0, sticky="w")
        self.username_or_email_entry = ttk.Entry(frame, width=40, textvariable=self.username_or_email_value, font=('TkDefaultFont', 10))
        self.username_or_email_entry.grid(row=0, column=1, padx=(10,10), pady=(10,10))
        self.username_or_email_entry.bind("<KeyRelease>", self.validate_email_or_username)
        self.username_or_email_entry.bind("<FocusOut>", self.validate_email_or_username)
        #PASSWORD LABEL AND FIELD
        self.password = ttk.Label(frame, text="Password: ", style="LoginLabel.TLabel")
        self.password.grid(row=1, column=0, sticky="w")
        self.password_entry = ttk.Entry(frame, width=40, show="*", textvariable=self.password_value, font=('TkDefaultFont', 10))
        self.password_entry.grid(row=1, column=1, padx=(10,10), pady=(10,5))
        self.password_entry.bind("<KeyRelease>", self.validate_password)
        self.password_entry.bind("<FocusOut>", self.validate_password)
        # Show Password Checkbutton
        self.show_password_checkbox = ttk.Checkbutton(
            frame,
            text="Show Password",
            variable=self.show_p_value,
            style="ShowPasswordCheckButton.TCheckbutton",
            command=lambda: self.toggleCheckButton(self.show_p_value.get(), self.password_entry)
            )
        self.show_password_checkbox.grid(row=2, column=0, sticky="w", padx=(10, 10), pady=(5, 10))
        #OTP LABEL AND FIELD
        self.otp_entry = ttk.Entry(frame, width=40, textvariable=self.otp_value, font=('TkDefaultFont', 10))
        self.otp_entry.bind("<KeyRelease>", self.validate_otp)
        self.otp_entry.bind("<FocusOut>", self.validate_otp)
        self.submit_otp_button = ttk.Button(frame, text="Submit OTP", command=self.submit_otp, style="LoginRegisterButton.TButton" )
        self.submit_otp_button["state"] = "disabled"
        #NEW PASSWORD LABEL AND FIELD
        self.new_password_label = ttk.Label(frame, text="New Password: ", style="LoginLabel.TLabel")
        self.new_password_entry = ttk.Entry(frame, width=40, show="*", textvariable=self.new_password_value, font=('TkDefaultFont', 10))
        self.new_password_entry.bind("<KeyRelease>", self.validate_new_password)
        self.new_password_entry.bind("<FocusOut>", self.validate_new_password)
        # Show Password Checkbutton
        self.show_new_password_checkbox = ttk.Checkbutton(
            frame,
            text="Show Password",
            variable=self.show_n_p_value,
            style="ShowPasswordCheckButton.TCheckbutton",
            command=lambda: self.toggleCheckButton(self.show_n_p_value.get(), self.new_password_entry)
            )
        
        self.new_password_button = ttk.Button(frame, text="Submit Password", command=self.new_password_submit, style="LoginRegisterButton.TButton")
        self.new_password_button["state"] = "disabled"

        
    def put_buttons(self, frame, raise_register_frame):
        #SUBMIT BUTTON
        self.submit_button = ttk.Button(frame, text="Submit", command=self.submit_function, style="LoginRegisterButton.TButton")
        self.submit_button.grid(row=0, column=0, padx=(10,10))
        self.submit_button["state"] = "disabled"
        
        #RESET BUTTON
        self.reset_button = ttk.Button(frame, text="Reset", command=self.reset_field_data, style="ResetCancelButton.TButton")
        self.reset_button.grid(row=0, column=1, padx=(10,10))
        
        self.forgot_password_button = ttk.Button(frame, text="Forgot Password", command=self.forgot_password, style="LoginRegisterButton.TButton")
        self.forgot_password_button.grid(row=0, column=2, padx=(10,10))

        #TOGGLE BUTTON FOR SIGNUP AND SIGNIN
        self.toggle_frame_button = ttk.Button(
            frame,
            text="Sign Up",
            command=lambda: [raise_register_frame(), self.reset_field_data()], 
            style="SignButton.TButton"
        )
        self.toggle_frame_button.grid(row=0, column=3, padx=(10,10))
        
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
        self.username_or_email_value.set("")
        self.password_value.set("")
        self.otp_value.set("")
        self.new_password_value.set("")
        self.errors.set("")
        self.show_p_value.set(0)
        self.show_n_p_value.set(0)
        self.username_or_email_entry["style"] = "TEntry"
        self.username_or_email_entry["state"] = "normal"
        self.password_entry["style"] = "TEntry"
        self.password_entry["state"] = "normal"
        self.show_password_checkbox["state"] = "normal"
        self.otp_entry["style"] = "TEntry"
        self.new_password_entry["style"] = "TEntry"
        self.forgot_password_button["state"] = "normal"
        self.submit_otp_button["state"] = "disabled"
        self.new_password_button["state"] = "disabled"
        self.submit_button["state"] = "disabled"
        self.forgot_password_button["text"] = "Forgot Password"
        self.error_label["style"] = "ErrorLoginRegisterLabel.TLabel"
        self.otp_entry.grid_forget()
        self.submit_otp_button.grid_forget()
        self.new_password_label.grid_forget()
        self.new_password_entry.grid_forget()
        self.show_new_password_checkbox.grid_forget()
        self.new_password_button.grid_forget()
            
    def forgot_password(self):
        if (self.username_or_email_value.get().strip() == ""):
            self.errors.set("Please enter your email or username for resetiing password")
        elif (self.c_email == False):
            self.errors.set("Username and email must be between 2-50 characters. Characters other than [A-Z], [a-z], [0-9], period(.) and underscore not allowed(_). Cannot start and end with (.)")
        else:
            try: 
                self.password_value.set("")
                query1=f"SELECT * FROM {DATABASE_NAME}.{USER_TABLE_NAME} WHERE {EMAIL} LIKE '{self.username_or_email_value.get().strip()}' OR {USERNAME} like '{self.username_or_email_value.get().strip()}'"
                self.mysql.query.execute(query1)
                otp_value = randint(11111111, 99999999)
                self.otp_ref = f"{otp_value}{self.username_or_email_value.get().strip()}{otp_value}"
                query_data = self.mysql.query.fetchone()
                if (query_data == None):
                    self.errors.set("No User Found. Please check the username or email")
                else:
                    self.username_or_email_entry["state"] = "disabled"
                    self.password_entry["state"] = "disabled"
                    self.show_password_checkbox["state"] = "disabled"
                    self.password_entry["style"] = "TEntry"
                    self.otp_entry.grid(row=3, column=1, padx=(10,10), pady=(10,10))
                    self.submit_otp_button.grid(row=3, column=0, padx=(10, 10))
                    self.otp_entry.focus()
                    self.dummy_user = query_data #It holds temporary value of email
                    query2 = f"INSERT INTO {DATABASE_NAME}.{OTP_TABLE_NAME} ({OTP_REFERENCE}, {OTP_VALUE}) VALUES (%s, %s)"
                    self.mysql.query.execute(query2, (self.otp_ref, otp_value))
                    self.mysql.db_connection.commit()
                    try:
                        message =f"OTP for password reset = {otp_value}"
                        
                        t_hread =threading.Thread(target=lambda: DigixMail(query_data[EMAIL], f"Password Reset: {getShopDetails()[SHOP_NAME]}", message), name="SendOTPForgottenPasswordMailThread")
                        t_hread.start()
                        self.error_label["style"] = "SuccessfulLoginRegisterLabel.TLabel"
                        self.errors.set("OTP sent successfully, OTP is valid for next 5 minutes")
                        curent_otp_ref = self.otp_ref
                        # Delete OTP after 5 minutes
                        timer = threading.Timer(300, lambda: self.deleteOTP(curent_otp_ref))
                        timer.start()
                    except Exception as errors:
                        print(f"Development Error (SendForgotPasswordOTPMail) {errors}")
                        ErrorModal("Something went wrong, please try again.", self.window_instance)
                    self.forgot_password_button["text"] = "Resend OTP"
            except Exception as errors:
                print(f"Development Error (ForgotPassword:FrogotDatabaseRelatedExecution): {errors}")
                ErrorModal("Something went wrong, please try again.", self.window_instance)
                    
    def submit_otp(self):
        try:
            query1 = f"SELECT * FROM {DATABASE_NAME}.{OTP_TABLE_NAME} WHERE {OTP_REFERENCE} LIKE %s"
            self.mysql.query.execute(query1, (self.otp_ref,))
            query_data = self.mysql.query.fetchone()
            if type(query_data) == None.__class__:
                self.errors.set("OTP expires or invalid")
            else:
                if(query_data["otp"] == int(self.otp_value.get().strip())):
                    self.otp_entry.grid_forget()
                    self.submit_otp_button.grid_forget()
                    self.forgot_password_button.configure(state="disabled")
                    self.new_password_entry["state"] = "normal"
                    self.new_password_button["state"] = "normal"
                    self.new_password_label.grid(row=3, column=0, sticky="w")
                    self.new_password_entry.grid(row=3, column=1, padx=(10,10), pady=(10,5))
                    self.show_new_password_checkbox.grid(row=4, column=0, sticky="w", padx=(10, 10), pady=(5, 10))
                    self.new_password_button.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(10))
                else:
                    self.errors.set("Invalid OTP")
        except Exception as errors:
            print(f"Development Error (While VerifyingOTP): {errors}")
            ErrorModal("Something went wrong, please try again.", self.window_instance)
            
            
    def new_password_submit(self):
        self.new_password_entry.configure(state="disabled")
        self.new_password_button.configure(state="disabled")
        try:
            if (self.dummy_user[PASSWORD] == self.new_password_value.get().strip()):
                self.errors.set("New Password cannot be same as old password.")
            else:
                try:
                    query1 = f"UPDATE {DATABASE_NAME}.{USER_TABLE_NAME} SET {PASSWORD} = %s WHERE {USER_ID} = {self.dummy_user[USER_ID]}"
                    self.mysql.query.execute(query1, (self.new_password_value.get().strip(),))
                    self.mysql.db_connection.commit()
                except Exception as errors:
                    print(f"Development Error (UpdatingNewPasswordOnDatabse): {errors}")
                    ErrorModal("Something went wrong, please try again.", self.window_instance)
                try:
                    self.deleteOTP(self.otp_ref)
                except Exception as errors:
                    print(f"Development Error (DeletingOTPDataOnDatabase): {errors}")
                    ErrorModal("Something went wrong, please try again.", self.window_instance)
                    self.error_label["style"] = "SuccessfulLoginRegisterLabel.TLabel"
                self.error_label["style"] = "SuccessfulLoginRegisterLabel.TLabel"
                self.errors.set("Password Succesfully Reset")
                self.after_id = self.after(5000, self.reset_field_data)
                self.thread_flag = True
        except Exception as errors:
            print(f"Development Error: {errors}")
            ErrorModal("Something went wrong, please try again.", self.window_instance)                
    
    def validate_email_or_username(self, event):
        # Terminating After Method if active
        if self.thread_flag:
            self.after_cancel(self.after_id)
            
        # username_email_regex = r"\b([A-Za-z_]+[A-Za-z0-9_@.]*){2,50}\b" # For characters more than 32 it keeps app freeze
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z]+\.[A-Z|a-z]{2,}\b'
        parameter_false_tuple = ("email", False, self.username_or_email_entry, "ErrorEntry.TEntry", self.on_invalid)
        parameter_true_tuple = ("email", True, self.username_or_email_entry, "TEntry", self.enable_submit_button)
        if (self.username_or_email_value.get() == ""):
            self._validation_fail("Username or E-Mail field cannot be empty", *parameter_false_tuple)
        # Either Match email format
        elif self.username_or_email_value.get().__contains__("@") and (not re.fullmatch(email_regex, self.username_or_email_value.get())):
            self._validation_fail("Invalid Username or E-Mail format.", *parameter_false_tuple)
        # or match username format
        elif not self.username_or_email_value.get().__contains__("@") and not self.username_or_email_value.get().isalnum():
            self._validation_fail("Invalid Username or E-Mail forma11t.", *parameter_false_tuple)
        else:
            self._validation_fail("", *parameter_true_tuple)
    
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
            self.new_password_button["state"] = "disabled"
        elif (not re.fullmatch(password_regex, password_value)):
            p_e_text = "Password must be 8-15 characters, contain uppercase letter, lowercase letter, number and special symbold (@$!%*?&).)"
            self._validation_fail(p_e_text, *parameter_false_tuple)
            self.new_password_button["state"] = "disabled"
        else:
            self._validation_fail("", *parameter_true_tuple)
            self.new_password_button["state"] = "normal"
        return   
    
    def validate_new_password(self, event):
        # Terminating After Method if active
        if self.thread_flag:
            self.after_cancel(self.after_id)
            
        password_value = self.new_password_value.get().strip()
        password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,15}$"
        self.error_label["style"] = "ErrorLoginRegisterLabel.TLabel"
        if (password_value == ""):
            self.errors.set("Password Field cannot be empty")
            self.new_password_button["state"] = "disabled"
        elif (not re.fullmatch(password_regex, password_value)):
            p_e_text = "Password must be 8-15 characters, contain uppercase letter, lowercase letter, number and special symbold (@$!%*?&).)"
            self.errors.set(p_e_text)
            self.new_password_button["state"] = "disabled"
        else:
            self.errors.set("")
            self.new_password_button["state"] = "normal"
        return 
    
    def validate_otp(self, event):
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
            self.submit_otp_button["state"] = "disabled"
        elif (not re.fullmatch(otp_regex, otp_value)):
            o_e_text = "OTP must be 8 digit numeric value"
            self._validation_fail(o_e_text, *parameter_false_tuple)
            self.submit_otp_button["state"] = "disabled"
        else:
            self._validation_fail("", *parameter_true_tuple)
            self.submit_otp_button["state"] = "normal"
        return


    # Delete OTP
    def deleteOTP(self, otp_ref):
        # Deleting the OTP from Database
        qw = f"DELETE FROM {DATABASE_NAME}.{OTP_TABLE_NAME} WHERE {OTP_REFERENCE} = %s"
        self.mysql.query.execute(qw, (otp_ref,))
        self.mysql.db_connection.commit()
        
     
    def on_invalid(self):
        self.submit_button["state"] = "disabled"
        self.bottom_error_frame.grid(row=3, column=0)
        
    def enable_submit_button(self):
        if (self.c_email and self.c_password):
            self.submit_button["state"] = "normal"
            
    def submit_function(self):
        try:
            email_value = self.username_or_email_value.get().strip().lower()
            password_value = self.password_value.get().strip()
            self.mysql.query.execute(f"SELECT * FROM {DATABASE_NAME}.{USER_TABLE_NAME} WHERE ({EMAIL} like %s) or ({USERNAME} like %s)", (email_value, email_value))
            user = self.mysql.query.fetchone()
            if (user != None): #ensure that dictionary not empty (empty dict return None)
                if (user[PASSWORD] == password_value):
                    # if details are correct but user no longer employed
                    if not (type(user[DATE_OF_LEAVING]) == None.__class__):
                        self.errors.set("Your account are no longer validated to access application, it may be because you are no longer employed.")
                        self.window_instance.user = dict()
                    else:
                        self.error_label["style"] = "SuccessfulLoginRegisterLabel.TLabel"
                        self.errors.set("Login Successfull") 
                        self.reset_field_data()
                        self.window_instance.user = user
                        self.window_instance.destroy() 
                else:
                    self.errors.set("Incorrect Password")
                    self.window_instance.user = dict()
            else:
                self.errors.set("E-Mail or Username not registered")
        except db.Error as error: 
            print(f"Development Error: {error}.")
            ErrorModal("Something went wrong, please try again.", self.window_instance)
            
            
            
            
            