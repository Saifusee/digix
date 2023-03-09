from tkinter import CENTER, LEFT, ttk
from CONSTANT.application_setting_constants import TTK_FRAME_DEFAULT_BG_COLOR, SINGLE_RECORD_DISPLAY_BACKGROUND, SINGLE_RECORD_DISPLAY_LABEL_FOREGROUND

# padding=(LEFT, TOP, RIGHT, BOTTOM)

# Login and Register Page
COLOR_PRIMARY_LABEL = "#33adff"
ORGANIZATION_LABEL = "#66ff99"
LOGIN_REGISTER_PAGE_HEADING_LABEL = "#80dfff"
COLOR_PRIMARY_BUTTON = "#80b3ff"
COLOR_SECONDARY_BUTTON = "#a6a6a6"
COLOR_BUTTON_RED = "#ff3333"
COLOR_BUTTON_SIGN = "#66ff66"
COLOR_BLACK = "#000000"
COLOR_LIGHT_BLACK = "#333333"
COLOR_WHITE = "#ffffff"
COLOR_YELLOW = "yellow"
COLOR_GREY = "grey"
COLOR_PURPLE_OF_TABLE_HEADING = "#0000ff"

# App Window Sidebar
SIDEBAR_PROFILE_FRAME_LABEL_BACKGROUND = "#ffff4d"
SIDEBAR_BUTTON_FRAME_LABEL_BACKGROUND = "#ccccff"# 8cff66
SIDEBAR_BUTTON_BUTTON_BACKGROUND = "#66ccff"
SIDEBAR_BUTTON_BUTTON_BORDER = "#0077b3"
COLOR_SIDEBAR_BUTTON_BUTTON_ACTIVE_STATE = "#262626"

# Invoice Select SUPPLIER BUTTON
SELECT_SUPPLIER_BUTTON_YELLOW_COLOR = "#ff99ff"

# Entry field
COLOR_RED_FOR_ENTRY_FOCUS = "red"



