import pandas
from sqlalchemy import create_engine
import shutil
from openpyxl import utils
from openpyxl.styles import Alignment
import os
import datetime
from modal import Modal
from CONSTANT.application_setting_constants import (DATABASE_USER, 
DATABASE_PASSWORD, DATABASE_host, DATABASE_NAME, PATH_TO_EXPORT_DATA_ASSETS_FOLDER)

class ExportDataBase:

    # Setting download locationa and file location in app
    def setFilePaths(self, file_name_prefix):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        # Get the file path in app
        self.file_path = os.path.join(PATH_TO_EXPORT_DATA_ASSETS_FOLDER, f"{file_name_prefix}_{timestamp}.xlsx")
        # Get the home directory path
        home_directory = os.path.expanduser("~")
        # Get the download folder path
        self.download_folder_destination = os.path.join(home_directory, "Downloads")

        # Creating a ExcelWriter object
        self.writer = pandas.ExcelWriter(self.file_path)



    # Creating DataFrame similar to 2d object
    def createDataFrame(self, getQueryMethod=None, query_str=None):
        # Connect to the database
        # Pandas not support mysql.connector but connectors such as SQLAlchemy
        # This code uses the create_engine function from SQLAlchemy to create a new database engine that can
        #  connect to a MySQL database using the mysql-connector-python.
        engine = create_engine(
            f'mysql+mysqlconnector://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_host}/{DATABASE_NAME}'
            )

        if not (type(getQueryMethod) == None.__class__):
            query = getQueryMethod()
        elif not (type(query_str) == None.__class__):
            query = query_str
        else:
            query = ""

        # from Query get data and create dataframe from it
        self.data_frame = pandas.read_sql_query(query, engine)



    # Configure column widths and their alingment
    def configureExcelSheetsWidthAndAlignment(self, sheet_names: list):

        for i in range(len(sheet_names)):
            # get the sheet
            worksheet = self.writer.sheets[sheet_names[i]]
            # Get Single column
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column # int id for columns
                column_letter = utils.get_column_letter(column_letter) # convert int id of columns to respective str() name
                # Get Single field in column
                for cell in column:
                    # Center align
                    cell.alignment = Alignment(horizontal='center')
                    # Find maximum width for a column
                    try: # Necessary to avoid error on empty cells
                        if len(str(cell.value)) > max_length:
                            max_length = len(cell.value)
                    except:
                        pass
                    # increase maximum width by few margin
                    adjusted_width = (max_length + 2) * 1.2
                    # Set new column widths
                    worksheet.column_dimensions[column_letter].width = adjusted_width



    # Move the finished file from app location to download folder
    def moveFileToDownload(self, tk_container=None):
        try:
            # Saving all modification in excel file
            self.writer.close()
            shutil.move(self.file_path, self.download_folder_destination)
            os.startfile(self.download_folder_destination)
            if type(tk_container) == None.__class__:
                Modal(None, "File successfully downloaded to local storage.")
            else:
                Modal(tk_container, "File successfully downloaded to local storage.")
        except Exception as error:
            print(f"Development Error (while moving file to downloads): {error}")