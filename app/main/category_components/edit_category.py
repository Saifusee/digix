import tkinter as tk
from tkinter import ttk
from CONSTANT.index import *
from app.base import Base
from error import ErrorModal
from os import path

class EditCategory(tk.Toplevel, Base):
    def __init__(self, container, mysql, user, category_id, refreshedTableMethod):

        # Note: when we call, instance.method(), method automatically take instance as first argument which we define as self
        # when we call, Class.method(), method need instance manually as first argument bcz it doesn't know whic one to take
        tk.Toplevel.__init__(self, container)
        Base.__init__(self, mysql, user)
                
        try:
            self.image = path.join(PATH_TO_IMAGES, FILE_APP_LOGO)
            self.iconbitmap(self.image)
        except Exception:
            self.image = path.join(PATH_TO_IMAGES, FILE_APP_DEFAULT_LOGO)
            self.iconbitmap(self.image)
            
        centerTkinterToplevel(container, self, dx=450, dy=250)
                
        self.input_data = tk.StringVar()
        self.temp_name = ""
        self.category_id = category_id
        self.thread_flag = False
        self.after_id = 0

        
        
        # Grid Configuratin for Edit Pop-Up
        self.columnconfigure(0, weight=1)
        self.configure(pady=(20))
        # Main Frame
        self.m_frame = ttk.Frame(self)
        self.m_frame.grid(row=0, column=0, sticky="ns")
        self.m_frame.columnconfigure(0, weight=1)
        # Label Frame
        self.l_frame = ttk.Frame(self.m_frame)
        self.l_frame.grid(row=0, column=0, sticky="ns")
        # Button Frame
        self.b_frame = ttk.Frame(self.m_frame)
        self.b_frame.grid(row=1, column=0, sticky="ns")
        self.b_frame.columnconfigure(0, weight=1)
        self.b_frame.columnconfigure(1, weight=1)
        
        # Only PopUp is accessible
        self.grab_set()
        
        headlb = ttk.Label(self.l_frame, text="Update Category", style="ApplicationLabel1.TLabel", anchor="center")
        headlb.grid(row=0, column=0, columnspan=2, sticky="ew")
        
        lb = ttk.Label(self.l_frame, text="Category Name: {}".format(self.superscript("*")), style="LoginLabel.TLabel")
        lb.grid(row=1, column=0, sticky="w")
        
        input = ttk.Entry(self.l_frame, width=60,  textvariable=self.input_data, font=("TkdefaultFont", 10, "bold"))
        input.grid(row=1, column=1, padx=(10,10), pady=(10,10))
        self.bindFormFields(input, self.validate_category_input)
        
        self.button = ttk.Button(self.b_frame,
                            text="Update",
                            command=lambda: self.commandUpdateCategory(mysql=mysql, refreshedTableMethod=lambda: refreshedTableMethod()),
                            style="SignButton.TButton",
                            state="disabled"
                            )
        self.button.grid(row=2, column=0, sticky="ew", padx=(30,30))
        
        self.cancel_button = ttk.Button(self.b_frame,
                            text="Cancel",
                            command=lambda: self.destroy(),
                            style="ResetCancelButton.TButton"
                            )
        self.cancel_button.grid(row=2, column=1, sticky="ew")
        self.lbsuc = ttk.Label(self.b_frame, anchor="center")
        
        self.fetchRelevantDataForRecord()
    
    
        
    def fetchRelevantDataForRecord(self):
        data = self.queryFetchSingleCategory(self.category_id)
        self.input_data.set(data[0][f"{CATEGORY_NAME}"])
        self.button.configure(state="normal")
        self.temp_name = self.input_data.get()
    
    
    # Submit Button Click
    def commandUpdateCategory(self, mysql, refreshedTableMethod):
        self.button.configure(state = "disabled")
        # Check for Duplicates Entry
        categories = self.queryFetchAllCategories()
        flag = self.checkDuplicates(categories, self.input_data.get(), CATEGORY_NAME)
        
        # If same as existing
        if self.temp_name == self.input_data.get():
            self.lbsuc.configure(
            style="ErrorLoginRegisterLabel.TLabel",
            text="Nothing to update, no changes are made."
            )
            self.lbsuc.grid(row=3, column=0, columnspan=2, sticky="ew")
        # If Duplicates present
        elif flag:
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
                query = f"""UPDATE `{DATABASE_NAME}`.`{CATEGORY_TABLE_NAME}`
                SET `{CATEGORY_NAME}` = %(name)s
                WHERE `{CATEGORY_ID}` = %(id)s;"""
                query_parameters = {"name": self.input_data.get().strip(), "id": int(self.category_id)}
                self.executeCommitSqlQuery(CATEGORY_TABLE_NAME, query, query_parameters)
                
                # After Saving
                self.lbsuc.configure(
                    style="SuccessfulLoginRegisterLabel.TLabel",
                    text=f"Category Successfully Updated "
                )
                self.lbsuc.grid(row=3, column=0, columnspan=2, sticky="ew")
                
                refreshedTableMethod() # Refresh Whole Table with updated Data
                self.fetchRelevantDataForRecord()
                self.after_id = self.after(5000, self.customReset)
                self.thread_flag = True
                
            except Exception as error:
                self.lbsuc.configure(
                    style="ErrorLoginRegisterLabel.TLabel",
                    text=f"Something went wrong. "
                )
                self.lbsuc.grid(row=3, column=0, columnspan=2, sticky="ew")
                print(f"Development Error (Storing CATEGORY Name): {error}")
                ErrorModal("Something went wrong while updating category, please contact software developer.")
           
           
           
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
            text=f"Category Successfully Updated "
        )
        self.lbsuc.grid_forget()
        # Submit Button Disabled
        self.button.configure(state="disabled")
        # Set all input fields to Defaults
        self.fetchRelevantDataForRecord()

    