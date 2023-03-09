from CONSTANT.table_constants import  *
from app.main.external_files.export_data_base import ExportDataBase

class ExportUserData(ExportDataBase):
    def __init__(self, getQueryMethod, container=None):
        super().__init__()

        # Setting download locationa and file location in app
        self.setFilePaths(file_name_prefix="users")
        
        # Creating DataFrame similar to 2d object
        self.createDataFrame(lambda: getQueryMethod())

        # Not show password data
        self.data_frame.pop(PASSWORD)
        # Custom Column Names
        columns_dictionary = {
            USER_ID: "User Id",
            USERNAME: "Username",
            EMAIL: "E-Mail",
            USER_CONTACT_1: "Primary Contact",
            USER_CONTACT_2: "Secondary Contact",
            USER_ADDRESS: "Address",
            USER_AUTHORITY: "User Authority",
            EMPLOYMENT_STATUS: "Employment Status",
            DATE_OF_JOINING: "Date of Joining",
            DATE_OF_LEAVING: "Date of Leaving",
            LEAVE_REASON: "Reason for Resignation",
            DATE_OF_REHIRING: "Date of Rehiring",
            LEAVE_REASON: "Reason for leaving job"
        }
        # Give custom column names to the DataFrame
        self.data_frame = self.data_frame.rename(columns=columns_dictionary)
        

        # Write the data to an Excel file
        self.data_frame.to_excel(self.writer, sheet_name="Users", index=False, na_rep="")

        # set width and center alignments to all columns
        self.configureExcelSheetsWidthAndAlignment(sheet_names=["Users"])

        if type(container) == None.__class__:
            # Moving excel file from app to downloads
            self.moveFileToDownload()
        else:
            # Moving excel file from app to downloads
            self.moveFileToDownload(container)