class CustomStyle(ttk.Style):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.theme_use("clam")
        
        
        #### LABELS ####
        # 1) Login and Register Page
        self.configure("ApplicationLabel1.TLabel", background=COLOR_PRIMARY_LABEL, font=("TkdefaultFont", 20, "bold"))
        self.configure("OraganizationLabel1.TLabel", background=ORGANIZATION_LABEL, font=("TkdefaultFont", 10, "bold"))
        self.configure("PageHeadingLabel.TLabel", background=LOGIN_REGISTER_PAGE_HEADING_LABEL, foreground=COLOR_BLACK, font=("TkdefaultFont", 10, "bold"))
        self.configure("LoginLabel.TLabel", anchor="w", justify=LEFT, font=("TkdefaultFont", 10, "bold"), padding=10)
        self.configure("ErrorLoginRegisterLabel.TLabel", anchor=CENTER, justify=CENTER, foreground="red", font=("TkdefaultFont", 10, "bold"), padding=5)
        self.configure("SuccessfulLoginRegisterLabel.TLabel", anchor=CENTER, justify=CENTER, foreground="green", font=("TkdefaultFont", 10, "bold"), padding=5)
        # 2) App Window Sidebar
        self.configure("SidebarProfileLabel.TLabel", background=SIDEBAR_PROFILE_FRAME_LABEL_BACKGROUND, wraplength=150, justify=CENTER)
        self.configure("SideBarButtonLabel.TLabel", anchor="w", background=SIDEBAR_BUTTON_FRAME_LABEL_BACKGROUND, justify=LEFT)
        # 3) Error Window
        self.configure("Errorlabel.TLabel", justify=CENTER, anchor=CENTER, font=("TkdefaultFont", 10, "bold"), padding=5)
        # 4) Show Treeview or Table Title
        self.configure("TreeviewTitleLabel.TLabel", foreground=COLOR_BLACK, font=("TkdefaultFont", 22, "bold","italic"), padding=10)
        # 5) Create Sales Order Right Hand Side Invoice Details
        self.configure("InvoiceDetailsPageHeadLabel.TLabel", background="#c2c2d6", font=("TkDefaultFont", 12, "bold"), anchor=CENTER)
        self.configure("InvoiceDetailsHeadLabel.TLabel", background="#e1e1ea", font=("TkDefaultFont", 9, "bold"), anchor=CENTER)
        self.configure("QuantityPopUpLabel.TLabel", justify=CENTER, anchor=CENTER, font=("TkdefaultFont", 12, "bold"), wraplength=500)
        # 6) Create Purchase Order 
        self.configure("SupplierLabels.TLabel", justify=CENTER, anchor=LEFT, font=("TkdefaultFont", 10, "bold"), wraplength=300)
        # 7) Calendar Label
        self.configure("CalendarLabel.TLabel", anchor="w", justify=LEFT, background=COLOR_WHITE, foreground=COLOR_BLACK, font=("TkdefaultFont", 8, "bold"), padding=10)
        # 8) Change Order Status PopUp
        self.configure("ChangeOrderStatusTitle.TLabel", font=("TkDefaultFont", 12, "bold"), anchor=CENTER, justify=CENTER, background=COLOR_PRIMARY_LABEL)
        self.configure("ChangeOrderStatusId.TLabel", anchor=CENTER, justify=CENTER, font=("TkdefaultFont", 10, "bold"), wraplength=500)
        # 8) Record Order Line of white color
        self.configure("EmptyLineLabel.TLabel", background=COLOR_WHITE)
        # 8) Profile Pages
        self.configure("ProfileLabels.TLabel", foreground=SINGLE_RECORD_DISPLAY_LABEL_FOREGROUND, background=SINGLE_RECORD_DISPLAY_BACKGROUND, justify=CENTER, anchor=CENTER, font=("TkdefaultFont", 12, "bold"), wraplength=400)
             
        #### BUTTONS ####
        # 1) Login and Register Page
        self.configure("LoginRegisterButton.TButton", background=COLOR_PRIMARY_BUTTON, bordercolor=COLOR_BLACK, font=("TkDefaultFont",10,"bold"), focuscolor=COLOR_PRIMARY_BUTTON)
        self.map("LoginRegisterButton.TButton", background = [("active", COLOR_LIGHT_BLACK), ("disabled", COLOR_GREY)], foreground = [("active", COLOR_WHITE)], focuscolor=[("active", COLOR_LIGHT_BLACK), ("disabled", COLOR_GREY)])
        self.configure("ResetCancelButton.TButton", background=COLOR_BUTTON_RED, bordercolor=COLOR_BLACK, font=("TkDefaultFont",10,"bold"), focuscolor=COLOR_BUTTON_RED)
        self.map("ResetCancelButton.TButton", background = [("active", COLOR_LIGHT_BLACK), ("disabled", COLOR_GREY)], foreground = [("active", COLOR_WHITE)], focuscolor=[("active", COLOR_LIGHT_BLACK), ("disabled", COLOR_GREY)])
        self.configure("SignButton.TButton", background=COLOR_BUTTON_SIGN, bordercolor=COLOR_BLACK, font=("TkDefaultFont",10,"bold"), focuscolor=COLOR_BUTTON_SIGN)
        self.map("SignButton.TButton", background = [("active", COLOR_LIGHT_BLACK), ("disabled", COLOR_GREY)], foreground = [("active", COLOR_WHITE)], focuscolor=[("active", COLOR_LIGHT_BLACK), ("disabled", COLOR_GREY)])
        # 2) App Window SideBar
        self.configure("SideBarButtons.TButton", background=SIDEBAR_BUTTON_BUTTON_BACKGROUND, bordercolor=COLOR_BLACK, font=("TkDefaultFont",8,"bold"), focuscolor=SIDEBAR_BUTTON_BUTTON_BACKGROUND)
        self.map("SideBarButtons.TButton",  background = [("active", COLOR_SIDEBAR_BUTTON_BUTTON_ACTIVE_STATE), ("disabled", COLOR_GREY)], foreground = [("active", COLOR_WHITE)], focuscolor=[("active", COLOR_SIDEBAR_BUTTON_BUTTON_ACTIVE_STATE), ("disabled", COLOR_GREY)])
        # 3) Pagination and Table Operations
        self.configure("TreeviewPaginateButtons.TButton", background=SIDEBAR_BUTTON_BUTTON_BACKGROUND, bordercolor=COLOR_BLACK, font=("TkDefaultFont",8,"bold"), focuscolor=SIDEBAR_BUTTON_BUTTON_BACKGROUND)
        self.map("TreeviewPaginateButtons.TButton",  background = [("active", COLOR_SIDEBAR_BUTTON_BUTTON_ACTIVE_STATE), ("disabled", COLOR_GREY)], foreground = [("active", COLOR_WHITE)], focuscolor=[("active", COLOR_SIDEBAR_BUTTON_BUTTON_ACTIVE_STATE), ("disabled", COLOR_GREY)])
        # 4) Single Record Page Link Buttons
        self.configure("SingleRecordLinkButton.TButton", background=COLOR_YELLOW,bordercolor=COLOR_BLACK, font=("TkDefaultFont",10,"bold"), focuscolor=COLOR_YELLOW)
        self.map("SingleRecordLinkButton.TButton",  background = [("active", COLOR_SIDEBAR_BUTTON_BUTTON_ACTIVE_STATE), ("disabled", COLOR_GREY)], foreground = [("active", COLOR_WHITE)], focuscolor=[("active", COLOR_SIDEBAR_BUTTON_BUTTON_ACTIVE_STATE), ("disabled", COLOR_GREY)])
        # 5) Select Supplier For Invoice Button
        self.configure("SelectSupplierButton.TButton", background=SELECT_SUPPLIER_BUTTON_YELLOW_COLOR, bordercolor=COLOR_BLACK, font=("TkDefaultFont",10,"bold"), focuscolor=SELECT_SUPPLIER_BUTTON_YELLOW_COLOR)
        self.map("SelectSupplierButton.TButton",  background = [("active", COLOR_SIDEBAR_BUTTON_BUTTON_ACTIVE_STATE), ("disabled", COLOR_GREY)], foreground = [("active", COLOR_WHITE)], focuscolor=[("active", COLOR_SIDEBAR_BUTTON_BUTTON_ACTIVE_STATE), ("disabled", COLOR_GREY)])

        
        #### Entry ####
        
        self.configure("ErrorEntry.TEntry", bordercolor=COLOR_RED_FOR_ENTRY_FOCUS, highlightcolor=COLOR_RED_FOR_ENTRY_FOCUS)
        
        #### FRAMES ####
        # 2) App Window Sidebar
        self.configure("SidebarProfileFrame.TFrame", background=SIDEBAR_PROFILE_FRAME_LABEL_BACKGROUND)
        self.configure("SideBarButtonFrame.TFrame", background=SIDEBAR_BUTTON_FRAME_LABEL_BACKGROUND)
        # 3) Main Page
        self.configure("MainFrameBackgroundFrame.TFrame", background=COLOR_BLACK)
        self.configure("MainFrameMainFrame.TFrame", background=COLOR_WHITE)
        self.configure("a.TFrame", anchor="c", justify=CENTER)
        
        
        #### TREEVIEW ####
        # ) In General to all Treeview
        # Configuring Heading Style
        self.configure("Tree.Treeview.Heading", font=("TkDefaultFont", 12, "bold"), rowheight=10, background=COLOR_PURPLE_OF_TABLE_HEADING, foreground=COLOR_WHITE, bordercolor=COLOR_BLACK)
        self.map("Tree.Treeview.Heading", background=[("active", COLOR_PURPLE_OF_TABLE_HEADING,)], foreground=[("active", COLOR_WHITE,)], bordercolor=[("active", COLOR_BLACK,)])
        # Configuring Row Style
        self.configure("Tree.Treeview", padding=15, font=("TkDefaultFont", 12), rowheight=30)
        self.map("Tree.Treeview", background=[("selected", COLOR_LIGHT_BLACK)])
        # 2) Treeview for showing selected product details in invoice
        # Configuring Heading Style
        self.configure("SelectedProductInInvoiceTree.Treeview.Heading", font=("TkDefaultFont", 8, "bold"), rowheight=5, background=COLOR_WHITE, foreground=COLOR_BLACK, bordercolor=COLOR_BLACK)
        self.map("SelectedProductInInvoiceTree.Treeview.Heading", background=[("active", COLOR_WHITE,)], foreground=[("active", COLOR_BLACK,)], bordercolor=[("active", COLOR_BLACK,)])
        # Configuring Row Style
        self.configure("SelectedProductInInvoiceTree.Treeview", padding=15, font=("TkDefaultFont", 8), rowheight=15)
        self.map("SelectedProductInInvoiceTree.Treeview", background=[("selected", COLOR_LIGHT_BLACK)])
        
        
    
        #### Radiobutton ####
        # 1) Treeview
        self.configure("TreeRadiobutton.TRadiobutton", font=("TkDefaultFont", 8, "bold"), focuscolor=TTK_FRAME_DEFAULT_BG_COLOR)
        self.map("TreeRadiobutton.TRadiobutton", background=[("active", TTK_FRAME_DEFAULT_BG_COLOR),], focuscolor=[("active", TTK_FRAME_DEFAULT_BG_COLOR)])
        # 2) Return/Cancel Order
        self.configure("OrderRadiobutton.TRadiobutton", font=("TkDefaultFont", 10, "bold"), focuscolor=TTK_FRAME_DEFAULT_BG_COLOR)
        self.map("OrderRadiobutton.TRadiobutton", background=[("active", TTK_FRAME_DEFAULT_BG_COLOR),], focuscolor=[("active", TTK_FRAME_DEFAULT_BG_COLOR)])

        
        
        
        #### Combobox #### 
        # 1) Treeview Limit
        self.map("ShowProduct.TCombobox", fieldbackground=[('readonly', COLOR_WHITE)], selectbackground=[('readonly', COLOR_WHITE)], background=[('readonly', COLOR_WHITE)], selectforeground=[('readonly', COLOR_BLACK)], foreground=[('readonly', COLOR_BLACK)])
        # 2) Show Product
        self.map("TreeviewLimit.TCombobox", fieldbackground=[('readonly', TTK_FRAME_DEFAULT_BG_COLOR)], selectbackground=[('readonly', TTK_FRAME_DEFAULT_BG_COLOR)], background=[('readonly', TTK_FRAME_DEFAULT_BG_COLOR)], selectforeground=[('readonly', COLOR_BLACK)], foreground=[('readonly', COLOR_BLACK)])


        #### Checkbutton #### 
        # 1) Show Password
        self.configure("ShowPasswordCheckButton.TCheckbutton", font=("TkDefaultFont", 8), focuscolor=TTK_FRAME_DEFAULT_BG_COLOR)
        self.map("ShowPasswordCheckButton.TCheckbutton", background=[("active", TTK_FRAME_DEFAULT_BG_COLOR),], focuscolor=[("active", TTK_FRAME_DEFAULT_BG_COLOR)])



        ##########          IMPORTANT          ##########
        # print(self.layout("TCombobox")) # Show All elements
        # print(self.element_options("Combobox.downarrow")) # Show all option available