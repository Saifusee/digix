import tkinter as tk
from tkinter import ttk
from CONSTANT.index import *
from app.base import Base
from error import ErrorModal

class CreateCategory(ttk.Frame, Base):
    def __init__(self, container, mysql, user):

        # Note: when we call, instance.method(), method automatically take instance as first argument which we define as self
        # when we call, Class.method(), method need instance manually as first argument bcz it doesn't know whic one to take
        ttk.Frame.__init__(self, container)
        Base.__init__(self, mysql, user)
                
        self.input_data = tk.StringVar()
        self.thread_flag = False
        self.after_id = 0
        
        
        headlb = ttk.Label(self, text="Create New Category", style="ApplicationLabel1.TLabel", anchor="center")
        headlb.grid(row=0, column=0, columnspan=2, sticky="ew")
        
        lb = ttk.Label(self, text="Category Name: {}".format(self.superscript("*")), style="LoginLabel.TLabel")
        lb.grid(row=1, column=0, sticky="w")
        
        input = ttk.Entry(self, width=60,  textvariable=self.input_data, font=("TkdefaultFont", 10, "bold"))
        input.grid(row=1, column=1, padx=(10,10), pady=(10,10))
        self.bindFormFields(input, self.validate_category_input)

        
        self.button = ttk.Button(self,
                            text="Submit",
                            command=lambda: self.commandSubmitCategory(mysql),
                            style="SignButton.TButton",
                            state="disabled"
                            )
        self.button.grid(row=2, column=0, columnspan=2, sticky="ew")
        
        self.lbsuc = ttk.Label(self, anchor="center")
    
    
        
    def commandSubmitCategory(self, mysql):
        self.button.configure(state="disabled")
        # Check for Duplicates Entry
        categories = self.queryFetchAllCategories()
        flag = self.checkDuplicates(categories, self.input_data.get(), CATEGORY_NAME)
        
        # If Duplicates present
        if flag:
                self.lbsuc.configure(
                style="ErrorLoginRegisterLabel.TLabel",
                text="Category already exist"
                )
                self.lbsuc.grid(row=3, column=0, columnspan=2, sticky="ew")
                self.button.configure(state="disabled")
        # If Duplicates not present
        else:
            try:
                # Saving to Database
                query = f"INSERT INTO `{DATABASE_NAME}`.`{CATEGORY_TABLE_NAME}` (`{CATEGORY_NAME}`) VALUES (%s)"
                query_parameters = (self.input_data.get().strip(),)
                self.executeCommitSqlQuery(CATEGORY_TABLE_NAME, query, query_parameters)
                
                # After Saving
                self.lbsuc.configure(
                    style="SuccessfulLoginRegisterLabel.TLabel",
                    text="Category Successfully Created "
                )
                self.lbsuc.grid(row=3, column=0, columnspan=2, sticky="ew")
                
                self.after_id = self.after(5000, self.customReset)
                self.thread_flag = True
                
            except Exception as error:
                self.lbsuc.configure(
                    style="ErrorLoginRegisterLabel.TLabel",
                    text="Something went wrong. "
                )
                self.lbsuc.grid(row=3, column=0, columnspan=2, sticky="ew")
                print(f"Development Error (Storing CATEGORY Name): {error}")
                ErrorModal("Something went wrong while creating new category, please contact software developer.")
           
           
           
    def validate_category_input(self, event):
        
        # If after pressing submit button, self.after() active then terminates
        self.terminateAfter(self, self.thread_flag, self.after_id)
        
        if self.input_data.get() == "" or self.input_data.get().isspace():
            self.lbsuc.configure(
                style="ErrorLoginRegisterLabel.TLabel",
                text="Category name cannot be empty."
            )
            self.lbsuc.grid(row=3, column=0, columnspan=2, sticky="ew")
            self.button.configure(state="disabled")
        elif len(self.input_data.get())  > 75:
            self.lbsuc.configure(
                style="ErrorLoginRegisterLabel.TLabel",
                text="Category name should be less than 75 characters"
            )
            self.lbsuc.grid(row=3, column=0, columnspan=2, sticky="ew")
            self.button.configure(state="disabled")
        else:
            self.lbsuc.grid_forget()
            self.button.configure(state="normal")
            
            
             
    # Resetting the Page
    def customReset(self):
        # Error Label Reset
        self.lbsuc.configure(
            style="SuccessfulLoginRegisterLabel.TLabel",
            text="Category Successfully Created "
        )
        self.lbsuc.grid_forget()
        # Submit Button Disabled
        self.button.configure(state="disabled")
        # Data Reset
        self.input_data.set("")

    