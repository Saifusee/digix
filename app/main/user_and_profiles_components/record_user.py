import tkinter as tk
from tkinter import ttk
from CONSTANT.index import *
from app.main.user_and_profiles_components.employee_authority_entry import UpdateEmployeeAuthority
from app.main.user_and_profiles_components.employee_status_entry import UpdateEmploymentStatus
from app.main.user_and_profiles_components.show_user_logs import ShowUserLogs
from app.main.other_components.record_base import RecordBase, CLabel

# Category Single Record Display
class RecordUser(tk.Toplevel, RecordBase):
    def __init__(self, container, mysql, user, user_id, refreshedTableMethod=None, *args, **kwargs):
        
        # Inheriting tk.Toplevel Class
        super().__init__(container, *args, **kwargs)
        self.grab_set()
        
        # Inheriting RecordBase Class
        # Class.contructor(instance_or_object) is right syntax
        RecordBase.__init__(self, mysql, user, POPUP_TITLE="User Details", button_1_text="Update Employment Status", button_2_text="Update Authority") # Class.contructor(instance or object) is right syntax
        
        # necessary instance variable for particular class
        self.user_id = user_id
        self.refreshedTableMethod = lambda: refreshedTableMethod()

        # Render Contents inside Canvas 
        self.renderLabels(record_table_name = self.POPUP_TITLE)
        
        # Fetch and show data
        self.fetchDataAndRender()
        
        
        
    def renderLabels(self, record_table_name):
        # Heading Label
        heading_label = ttk.Label(self.frame, text=record_table_name, anchor="center", style="PageHeadingLabel.TLabel")
        heading_label.grid(row=0, column=0, columnspan=2, sticky="ew")
        
        # Contents to Display in Canvas
        lb_1 = CLabel(self.frame, text="User ID: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_1.grid(row=1, column=0, sticky="nsew")
        self.user_id_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.user_id_label.grid(row=1, column=1, sticky="nsew")
        
        lb_2 = CLabel(self.frame, text="Username: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_2.grid(row=2, column=0, sticky="nsew")
        self.username_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.username_label.grid(row=2, column=1, sticky="nsew")
        
        lb_3 = CLabel(self.frame, text="E-Mail: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_3.grid(row=3, column=0, sticky="nsew")
        self.email_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.email_label.grid(row=3, column=1, sticky="nsew")

        lb_3 = CLabel(self.frame, text="Contact 1: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_3.grid(row=4, column=0, sticky="nsew")
        self.contact_1_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.contact_1_label.grid(row=4, column=1, sticky="nsew")

        lb_3 = CLabel(self.frame, text="Contact 2: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_3.grid(row=5, column=0, sticky="nsew")
        self.contact_2_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.contact_2_label.grid(row=5, column=1, sticky="nsew")

        lb_3 = CLabel(self.frame, text="Address: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_3.grid(row=6, column=0, sticky="nsew")
        self.address_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.address_label.grid(row=6, column=1, sticky="nsew")
        
        lb_4 = CLabel(self.frame, text="User Authority: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_4.grid(row=7, column=0, sticky="nsew")
        self.authority_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.authority_label.grid(row=7, column=1, sticky="nsew")
        
        lb_5 = CLabel(self.frame, text="Employment Status: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_5.grid(row=8, column=0, sticky="nsew")
        self.employment_status_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.employment_status_label.grid(row=8, column=1, sticky="nsew")
        
        lb_6 = CLabel(self.frame, text="Date of Joining: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_6.grid(row=9, column=0, sticky="nsew")
        self.date_of_joining_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.date_of_joining_label.grid(row=9, column=1, sticky="nsew")
        
        lb_7 = CLabel(self.frame, text="Date of Leaving: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_7.grid(row=10, column=0, sticky="nsew")
        self.date_of_leaving_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.date_of_leaving_label.grid(row=10, column=1, sticky="nsew")
        
        lb_8 = CLabel(self.frame, text="Reason for Leaving: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_8.grid(row=11, column=0, sticky="nsew")
        self.reason_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.reason_label.grid(row=11, column=1, sticky="nsew")
        
        lb_9 = CLabel(self.frame, text="Date of Rehiring: ", font=SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT)
        lb_9.grid(row=12, column=0, sticky="nsew")
        self.date_of_rehiring_label = CLabel(self.frame, font=SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT)
        self.date_of_rehiring_label.grid(row=12, column=1, sticky="nsew")
        
        
        self.show_purchases = ttk.Button(
            self.frame,
            text="Show User Logs",
            command= lambda: ShowUserLogs(
                self,
                self.mysql,
                self.current_user,
                self.user_id
            ),
            style="SingleRecordLinkButton.TButton"
            )
        self.show_purchases.grid(row=13, column=0, columnspan=2, sticky="ew")
        
        
        
    # Fetch Data from Database of Record and display it    
    def fetchDataAndRender(self):
        # Fetch Data
        data = self.queryFetchSingleUser(self.user_id)
        
        # Display Data
        self.user_id_label.configure(text=data[0][USER_ID])
        self.username_label.configure(text=data[0][USERNAME])
        self.email_label.configure(text=data[0][EMAIL])
        self.contact_1_label.configure(text=data[0][USER_CONTACT_1])
        self.contact_2_label.configure(text=data[0][USER_CONTACT_2])
        self.address_label.configure(text=data[0][USER_ADDRESS])
        self.authority_label.configure(text=data[0][USER_AUTHORITY])
        self.employment_status_label.configure(text=data[0][EMPLOYMENT_STATUS])
        self.date_of_joining_label.configure(text=data[0][DATE_OF_JOINING])
        self.date_of_leaving_label.configure(text=data[0][DATE_OF_LEAVING])
        self.reason_label.configure(text=data[0][LEAVE_REASON])
        self.date_of_rehiring_label.configure(text=data[0][DATE_OF_REHIRING])
        
        
        
        
    # Update Employment Status Button Record    
    def commandButton1(self):
        # Update Employment Status of user
        UpdateEmploymentStatus(
                        self,
                        self.user_id,
                        logged_in_user=self.current_user, 
                        refreshedTableMethod=lambda: self.refreshedTableMethod()
                    )
        # Refresh Details in Popup
        self.fetchDataAndRender()
        
        
        
    # Delete record
    def commandButton2(self):
        # Update Employee Authority
        UpdateEmployeeAuthority(
            self,
            self.user_id,
            logged_in_user=self.current_user,
            refreshedTableMethod=lambda: self.refreshedTableMethod()
            )
        # Refresh Details in Popup
        self.fetchDataAndRender()
        
        

     # Refreshing the Widget   
    def customReset(self):
        self.fetchDataAndRender()