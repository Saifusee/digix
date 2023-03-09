# COMMON
CREATED_AT = "created_at"
UPDATED_AT = "updated_at"
ORDER_RETURNED = "Returned"
ORDER_CANCELLED = "Cancelled"
ORDER_PENDING = "Pending"
ORDER_COMPLETED = "Completed"
CANCELLED_QUANTITY = "cancelled_quantity"
RETURNED_QUANTITY = "returned_quantity"
REFUNDED_AMOUNT = "refund_till_today"
PRODUCT_COUNT = "total_products"
UNIT_COUNT = "total_units"

# SHOP TABLE
SHOP_TABLE_NAME = "shop"
SHOP_ID = "shop_id"
SHOP_NAME = "shop_name"
SHOP_CONTACT_1 = "shop_contact_1"
SHOP_CONTACT_2 = "shop_contact_2"
SHOP_ADDRESS = "shop_address"
SHOP_EMAIL = "shop_email"
SHOP_GST_NUMBER = "shop_gst_number"
SHOP_OWNER_NAME = "shop_owner_name"
SHOP_LOGO = "logo_data"

# USER TABLE
USER_TABLE_NAME = "user"
USER_ID = "user_id"
EMAIL = "email"
USERNAME = "username"
PASSWORD = "password"
USER_CONTACT_1 = "contact_1"
USER_CONTACT_2 = "contact_2"
USER_ADDRESS = "address"
USER_AUTHORITY = "authority"
EMPLOYMENT_STATUS = "working_status"
LEAVE_REASON = "resgination_reason"
USER_USER_CONSTRAINT = "user_user_constraint"
AUTHORITY_PRIMARY = "Admin"
AUTHORITY_SECONDARY = "Management"
AUTHORITY_TERTIARY = "Employee"
AUTHORITY_OPTIONS = (AUTHORITY_PRIMARY, AUTHORITY_SECONDARY, AUTHORITY_TERTIARY) 
ABSCONDED = "Absconded"
EMPLOYED = "Employed"
NOT_EMPLOYED = "Not Employed"
EMPLOYMENT_OPTIONS = (EMPLOYED, NOT_EMPLOYED, ABSCONDED)
DATE_OF_JOINING = "date_of_joining"
DATE_OF_LEAVING = "date_of_leaving"
DATE_OF_REHIRING = "date_of_rehiring"

# USER LOGS TABLE
USER_LOGS_TABLE_NAME = "user_logs"
USER_LOGS_ID = "logs_id"
USER_LOGS_LOG= "log_description"
USER_LOGS_FOREIGNKEY_ACTIVE_USER_ID = "active_user_id"
USER_LOGS_FOREIGNKEY_TARGET_USER_ID = "target_user_id"
USER_LOGS_ACTIVE_USER_CONSTRAINT = "user_logs_active_user_constraint"
USER_LOGS_TARGET_USER_CONSTRAINT = "user_logs_target_user_constraint"
ACTIVE_USER = "active_user"
TARGET_USER = "target_user"

# OTP TABLE
OTP_TABLE_NAME = "otp"
OTP_ID = "otp_table_id"
OTP_REFERENCE = "otp_reference"
OTP_VALUE = "otp"

# CATEGORY TABLE
CATEGORY_TABLE_NAME = "category"
CATEGORY_ID = "category_id"
CATEGORY_NAME = "category_name"

# SUB-CATEGORY TABLE
SUB_CATEGORY_TABLE_NAME = "sub_category"
SUB_CATEGORY_ID = "sub_category_id"
SUB_CATEGORY_NAME = "sub_category_name"
SUB_CATEGORY_FOREIGNKEY_CATEGORY_ID = "category_id"
CATEGORY_SUB_CATEGORY_CONSTRAINT = "category_sub_category_constraint"

# SUPPLIER TABLE
SUPPLIER_TABLE_NAME = "supplier"
SUPPLIER_ID = "supplier_id"
SUPPLIER_NAME = "supplier_name"
SUPPLIER_CONTACT_1 = "supplier_contact_1"
SUPPLIER_CONTACT_2 = "supplier_contact_2"
SUPPLIER_GSTIN = "supplier_gst"
SUPPLIER_ADDRESS = "supplier_address"
SUPPLIER_ORGANIZATION_NAME = "supplier_organization_name"
SUPPLIER_ORGANIZATION_CONTACT_1 = "supplier_organization_contact_1"
SUPPLIER_ORGANIZATION_CONTACT_2 = "supplier_organization_contact_2"
SUPPLIER_ORGANIZATION_ADDRESS = "supplier_organization_address"
SUPPLIER_ACTIVE_STATE = "supplier_is_active"
SUPPLIER_DESCRIPTION = "supplier_description"

