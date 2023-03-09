from tkinter import ttk
from app.main.category import Category
from app.main.supplier import Supplier
from app.main.product import Product
from app.main.sales_order import SalesOrder
from app.main.purchase_order import PurchaseOrder
from app.main.return_cancel_order import ReturnCancelOrder
from app.main.notifications import Notifications
from app.main.user_profile import UserProfile
from app.main.shop_profile import ShopProfile
from app.main.user import User

# Itself is a Frame
class Main(ttk.Frame):
    def __init__(self, main_page_frame_background, user, mysql, *args, **kwargs):
        super().__init__(main_page_frame_background, *args, **kwargs)    
        
        self.mysql = mysql
        self.user = user
        self.grid(row=0, column=0, sticky="nsew")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self["style"] = "MainFrameMainFrame.TFrame"
        
        # Creating Instance of All Contents for Main Page
        self.createInstanceOfAllContent()
       
    # Creating Instance of All Contents for Main Page
    def createInstanceOfAllContent(self):
        self.category_instance =  Category(self, self.mysql, self.user)
        self.supplier_instance =  Supplier(self, self.mysql, self.user)
        self.product_instance =  Product(self, self.mysql, self.user)
        self.sales_order_instance =  SalesOrder(self, self.mysql, self.user)
        self.purchase_order_instance =  PurchaseOrder(self, self.mysql, self.user)
        self.return_cancel_order_instance =  ReturnCancelOrder(self, self.mysql, self.user)
        self.notifications_instance =  Notifications(self, self.mysql, self.user)
        self.profile_instance =  UserProfile(self, self.mysql, self.user)
        self.user_profile_instance =  User(self, self.mysql, self.user)
        self.shop_profile_instance =  ShopProfile(self, self.mysql, self.user)
        
        
    # Rendering Contents for Category Page
    def commandRenderCategory(self):
       self.ungridAllContent()
       self.category_instance.grid(row=0, column=0, sticky="nsew")
    
    # Rendering Contents for Supplier Page
    def commandRenderSupplier(self):
       self.ungridAllContent()
       self.supplier_instance.grid(row=0, column=0, sticky="nsew")
       
    # Rendering Contents for Product Page
    def commandRenderProduct(self):
       self.ungridAllContent()
       self.product_instance.grid(row=0, column=0, sticky="nsew")

    # Rendering Contents for SalesOrder Page
    def commandRenderSalesOrder(self):
       self.ungridAllContent()
       self.sales_order_instance.grid(row=0, column=0, sticky="nsew")

    # Rendering Contents for PurchaseOrder Page
    def commandRenderPurchaseOrder(self):
       self.ungridAllContent()
       self.purchase_order_instance.grid(row=0, column=0, sticky="nsew")

    # Rendering Contents for ReturnCancelOrder Page
    def commandRenderReturnCancelOrder(self):
       self.ungridAllContent()
       self.return_cancel_order_instance.grid(row=0, column=0, sticky="nsew")

    # Rendering Contents for Dashboard Page
    def commandRenderDashboard(self):
       self.ungridAllContent()
       self.notifications_instance.grid(row=0, column=0, sticky="nsew")

    # Rendering Contents for User Profile Page
    def commandRenderUserProfile(self):
       self.ungridAllContent()
       self.profile_instance.grid(row=0, column=0, sticky="nsew")

    # Rendering Contents for User Page
    def commandRenderUser(self):
       self.ungridAllContent()
       self.user_profile_instance.grid(row=0, column=0, sticky="nsew")

    # Rendering Contents for Shop Profile Page
    def commandRenderShopProfile(self):
       self.ungridAllContent()
       self.shop_profile_instance.grid(row=0, column=0, sticky="nsew")

    # Ungriding all the pages from Main Window
    def ungridAllContent(self):
        
        self.category_instance.grid_forget()
        self.category_instance.customReset()
        
        self.supplier_instance.grid_forget()
        self.supplier_instance.customReset()
        
        self.product_instance.grid_forget()
        self.product_instance.customReset()

        self.sales_order_instance.grid_forget()
        self.sales_order_instance.customReset()

        self.purchase_order_instance.grid_forget()
        self.purchase_order_instance.customReset()

        self.notifications_instance.grid_forget()
        self.notifications_instance.customReset()

        self.profile_instance.grid_forget()
        self.profile_instance.customReset()

        self.shop_profile_instance.grid_forget()
        self.shop_profile_instance.customReset()

        self.user_profile_instance.grid_forget()
        self.user_profile_instance.customReset()

        self.return_cancel_order_instance.grid_forget()
        self.return_cancel_order_instance.customReset()