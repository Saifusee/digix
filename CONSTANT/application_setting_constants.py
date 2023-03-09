import sys
from os import path
from mail.mail_config import *
from database.db_config import *

## Imported mail configuration setting constants ##
## Imported database configuration setting constants ##

# App Constants
APPLICATION_NAME = "DigiX"

# Files Name
cus_path = path.split(getattr(sys, "_MEIPASS", path.abspath(path.dirname(__file__)))) 
# Gives File location of constant.py and split() cut string after last slash with two indexes
PATH_TO_ROOT = cus_path[0] # Getting Parent Folder Location
PATH_TO_ROOT = path.split(path.dirname(__file__))[0]
FILE_ERROR_LOGO = "error.png"
FILE_APP_LOGO = "shop_logo.ico"
FILE_APP_DEFAULT_LOGO = "default_shop_logo.ico"
FILE_TABLE_SEARCH_BUTTON = "search_button.png"
PATH_TO_IMAGES = path.join(PATH_TO_ROOT, "assets",  "app_icon")
PATH_TO_INVOICE_ASSETS_FOLDER = path.join(PATH_TO_ROOT, "assets", "invoice")
PATH_TO_EXPORT_DATA_ASSETS_FOLDER = path.join(PATH_TO_ROOT, "assets", "export_data")



# Tk widget Style Constants
## Sidebar Buttons
SIDEBAR_BUTTON_BACKGROUND = "#66ccff"
SIDEBAR_BUTTON_ACTIVE_BACKGROUND = "#262626"
SIDEBAR_BUTTON_ACTIVE_FOREGROUND = "#ffffff"
SIDEBAR_BUTTON_TEXT_WRAP_VALUE = 150
SIDEBAR_BUTTON_FONT = ("Trajan Pro",8, "bold")
## Category Page Tabs Button
CATEGORY_PAGE_TAB_BUTTON_FONT = ("Trajan Pro",10, "bold")
CATEGORY_PAGE_TAB_BUTTON_BACKGROUND = "#99ff99"

## Single Records Display
SINGLE_RECORD_DISPLAY_LABEL_FOREGROUND = "white"
SINGLE_RECORD_DISPLAY_BACKGROUND = "black"
SINGLE_RECORD_DISPLAY_LABEL_TITLE_FONT = ("TkDefaultFont", 10, "bold")
SINGLE_RECORD_DISPLAY_LABEL_VALUE_FONT = ("TkDefaultFont", 10, "italic")
SINGLE_RECORD_DISPLAY_LABEL_WRAPLENGTH = 250

# Extra
TTK_FRAME_DEFAULT_BG_COLOR = "#dcdad5"


# Centered the tkinter toplevel in center
def centerTkinterToplevel(container, toplevel_instance, dx=550, dy=300):
    """
    Set the position of tk.toplevel instance with respect to their conatiner.
    container = parent window
    toplevel_instance = tk.Toplevel intance
    dx = modification in x-axis
    dx = modification in y-axis
    """
    x = container.winfo_x()
    y = container.winfo_y()
    toplevel_instance.geometry("+%d+%d" % (x + dx, y + dy))




