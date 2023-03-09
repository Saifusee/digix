import tkinter as tk
from tkinter import ttk
from CONSTANT.index import *
from app.base import Base
from error import ErrorModal
from app.main.other_components.custom_combobx import CustomCombobox

class EditSubCategory(tk.Toplevel, Base):
    def __init__(self, container, mysql, user, sub_category_id, refreshedTableMethod):
        # Note: when we call, instance.method(), method automatically take instance as first argument which we define as self
        # when we call, Class.method(), method need instance manually as first argument bcz it doesn't know whic one to take
        tk.Toplevel.__init__(self, container)
        Base.__init__(self, mysql, user)

        centerTkinterToplevel(container, self, dx=400, dy=250)
        
        # Declaring Data variables
        self.sub_category_data = tk.StringVar()
        self.category_type_data = tk.StringVar()
        self.selected_category_id = ""
        self.mysql = mysql
        self.sub_category_id = sub_category_id
        self.refreshedTableMethod = lambda: refreshedTableMethod()
        self.temp_name = ""
        self.temp_id = ""
        self.thread_flag = False
        self.after_id = 0

        # Rendering Components of Sub-category page
        self.renderingComponents()
        # Fetch Sub-Category
        self.fetchRelevantDataForRecord()
        
        
        
    # Fetch Relevant Sub-Category
    def fetchRelevantDataForRecord(self):
        # Fetching Sub-Category
        data = self.queryFetchSingleSubCategory(self.sub_category_id)
        
        # Setting default values for fields
        self.sub_category_data.set(data[0][f"{SUB_CATEGORY_NAME}"])
        self.selected_category_id = data[0][f"{SUB_CATEGORY_FOREIGNKEY_CATEGORY_ID}"]
        self.combobox_instance.set(data[0][CATEGORY_NAME])
        self.submit_button.configure(state="normal")
        
        # Setting Temp value for duplicate verification while submitting
        self.temp_name = self.sub_category_data.get()
        self.temp_id = self.selected_category_id
        
        
        
    # Rendering Components of this page
    def renderingComponents(self):
        # Configuring Tk.Toplevel
        self.columnconfigure(0, weight=1)
        self.configure(pady=(20))
        # Main Frame
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(row=0, column=0, sticky="ns")
        # Contents
        self.headlb = ttk.Label(self.main_frame, text="Update Sub-Category", style="ApplicationLabel1.TLabel", anchor="center")
        self.headlb.grid(row=0, column=0, columnspan=2, sticky="ew")
        
        self.lb = ttk.Label(self.main_frame, text="Sub-Category Name: {}".format(self.superscript("*")), style="LoginLabel.TLabel")
        self.lb.grid(row=1, column=0, sticky="w")
        
        self.sub_category_input = ttk.Entry(self.main_frame, width=60,
                                            textvariable=self.sub_category_data,
                                            font=("TkdefaultFont", 10, "bold")
                                            )
        self.sub_category_input.grid(row=1, column=1, padx=(10,10), pady=(10,10))
        self.bindFormFields(self.sub_category_input, self.validate_input)
        
        self.lb2 = ttk.Label(self.main_frame, text="Category Type: {}".format(self.superscript("*")), style="LoginLabel.TLabel")
        self.lb2.grid(row=2, column=0, sticky="w")
        
        # Rendering Combo Box
        self.renderComboBox()
        
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(row=3, column=0, columnspan=2, sticky="nsew")
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
        
        self.submit_button = ttk.Button(self.button_frame, text="Update",
                            command=self.commandSubmitSubCategory,
                            style="SignButton.TButton",
                            state="disabled"
                            )
        self.submit_button.grid(row=0, column=0, sticky="ns")
        
        self.cancel_button = ttk.Button(self.button_frame, text="Cancel",
                            command=lambda: self.destroy(),
                            style="ResetCancelButton.TButton",
                            )
        self.cancel_button.grid(row=0, column=1, sticky="ns")
        
        self.lbsuc = ttk.Label(self.main_frame, anchor="center")
        
        
        
    # Rendering ComboBox and its configuration
    def renderComboBox(self):
        
        # Fetching Values for ComboBox
        self.fetchCategoriesForComboBox()
        
        self.combobox_instance = CustomCombobox(
            self.main_frame,
            textvariable=self.category_type_data,
            valueList=self.categoryNameList, 
            width=60,
            font=("TkdefaultFont", 10, "bold"),
            state="readonly",
            justify="center",
            style="ShowProduct.TCombobox"
            )
        self.selected_category_id = self.categoryIdList[self.combobox_instance.current()]
        self.combobox_instance.current(0)
        self.combobox_instance.grid(row=2, column=1)
        
        self.combobox_instance.bind("<<ComboboxSelected>>",
                                 lambda event: [
                                     self.afterComboBoxSelected(self.combobox_instance, self.category_type_data), 
                                     self.validate_input(event)
                                     ]
                                )

         
                  
    # Fetching all Catgories
    def fetchCategoriesForComboBox(self):
        
            allData = self.queryFetchAllCategories()
            
            self.categoryNameList = self.dbValTuple(allData, CATEGORY_NAME) # Extracting Categories values from query fetched dictionaries
            self.categoryIdList = self.dbValTuple(allData, CATEGORY_ID) # Extracting Categories values from query fetched dictionaries



    # Function for complete submission
    def commandSubmitSubCategory(self):
        self.submit_button.configure(state = "disabled")
        # CategoryId = listOfCategoryId from Database in sequence as values in combobox
        #  current() gives us index of selected value in combobox which also same in listOfCategoryId
        self.selected_category_id = self.categoryIdList[self.combobox_instance.current()]
        
        # Check for Duplicates Entry
        sub_categories = self.queryFetchRelevantSubCategories(self.selected_category_id)
        flag = self.checkDuplicates(sub_categories, self.sub_category_input.get(), SUB_CATEGORY_NAME)
        
        # If Duplicates present
        if self.temp_id == self.selected_category_id and self.temp_name == self.sub_category_data.get():
            self.lbsuc.configure(
                style="ErrorLoginRegisterLabel.TLabel",
                text="Nothing to update, no changes are made."
            )
            self.lbsuc.grid(row=4, column=0, columnspan=2, sticky="ew")
            self.submit_button.configure(state="disabled")
        # If Duplicates present
        elif flag:
            self.lbsuc.configure(
                style="ErrorLoginRegisterLabel.TLabel",
                text="Sub-Category already exist."
            )
            self.lbsuc.grid(row=4, column=0, columnspan=2, sticky="ew")
            self.submit_button.configure(state="disabled")
        # If Duplicates not present
        else:
            try:
                # Saving to Database
                query = f"""UPDATE `{DATABASE_NAME}`.`{SUB_CATEGORY_TABLE_NAME}` SET 
                `{SUB_CATEGORY_NAME}` = %(data)s,
                `{SUB_CATEGORY_FOREIGNKEY_CATEGORY_ID}` = %(category_id)s
                WHERE {SUB_CATEGORY_ID} = %(sub_category_id)s;"""
                query_parameters = {
                    "data": self.sub_category_data.get().strip(),
                    "category_id": self.selected_category_id,
                    "sub_category_id": self.sub_category_id
                    }
                self.executeCommitSqlQuery(SUB_CATEGORY_TABLE_NAME, query, query_parameters)
                
                # After Saving
                self.lbsuc.configure(
                        style="SuccessfulLoginRegisterLabel.TLabel",
                        text=f"Sub-Category Successfully Updated "
                    )
                self.lbsuc.grid(row=4, column=0, columnspan=2, sticky="ew")
                
                self.after_id = self.after(5000, self.customReset)
                self.thread_flag = True
                
                self.refreshedTableMethod()
                self.fetchCategoriesForComboBox()
                
            except Exception as error:
                self.lbsuc.configure(
                        style="ErrorLoginRegisterLabel.TLabel",
                        text=f"Something went wrong."
                    )
                self.lbsuc.grid(row=4, column=0, columnspan=2, sticky="ew")
                print(f"Development Error (Storing SUB-CATEGORY Name): {error}")
                ErrorModal("Something went wrong while updating sub-category, please contact software developer.")
            

            
    def validate_input(self, event):
        
        # If after pressing submit button, self.after() active then terminates
        self.terminateAfter(self, self.thread_flag, self.after_id)

        if self.category_type_data.get() == "" or self.selected_category_id == "":
            self.lbsuc.configure(
                style="ErrorLoginRegisterLabel.TLabel",
                text="Category Type cannot be empty"
            )
            self.lbsuc.grid(row=4, column=0, columnspan=2, sticky="ew")
            self.submit_button.configure(state="disabled")
        elif self.sub_category_data.get() == "" or self.sub_category_data.get().isspace():
            self.lbsuc.configure(
                style="ErrorLoginRegisterLabel.TLabel",
                text="Sub-Category name cannot be empty"
            )
            self.lbsuc.grid(row=4, column=0, columnspan=2, sticky="ew")
            self.submit_button.configure(state="disabled")
        elif len(self.sub_category_data.get())  > 75:
            self.lbsuc.configure(
                style="ErrorLoginRegisterLabel.TLabel",
                text="Sub-Category name should be less than 75 characters"
            )
            self.lbsuc.grid(row=4, column=0, columnspan=2, sticky="ew")
            self.submit_button.configure(state="disabled")
        else:
            self.lbsuc.grid_forget()
            self.submit_button.configure(state="normal")
        
        
        
    # Resetting the Page
    def customReset(self):
        # Error Label Reset
        self.lbsuc.configure(
            style="SuccessfulLoginRegisterLabel.TLabel",
            text=f"Sub-Category Successfully Updated "
        )
        self.lbsuc.grid_forget()
        # Submit Button Disabled
        self.submit_button.configure(state="disabled")
        # Data Reset
        self.sub_category_data.set("")
        self.category_type_data.set("")
        # Category List refreshed
        self.fetchCategoriesForComboBox()
        # Set all input fields to Defaults
        self.fetchRelevantDataForRecord()