# PRODUCT TABLE
PRODUCT_TABLE_NAME = "product"
PRODUCT_ID = "product_id"
PRODUCT_NAME = "product_name"
PRODUCT_PRICE = "product_price"
PRODUCT_QUANTITY = "product_quantity"
PRODUCT_REORDER_QUANTITY = "product_reorder_quantity"
PRODUCT_DESCRIPTION = "product_description"
PRODUCT_FOREIGNKEY_CATEGORY_ID = "category_id"
PRODUCT_FOREIGNKEY_SUB_CATEGORY_ID = "sub_category_id"
PRODUCT_IS_DELETED = "is_delete"
PRODUCT_PRICE_UPDATE_DATETIME = "price_updated_at"
PRODUCT_CATEGORY_CONSTRAINT = "product_category_constraint"
PRODUCT_SUB_CATEGORY_CONSTRAINT = "product_sub_category_constraint"

# PRODUCT LOGS TABLE
PRODUCT_LOGS_TABLE_NAME = "product_logs"
PRODUCT_LOGS_ID = "logs_id"
PRODUCT_LOGS_LOG= "log_description"
PRODUCT_LOGS_FOREIGNKEY_USER_ID = "user_id"
PRODUCT_LOGS_FOREIGNKEY_PRODUCT_ID = "product_id"
PRODUCT_LOGS_PRODUCT_CONSTRAINT = "product_logs_product_constraint"
PRODUCT_LOGS_USER_CONSTRAINT = "product_logs_user_constraint"

# SALES ORDER TABLE
SALES_ORDER_TABLE_NAME = "sales_order"
SALES_ORDER_ID = "sales_order_id"
SALES_ORDER_C_NAME= "customer_name"
SALES_ORDER_C_MOBILE = "customer_contact"
SALES_ORDER_C_EMAIL = "customer_email"
SALES_ORDER_PAYMENT_MODE = "payment_mode"
SALES_ORDER_TOTAL_PRICE = "total_price"
SALES_ORDER_FOREIGNKEY_USER_ID = "user_id"
SALES_ORDER_STATUS = "order_status"
SALES_ORDER_USER_CONSTRAINT = "sales_order_user_constraint"
CARD = "CARD"
CASH = "CASH"
UPI = "UPI"
S_O_PAYMENT_MODE_OPTIONS = (CARD, CASH, UPI)
S_O_ORDER_STATUS_OPTIONS = (ORDER_COMPLETED, ORDER_RETURNED, ORDER_CANCELLED)


# SALES_ORDER_PRODUCT TABLE
SALES_ORDER_PRODUCT_TABLE_NAME = "sales_order_product"
S_O_P_ID = "sales_order_product_id"
S_O_P_FOREIGNKEY_SALES_ORDER_ID = "sales_order_id"
S_O_P_FOREIGNKEY_PRODUCT_ID = "product_id"
S_O_P_PRODUCT_PRICE = PRODUCT_PRICE
S_O_P_PRODUCT_QUANTITY = PRODUCT_QUANTITY
S_O_P_PRODUCT_TOTAL_AMOUNT = "product_total_amount_with_quantity"
S_O_P_SALES_ORDER_CONSTRAINT = "sales_order_product_sales_order_constraint"
S_O_P_PRODUCT_CONSTRAINT = "sales_order_product_product_constraint"

# PURCHASE ORDER TABLE
PURCHASE_ORDER_TABLE_NAME = "purchase_order"
PURCHASE_ORDER_ID = "purchase_order_id"
PURCHASE_ORDER_FOREIGNKEY_SUPPLIER_ID = "supplier_id"
PURCHASE_ORDER_PAYMENT_MODE = "payment_mode"
PURCHASE_ORDER_STATUS = "order_status"
PURCHASE_ORDER_TOTAL_PRICE = "total_price"
PURCHASE_ORDER_FOREIGNKEY_USER_ID = "user_id"
PURCHASE_ORDER_PAYMENT_STATUS = "payment_status"
PURCHASE_ORDER_DELIVERY_STATUS = "delivery_status"
PURCHASE_ORDER_SUPPLIER_CONSTRAINT = "purchase_order_supplier_constraint"
PURCHASE_ORDER_USER_CONSTRAINT = "purchase_order_user_constraint"
CARD = "CARD"
CASH = "CASH"
UPI = "UPI"
CHEQUE = "CHEQUE"
PAYMENT_PENDING = "Payment Due"
PAYMENT_COMPLETED = "Payment Successful"
NOT_DISPATCHED = "Not Dispatched"
DISPATCHED = "Dispatched"
DELIVERED = "Delivered"
P_O_PAYMENT_MODE_OPTIONS = (CARD, CASH, CHEQUE, UPI)
P_O_ORDER_STATUS_OPTIONS = (ORDER_PENDING, ORDER_COMPLETED, ORDER_RETURNED, ORDER_CANCELLED)
P_O_PAYMENT_STATUS_OPTIONS = (PAYMENT_PENDING, PAYMENT_COMPLETED)
P_O_DELIVERY_STATUS_OPTIONS = (NOT_DISPATCHED, DISPATCHED, DELIVERED)

