import tkinter as tk
from tkinter import ttk
from CONSTANT.index import *
from database.dbconnection import Connection
from error import ErrorModal
from app.base import Base

class POStatusChangeEntry(tk.Toplevel, Base):
    def __init__(self, container, mysql, user, order_id, refreshedTableMethod, *args, **kwargs) -> None:
        super().__init__(container, *args, **kwargs)
        Base.__init__(self, mysql, user)

        self.grab_set()
        try:
            self.image = path.join(PATH_TO_IMAGES, FILE_APP_LOGO)
            self.iconbitmap(self.image)
        except Exception:
            self.image = path.join(PATH_TO_IMAGES, FILE_APP_DEFAULT_LOGO)
            self.iconbitmap(self.image)
            
        centerTkinterToplevel(container, self, dx=500, dy=200)
        self.resizable(False, False)
        self.refreshedTableMethod = lambda: refreshedTableMethod()

        self.order_id = order_id
        self.mysql = ""
        self.payment_status_data = tk.StringVar()
        self.payment_status_option_list = P_O_PAYMENT_STATUS_OPTIONS
        self.delivery_status_data = tk.StringVar()
        self.delivery_status_option_list = P_O_DELIVERY_STATUS_OPTIONS
        self.temp_payment_status = "" 
        self.temp_delivery_status = ""
        self.order_status = ""

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        frame = ttk.Frame(self)
        frame.grid(row=0, column=0, sticky="nsew")

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        lb0 = ttk.Label(frame, text="Change Order Status", style="ChangeOrderStatusTitle.TLabel")
        lb0.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=(10, 0))
        self.label = ttk.Label(frame, text="HP NEVERSTOP + 12212", style="ChangeOrderStatusId.TLabel")
        self.label.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(10, 0))

        lb = ttk.Label(frame, text="Payment Status: ", style="LoginLabel.TLabel")
        lb.grid(row=2, column=0, sticky="w", pady=(10, 0), padx=10)
        self.payment_status_entry = ttk.Combobox(
            frame,
            textvariable=self.payment_status_data,
            values=self.payment_status_option_list, 
            width=50,
            font=("TkdefaultFont", 10, "bold"),
            justify="center",
            style="ShowProduct.TCombobox",
            state="readonly",
            )
        self.payment_status_entry.current(0)
        self.payment_status_entry.grid(row=2, column=1, sticky="ew", pady=(10, 0), padx=10)

        lb = ttk.Label(frame, text="Delivery Status: ", style="LoginLabel.TLabel")
        lb.grid(row=3, column=0, sticky="w", pady=(10, 0), padx=10)
        self.delivery_status_entry = ttk.Combobox(
            frame,
            textvariable=self.delivery_status_data,
            values=self.delivery_status_option_list, 
            width=25,
            font=("TkdefaultFont", 10, "bold"),
            justify="center",
            style="ShowProduct.TCombobox",
            state="readonly",
            )
        self.delivery_status_entry.current(0)
        self.delivery_status_entry.grid(row=3, column=1, sticky="ew", pady=(10, 0), padx=10)

        self.button = ttk.Button(frame, text="Submit", command=self.submitStatus, style="SignButton.TButton")
        self.button.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(10, 10))

        # Fetching Order Details
        self.fetchOrderDetails()

        # If order already completed than no change at all
        if self.order_status == ORDER_COMPLETED:
            self.delivery_status_entry.configure(state="disabled")
            self.payment_status_entry.configure(state="disabled")
            self.button.configure(state="disabled")
            lb = ttk.Label(frame, text="Successfully completed order cannot be modified.", style="ChangeOrderStatusId.TLabel")
            lb.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(10, 10))



    def submitStatus(self):
        # If any changes take place
        if (not (self.temp_delivery_status == self.delivery_status_data.get())) or (not (self.temp_payment_status == self.payment_status_data.get())):
            # Updating log details
            try:
                order_status = ORDER_COMPLETED if (self.payment_status_data.get() == PAYMENT_COMPLETED) and (self.delivery_status_data.get() == DELIVERED) else ORDER_PENDING
                query = f"""UPDATE `{DATABASE_NAME}`.`{PURCHASE_ORDER_TABLE_NAME}` 
                SET `{PURCHASE_ORDER_STATUS}` = '{order_status}' , `{PURCHASE_ORDER_DELIVERY_STATUS}` = '{self.delivery_status_data.get()}' ,
                `{PURCHASE_ORDER_PAYMENT_STATUS}` = '{self.payment_status_data.get()}' WHERE `{PURCHASE_ORDER_ID}` = {self.order_id} ;"""
                self.executeCommitSqlQuery(PURCHASE_ORDER_TABLE_NAME, query)

            except Exception as error:
                print(f"Development Error (While updating order details): {error}")
                ErrorModal("Something went wrong, please contact the software developer")

            # Creating Log
            try:
                log_data = ""
                if not (self.temp_delivery_status == self.delivery_status_data.get()):
                    log_data = f'Order delivery status changed from "{self.temp_delivery_status}" to "{self.delivery_status_data.get()}"'
                if not (self.temp_payment_status == self.payment_status_data.get()):
                    log_data = f'Order payment status changed from "{self.temp_payment_status}" to "{self.payment_status_data.get()}"'
                if (not (self.temp_delivery_status == self.delivery_status_data.get())) and (not (self.temp_payment_status == self.payment_status_data.get())):
                    log_data = f'Order delivery status changed from "{self.temp_delivery_status}" to "{self.delivery_status_data.get()}" and order payment status changed from "{self.temp_payment_status}" to "{self.payment_status_data.get()}"'

                query_log = f"""INSERT INTO `{DATABASE_NAME}`.`{PURCHASE_ORDER_LOGS_TABLE_NAME}` 
                (`{PURCHASE_ORDER_LOGS_LOG}` , `{PURCHASE_ORDER_LOGS_FOREIGNKEY_PURCHASE_ORDER_ID}` , `{PURCHASE_ORDER_LOGS_FOREIGNKEY_USER_ID}`)
                VALUES ('{log_data}' , {self.order_id} , {self.current_user[USER_ID]}) ;"""

                self.executeCommitSqlQuery(PURCHASE_ORDER_LOGS_TABLE_NAME, query_log)


                # If product is delivered then increased product quantities in inventory
                if self.delivery_status_data.get() == DELIVERED:

                    product_data = self.queryFetchAllPurchaseOrderProduct(self.order_id)
                    for product in product_data:
                        product_id = product[PRODUCT_ID]
                        product_order_quantity = int(product[PRODUCT_QUANTITY])
                        product_order_cancelled_quantity = int(product[CANCELLED_QUANTITY])
                        product_order_returned_quantity = int(product[RETURNED_QUANTITY])
                        effective_purchase_order_quantity = (product_order_quantity - product_order_cancelled_quantity) - product_order_returned_quantity
                        query_get_quantity = f"SELECT `{PRODUCT_QUANTITY}` FROM `{DATABASE_NAME}`.`{PRODUCT_TABLE_NAME}` WHERE `{PRODUCT_ID}` = {product_id}"
                        already_available_quantity = int(self.executeFetchSqlQuery(PRODUCT_TABLE_NAME, query_get_quantity)[0][PRODUCT_QUANTITY])

                        query_product_quantity = f"""UPDATE `{DATABASE_NAME}`.`{PRODUCT_TABLE_NAME}` 
                        SET `{PRODUCT_QUANTITY}` = '{already_available_quantity + effective_purchase_order_quantity}'
                        WHERE `{PRODUCT_ID}` = {product_id}""" 
                        self.executeCommitSqlQuery(PRODUCT_TABLE_NAME, query_product_quantity)


                        # Add inventory addition log to product_log table
                        query_logs_2 = f"""INSERT INTO `{DATABASE_NAME}`.`{PRODUCT_LOGS_TABLE_NAME}`
                        ( 
                            `{PRODUCT_LOGS_LOG}`, `{PRODUCT_LOGS_FOREIGNKEY_PRODUCT_ID}`, `{PRODUCT_LOGS_FOREIGNKEY_USER_ID}`
                        )
                        VALUES (%(log)s, %(p_o_id)s, %(user_id)s)"""

                        query_logs_parameters_2 = {
                            "log": f'x {effective_purchase_order_quantity} unit added to inventory via Purchase Order Id = {self.order_id}.',
                            "p_o_id": product_id,
                            "user_id": self.current_user[USER_ID]
                        }
                        self.executeCommitSqlQuery(PRODUCT_LOGS_TABLE_NAME, query_logs_2, query_logs_parameters_2)

                self.refreshedTableMethod()
                self.destroy()
            except Exception as error:
                print(f"Development Error (While creating purchase order log): {error}")
                ErrorModal("Something went wrong, please contact the software developer")



    # Fetching Order Details
    def fetchOrderDetails(self):
        try:
            self.mysql = Connection()
            query = f"SELECT * FROM `{DATABASE_NAME}`.`{PURCHASE_ORDER_TABLE_NAME}` WHERE `{PURCHASE_ORDER_ID}` = {self.order_id}"
            self.mysql.query.execute(query)
            data = self.mysql.query.fetchall()
            self.temp_payment_status = data[0][PURCHASE_ORDER_PAYMENT_STATUS]
            self.temp_delivery_status = data[0][PURCHASE_ORDER_DELIVERY_STATUS]
            self.order_status = data[0][PURCHASE_ORDER_STATUS]
            self.payment_status_data.set(self.temp_payment_status)
            self.delivery_status_data.set(self.temp_delivery_status)
        except Exception as error:
            print(f"Development Error (While fetching order details): {error}")
            ErrorModal("Something went wrong, please contact the software developer")