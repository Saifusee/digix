from CONSTANT.table_constants import  *
from app.main.external_files.export_data_base import ExportDataBase

class ExportSupplierData(ExportDataBase):
    def __init__(self, getQueryMethod, container=None):
        super().__init__()

        # Setting download locationa and file location in app
        self.setFilePaths(file_name_prefix="supplier")
        
        # Creating DataFrame similar to 2d object
        self.createDataFrame(lambda: getQueryMethod())


        # Modify Data in dataframe: dataframe[ColumnName].apply(callback) where callback takes field value of that column
        self.data_frame[SUPPLIER_ACTIVE_STATE] = self.data_frame[SUPPLIER_ACTIVE_STATE].apply(self.customIsSupplierActive)

        # Custom Column Names
        columns_dictionary = {
            SUPPLIER_ID: "Supplier Id",
            SUPPLIER_NAME: "Supplier Name",
            SUPPLIER_CONTACT_1: "Supplier Contact 1",
            SUPPLIER_CONTACT_2: "Supplier Contact 2",
            SUPPLIER_ADDRESS: "Supplier Address",
            SUPPLIER_GSTIN: "Supplier GSTIN",
            SUPPLIER_ACTIVE_STATE: "Supplier Status",
            SUPPLIER_ORGANIZATION_NAME: "Supplier's Organization Name",
            SUPPLIER_ORGANIZATION_CONTACT_1: "Organization's Contact 1",
            SUPPLIER_ORGANIZATION_CONTACT_2: "Organization Contact 2",
            SUPPLIER_ORGANIZATION_ADDRESS: "Organization Address",
            SUPPLIER_DESCRIPTION: "Supplier Description",
            CREATED_AT: "Registered on",
        }
        # Give custom column names to the DataFrame
        self.data_frame = self.data_frame.rename(columns=columns_dictionary)
        

        # Write the data to an Excel file
        self.data_frame.to_excel(self.writer, sheet_name="Supplier Details", index=False, na_rep="")

        # set width and center alignments to all columns
        self.configureExcelSheetsWidthAndAlignment(sheet_names=["Supplier Details"])

        if type(container) == None.__class__:
            # Moving excel file from app to downloads
            self.moveFileToDownload()
        else:
            # Moving excel file from app to downloads
            self.moveFileToDownload(container)



    # Modify is_delete column value for user
    def customIsSupplierActive(self, value):
        if value == 0:
            return "Inactive"
        else:
            return "Active"