# PURCHASE_ORDER_PRODUCT TABLE
PURCHASE_ORDER_PRODUCT_TABLE_NAME = "purchase_order_product"
P_O_P_ID = "purchase_order_product_id"
P_O_P_FOREIGNKEY_PURCHASE_ORDER_ID = "purchase_order_id"
P_O_P_FOREIGNKEY_PRODUCT_ID = "product_id"
P_O_P_PRODUCT_PRICE = PRODUCT_PRICE
P_O_P_PRODUCT_QUANTITY = PRODUCT_QUANTITY
P_O_P_PRODUCT_TOTAL_AMOUNT = "product_total_amount_with_quantity"
P_O_P_PURCHASE_ORDER_CONSTRAINT = "purchase_order_product_purchase_order_constraint"
P_O_P_PRODUCT_CONSTRAINT = "purchase_order_product_product_constraint"

# PURCHASE ORDER LOGS TABLE
PURCHASE_ORDER_LOGS_TABLE_NAME = "purchase_order_logs"
PURCHASE_ORDER_LOGS_ID = "logs_id"
PURCHASE_ORDER_LOGS_LOG= "log_description"
PURCHASE_ORDER_LOGS_FOREIGNKEY_USER_ID = "user_id"
PURCHASE_ORDER_LOGS_FOREIGNKEY_PURCHASE_ORDER_ID = "purchase_order_id"
PURCHASE_ORDER_LOGS_PURCHASE_ORDER_CONSTRAINT = "purchase_order_logs_purchase_order_constraint"
PURCHASE_ORDER_LOGS_USER_CONSTRAINT = "purchase_order_logs_user_constraint"

# SALES ORDER LOGS TABLE
SALES_ORDER_LOGS_TABLE_NAME = "sales_order_logs"
SALES_ORDER_LOGS_ID = "logs_id"
SALES_ORDER_LOGS_LOG= "log_description"
SALES_ORDER_LOGS_FOREIGNKEY_USER_ID = "user_id"
SALES_ORDER_LOGS_FOREIGNKEY_SALES_ORDER_ID = "sales_order_id"
SALES_ORDER_LOGS_SALES_ORDER_CONSTRAINT = "sales_order_logs_sales_order_constraint"
SALES_ORDER_LOGS_USER_CONSTRAINT = "sales_order_logs_user_constraint"

# RETURN_CANCEL_ORDER TABLE
RETURN_CANCEL_ORDER_TABLE_NAME = "return_cancel_order"
RETURN_CANCEL_ORDER_ID = "return_cancel_order_id"
RETURN_CANCEL_ORDER_FOREIGNKEY_SALES_ORDER_ID = "sales_order_id"
RETURN_CANCEL_ORDER_FOREIGNKEY_PURCHASE_ORDER_ID = "purchase_order_id"
RETURN_CANCEL_ORDER_STATUS = "return_cancel_order_status"
RETURN_CANCEL_ORDER_TOTAL_REFUND_AMOUNT = "total_refunded_amount"
RETURN_CANCEL_ORDER_FOREIGNKEY_USER_ID = "user_id"
RETURN_CANCEL_ORDER_SALES_ORDER_CONSTRAINT = "return_cancel_order_sales_order_constraint"
RETURN_CANCEL_ORDER_PURCHASE_ORDER_CONSTRAINT = "return_cancel_order_purchase_order_constraint"    
RETURN_CANCEL_ORDER_USER_CONSTRAINT = "return_cancel_order_user_constraint"
RETURN_CANCEL_ORDER_STATUS_OPTIONS = (ORDER_COMPLETED, ORDER_CANCELLED)

# RETURN_CANCEL_ORDER_PRODUCT TABLE
RETURN_CANCEL_ORDER_PRODUCT_TABLE_NAME = "return_cancel_order_product"
R_C_O_P_ID = "return_cancel_order_product_id"
R_C_O_P_FOREIGNKEY_RETURN_CANCEL_ORDER_ID = "return_cancel_order_id"
R_C_O_P_FOREIGNKEY_PRODUCT_ID = "product_id"
R_C_O_P_PRODUCT_REFUND_AMOUNT = "refund"
R_C_O_P_PRODUCT_CANCEL_QUANTITY = "cancel_quantity"
R_C_O_P_PRODUCT_RETURN_QUANTITY = "return_quantity"
R_C_O_P_REASON = "return_cancel_reason"
R_C_O_P_RETURN_CANCEL_ORDER_CONSTRAINT = "return_cancel_order_product_return_cancel_order_constraint"
R_C_O_P_PRODUCT_CONSTRAINT = "return_cancel_order_product_product_constraint"

