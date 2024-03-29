from CONSTANT.table_constants import  *
from app.main.external_files.export_data_base import ExportDataBase

class ExportSalesOrderData(ExportDataBase):
    def __init__(self, getQueryMethod, container=None):
        super().__init__()

        # Setting download locationa and file location in app
        self.setFilePaths(file_name_prefix="sales_order")
        
        # Creating DataFrame for main sales order table similar to 2d object
        self.createDataFrame(lambda: getQueryMethod())


        # Getting all the selected sales order id
        sales_order_id_tuple = tuple(self.data_frame[SALES_ORDER_ID].values)
        
        # Custom Column Names for Sales Order
        columns_dictionary_main = {
            SALES_ORDER_ID: "Sales Order Id",
            SALES_ORDER_C_NAME: "Customer Name",
            SALES_ORDER_C_MOBILE: "Customer Mobile",
            SALES_ORDER_C_EMAIL: "Customer E-Mail",
            SALES_ORDER_PAYMENT_MODE: "Payment Mode",
            SALES_ORDER_TOTAL_PRICE: "Total Bill Amount (INR)",
            SALES_ORDER_FOREIGNKEY_USER_ID: "Generated By (User Id)",
            USERNAME: "Generated By (Username)",
            SALES_ORDER_STATUS: "Order Status",
            CREATED_AT: "Generated At",
        }
        # Give custom column names to the DataFrame of Sales Order
        self.data_frame = self.data_frame.rename(columns=columns_dictionary_main)

        # Write the data to an Excel file
        self.data_frame.to_excel(self.writer, sheet_name="Sales Order Details", index=False, na_rep="")
        # Query for get SALES_ORDER_PRODUCT
        if len(sales_order_id_tuple) == 1:
            # When only one element in tuple (1,) comma will give error in sql statement
            query_sales_order_product = f"SELECT * FROM  `{SALES_ORDER_PRODUCT_TABLE_NAME}` WHERE `{S_O_P_FOREIGNKEY_SALES_ORDER_ID}` IN ({sales_order_id_tuple[0]});"
        else:
            query_sales_order_product = f"SELECT * FROM  `{SALES_ORDER_PRODUCT_TABLE_NAME}` WHERE `{S_O_P_FOREIGNKEY_SALES_ORDER_ID}` IN {sales_order_id_tuple};"

        # Creating DataFrame for main sales order products table similar to 2d object
        self.createDataFrame(query_str=query_sales_order_product)

        # Remove first Column
        self.data_frame.pop(S_O_P_ID)
        # Custom Column Names for Sales Order
        columns_dictionary_sub = {
            S_O_P_ID: "Id",
            S_O_P_FOREIGNKEY_SALES_ORDER_ID: "Sales Order Id",
            S_O_P_FOREIGNKEY_PRODUCT_ID: "Product Id",
            PRODUCT_NAME: "Product Name",
            S_O_P_PRODUCT_PRICE: "Selling Price",
            S_O_P_PRODUCT_QUANTITY: "Sold quantity",
            S_O_P_PRODUCT_TOTAL_AMOUNT: "Total for product (INR)",
            RETURNED_QUANTITY: "Returned Quantities",
            CANCELLED_QUANTITY: "Cancelled Quantities",
            REFUNDED_AMOUNT: "Amount Refunded (INR)",
            CREATED_AT: "Generated At",
        }
        # Give custom column names to the DataFrame of Sales Order
        self.data_frame = self.data_frame.rename(columns=columns_dictionary_sub)

        # Write the data to an Excel file
        self.data_frame.to_excel(self.writer, sheet_name="Product Details in Orders", index=False, na_rep="")

        # set width and center alignments to all columns
        self.configureExcelSheetsWidthAndAlignment(sheet_names = ["Sales Order Details", "Product Details in Orders"])

        if type(container) == None.__class__:
            # Moving excel file from app to downloads
            self.moveFileToDownload()
        else:
            # Moving excel file from app to downloads
            self.moveFileToDownload(container)