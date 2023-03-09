from CONSTANT.table_constants import  *
from app.main.external_files.export_data_base import ExportDataBase

class ExportProductData(ExportDataBase):
    def __init__(self, getQueryMethod, container=None):
        super().__init__()

        # Setting download locationa and file location in app
        self.setFilePaths(file_name_prefix="product")
        
        # Creating DataFrame similar to 2d object
        self.createDataFrame(lambda: getQueryMethod())


        # Modify Data in dataframe: dataframe[ColumnName].apply(callback) where callback takes field value of that column
        self.data_frame[PRODUCT_IS_DELETED] = self.data_frame[PRODUCT_IS_DELETED].apply(self.customIsProductDeleted)

        # Custom Column Names
        columns_dictionary = {
            PRODUCT_ID: "Product Id",
            PRODUCT_NAME: "Product Name",
            PRODUCT_PRICE: "Unit Price",
            PRODUCT_QUANTITY: "Quantity",
            PRODUCT_REORDER_QUANTITY: "Reorder Value",
            PRODUCT_DESCRIPTION: "Product Description",
            PRODUCT_FOREIGNKEY_CATEGORY_ID: "Category Id",
            CATEGORY_NAME: "Category Name",
            PRODUCT_FOREIGNKEY_SUB_CATEGORY_ID: "Sub-Category Id",
            SUB_CATEGORY_NAME: "Sub-Category Name",
            CREATED_AT: "Registration Date",
            UPDATED_AT: "Product Updated At",
            PRODUCT_PRICE_UPDATE_DATETIME: "Price Updated At",
            PRODUCT_IS_DELETED: "Product Status",
        }
        # Give custom column names to the DataFrame
        self.data_frame = self.data_frame.rename(columns=columns_dictionary)
        

        # Write the data to an Excel file
        self.data_frame.to_excel(self.writer, sheet_name="Product Details", index=False, na_rep="")

        # set width and center alignments to all columns
        self.configureExcelSheetsWidthAndAlignment(sheet_names=["Product Details"])

        if type(container) == None.__class__:
            # Moving excel file from app to downloads
            self.moveFileToDownload()
        else:
            # Moving excel file from app to downloads
            self.moveFileToDownload(container)



    # Modify is_delete column value for user
    def customIsProductDeleted(self, value):
        if value == 0:
            return "Active Product"
        else:
            return "Inactive Product"