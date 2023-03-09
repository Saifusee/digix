from CONSTANT.index import *
from error import ErrorModal
import tkinter as tk
from database.dbconnection import Connection



class Base():
    
    # Get Category Table with required columns
    saved_query_user_morphed = f"""SELECT * FROM 
    (SELECT A.{USER_ID}, A.{USERNAME}, A.{EMAIL}, A.{PASSWORD}, A.{USER_CONTACT_1}, A.{USER_CONTACT_2}, A.{USER_ADDRESS}, 
    A.{USER_AUTHORITY}, A.{EMPLOYMENT_STATUS}, A.{DATE_OF_JOINING}, A.{DATE_OF_LEAVING}, A.{DATE_OF_REHIRING}, A.{LEAVE_REASON}
    FROM {DATABASE_NAME}.{USER_TABLE_NAME} AS A )
    AS merge_table """

    # Get Category Table with required columns
    saved_query_category = f"""SELECT * FROM {DATABASE_NAME}.{CATEGORY_TABLE_NAME}"""
    
    # Get Sub-Category Table  without foreign key relations valuess
    saved_query_sub_category_basic = f"SELECT * FROM `{DATABASE_NAME}`.`{SUB_CATEGORY_TABLE_NAME}`"
    
    # Get Sub-Category Table with required columns with foreign key relations values
    saved_query_sub_category_morphed = f"""
        SELECT * FROM 
        (SELECT A.{SUB_CATEGORY_ID}, A.{SUB_CATEGORY_NAME}, A.{SUB_CATEGORY_FOREIGNKEY_CATEGORY_ID},
        B.{CATEGORY_NAME} AS {CATEGORY_NAME}
        FROM {DATABASE_NAME}.{SUB_CATEGORY_TABLE_NAME} AS A
        LEFT JOIN {DATABASE_NAME}.{CATEGORY_TABLE_NAME} AS B
        ON A.{SUB_CATEGORY_FOREIGNKEY_CATEGORY_ID} = B.{CATEGORY_ID})
        AS merge_table"""
        
    # Get Supplier Table with required columns
    saved_query_supplier = f"""SELECT * FROM {DATABASE_NAME}.{SUPPLIER_TABLE_NAME}"""
    
    # Get Product Table with required columns with foreign key relations values
    saved_query_product_morphed = f"""
    SELECT * FROM 
    (SELECT A.{PRODUCT_ID}, A.{PRODUCT_NAME}, A.{PRODUCT_PRICE},
    A.{PRODUCT_QUANTITY}, A.{PRODUCT_REORDER_QUANTITY},
    A.{PRODUCT_DESCRIPTION}, A.{PRODUCT_FOREIGNKEY_CATEGORY_ID}, B.{CATEGORY_NAME} AS {CATEGORY_NAME}, 
    A.{PRODUCT_FOREIGNKEY_SUB_CATEGORY_ID}, C.{SUB_CATEGORY_NAME} AS {SUB_CATEGORY_NAME},
    A.{CREATED_AT}, A.{UPDATED_AT}, A.{PRODUCT_PRICE_UPDATE_DATETIME}, A.{PRODUCT_IS_DELETED}
    FROM {DATABASE_NAME}.{PRODUCT_TABLE_NAME} AS A
    LEFT JOIN 
    {DATABASE_NAME}.{CATEGORY_TABLE_NAME} AS B ON A.{PRODUCT_FOREIGNKEY_CATEGORY_ID} = B.{CATEGORY_ID}
    LEFT JOIN 
    {DATABASE_NAME}.{SUB_CATEGORY_TABLE_NAME} AS C ON A.{PRODUCT_FOREIGNKEY_SUB_CATEGORY_ID} = C.{SUB_CATEGORY_ID}) 
    AS merge_table"""

    # Get Purchase Order Table with required columns
    saved_query_purchase_order_morphed = f"""SELECT * FROM 
    (SELECT A.`{PURCHASE_ORDER_ID}`, A.`{PURCHASE_ORDER_FOREIGNKEY_SUPPLIER_ID}`, A.`{SUPPLIER_NAME}`, A.`{SUPPLIER_CONTACT_1}`, A.`{SUPPLIER_ADDRESS}`,
        A.`{SUPPLIER_GSTIN}`, A.`{SUPPLIER_ORGANIZATION_NAME}`, A.`{SUPPLIER_ORGANIZATION_CONTACT_1}`, A.`{SUPPLIER_ORGANIZATION_ADDRESS}`, A.`{PURCHASE_ORDER_PAYMENT_MODE}`,
        A.`{PURCHASE_ORDER_STATUS}`, A.`{PURCHASE_ORDER_TOTAL_PRICE}`, A.`{PURCHASE_ORDER_PAYMENT_STATUS}`, A.`{PURCHASE_ORDER_DELIVERY_STATUS}`,
        A.`{PURCHASE_ORDER_FOREIGNKEY_USER_ID}`, A.`{CREATED_AT}`, B.`{USERNAME}` AS {USERNAME} FROM `{DATABASE_NAME}`.`{PURCHASE_ORDER_TABLE_NAME}` AS A
        LEFT JOIN
        `{DATABASE_NAME}`.`{USER_TABLE_NAME}` AS B ON A.`{PURCHASE_ORDER_FOREIGNKEY_USER_ID}` = B.`{USER_ID}`
        ) AS merge_table"""

    # Get Sales Order Table with required columns
    saved_query_sales_order_morphed = f"""SELECT * FROM 
    (SELECT A.`{SALES_ORDER_ID}`, A.`{SALES_ORDER_C_NAME}`, A.`{SALES_ORDER_C_MOBILE}`, A.`{SALES_ORDER_C_EMAIL}`, A.`{SALES_ORDER_PAYMENT_MODE}`,
    A.`{SALES_ORDER_TOTAL_PRICE}`, A.`{SALES_ORDER_FOREIGNKEY_USER_ID}`, B.`{USERNAME}` AS {USERNAME}, A.`{SALES_ORDER_STATUS}`, A.`{CREATED_AT}`
    FROM `{DATABASE_NAME}`.`{SALES_ORDER_TABLE_NAME}` AS A
    LEFT JOIN
    `{DATABASE_NAME}`.`{USER_TABLE_NAME}` AS B ON A.`{SALES_ORDER_FOREIGNKEY_USER_ID}` = B.`{USER_ID}`
    ) AS merge_table"""

    # Get Sales Order Table with required columns
    saved_query_return_cancel_order_morphed = f"""SELECT * FROM 
    (SELECT A.`{RETURN_CANCEL_ORDER_ID}`, A.`{RETURN_CANCEL_ORDER_FOREIGNKEY_SALES_ORDER_ID}`, A.`{RETURN_CANCEL_ORDER_FOREIGNKEY_PURCHASE_ORDER_ID}`,
    A.`{RETURN_CANCEL_ORDER_STATUS}`, A.`{RETURN_CANCEL_ORDER_TOTAL_REFUND_AMOUNT}`,
    A.`{RETURN_CANCEL_ORDER_FOREIGNKEY_USER_ID}`, A.`{CREATED_AT}`,
    B.`{USERNAME}` AS {USERNAME} FROM `{DATABASE_NAME}`.`{RETURN_CANCEL_ORDER_TABLE_NAME}` AS A
    LEFT JOIN
    `{DATABASE_NAME}`.`{USER_TABLE_NAME}` AS B ON A.`{RETURN_CANCEL_ORDER_FOREIGNKEY_USER_ID}` = B.`{USER_ID}`
    ) AS merge_table"""


    # Constructor
    def __init__ (self, mysql, user):
        self.mysql = mysql
        self.current_user = user
        
        ##############################################
        #########      Some Saved Queries    #########
        ##############################################
    

    
    ##############################################
    ##############################################
    #######   Queries Execution Methods   ########
    ##############################################
    ##############################################
    


    ##############################################
    #########    Search Data in Tables   #########
    ##############################################
    
    def queryFetchSearchedData(self, offset, limit, query_data, selectable_columns_from_table_query, table_name,  sort_column=False, sort_order="ASC", product_table_get_column_query=None, export=False):
        # Getting Column name list for each table
        if type(product_table_get_column_query) == None.__class__:
            dummy_query = selectable_columns_from_table_query + " LIMIT 1;"
        else:
            dummy_query = product_table_get_column_query + " LIMIT 1;"
        dummy_data = self.executeFetchSqlQuery(table_name, dummy_query)

        if len(dummy_data) > 0:
            # Getting All column names from response
            all_columns = list(dummy_data[0].keys())
            
            query = selectable_columns_from_table_query
            count = 0
            for each_column in all_columns:
                if count == 0:
                    sub_query = f" WHERE {each_column} LIKE '%{query_data}%'"
                elif count == (len(all_columns) - 1):
                    if sort_column == False:
                        sub_query = f" OR {each_column} LIKE '%{query_data}%' LIMIT {limit} OFFSET {offset};"
                    else:
                        sub_query = f" OR {each_column} LIKE '%{query_data}%' ORDER BY {sort_column} {sort_order} LIMIT {limit} OFFSET {offset};"
                else:
                    sub_query = f" OR {each_column} LIKE '%{query_data}%'"
                query = query + sub_query
                count = count + 1
            
            # if export is true means non-paginated string query is needed 
            if export:
                query = query.replace(f"LIMIT {limit} OFFSET {offset}", "")
                return query
                
            # Counting Total Records
            queryy_count = query.replace("*", "COUNT(*) AS COUNT", 1) # Making SELECT *    =    SELECT COUNT(*)
            queryy_count = queryy_count.split("LIMIT") # Removing Offset and limit from query
            self.setTotalRecordsCount(queryy_count[0], table_name)
            
            # Fetching and returning the data
            return self.executeFetchSqlQuery(table_name, query)
        else:
            return list()




    ##############################################
    #########      User and Profile      #########
    ##############################################
    
    # Fetching all sales order paginated for treeview
    def queryFetchPaginatedUser(
        self, offset, limit, from_join_date="0000-00-00", to_join_date="0000-00-00", 
        from_leave_date="0000-00-00", to_leave_date="0000-00-00",
        radio_authority_data=0, radio_status_data=0, query_data=None, export=False
        ):
        
        # Setting data for User Authority filters Parameters
        add_on_1 = ""
        match radio_authority_data:
            case 0:
                add_on_1 = ""
            case 1:
                add_on_1 = f"(`{USER_AUTHORITY}` = '{AUTHORITY_TERTIARY}') "
            case 2:
                add_on_1 = f"(`{USER_AUTHORITY}` = '{AUTHORITY_SECONDARY}') "
            case 3:
                add_on_1 = f"(`{USER_AUTHORITY}` = '{AUTHORITY_PRIMARY}') "
            case _:
                add_on_1 = ""

        # Setting data for User Employment Status filters Parameters
        add_on_2 = ""
        match radio_status_data:
            case 0:
                add_on_2 = ""
            case 1:
                add_on_2 = f"(`{EMPLOYMENT_STATUS}` = '{EMPLOYED}') "
            case 2:
                add_on_2 = f"(`{EMPLOYMENT_STATUS}` = '{NOT_EMPLOYED}') "
            case 3:
                add_on_2 = f"(`{EMPLOYMENT_STATUS}` = '{ABSCONDED}') "
            case _:
                add_on_2 = ""
        
        flag_join_date = not (from_join_date == "0000-00-00" and to_join_date == "0000-00-00")
        flag_leave_date = not (from_leave_date == "0000-00-00" and to_leave_date == "0000-00-00")
        # Setting data for if records filtered on basis of joining date
        add_on_3 = ""
        if flag_join_date:
            add_on_3 = f"(`{DATE_OF_JOINING}` BETWEEN '{from_join_date} 00:00:00' AND '{to_join_date} 23:59:59')"

        # Setting data for if records filtered on basis of joining date
        if flag_leave_date:
            add_on_3 = f"(`{DATE_OF_LEAVING}` BETWEEN '{from_leave_date} 00:00:00' AND '{to_leave_date} 23:59:59')"

        # Setting data for if records filtered on basis of joining date and leaving date both
        if flag_join_date and flag_leave_date:
            add_on_3 = f"""(`{DATE_OF_JOINING}` BETWEEN '{from_join_date} 00:00:00' AND '{to_join_date} 23:59:59') AND
            (`{DATE_OF_LEAVING}` BETWEEN '{from_leave_date} 00:00:00' AND '{to_leave_date} 23:59:59')"""


        if not (len(add_on_1) == 0) and not (len(add_on_2) == 0) and not (len(add_on_3) == 0):
            queryy = f"""{self.saved_query_user_morphed} WHERE {add_on_1} AND {add_on_2} AND {add_on_3}"""
        elif not (len(add_on_1) == 0) and not (len(add_on_2) == 0):
            queryy = f"""{self.saved_query_user_morphed} WHERE {add_on_1} AND {add_on_2}"""
        elif not (len(add_on_1) == 0) and not (len(add_on_3) == 0):
            queryy = f"""{self.saved_query_user_morphed} WHERE {add_on_1} AND {add_on_3}"""
        elif not (len(add_on_2) == 0) and not (len(add_on_3) == 0):
            queryy = f"""{self.saved_query_user_morphed} WHERE {add_on_2} AND {add_on_3}"""
        elif not (len(add_on_1) == 0):
            queryy = f"""{self.saved_query_user_morphed} WHERE {add_on_1}"""
        elif not (len(add_on_2) == 0):
            queryy = f"""{self.saved_query_user_morphed} WHERE {add_on_2}"""
        elif not (len(add_on_3) == 0):
            queryy = f"""{self.saved_query_user_morphed} WHERE {add_on_3}"""
        else:
            queryy = f"""{self.saved_query_user_morphed}"""


         # If there's anything to search in search entry               
        if not (type(query_data) == None.__class__ or query_data == "" or query_data == "Search"):
            searched_query = f"SELECT * FROM ({queryy}) AS merge_table"
            return self.queryFetchSearchedData(
                offset=offset,
                limit=limit,
                query_data=query_data,
                selectable_columns_from_table_query=searched_query,
                table_name=USER_TABLE_NAME,
                sort_column=False,
                export=export
            )

        # if export is true means count is not affected
        if export:
            pass
        else:
            # Counting Total Records if nothing in searched query entry
            queryy_count = queryy.replace("*", "COUNT(*) AS COUNT", 1) # Making SELECT *    =    SELECT COUNT(*)
            queryy_count = queryy_count.split("ORDER") # Removing Offset and limit from query
            self.setTotalRecordsCount(queryy_count[0], USER_TABLE_NAME)

        # if export is true means non-paginated string query is needed 
        if export:
            # Adding order and pagination
           return queryy + f""" ORDER BY `{USER_ID}` ASC;"""
        else:
            # Adding order and pagination
            queryy = queryy + f""" ORDER BY `{USER_ID}` ASC LIMIT {limit} OFFSET {offset};"""

        
        return self.executeFetchSqlQuery(USER_TABLE_NAME, queryy)



    # Fetching Single User
    def queryFetchSingleUser(self, user_id):
        # Fetching Desired Records
        queryy = self.saved_query_user_morphed + f" WHERE `{USER_ID}` =  {user_id};"
        return self.executeFetchSqlQuery(USER_TABLE_NAME, queryy)


    # Fetch Single User Log
    def queryFetchSingleUserLog(self, user_log_id):
        queryy = f"""SELECT A.{USER_LOGS_ID}, A.{USER_LOGS_LOG}, A.{USER_LOGS_FOREIGNKEY_TARGET_USER_ID},
        A.{USER_LOGS_FOREIGNKEY_ACTIVE_USER_ID}, A.{CREATED_AT},
        B.{USERNAME} AS {TARGET_USER},
        C.{USERNAME} AS {ACTIVE_USER}
        FROM {DATABASE_NAME}.{USER_LOGS_TABLE_NAME} AS A
        LEFT JOIN 
        {DATABASE_NAME}.{USER_TABLE_NAME} AS B ON A.{USER_LOGS_FOREIGNKEY_TARGET_USER_ID} = B.{USER_ID}
        LEFT JOIN 
        {DATABASE_NAME}.{USER_TABLE_NAME} AS C ON A.{USER_LOGS_FOREIGNKEY_ACTIVE_USER_ID} = C.{USER_ID}
        WHERE A.{USER_LOGS_ID} = {user_log_id}"""
        return self.executeFetchSqlQuery(USER_LOGS_TABLE_NAME, queryy)

    
    
    ##############################################
    #########          Category          #########
    ##############################################
    
    # Fetching all Categories
    def queryFetchAllCategories(self):
        # Fetching Desired Records
        queryy =  self.saved_query_category + f" ORDER BY `{CATEGORY_NAME}` ASC;"
        return self.executeFetchSqlQuery(CATEGORY_TABLE_NAME, queryy)
            
           
            
    # Fetching all Categories paginated for treeview
    def queryFetchPaginatedCategories(self, offset, limit):
        # Counting Total Records
        queryy_count = f"""SELECT COUNT(*) AS 'COUNT' FROM `{DATABASE_NAME}`.`{CATEGORY_TABLE_NAME}`;"""
        self.setTotalRecordsCount(queryy_count, CATEGORY_TABLE_NAME)

        # Fetching Desired Records
        queryy = self.saved_query_category + f""" ORDER BY {CATEGORY_NAME} ASC LIMIT {limit} OFFSET {offset};"""
        return self.executeFetchSqlQuery(CATEGORY_TABLE_NAME, queryy)
        
    

    # Fetching Single Category
    def queryFetchSingleCategory(self, category_id):
        # Fetching Desired Records
        queryy = self.saved_query_category + f" WHERE `{CATEGORY_ID}` =  {category_id};"
        return self.executeFetchSqlQuery(CATEGORY_TABLE_NAME, queryy)
            
            
           
     # Deleting Catgory      
    def queryDeleteCategory(self, category_id):
        queryy = f"""DELETE FROM `{DATABASE_NAME}`.`{CATEGORY_TABLE_NAME}`
        WHERE `{CATEGORY_ID}` = {category_id};"""
        self.executeCommitSqlQuery(CATEGORY_TABLE_NAME, queryy)
    
    
    
    ##############################################
    #########        Sub-Category        #########
    ##############################################
    
    # Fetching all Sub-Catgories irrespect of categories
    def queryFetchAllSubCategories(self):
        # Counting Total Records
        queryy_count = f"SELECT COUNT(*) AS COUNT FROM `{DATABASE_NAME}`.`{SUB_CATEGORY_TABLE_NAME}`;"
        self.setTotalRecordsCount(queryy_count, CATEGORY_TABLE_NAME)

        # Fetching Desired Records
        queryy =  self.saved_query_sub_category_basic + f" ORDER BY `{SUB_CATEGORY_NAME}` ASC;"
        return self.executeFetchSqlQuery(SUB_CATEGORY_TABLE_NAME, queryy)
            
            
            
     # Fetching all Sub-Catgories with respect to their categories       
    def queryFetchRelevantSubCategories(self, category_id):
        # Counting Total Records
        queryy_count = f"""SELECT COUNT(*) AS COUNT FROM `{DATABASE_NAME}`.`{SUB_CATEGORY_TABLE_NAME}`
        WHERE `{SUB_CATEGORY_FOREIGNKEY_CATEGORY_ID}` = {category_id}"""
        self.setTotalRecordsCount(queryy_count, CATEGORY_TABLE_NAME)

        # Fetching Desired Records
        queryy =  self.saved_query_sub_category_basic + f"""WHERE `{SUB_CATEGORY_FOREIGNKEY_CATEGORY_ID}` = {category_id} 
        ORDER BY `{SUB_CATEGORY_NAME}` ASC;"""
        return self.executeFetchSqlQuery(SUB_CATEGORY_TABLE_NAME, queryy)
    
    
    
    # Fetching all Sub-Categories paginated for treeview
    def queryFetchPaginatedSubCategories(self, offset, limit):
        # Counting Total Records
        queryy_count = f"""SELECT COUNT({SUB_CATEGORY_ID}) AS COUNT
        FROM {DATABASE_NAME}.{SUB_CATEGORY_TABLE_NAME};"""
        self.setTotalRecordsCount(queryy_count, SUB_CATEGORY_TABLE_NAME)

        # Fetching Desired Records
        queryy = self.saved_query_sub_category_morphed + f""" ORDER BY {CATEGORY_NAME}, {SUB_CATEGORY_NAME}
        LIMIT {limit}
        OFFSET {offset};"""
        return self.executeFetchSqlQuery(SUB_CATEGORY_TABLE_NAME, queryy)
    
    
    
    # Fetching Single Sub-Category
    def queryFetchSingleSubCategory(self, sub_category_id):
        # Fetching Desired Records
        queryy = f"""SELECT A.{SUB_CATEGORY_ID}, A.{SUB_CATEGORY_NAME}, A.{SUB_CATEGORY_FOREIGNKEY_CATEGORY_ID}, B.{CATEGORY_NAME} AS {CATEGORY_NAME}
        FROM {DATABASE_NAME}.{SUB_CATEGORY_TABLE_NAME} as A, {DATABASE_NAME}.{CATEGORY_TABLE_NAME} as B 
        WHERE A.{SUB_CATEGORY_FOREIGNKEY_CATEGORY_ID} = B.{CATEGORY_ID} AND A.{SUB_CATEGORY_ID} = {sub_category_id};"""
        return self.executeFetchSqlQuery(SUB_CATEGORY_TABLE_NAME, queryy)
    
    
    
    # Fetch Sub-categories with respect to one category
    def queryFetchPaginatedSubCategoriesRelevantCategory(self, offset, limit, category_id, query_for_get_table):
        # Counting Total Records
        queryy_count = f"""SELECT COUNT({SUB_CATEGORY_ID}) AS COUNT
        FROM {DATABASE_NAME}.{SUB_CATEGORY_TABLE_NAME} WHERE {SUB_CATEGORY_FOREIGNKEY_CATEGORY_ID} = {category_id};"""
        self.setTotalRecordsCount(queryy_count, SUB_CATEGORY_TABLE_NAME)

        # Fetching Desired Records
        queryy = query_for_get_table + f""" ORDER BY {CATEGORY_NAME}, {SUB_CATEGORY_NAME}
        LIMIT {limit}
        OFFSET {offset};"""
        return self.executeFetchSqlQuery(SUB_CATEGORY_TABLE_NAME, queryy)
    
    

     # Deleting Sub-Category      
    def queryDeleteSubCategory(self, sub_category_id):
        queryy = f"""DELETE FROM `{DATABASE_NAME}`.`{SUB_CATEGORY_TABLE_NAME}`
        WHERE `{SUB_CATEGORY_ID}` = {sub_category_id};"""
        self.executeCommitSqlQuery(SUB_CATEGORY_TABLE_NAME, queryy)

        
    
    ##############################################
    #########          Supplier          #########
    ##############################################
    
    # Fetching all Suppliers
    def queryFetchAllSuppliers(self):
        # Fetching Desired Records
        queryy =  self.saved_query_supplier + f" ORDER BY `{SUPPLIER_NAME}` ASC;"
        return self.executeFetchSqlQuery(SUPPLIER_TABLE_NAME, queryy)
            
           
            
    # Fetching all Suppliers paginated for treeview
    def queryFetchPaginatedSuppliers(self, offset, limit, for_invoice=False, export=False, search_box_query_for_download_filter=None):

        # if supliers is selected for Invoice 
        if for_invoice:
            queryy_count = f"""SELECT COUNT(*) AS 'COUNT' FROM `{DATABASE_NAME}`.`{SUPPLIER_TABLE_NAME}` WHERE `{SUPPLIER_ACTIVE_STATE}` = 1;"""
            queryy = self.saved_query_supplier + f"""  WHERE `{SUPPLIER_ACTIVE_STATE}` = 1 ORDER BY `{SUPPLIER_ACTIVE_STATE}` = 1 DESC , {SUPPLIER_NAME} ASC LIMIT {limit} OFFSET {offset};"""
        # if export is true means non-paginated string query is needed 
        elif export:
            return self.saved_query_supplier + f""" ORDER BY `{SUPPLIER_ACTIVE_STATE}` = 1 DESC , {SUPPLIER_NAME} ASC;"""
        else:
            queryy_count = f"""SELECT COUNT(*) AS 'COUNT' FROM `{DATABASE_NAME}`.`{SUPPLIER_TABLE_NAME}`;"""    
            queryy = self.saved_query_supplier + f""" ORDER BY `{SUPPLIER_ACTIVE_STATE}` = 1 DESC , {SUPPLIER_NAME} ASC LIMIT {limit} OFFSET {offset};"""
        

        # if export is true means count is not affected
        if export:
            pass
        else:
            # Counting Total Records
            self.setTotalRecordsCount(queryy_count, SUPPLIER_TABLE_NAME)

        # Fetching Desired Records
        return self.executeFetchSqlQuery(SUPPLIER_TABLE_NAME, queryy)
        
    

    # Fetching Single Supplier
    def queryFetchSingleSupplier(self, supplier_id):
        # Fetching Desired Records
        queryy = self.saved_query_supplier + f" WHERE `{SUPPLIER_ID}` =  {supplier_id};"
        return self.executeFetchSqlQuery(SUPPLIER_TABLE_NAME, queryy)
            
            
           
     # Deleting Supplier      
    def queryToggleSupplierStatus(self, supplier_id):
        queryy = f"""SELECT {SUPPLIER_ACTIVE_STATE} AS STATE FROM `{DATABASE_NAME}`.`{SUPPLIER_TABLE_NAME}`
        WHERE `{SUPPLIER_ID}` = {supplier_id};"""
        state = self.executeFetchSqlQuery(SUPPLIER_TABLE_NAME, queryy)
        
        if state[0]["STATE"] == 1:
            value = 0
        else:
            value = 1
            
        queryy_2 = f"""UPDATE {DATABASE_NAME}.{SUPPLIER_TABLE_NAME} SET
        `{SUPPLIER_ACTIVE_STATE}` = {value} WHERE `{SUPPLIER_ID}` = {supplier_id};"""
        self.executeCommitSqlQuery(SUPPLIER_TABLE_NAME, queryy_2)
        
        
        
    ##############################################
    #########          Product           #########
    ##############################################
    
    # Fetching all Products paginated for treeview
    def queryFetchPaginatedProducts(self, offset, limit, radio=1, category_id=None, sub_category_id=None, query=None, export=False):

        # if export is true means count is not affected
        if export:
            pass
        else:
            # Counting Total Records
            queryy_count = f"""SELECT COUNT(*) AS 'COUNT' FROM `{DATABASE_NAME}`.`{PRODUCT_TABLE_NAME}`;"""
            self.setTotalRecordsCount(queryy_count, PRODUCT_TABLE_NAME)

        # Fetching Desired Records
        queryy = self.saved_query_product_morphed
        
        match radio:
            # All Products
            case 0:
                queryy = queryy
                if not (type(category_id) == None.__class__):
                    queryy = queryy + f" WHERE {PRODUCT_FOREIGNKEY_CATEGORY_ID} = {category_id}"
                    if not (type(sub_category_id) == None.__class__):
                        queryy = queryy + f" AND {PRODUCT_FOREIGNKEY_SUB_CATEGORY_ID} = {sub_category_id}"
                    
            # Active Products
            case 1:
                queryy = queryy + f" WHERE {PRODUCT_IS_DELETED} = 0"
                if not (type(category_id) == None.__class__):
                    queryy = queryy + f" AND {PRODUCT_FOREIGNKEY_CATEGORY_ID} = {category_id}"
                    if not (type(sub_category_id) == None.__class__):
                        queryy = queryy + f" AND {PRODUCT_FOREIGNKEY_SUB_CATEGORY_ID} = {sub_category_id}"
                 
            # Deleted Products
            case 2:
                queryy = queryy + f" WHERE {PRODUCT_IS_DELETED} = 1"
                if not (type(category_id) == None.__class__):
                    queryy = queryy + f" AND {PRODUCT_FOREIGNKEY_CATEGORY_ID} = {category_id}"
                    if not (type(sub_category_id) == None.__class__):
                        queryy = queryy + f" AND {PRODUCT_FOREIGNKEY_SUB_CATEGORY_ID} = {sub_category_id}"
                
            # Products in Low Stock
            case 3:
                queryy = queryy + f" WHERE {PRODUCT_QUANTITY} <= {PRODUCT_REORDER_QUANTITY} AND {PRODUCT_IS_DELETED} = 0"
                if not (type(category_id) == None.__class__):
                    queryy = queryy + f" AND {PRODUCT_FOREIGNKEY_CATEGORY_ID} = {category_id}"
                    if not (type(sub_category_id) == None.__class__):
                        queryy = queryy + f" AND {PRODUCT_FOREIGNKEY_SUB_CATEGORY_ID} = {sub_category_id}"
                        
         # If there's anything to search in search entry               
        if not (type(query) == None.__class__ or query == "" or query == "Search"):
            searched_query = f"SELECT * FROM ({queryy}) AS merge_table"
            return self.queryFetchSearchedData(
                offset=offset,
                limit=limit,
                query_data=query,
                selectable_columns_from_table_query=searched_query,
                table_name=PRODUCT_TABLE_NAME,
                sort_column=PRODUCT_NAME,
                product_table_get_column_query=self.saved_query_product_morphed,
                export=export
            )
            
        # if export is true means count is not affected
        if export:
            pass
        else:
            # Counting Total Records
            queryy_count = queryy.replace("*", "COUNT(*) AS COUNT", 1) # Making SELECT *    =    SELECT COUNT(*)
            queryy_count = queryy_count.split("ORDER") # Removing Offset and limit from query
            self.setTotalRecordsCount(queryy_count[0], PRODUCT_TABLE_NAME)

        # if export is true means non-paginated string query is needed 
        if export:
            return queryy + f" ORDER BY `{PRODUCT_NAME}` ASC"
        
        queryy = queryy + f" ORDER BY `{PRODUCT_NAME}` ASC LIMIT {limit} OFFSET {offset};"
        return self.executeFetchSqlQuery(PRODUCT_TABLE_NAME, queryy)
    
    
    # Fetching All Products
    def queryFetchAllProducts(self):
        # Fetching Desired Records
        queryy = self.saved_query_product_morphed + f" WHERE {PRODUCT_IS_DELETED} <> 1;"
        return self.executeFetchSqlQuery(PRODUCT_TABLE_NAME, queryy)
    
    
    
    # Fetching Single Product
    def queryFetchSingleProduct(self, product_id):
        # Fetching Desired Records
        queryy = self.saved_query_product_morphed + f" WHERE `{PRODUCT_ID}` =  {product_id};"
        return self.executeFetchSqlQuery(PRODUCT_TABLE_NAME, queryy)


    
     # Deleting Product      
    def queryToggleProductDeleteStatus(self, product_id):

        query_get_details = f"""SELECT {PRODUCT_ID}, {PRODUCT_IS_DELETED} AS 'DELETED' FROM `{DATABASE_NAME}`.`{PRODUCT_TABLE_NAME}`
        WHERE `{PRODUCT_ID}` = {product_id};"""
        
        product = self.executeFetchSqlQuery(PRODUCT_TABLE_NAME, query_get_details)
        
        if product[0]["DELETED"] == 1:
            value = 0
            log_description_data = "Product is restored back to inventory"
        else:
            value = 1
            log_description_data = "Product is removed or deleted from inventory"
              
        try:
            # Updating Product Table
            query_delete = f"""UPDATE {DATABASE_NAME}.{PRODUCT_TABLE_NAME} SET
            `{PRODUCT_IS_DELETED}` = {value}, `{UPDATED_AT}` = CURRENT_TIMESTAMP WHERE `{PRODUCT_ID}` = {product_id};"""
            self.executeCommitSqlQuery(PRODUCT_TABLE_NAME, query_delete)
            # Updating Product Log
            self.queryInsertProductLog(log_description_data, product[0][PRODUCT_ID])
        except Exception as error:
            log_description_data_dummy = log_description_data.replace("is", "is attempted to")
            log_description_data_dummy = log_description_data_dummy + ", but something went wrong."
            # Updating Product Log
            self.queryInsertProductLog(log_description_data_dummy, product[0][PRODUCT_ID])
            print(f"Development Error (queryToggleProductDeleteStatus()  method {PRODUCT_TABLE_NAME} table): {error}")
            ErrorModal("Something went wrong, please contact software developer.")
        
        
        
        
    # Fetching all logs relevant to one record paginated for treeview
    def queryFetchPaginatedLogs(self, offset, limit, query_to_get):
        queryy = query_to_get

        # Counting Total Records
        queryy_count = queryy.replace("*", "COUNT(*) AS COUNT", 1)
        self.setTotalRecordsCount(queryy_count, "")

        # Fetching Desired Records
        queryy = queryy + f""" ORDER BY {CREATED_AT} DESC LIMIT {limit} OFFSET {offset};"""
        return self.executeFetchSqlQuery("", queryy)
        
        
        
    # Fetching Single Product Log
    def queryFetchSingleProductLog(self, product_log_id):
        queryy = f"""SELECT A.{PRODUCT_LOGS_ID}, A.{PRODUCT_LOGS_LOG}, A.{PRODUCT_LOGS_FOREIGNKEY_PRODUCT_ID},
        A.{PRODUCT_LOGS_FOREIGNKEY_USER_ID}, A.{CREATED_AT},
        B.{PRODUCT_NAME} AS {PRODUCT_NAME},
        C.{USERNAME} AS {USERNAME}
        FROM {DATABASE_NAME}.{PRODUCT_LOGS_TABLE_NAME} AS A
        LEFT JOIN 
        {DATABASE_NAME}.{PRODUCT_TABLE_NAME} AS B ON A.{PRODUCT_LOGS_FOREIGNKEY_PRODUCT_ID} = B.{PRODUCT_ID}
        LEFT JOIN 
        {DATABASE_NAME}.{USER_TABLE_NAME} AS C ON A.{PRODUCT_LOGS_FOREIGNKEY_USER_ID} = C.{USER_ID}
        WHERE A.{PRODUCT_LOGS_ID} = {product_log_id}"""
        return self.executeFetchSqlQuery(PRODUCT_LOGS_TABLE_NAME, queryy)
        
        
        
    # Inserting Product Logs
    def queryInsertProductLog(self, log_description: str, product_id, user_id=None):
        try:
            if type(user_id) == None.__class__:
                user_id = self.current_user[USER_ID]
            # Create a Log
            query_delete_log = f"""INSERT INTO `{DATABASE_NAME}`.`{PRODUCT_LOGS_TABLE_NAME}` 
            (`{PRODUCT_LOGS_LOG}`, `{PRODUCT_ID}`, `{USER_ID}`) 
            VALUES (%s, %s, %s)"""
            query_parameters = (log_description, product_id, user_id)
            self.executeCommitSqlQuery(PRODUCT_LOGS_TABLE_NAME, query_delete_log, query_parameters)
        except Exception as error:
            print(f"Development Error (queryInsertProductLog()  method {PRODUCT_LOGS_TABLE_NAME} table): {error}")
            ErrorModal("Something went wrong, please contact software developer.")
        


    ##############################################
    #########      Purchase Order        #########
    ##############################################
        
    # Fetching all purchase order paginated for treeview
    def queryFetchPaginatedPurchaseOrder(self, offset, limit, from_date, to_date, radio_data=0, query_data=None, query_add_on=None, export=False):
        
        # Setting data for RadioButtons Parameters
        add_on = ""
        match radio_data:
            case 0:
                add_on = ""
            case 100:
                add_on = f"(`{PURCHASE_ORDER_STATUS}` <> '{ORDER_CANCELLED}') AND (`{PURCHASE_ORDER_STATUS}` <> '{ORDER_RETURNED}') AND"
            case 1:
                add_on = f"(`{PURCHASE_ORDER_STATUS}` = '{ORDER_COMPLETED}') AND"
            case 2:
                add_on = f"(`{PURCHASE_ORDER_STATUS}` = '{ORDER_PENDING}') AND"
            case 3:
                add_on = f"(`{PURCHASE_ORDER_STATUS}` = '{ORDER_CANCELLED}') AND"
            case 4:
                add_on = f"(`{PURCHASE_ORDER_STATUS}` = '{ORDER_RETURNED}') AND"
            case 5:
                add_on = f"""(`{PURCHASE_ORDER_PAYMENT_STATUS}` = '{PAYMENT_PENDING}') AND 
                (`{PURCHASE_ORDER_STATUS}` <> '{ORDER_RETURNED}') AND (`{PURCHASE_ORDER_STATUS}` <> '{ORDER_CANCELLED}') AND"""
            case 6:
                add_on = f"""(`{PURCHASE_ORDER_PAYMENT_STATUS}` = '{PAYMENT_COMPLETED}') AND 
                (`{PURCHASE_ORDER_STATUS}` <> '{ORDER_RETURNED}') AND (`{PURCHASE_ORDER_STATUS}` <> '{ORDER_CANCELLED}') AND"""
            case 7:
                add_on = f"""(`{PURCHASE_ORDER_DELIVERY_STATUS}` = '{NOT_DISPATCHED}' OR `{PURCHASE_ORDER_DELIVERY_STATUS}` = '{DISPATCHED}') AND 
                (`{PURCHASE_ORDER_STATUS}` <> '{ORDER_RETURNED}') AND (`{PURCHASE_ORDER_STATUS}` <> '{ORDER_CANCELLED}') AND"""
            case 8:
                add_on = f"""(`{PURCHASE_ORDER_DELIVERY_STATUS}` = '{DELIVERED}') AND (`{PURCHASE_ORDER_STATUS}` <> '{ORDER_RETURNED}') AND 
                (`{PURCHASE_ORDER_STATUS}` <> '{ORDER_CANCELLED}') AND"""
            case _:
                add_on = ""


        # Creating Desired Query
        if type(query_add_on) == None.__class__:
            queryy = self.saved_query_purchase_order_morphed + f""" WHERE {add_on} (`{CREATED_AT}` BETWEEN '{from_date} 00:00:00' AND '{to_date} 23:59:59')"""
        else:
            queryy = self.saved_query_purchase_order_morphed + query_add_on + f""" AND {add_on} (`{CREATED_AT}` BETWEEN '{from_date} 00:00:00' AND '{to_date} 23:59:59')"""


         # If there's anything to search in search entry               
        if not (type(query_data) == None.__class__ or query_data == "" or query_data == "Search"):
            searched_query = f"SELECT * FROM ({queryy}) AS merge_table"
            return self.queryFetchSearchedData(
                offset=offset,
                limit=limit,
                query_data=query_data,
                selectable_columns_from_table_query=searched_query,
                table_name=PURCHASE_ORDER_TABLE_NAME,
                sort_column=False,
                export=export
            )


        # if export is true means count is not affected
        if export:
            pass
        else:
            # Counting Total Records if nothing in searched query entry
            queryy_count = queryy.replace("*", "COUNT(*) AS COUNT", 1) # Making SELECT *    =    SELECT COUNT(*)
            queryy_count = queryy_count.split("ORDER") # Removing Offset and limit from query
            self.setTotalRecordsCount(queryy_count[0], PURCHASE_ORDER_TABLE_NAME)


        if export:
            # Adding order and pagination
            a = queryy + f""" ORDER BY `{PURCHASE_ORDER_STATUS}` = '{ORDER_CANCELLED}' ASC , `{PURCHASE_ORDER_STATUS}` = '{ORDER_RETURNED}' ASC ,
            `{PURCHASE_ORDER_STATUS}` = '{ORDER_COMPLETED}' ASC , `{PURCHASE_ORDER_STATUS}` = '{ORDER_PENDING}' ASC , `{CREATED_AT}` DESC;"""
            return a
        else:
            # Adding order and pagination
            queryy = queryy + f""" ORDER BY `{PURCHASE_ORDER_STATUS}` = '{ORDER_CANCELLED}' ASC , `{PURCHASE_ORDER_STATUS}` = '{ORDER_RETURNED}' ASC ,
            `{PURCHASE_ORDER_STATUS}` = '{ORDER_COMPLETED}' ASC , `{PURCHASE_ORDER_STATUS}` = '{ORDER_PENDING}' ASC , `{CREATED_AT}` DESC
            LIMIT {limit} OFFSET {offset};"""

        return self.executeFetchSqlQuery(PURCHASE_ORDER_TABLE_NAME, queryy)


    #  Fetch Single Purchase Order Details
    def queryFetchSinglePurchaseOrder(self, purchase_order_id, custom_query=None):
        """
        Args:
            purchase_order_id (int): integer purchase order id
            custom_query (str): string add on to query needed in return cancel order to calculate number of products
                                and units in order
        """
        # Fetching Desired Records
        if type(custom_query) == None.__class__:
            queryy = self.saved_query_purchase_order_morphed + f" WHERE `{PURCHASE_ORDER_ID}` =  {purchase_order_id};"
        else:
            queryy = custom_query + f" WHERE `{PURCHASE_ORDER_ID}` =  {purchase_order_id};"
        return self.executeFetchSqlQuery(PURCHASE_ORDER_TABLE_NAME, queryy)



    # Fetch Single Purchase Order Log
    def queryFetchSinglePurchaseOrderLog(self, purchase_order_id):
        queryy = f"""SELECT A.{PURCHASE_ORDER_LOGS_ID}, A.{PURCHASE_ORDER_LOGS_LOG}, A.{PURCHASE_ORDER_LOGS_FOREIGNKEY_PURCHASE_ORDER_ID},
        A.{PURCHASE_ORDER_LOGS_FOREIGNKEY_USER_ID}, A.{CREATED_AT},
        C.{USERNAME} AS {USERNAME}
        FROM {DATABASE_NAME}.{PURCHASE_ORDER_LOGS_TABLE_NAME} AS A
        LEFT JOIN 
        {DATABASE_NAME}.{USER_TABLE_NAME} AS C ON A.{PURCHASE_ORDER_LOGS_FOREIGNKEY_USER_ID} = C.{USER_ID}
        WHERE A.{PURCHASE_ORDER_LOGS_ID} = {purchase_order_id}"""
        return self.executeFetchSqlQuery(PURCHASE_ORDER_LOGS_TABLE_NAME, queryy)



    # Fetch Product of particular purchase order
    def queryFetchAllPurchaseOrderProduct(self, purchase_order_id):
        queryy = f"SELECT * FROM `{DATABASE_NAME}`.`{PURCHASE_ORDER_PRODUCT_TABLE_NAME}` WHERE `{P_O_P_FOREIGNKEY_PURCHASE_ORDER_ID}` = {purchase_order_id};"
        return self.executeFetchSqlQuery(PURCHASE_ORDER_TABLE_NAME, queryy)



    # Fetch Paginated Product of particular purchase order
    def queryFetchPaginatedPurchaseOrderProduct(self, offset, limit, purchase_order_id):
        # Counting Total Records
        queryy_count = f"""SELECT COUNT(*) AS 'COUNT' FROM `{DATABASE_NAME}`.`{PURCHASE_ORDER_PRODUCT_TABLE_NAME}` WHERE `{P_O_P_FOREIGNKEY_PURCHASE_ORDER_ID}` = {purchase_order_id};"""
        self.setTotalRecordsCount(queryy_count, PURCHASE_ORDER_PRODUCT_TABLE_NAME)

        queryy = f"SELECT * FROM `{DATABASE_NAME}`.`{PURCHASE_ORDER_PRODUCT_TABLE_NAME}` WHERE `{P_O_P_FOREIGNKEY_PURCHASE_ORDER_ID}` = {purchase_order_id} LIMIT {limit} OFFSET {offset};"
        return self.executeFetchSqlQuery(PURCHASE_ORDER_TABLE_NAME, queryy)



    ##############################################
    #########        Sales Order         #########
    ##############################################
        
    # Fetching all sales order paginated for treeview
    def queryFetchPaginatedSalesOrder(self, offset, limit, from_date, to_date, radio_data=0, query_data=None, query_add_on=None, export=False):
        
        # Setting data for RadioButtons Parameters
        add_on = ""
        match radio_data:
            case 0:
                add_on = ""
            case 1:
                add_on = f"(`{SALES_ORDER_STATUS}` = '{ORDER_COMPLETED}') AND"
            case 2:
                add_on = f"(`{SALES_ORDER_STATUS}` = '{ORDER_CANCELLED}') AND"
            case 3:
                add_on = f"(`{SALES_ORDER_STATUS}` = '{ORDER_RETURNED}') AND"
            case _:
                add_on = ""


        # Creating Desired Query
        if type(query_add_on) == None.__class__:
            queryy = self.saved_query_sales_order_morphed + f""" WHERE {add_on} (`{CREATED_AT}` BETWEEN '{from_date} 00:00:00' AND '{to_date} 23:59:59')"""
        else:
            queryy = self.saved_query_sales_order_morphed + query_add_on + f""" AND {add_on} (`{CREATED_AT}` BETWEEN '{from_date} 00:00:00' AND '{to_date} 23:59:59')"""



         # If there's anything to search in search entry               
        if not (type(query_data) == None.__class__ or query_data == "" or query_data == "Search"):
            searched_query = f"SELECT * FROM ({queryy}) AS merge_table"
            return self.queryFetchSearchedData(
                offset=offset,
                limit=limit,
                query_data=query_data,
                selectable_columns_from_table_query=searched_query,
                table_name=SALES_ORDER_TABLE_NAME,
                sort_column=False,
                export=export
            )

        # if export is true means count is not affected
        if export:
            pass
        else:
            # Counting Total Records if nothing in searched query entry
            queryy_count = queryy.replace("*", "COUNT(*) AS COUNT", 1) # Making SELECT *    =    SELECT COUNT(*)
            queryy_count = queryy_count.split("ORDER") # Removing Offset and limit from query
            self.setTotalRecordsCount(queryy_count[0], SALES_ORDER_TABLE_NAME)


        # if export is true means non-paginated string query is needed 
        if export:
            # Adding order and pagination
           return queryy + f""" ORDER BY `{SALES_ORDER_STATUS}` = '{ORDER_CANCELLED}' ASC , `{PURCHASE_ORDER_STATUS}` = '{ORDER_RETURNED}' ASC ,
            `{PURCHASE_ORDER_STATUS}` = '{ORDER_COMPLETED}' ASC , `{CREATED_AT}` DESC;"""
        else:
            # Adding order and pagination
            queryy = queryy + f""" ORDER BY `{SALES_ORDER_STATUS}` = '{ORDER_CANCELLED}' ASC , `{PURCHASE_ORDER_STATUS}` = '{ORDER_RETURNED}' ASC ,
            `{PURCHASE_ORDER_STATUS}` = '{ORDER_COMPLETED}' ASC , `{CREATED_AT}` DESC
            LIMIT {limit} OFFSET {offset};"""
        
        return self.executeFetchSqlQuery(SALES_ORDER_TABLE_NAME, queryy)



    #  Fetch Single Sales Order Details
    def queryFetchSingleSalesOrder(self, sales_order_id, custom_query=None):
        """
        Args:
            sales_order_id (int): integer sales order id
            custom_query (str): string add on to query needed in return cancel order to calculate number of products
                                and units in order
        """
        # Fetching Desired Records
        if type(custom_query) == None.__class__:
            queryy = self.saved_query_sales_order_morphed + f" WHERE `{SALES_ORDER_ID}` =  {sales_order_id};"
        else:
            queryy = custom_query + f" WHERE `{SALES_ORDER_ID}` =  {sales_order_id};"
        return self.executeFetchSqlQuery(SALES_ORDER_TABLE_NAME, queryy)



    # Fetch Single Sales Order Log
    def queryFetchSingleSalesOrderLog(self, sales_order_id):
        queryy = f"""SELECT A.{SALES_ORDER_LOGS_ID}, A.{SALES_ORDER_LOGS_LOG}, A.{SALES_ORDER_LOGS_FOREIGNKEY_SALES_ORDER_ID},
        A.{SALES_ORDER_LOGS_FOREIGNKEY_USER_ID}, A.{CREATED_AT},
        C.{USERNAME} AS {USERNAME}
        FROM {DATABASE_NAME}.{SALES_ORDER_LOGS_TABLE_NAME} AS A
        LEFT JOIN 
        {DATABASE_NAME}.{USER_TABLE_NAME} AS C ON A.{SALES_ORDER_LOGS_FOREIGNKEY_USER_ID} = C.{USER_ID}
        WHERE A.{SALES_ORDER_LOGS_ID} = {sales_order_id}"""
        return self.executeFetchSqlQuery(SALES_ORDER_LOGS_TABLE_NAME, queryy)



    # Fetch Product of particular purchase order
    def queryFetchAllSalesOrderProduct(self, sales_order_id):
        queryy = f"SELECT * FROM `{DATABASE_NAME}`.`{SALES_ORDER_PRODUCT_TABLE_NAME}` WHERE `{S_O_P_FOREIGNKEY_SALES_ORDER_ID}` = {sales_order_id};"
        return self.executeFetchSqlQuery(SALES_ORDER_PRODUCT_TABLE_NAME, queryy)



    # Fetch Paginated Product of particular purchase order
    def queryFetchPaginatedSalesOrderProduct(self, offset, limit, sales_order_id):
        # Counting Total Records
        queryy_count = f"""SELECT COUNT(*) AS 'COUNT' FROM `{DATABASE_NAME}`.`{SALES_ORDER_PRODUCT_TABLE_NAME}` WHERE `{S_O_P_FOREIGNKEY_SALES_ORDER_ID}` = {sales_order_id};"""
        self.setTotalRecordsCount(queryy_count, SALES_ORDER_PRODUCT_TABLE_NAME)

        queryy = f"SELECT * FROM `{DATABASE_NAME}`.`{SALES_ORDER_PRODUCT_TABLE_NAME}` WHERE `{S_O_P_FOREIGNKEY_SALES_ORDER_ID}` = {sales_order_id} LIMIT {limit} OFFSET {offset};"
        return self.executeFetchSqlQuery(SALES_ORDER_PRODUCT_TABLE_NAME, queryy)
        


    ##############################################
    ######       Return Cancel Order        ######
    ##############################################
        
    # Fetching all return cancel order paginated for treeview
    def queryFetchPaginatedReturnCancelOrder(self, offset, limit, from_date, to_date, radio_data=0, query_data=None, export=False):
        
        # Setting data for RadioButtons Parameters
        add_on = ""
        match radio_data:
            case 0:
                add_on = ""
            case 1:
                add_on = f"(`{RETURN_CANCEL_ORDER_STATUS}` = '{ORDER_CANCELLED}') AND"
            case 2:
                add_on = f"(`{RETURN_CANCEL_ORDER_FOREIGNKEY_PURCHASE_ORDER_ID}` <> '{None}') AND"
            case 3:
                add_on = f"(`{RETURN_CANCEL_ORDER_FOREIGNKEY_SALES_ORDER_ID}` <> '{None}') AND"
            case _:
                add_on = ""



        # Creating Desired Query
        queryy = self.saved_query_return_cancel_order_morphed + f""" WHERE {add_on} (`{CREATED_AT}` BETWEEN '{from_date} 00:00:00' AND '{to_date} 23:59:59')"""

         # If there's anything to search in search entry               
        if not (type(query_data) == None.__class__ or query_data == "" or query_data == "Search"):
            searched_query = f"SELECT * FROM ({queryy}) AS merge_table"
            return self.queryFetchSearchedData(
                offset=offset,
                limit=limit,
                query_data=query_data,
                selectable_columns_from_table_query=searched_query,
                table_name=RETURN_CANCEL_ORDER_TABLE_NAME,
                sort_column=False,
            )

        # if export is true means count is not affected
        if export:
            pass
        else:
            # Counting Total Records if nothing in searched query entry
            queryy_count = queryy.replace("*", "COUNT(*) AS COUNT", 1) # Making SELECT *    =    SELECT COUNT(*)
            queryy_count = queryy_count.split("ORDER") # Removing Offset and limit from query
            self.setTotalRecordsCount(queryy_count[0], PURCHASE_ORDER_TABLE_NAME)

        # if export is true means non-paginated string query is needed 
        if export:
            # Adding order and pagination
            return queryy + f""" ORDER BY `{RETURN_CANCEL_ORDER_STATUS}` = '{ORDER_CANCELLED}' ASC , `{CREATED_AT}` DESC;"""
        else:
            # Adding order and pagination
            queryy = queryy + f""" ORDER BY `{RETURN_CANCEL_ORDER_STATUS}` = '{ORDER_CANCELLED}' ASC , `{CREATED_AT}` DESC
            LIMIT {limit} OFFSET {offset};"""

        return self.executeFetchSqlQuery(RETURN_CANCEL_ORDER_TABLE_NAME, queryy)



    #  Fetch Single Return/Cancel Order Details
    def queryFetchSingleReturnCancelOrder(self, return_cancel_order_id, custom_query=None):
        # Fetching Desired Records
        if type(custom_query) == None.__class__:
            queryy = self.saved_query_return_cancel_order_morphed + f" WHERE `{RETURN_CANCEL_ORDER_ID}` =  {return_cancel_order_id};"
        else:
            queryy = custom_query + f" WHERE `{RETURN_CANCEL_ORDER_ID}` =  {return_cancel_order_id};"
        return self.executeFetchSqlQuery(RETURN_CANCEL_ORDER_TABLE_NAME, queryy)



    # Fetch Product of particular return cancel order
    def queryFetchAllReturnCancelOrderProduct(self, return_cancel_order_id):
        queryy = f"""SELECT * FROM `{DATABASE_NAME}`.`{RETURN_CANCEL_ORDER_PRODUCT_TABLE_NAME}` 
        WHERE `{R_C_O_P_FOREIGNKEY_RETURN_CANCEL_ORDER_ID}` = {return_cancel_order_id};"""
        return self.executeFetchSqlQuery(RETURN_CANCEL_ORDER_PRODUCT_TABLE_NAME, queryy)



    ##############################################
    #######  Query Exceute Support Method  #######
    ##############################################
    
    # Execute Fetching SQL Query  
    def executeFetchSqlQuery(self, table_name, query, query_parameters=None):
        try:
            # Closing cursor so excute() not execute multiple statements and  commands don't go out of sync error arise  
            self.mysql.query.close()
            # Reconnecting to new cusror
            self.mysql = Connection()
            if type(query_parameters) == None.__class__:
                self.mysql.query.execute(query)
            else:
                self.mysql.query.execute(query, query_parameters)
            return self.mysql.query.fetchall()
        except Exception as error:
            print(f"Development Error (executeFetchSqlQuery()  method {table_name} table): {error}")
            ErrorModal("Something went wrong, please contact software developer.")
            

      
    # Execute Committing Changes SQL Query  
    def executeCommitSqlQuery(self, table_name, query, query_parameters=None):
        try:
            # Closing cursor so excute() not execute multiple statements and  commands don't go out of sync error arise  
            self.mysql.query.close()
            # Reconnecting to new cusror
            self.mysql = Connection()
            if type(query_parameters) == None.__class__:
                self.mysql.query.execute(query)
            else:
                self.mysql.query.execute(query, query_parameters)
            self.mysql.db_connection.commit()
            return self.mysql.query.lastrowid
        except Exception as error:
            print(f"Development Error (executeCommitSqlQuery()  method {table_name} table): {error}")
            ErrorModal("Something went wrong, please contact software developer.")
            
            
            
    # Set Value for totalRecordsCount variable  
    def setTotalRecordsCount(self, query, table_name):
        no = self.executeFetchSqlQuery(table_name, query)
        self.totalRecordsCount = (no[0]["COUNT"] if (len(no) == 1) else  0)
        
        
        
    # Takes Null or empty from database and formatted it correctly to display
    def checkNullFormat(self, data):
        """Can take value from database if it can be null or empty and formatted it correctly 
        by removing NoneType class instance

        Args:
            data (str): data to be checked
        """
        
        return "" if type(data) == None.__class__ else data
        
        
    
    ##############################################
    #########           Others           #########
    ##############################################
    
    # Checking if record already exist in database or not
    def checkDuplicates(self, data_from_database, value_to_be_matched, database_column_whose_value_to_be_comapred):
        flag = ""
        if value_to_be_matched == None or value_to_be_matched == "":
            flag = False
        else:
            for i in range(len(data_from_database)):
                if str(data_from_database[i][database_column_whose_value_to_be_comapred]).lower() == value_to_be_matched.lower():
                    flag = True
                    break
                else:
                    flag = False
        return flag
    
    

    # Take datafrom database in a list containing dictionary of records of Table from Database
    # Return either list of tuples where each tuple hold values of a single record from Table of Database, or
    # Return a list containing values of particular column of Table in Database
    def dbValTuple(self, dataFromDatabase : list[dict], columnName = None):

        # Return List of Tuple where each Tuple represent a Row from Table of database
        if columnName == None:
            return [list(dictionaries.values()) for dictionaries in dataFromDatabase]
        
        # Return List containing values from particular column in Table of database
        else:
            return [i[f"{columnName}"] for i in dataFromDatabase]
        
    
    
    # Clearing unecessary focus of comboBox
    def afterComboBoxSelected(self, combobox_instance, textvariable: tk.StringVar = None):
        # Clearing Unecessary focus from comboBox text by reseting it
        if textvariable == None:
            pass
        else:
            value = textvariable.get()
            textvariable.set("")
            textvariable.set(value)
        
        # Clearing unecessary focus of comboBox for whitespace and text
        combobox_instance.useless_entry.focus()
        
        
    
    # Terminate the current running thread
    def terminateAfter(self, instance_of_class, flag, after_id):
        """if after function is running, it terminates that and its process
        """
        if flag:
            instance_of_class.after_cancel(after_id)
            return 1
        else:
            return 0



    # Bind All Entry fields of create and edit form
    def bindFormFields(self, entry, _callback=None):
        """Bind fields for Create and Edit Class for Application
        binding event are on focusout and keyrelease 

        Args:
            entry (tk.Entry): Tkinter Entry Widget Instnce
            _callback (def, optional): if callback passed it takes event as first positional parameter.
        """
        if _callback:
            entry.bind("<KeyRelease>", _callback)
            entry.bind("<FocusOut>", _callback)
            
            
            
    # Made GUI changes for Validation of fields     
    def validateGui(self, entry_instance, entry_style, button_state, toggle_error_label, error_label_style, error_label_value, error_label_grid_row, submit_button_instance=None):
        """Made Changes in GUI for forms in Application for Validating fields

        Args:
            entry_instance (tk.Entry): entry field instance to whom validation is applied
            entry_style (str): style for entry to whose validation is applied
            button_state (str): widget Button state
            toggle_error_label (str): Grid or Ungrid Error Label, accept boolean values or 0 and 1
            error_label_style (str): style for label showing error message
            error_label_value (str): text for label error message
        """
        # Create Reset Entries in your own class
        self.resetEntries()
        self.lbsuc.configure(
            style=error_label_style,
            text=error_label_value
        )
        if toggle_error_label == 1:
            self.lbsuc.grid(row=error_label_grid_row, column=0, columnspan=4, sticky="ew")
        else:
            self.lbsuc.grid_forget()
            
        if entry_instance == None and entry_style == None:
            pass
        else: 
            entry_instance.configure(style=entry_style)
            
        if not (type(submit_button_instance) == None.__class__):
            self.submit_button_instance.configure(state=button_state)
        else:
            self.button.configure(state=button_state)



    # Method to convert to superscript
    def superscript(self, text):
            normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=*()"
            super_s = "ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖ۹ʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼*⁽⁾"
            res = text.maketrans(''.join(normal), ''.join(super_s))
            return text.translate(res)


        
    # Method to convert to subscript
    def subscript(self, text):
        normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
        sub_s = "ₐ₈CDₑբGₕᵢⱼₖₗₘₙₒₚQᵣₛₜᵤᵥwₓᵧZₐ♭꜀ₑբ₉ₕᵢⱼₖₗₘₙₒₚ૧ᵣₛₜᵤᵥwₓᵧ₂₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎"
        res = text.maketrans(''.join(normal), ''.join(sub_s))
        return text.translate(res)


    # Method to convert price string to INR Format
    def formatINR(self, number):
        number = round(float(number), 2)
        s, *d = str(number).partition(".")
        r = ",".join([s[x-2:x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
        return f'\u20B9{"".join([r] + d)}'


    # Method to convert price string to INR Format
    def formatReverseINR(self, number):
        a = number
        a = float(a.replace("\u20B9", "").replace(",", ""))
        return a
