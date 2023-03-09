import tkinter as tk
from tkinter import ttk
from CONSTANT.index import *
from app.main.user_and_profiles_components.record_user import RecordUser
from datetime import *
from tkcalendar import DateEntry
from app.main.external_files.export_user_data import ExportUserData
from app.main.user_and_profiles_components.employee_authority_entry import UpdateEmployeeAuthority
from app.main.user_and_profiles_components.employee_status_entry import UpdateEmploymentStatus
from app.main.tree_essentials import TreeEssentials

class ShowUser(tk.Canvas, TreeEssentials):
    
    def __init__(self, container, mysql, user):
        
        self.offset = 0
        self.limit = 10
        self.from_joining_date = tk.StringVar()
        self.to_joining_date = tk.StringVar()
        self.from_leaving_date = tk.StringVar()
        self.to_leaving_date = tk.StringVar()

        self.from_joining_date.set("0000-00-00")
        self.to_joining_date.set("0000-00-00")
        self.from_leaving_date.set("0000-00-00")
        self.to_leaving_date.set("0000-00-00")

        self.radio_value_2 = tk.IntVar()

        
        # Note: when we call, instance.method(), method automatically take instance as first argument which we define as self
        # when we call, Class.method(), method need instance manually as first argument bcz it doesn't know which one to take
        tk.Canvas.__init__(self, container)
        
        # Configuration for Frame
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=95)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=4)

        # Define Frames above Table
        self.defineAboveFrames()
        
        # Define Search above Table
        self.defineSearchButtons(
            frame=self.above_frame,
            page_heading="Registered Users:",
            refreshedTableMethod=lambda: self.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.queryFetchPaginatedUser(
                    self.offset,
                    self.limit,
                    self.from_joining_date.get(),
                    self.to_joining_date.get(),
                    self.from_leaving_date.get(),
                    self.to_leaving_date.get(),
                    radio_authority_data=self.radio_value.get(),
                    radio_status_data=self.radio_value_2.get(),
                    query_data=self.search_data.get()
                    )
                ),
            searchedRefreshTableMethod=lambda: self.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.queryFetchPaginatedUser(
                    self.offset,
                    self.limit,
                    self.from_joining_date.get(),
                    self.to_joining_date.get(),
                    self.from_leaving_date.get(),
                    self.to_leaving_date.get(),
                    radio_authority_data=self.radio_value.get(),
                    radio_status_data=self.radio_value_2.get(),
                    query_data=self.search_data.get()
                    )
                )
        )
        
        # Create Tree
        self.createTreeAndConfiguration()
        
        # Rendering Scrollbar
        self.renderScrollbar()
        
        # Initiliazing Tree essentials method and components
        TreeEssentials.__init__(self, mysql=mysql, user=user, tree_instance=self.tree)
        
        # Define Frames below Table
        self.defineBelowFrames(container=self)
        
        # Define Buttons below Table
        self.definePaginateButtons(
            refreshedTableMethod=lambda: self.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.queryFetchPaginatedUser(
                    self.offset,
                    self.limit,
                    self.from_joining_date.get(),
                    self.to_joining_date.get(),
                    self.from_leaving_date.get(),
                    self.to_leaving_date.get(),
                    radio_authority_data=self.radio_value.get(),
                    radio_status_data=self.radio_value_2.get(),
                    query_data=self.search_data.get()
                    )
                ),
            searchedRefreshTableMethod=lambda: self.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.queryFetchSearchedData(
                    offset=self.offset, 
                    limit=self.limit,
                    query_data=self.search_data.get(),
                    selectable_columns_from_table_query=self.saved_query_category,
                    table_name=CATEGORY_TABLE_NAME,
                    sort_column=CATEGORY_NAME
                    )
                ),
            first_functionality_switch="download",
            first_functionality_button_text="Download Records",
            firstFunctionalityMethod=lambda: ExportUserData(
                lambda: self.queryFetchPaginatedUser(
                    self.offset,
                    self.limit,
                    self.from_joining_date.get(),
                    self.to_joining_date.get(),
                    self.from_leaving_date.get(),
                    self.to_leaving_date.get(),
                    radio_authority_data=self.radio_value.get(),
                    radio_status_data=self.radio_value_2.get(),
                    query_data=self.search_data.get(),
                    export=True
                    ),
                container=self
                ),
            second_functionality_switch="call_passed_method_directly",
            second_functionality_button_text="Change Authority",
            secondFunctionalityMethod=lambda: UpdateEmployeeAuthority(
                self,
                self.tree.item(self.tree.focus())["values"][1],
                logged_in_user=self.current_user, 
                refreshedTableMethod=lambda: self.insertDataInTree(
                    tableRowFetchAndRenderMethod=lambda: self.definingRowsOfParticularTree(
                        dataFetchingMethod=lambda: self.queryFetchPaginatedUser(
                            self.offset,
                            self.limit,
                            self.from_joining_date.get(),
                            self.to_joining_date.get(),
                            self.from_leaving_date.get(),
                            self.to_leaving_date.get(),
                            radio_authority_data=self.radio_value.get(),
                            radio_status_data=self.radio_value_2.get(),
                            query_data=self.search_data.get()
                            )
                        )
                    )
            ),
            third_functionality_switch="call_passed_method_directly",
            third_functionality_button_text="Update Employment Status",
            thirdFunctionalityMethod=lambda: UpdateEmploymentStatus(
                self,
                self.tree.item(self.tree.focus())["values"][1],
                logged_in_user=self.current_user, 
                refreshedTableMethod=lambda: self.insertDataInTree(
                    tableRowFetchAndRenderMethod=lambda: self.definingRowsOfParticularTree(
                        dataFetchingMethod=lambda: self.queryFetchPaginatedUser(
                            self.offset,
                            self.limit,
                            self.from_joining_date.get(),
                            self.to_joining_date.get(),
                            self.from_leaving_date.get(),
                            self.to_leaving_date.get(),
                            radio_authority_data=self.radio_value.get(),
                            radio_status_data=self.radio_value_2.get(),
                            query_data=self.search_data.get()
                            )
                        )
                    )
            ),
            is_triple_button_functionality_needed=True
        )

        self.defineParticularSearchesWidgets(self.above_frame)



        # Insert Data
        self.insertDataInTree(
            tableRowFetchAndRenderMethod=lambda: self.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.queryFetchPaginatedUser(
                    self.offset,
                    self.limit,
                    self.from_joining_date.get(),
                    self.to_joining_date.get(),
                    self.from_leaving_date.get(),
                    self.to_leaving_date.get(),
                    radio_authority_data=self.radio_value.get(),
                    radio_status_data=self.radio_value_2.get(),
                    query_data=self.search_data.get()
                    ))
            )
        
        # Defining Key and Mouse Bindings on Table  
        self.definingEventBindings(
            refreshTableMethod=lambda: self.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.queryFetchPaginatedUser(
                    self.offset,
                    self.limit,
                    self.from_joining_date.get(),
                    self.to_joining_date.get(),
                    self.from_leaving_date.get(),
                    self.to_leaving_date.get(),
                    radio_authority_data=self.radio_value.get(),
                    radio_status_data=self.radio_value_2.get(),
                    query_data=self.search_data.get()
                    )
                ),
            RecordPopupClass=lambda: RecordUser(
                container=self,
                mysql=self.mysql,
                user=self.current_user,
                user_id=self.tree.item(self.tree.focus())["values"][1],
                refreshedTableMethod=lambda: self.insertDataInTree(
                    tableRowFetchAndRenderMethod=lambda: self.definingRowsOfParticularTree(
                        dataFetchingMethod=lambda: self.queryFetchPaginatedUser(
                            self.offset,
                            self.limit,
                            self.from_joining_date.get(),
                            self.to_joining_date.get(),
                            self.from_leaving_date.get(),
                            self.to_leaving_date.get(),
                            radio_authority_data=self.radio_value.get(),
                            radio_status_data=self.radio_value_2.get(),
                            query_data=self.search_data.get()
                            )
                        )
                    )
                ),
            secondFunctionalityMethod=self.queryDeleteCategory
            )



    # Define Widgets Above TreeView for Searching Purposes of Product
    def defineParticularSearchesWidgets(self, frame):
        
        # Frame for Radio Buttons
        t_frame_1 = ttk.Frame(frame)
        t_frame_1.pack(side="top", anchor="w", pady=5)
        t_frame_2 = ttk.Frame(frame)
        t_frame_2.pack(side="top", anchor="w", pady=5)
        t_frame_3 = ttk.Frame(frame)
        t_frame_3.pack(side="top", anchor="w", pady=5)
        t_frame_4 = ttk.Frame(frame)
        t_frame_4.pack(side="top", anchor="w", pady=5)
        # Frame for Calendar Buttons
        joining_date_frame = tk.Frame(t_frame_3, background="white")
        joining_date_frame.pack(side="left", anchor="w", pady=5, padx=5)
        leaving_date_frame = tk.Frame(t_frame_4, background="white")
        leaving_date_frame.pack(side="left", anchor="w", pady=5, padx=5)

        

        self.from_date_data = tk.StringVar()
        self.to_date_data = tk.StringVar()

        # Radiobuttons
        lb_1 = ttk.Label(t_frame_1, text="Authorities: ", font=("TkDefaultFont", 8, "bold"))
        self.radio_0 = ttk.Radiobutton(t_frame_1, text="All", variable=self.radio_value, value=0, command=self.radioButtonSelect, style="TreeRadiobutton.TRadiobutton")
        self.radio_1 = ttk.Radiobutton(t_frame_1, text="Employee", variable=self.radio_value, value=1, command=self.radioButtonSelect, style="TreeRadiobutton.TRadiobutton")
        self.radio_2 = ttk.Radiobutton(t_frame_1, text="Managemnet", variable=self.radio_value, value=2, command=self.radioButtonSelect, style="TreeRadiobutton.TRadiobutton")
        self.radio_3 = ttk.Radiobutton(t_frame_1, text="Admin", variable=self.radio_value, value=3, command=self.radioButtonSelect, style="TreeRadiobutton.TRadiobutton")
        
        lb_2 = ttk.Label(t_frame_2, text="Status: ", font=("TkDefaultFont", 8, "bold"))
        self.radio_00 = ttk.Radiobutton(t_frame_2, text="All", variable=self.radio_value_2, value=0, command=self.radioButtonSelect, style="TreeRadiobutton.TRadiobutton")
        self.radio_10 = ttk.Radiobutton(t_frame_2, text="Employed", variable=self.radio_value_2, value=1, command=self.radioButtonSelect, style="TreeRadiobutton.TRadiobutton")
        self.radio_20 = ttk.Radiobutton(t_frame_2, text="Not-Working", variable=self.radio_value_2, value=2, command=self.radioButtonSelect, style="TreeRadiobutton.TRadiobutton")
        self.radio_30 = ttk.Radiobutton(t_frame_2, text="Absconded", variable=self.radio_value_2, value=3, command=self.radioButtonSelect, style="TreeRadiobutton.TRadiobutton")
    
        self.radio_0.invoke()
        self.radio_00.invoke()
        self.radio_3.pack(side="right", fill="x", padx=5)
        self.radio_2.pack(side="right", fill="x", padx=5)
        self.radio_1.pack(side="right", fill="x", padx=5)
        self.radio_0.pack(side="right", fill="x", padx=5)
        lb_1.pack(side="right", fill="x", padx=(5, 15))

        self.radio_30.pack(side="right", fill="x", padx=5)
        self.radio_20.pack(side="right", fill="x", padx=5)
        self.radio_10.pack(side="right", fill="x", padx=5)
        self.radio_00.pack(side="right", fill="x", padx=5)
        lb_2.pack(side="right", fill="x", padx=(5, 43))

        # Joining Date
        lb_3 = tk.Label(joining_date_frame, text="Joining Date", background="white", font=("TkDefaultFont", 8, "bold"))
        lb_3.pack(side="left", fill="x", padx=5)
        # Calendars
        from_join_label = ttk.Label(joining_date_frame, text="From:", style="CalendarLabel.TLabel")
        from_join_label.pack(side="left", fill="x", padx=5)
        self.from_join_calendar = DateEntry(
            joining_date_frame,
            textvariable=self.from_joining_date,
            justify="center",
            font=("TkDefaultFont", 8, "bold"),
            date_pattern="y-mm-d",
            maxdate=date.today(),
            showothermonthdays=False,
            showweeknumbers=False,
            weekendbackground="white",
            weekendforeground="black",
            )
        self.from_join_calendar.pack(side="left", fill="x", padx=5)
        self.from_join_calendar.bind("<<DateEntrySelected>>", self.dateChanged)
        self.from_join_calendar.delete(0, "end")
        self.from_join_calendar.insert(0, "0000-00-00")

        to_join_label = ttk.Label(joining_date_frame, text="To:", style="CalendarLabel.TLabel")
        to_join_label.pack(side="left", fill="x", padx=5)
        self.to_join_calendar = DateEntry(
            joining_date_frame,
            textvariable=self.to_joining_date,
            justify="center",
            font=("TkDefaultFont", 8, "bold"),
            date_pattern="y-mm-d",
            maxdate=date.today(),
            showothermonthdays=False,
            showweeknumbers=False,
            weekendbackground="white",
            weekendforeground="black"
            )
        self.to_join_calendar.pack(side="left", fill="x", padx=5)
        self.to_join_calendar.bind("<<DateEntrySelected>>", self.dateChanged)
        self.to_join_calendar.delete(0, "end")
        self.to_join_calendar.insert(0, "0000-00-00")

        # Leaving Date
        lb_4 = tk.Label(leaving_date_frame, text="Leaving Date", background="white", font=("TkDefaultFont", 8, "bold"))
        lb_4.pack(side="left", fill="x", padx=5)
        # Calendars
        from_leave_label = ttk.Label(leaving_date_frame, text="From:", style="CalendarLabel.TLabel")
        from_leave_label.pack(side="left", fill="x", padx=5)
        self.from_leave_calendar = DateEntry(
            leaving_date_frame,
            textvariable=self.from_leaving_date,
            justify="center",
            font=("TkDefaultFont", 8, "bold"),
            date_pattern="y-mm-d",
            maxdate=date.today(),
            showothermonthdays=False,
            showweeknumbers=False,
            weekendbackground="white",
            weekendforeground="black"
            )
        self.from_leave_calendar.pack(side="left", fill="x", padx=5)
        self.from_leave_calendar.bind("<<DateEntrySelected>>", self.dateChanged)
        self.from_leave_calendar.delete(0, "end")
        self.from_leave_calendar.insert(0, "0000-00-00")


        to_leave_label = ttk.Label(leaving_date_frame, text="To:", style="CalendarLabel.TLabel")
        to_leave_label.pack(side="left", fill="x", padx=5)
        self.to_leave_calendar = DateEntry(
            leaving_date_frame,
            textvariable=self.to_leaving_date,
            justify="center",
            font=("TkDefaultFont", 8, "bold"),
            date_pattern="y-mm-d",
            maxdate=date.today(),
            showothermonthdays=False,
            showweeknumbers=False,
            weekendbackground="white",
            weekendforeground="black"
            )
        self.to_leave_calendar.pack(side="left", fill="x", padx=5)
        self.to_leave_calendar.bind("<<DateEntrySelected>>", self.dateChanged)
        self.to_leave_calendar.delete(0, "end")
        self.to_leave_calendar.insert(0, "0000-00-00")



    # When any radio button selected
    def radioButtonSelect(self):
         self.insertDataInTree(
            tableRowFetchAndRenderMethod=lambda: self.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.queryFetchPaginatedUser(
                    self.offset,
                    self.limit,
                    self.from_joining_date.get(),
                    self.to_joining_date.get(),
                    self.from_leaving_date.get(),
                    self.to_leaving_date.get(),
                    radio_authority_data=self.radio_value.get(),
                    radio_status_data=self.radio_value_2.get(),
                    query_data=self.search_data.get()
                    )
                )
            )



    # When any date entry changes
    def dateChanged(self, e):
        self.insertDataInTree(
            tableRowFetchAndRenderMethod=lambda: self.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.queryFetchPaginatedUser(
                    self.offset,
                    self.limit,
                    self.from_joining_date.get(),
                    self.to_joining_date.get(),
                    self.from_leaving_date.get(),
                    self.to_leaving_date.get(),
                    radio_authority_data=self.radio_value.get(),
                    radio_status_data=self.radio_value_2.get(),
                    query_data=self.search_data.get()
                    )
                )
            )
        

        
    # Create Rows of Particular Tree with data from database   
    def definingRowsOfParticularTree(self, dataFetchingMethod):
        data = dataFetchingMethod()
        # Inserting Data In Tree
        if len(data) >= 1:
            count = 0
            s_no_count = self.offset
            for i in range(len(data)):
                
                username = self.morphText(data[i][USERNAME], 30)
                email = self.morphText(data[i][EMAIL], 40)   
                reason = self.morphText(data[i][LEAVE_REASON])

                val = (s_no_count+1, data[i][USER_ID], username, email, data[i][USER_AUTHORITY],
                data[i][EMPLOYMENT_STATUS], self.checkNullFormat(data[i][DATE_OF_JOINING]),
                self.checkNullFormat(data[i][DATE_OF_LEAVING]), reason, self.checkNullFormat(data[i][DATE_OF_REHIRING]))       
                
                if count % 2 != 0:
                    self.tree.insert(
                        "",
                        tk.END,
                        values=val,
                        tags=("odd_row",)
                        )
                else:
                    self.tree.insert("",
                                     tk.END,
                                     values=val,
                                     tags=("even_row",)
                                     )
                count = count + 1
                s_no_count = s_no_count + 1
                self.tree.configure(selectmode="extended")
        else:
            self.tree.insert("",
                             tk.END,
                             values=(
                                 "No Records Found",
                                 "No Records Found", 
                                 "No Records Found",
                                 "No Records Found",
                                 "No Records Found", 
                                 "No Records Found",
                                 "No Records Found",
                                 "No Records Found", 
                                 "No Records Found", 
                                 ),
                             tags=("odd_row",)
                             )
            
            self.tree.configure(selectmode="none")

        
       
    # Create Tree Instance and set its Configuration 
    def createTreeAndConfiguration(self):
        
        # Tuple of Tree Columns
        columnTuple = ("s_no", USER_ID, USERNAME, EMAIL, USER_AUTHORITY, EMPLOYMENT_STATUS, DATE_OF_JOINING, DATE_OF_LEAVING, LEAVE_REASON, DATE_OF_REHIRING)
        
        self.tree = ttk.Treeview(self, columns=columnTuple, show="headings", selectmode="extended", style="Tree.Treeview")
        
        # Defining Column Name 
        self.tree.heading("s_no", text="S. No.")
        self.tree.heading(USER_ID, text="User Id")
        self.tree.heading(USERNAME, text="Username")
        self.tree.heading(EMAIL, text="E-Mail")
        self.tree.heading(USER_AUTHORITY, text="User Authority")
        self.tree.heading(EMPLOYMENT_STATUS, text="Employment Status")
        self.tree.heading(LEAVE_REASON, text="Reason of Resigning")
        self.tree.heading(DATE_OF_JOINING, text="Date of Joining")
        self.tree.heading(DATE_OF_LEAVING, text="Date of Leaving")
        self.tree.heading(DATE_OF_REHIRING, text="Date of Rehiring")
        

        # Defining Configuration for Columns
        self.tree.column("s_no", anchor="center", stretch=tk.NO, width=100)
        self.tree.column(USER_ID, anchor="center", stretch=tk.NO, width=100)
        self.tree.column(USERNAME, anchor="center", stretch=tk.NO, width=300)
        self.tree.column(EMAIL, anchor="center", stretch=tk.NO, width=350)
        self.tree.column(USER_AUTHORITY, anchor="center")
        self.tree.column(EMPLOYMENT_STATUS, anchor="center")
        self.tree.column(LEAVE_REASON, anchor="center")
        self.tree.column(DATE_OF_JOINING, anchor="center")
        self.tree.column(DATE_OF_LEAVING, anchor="center")
        self.tree.column(DATE_OF_REHIRING, anchor="center")

        # Giving Striped Rows Style
        self.tree.tag_configure("even_row", background="lightblue")
        self.tree.tag_configure("odd_row", background="white")
        
        # Rendering Tree
        self.tree.grid(row=1, column=0, sticky="nsew")

        
    
    # Frame Configurations for Search above Tables
    def defineAboveFrames(self):
        self.above_frame = ttk.Frame(self, padding=15)
        self.above_frame.grid(row=0, column=0, sticky="nsew")



    # Reset Page
    def customReset(self):
        self.offset = 0
        # Because initially user get data irrespect of date until a date is selected
        self.from_joining_date.set("0000-00-00")
        self.to_joining_date.set("0000-00-00")
        self.from_leaving_date.set("0000-00-00")
        self.to_leaving_date.set("0000-00-00")
        self.insertDataInTree(
            tableRowFetchAndRenderMethod=lambda: self.definingRowsOfParticularTree(
                dataFetchingMethod=lambda: self.queryFetchPaginatedUser(
                    self.offset,
                    self.limit,
                    self.from_joining_date.get(),
                    self.to_joining_date.get(),
                    self.from_leaving_date.get(),
                    self.to_leaving_date.get(),
                    radio_authority_data=self.radio_value.get(),
                    radio_status_data=self.radio_value_2.get(),
                    query_data=self.search_data.get()
                    )
                )
            )