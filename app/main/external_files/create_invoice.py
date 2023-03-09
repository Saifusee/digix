from database.dbconnection import Connection
from CONSTANT.index import *
from error import ErrorModal
from app.base import Base
import webbrowser
from os import remove
import threading
from datetime import datetime

class GenerateInvoice(Base):
    def __init__(self, sales_order_id=None, purchase_order_id=None, return_cancel_order_id=None):
        mysql = Connection()
        super().__init__(mysql, None)

        temp_file_name = str(round(datetime.now().timestamp()))
        temp_file_path = path.join(PATH_TO_INVOICE_ASSETS_FOLDER, f"invoice_{temp_file_name}.html")

        # Checking and alloting data
        
        ## When Sales Order
        if not (type(sales_order_id) == None.__class__):
            sales_order_data = self.queryFetchSingleSalesOrder(sales_order_id)[0]
            sales_order_product_data = self.queryFetchAllSalesOrderProduct(sales_order_id)

            # Setting Customer Details
            third_party_div = f"""
            <div id="details" class="clearfix">
                <div id="client">
                <div class="to">INVOICE TO CUSTOMER:</div>
                <h2 class="name">{sales_order_data[SALES_ORDER_C_NAME]}</h2>
                <div class="contact">{sales_order_data[SALES_ORDER_C_MOBILE]}</div>
                <div class="email"><a href="mailto:{sales_order_data[SALES_ORDER_C_EMAIL]}">{sales_order_data[SALES_ORDER_C_EMAIL]}</a></div>
                <div class="mode">Payment Mode: {sales_order_data[SALES_ORDER_PAYMENT_MODE]}</div>
                <div class="status">Order Status: {sales_order_data[SALES_ORDER_STATUS]}</div>
                </div>
                <div id="invoice">
                <h1>Customer Invoice</h1>
                <div class="date"><strong>Date:</strong> {sales_order_data[CREATED_AT].strftime("%B %d, %Y")}<br>{sales_order_data[CREATED_AT].strftime("%I:%M %p")}</div>
                <h3 class="date">Order Id: {sales_order_data[SALES_ORDER_ID]}</h3>
                </div>
            </div>
            """

            # Modifying rows for each product
            s_no = 1
            total_tax = float(0)
            total_amount_without_tax = float(0)
            new_table_row = ""
            for product in sales_order_product_data:
                sgst = float(product[S_O_P_PRODUCT_PRICE]) * (9 / 100)
                cgst = float(product[S_O_P_PRODUCT_PRICE]) * (9 / 100)
                price_without_tax = float(product[S_O_P_PRODUCT_PRICE]) - sgst - cgst
                new_table_row = new_table_row + f"""
                <tr>
                    <td class="no">{s_no}</td>
                    <td class="desc" colspan=2>{product[PRODUCT_NAME]}<br>(Product Id: {product[P_O_P_FOREIGNKEY_PRODUCT_ID]})</td>
                    <td class="desc">{self.formatINR(price_without_tax)}</td>
                    <td class="desc">{self.formatINR(sgst)}</td>
                    <td class="desc">{self.formatINR(cgst)}</td>
                    <td class="desc">{self.formatINR(product[S_O_P_PRODUCT_PRICE])}</td>
                    <td class="desc">x {product[S_O_P_PRODUCT_QUANTITY]}</td>
                    <td class="total">{self.formatINR(product[S_O_P_PRODUCT_TOTAL_AMOUNT])}</td>
                </tr>
                """
                s_no = s_no + 1
                total_tax = total_tax + ((sgst + cgst) * int(product[S_O_P_PRODUCT_QUANTITY]))
                total_amount_without_tax = total_amount_without_tax + (price_without_tax * int(product[S_O_P_PRODUCT_QUANTITY]))
            
            # Setting Product Details in tabular format in html invoice
            table_details = f"""
            <table border="0" cellspacing="0" cellpadding="0">
                <thead>
                <tr>
                    <th class="no">#</th>
                    <th class="desc" colspan=2>Product Name</th>
                    <th class="desc">UNIT PRICE</th>
                    <th class="desc">SGST (9%)</th>
                    <th class="desc">CGST (9%)</th>
                    <th class="desc">UNIT TOTAL</th>
                    <th class="desc">QUANTITY</th>
                    <th class="total">TOTAL</th>
                </tr>
                </thead>
                <tbody>
                {new_table_row}
                </tbody>
                <tfoot>
                <tr>
                    <td colspan="1"></td>
                    <td colspan="2"></td>
                    <td colspan="1"></td>
                    <td colspan="1"></td>
                    <td colspan="3">SUBTOTAL (without tax)</td>
                    <td>{self.formatINR(total_amount_without_tax)}</td>
                </tr>
                <tr>
                    <td colspan="1"></td>
                    <td colspan="2"></td>
                    <td colspan="1"></td>
                    <td colspan="1"></td>
                    <td colspan="3">TOTAL GST (18%)</td>
                    <td>{self.formatINR(total_tax)}</td>
                </tr>
                <tr>
                    <td colspan="1"></td>
                    <td colspan="2"></td>
                    <td colspan="1"></td>
                    <td colspan="1"></td>
                    <td colspan="3">GRAND TOTAL</td>
                    <td>{self.formatINR((sales_order_data[SALES_ORDER_TOTAL_PRICE]))}</td>
                </tr>
                </tfoot>
            </table>
            """

            # Notice warning messages in invoce
            notice_div = self.returnAndCancelProductWarning(sales_order_product_data)



        ## When Purchase Order
        elif not (type(purchase_order_id) == None.__class__):
            purchase_order_data = self.queryFetchSinglePurchaseOrder(purchase_order_id)[0]
            purchase_order_product_data = self.queryFetchAllPurchaseOrderProduct(purchase_order_id)

            # Setting Customer Details
            third_party_div = f"""
            <div id="details" class="clearfix">
                <div id="client">
                <div class="to">RECEIPT TO SUPPLIER: </div>
                <h2 class="name">{purchase_order_data[SUPPLIER_NAME]} <small style="font-size:small;">(Supplier Id: {purchase_order_data[PURCHASE_ORDER_FOREIGNKEY_SUPPLIER_ID]})</small></h2>
                <div class="contact">{purchase_order_data[SUPPLIER_CONTACT_1]}</div>
                <div class="address">{purchase_order_data[SUPPLIER_ADDRESS]}</div>
                <div class="name"><strong>Organization:</strong> {purchase_order_data[SUPPLIER_ORGANIZATION_NAME]}</div>
                <div class="contact"><strong>Organization;s Contact:</strong> {purchase_order_data[SUPPLIER_ORGANIZATION_CONTACT_1]}</div>
                <div class="address"><strong>Organization's Address:</strong> {purchase_order_data[SUPPLIER_ORGANIZATION_ADDRESS]}</div>
                <div class="address"><strong>Supplier GSTIN:</strong> {purchase_order_data[SUPPLIER_GSTIN]}</div>
                </div>
                <div id="invoice">
                <div class="mode"><strong>Payment Mode:</strong> {purchase_order_data[PURCHASE_ORDER_PAYMENT_MODE]}</div>
                <div class="mode"><strong>Payment Status:</strong> {purchase_order_data[PURCHASE_ORDER_PAYMENT_STATUS]}</div>
                <div class="mode"><strong>Delivery Status:</strong> {purchase_order_data[PURCHASE_ORDER_DELIVERY_STATUS]}</div>
                <div class="status"><strong>Order Status:</strong> {purchase_order_data[PURCHASE_ORDER_STATUS]}</div>
                <div class="date"><strong>Date:</strong> {purchase_order_data[CREATED_AT].strftime("%B %d, %Y")}<br>{purchase_order_data[CREATED_AT].strftime("%I:%M %p")}</div>
                <h3 class="date">Purchase Order Id: {purchase_order_data[PURCHASE_ORDER_ID]}</h3>
                </div>
            </div>
            """

            # Modifying rows for each product
            s_no = 1
            total_tax = float(0)
            total_amount_without_tax = float(0)
            new_table_row = ""
            for product in purchase_order_product_data:
                sgst = float(product[P_O_P_PRODUCT_PRICE]) * (9 / 100)
                cgst = float(product[P_O_P_PRODUCT_PRICE]) * (9 / 100)
                price_without_tax = float(product[P_O_P_PRODUCT_PRICE]) - sgst - cgst
                new_table_row = new_table_row + f"""
                <tr>
                    <td class="no">{s_no}</td>
                    <td class="desc" colspan=2>{product[PRODUCT_NAME]}<br>(Product Id: {product[P_O_P_FOREIGNKEY_PRODUCT_ID]})</td>
                    <td class="desc">{self.formatINR(price_without_tax)}</td>
                    <td class="desc">{self.formatINR(sgst)}</td>
                    <td class="desc">{self.formatINR(cgst)}</td>
                    <td class="desc">{self.formatINR(product[P_O_P_PRODUCT_PRICE])}</td>
                    <td class="desc">x {product[P_O_P_PRODUCT_QUANTITY]}</td>
                    <td class="total">{self.formatINR(product[P_O_P_PRODUCT_TOTAL_AMOUNT])}</td>
                </tr>
                """
                s_no = s_no + 1
                total_tax = total_tax + ((sgst + cgst) * int(product[P_O_P_PRODUCT_QUANTITY]))
                total_amount_without_tax = total_amount_without_tax + (price_without_tax * int(product[P_O_P_PRODUCT_QUANTITY]))
            
            # Setting Product Details in tabular format in html invoice
            table_details = f"""
            <table border="0" cellspacing="0" cellpadding="0">
                <thead>
                <tr>
                    <td class="no">#</td>
                    <td class="desc" colspan=2>PRODUCT NAME</td>
                    <td class="desc">UNIT PRICE</td>
                    <td class="desc">SGST (9%)</td>
                    <td class="desc">CGST (9%)</td>
                    <td class="desc">UNIT TOTAL</td>
                    <td class="desc">BOUGHT QUANTITY</td>
                    <td class="total">TOTAL PAID</td>
                </tr>
                </thead>
                <tbody>
                {new_table_row}
                </tbody>
                <tfoot>
                <tr>
                    <td colspan="1"></td>
                    <td colspan="2"></td>
                    <td colspan="1"></td>
                    <td colspan="1"></td>
                    <td colspan="3">SUBTOTAL (without tax)</td>
                    <td>{self.formatINR(total_amount_without_tax)}</td>
                </tr>
                <tr>
                    <td colspan="1"></td>
                    <td colspan="2"></td>
                    <td colspan="1"></td>
                    <td colspan="1"></td>
                    <td colspan="3">TOTAL GST (18%)</td>
                    <td>{self.formatINR(total_tax)}</td>
                </tr>
                <tr>
                    <td colspan="1"></td>
                    <td colspan="2"></td>
                    <td colspan="1"></td>
                    <td colspan="1"></td>
                    <td colspan="3">TOTAL AMOUNT PAID</td>
                    <td>{self.formatINR((purchase_order_data[PURCHASE_ORDER_TOTAL_PRICE]))}</td>
                </tr>
                </tfoot>
            </table>
            """

            # Notice warning messages in invoce
            notice_div = self.returnAndCancelProductWarning(purchase_order_product_data)



        ## When Return Cancel Order
        elif not (type(return_cancel_order_id) == None.__class__):
            return_cancel_order_data = self.queryFetchSingleReturnCancelOrder(return_cancel_order_id)[0]
            return_cancel_order_product_data = self.queryFetchAllReturnCancelOrderProduct(return_cancel_order_id)

            if not (type(return_cancel_order_data[RETURN_CANCEL_ORDER_FOREIGNKEY_SALES_ORDER_ID]) == None.__class__):
                return_cancel_order_details = f"<strong>Sales Order Id:</strong> {return_cancel_order_data[RETURN_CANCEL_ORDER_FOREIGNKEY_SALES_ORDER_ID]}"
            elif not (type(return_cancel_order_data[RETURN_CANCEL_ORDER_FOREIGNKEY_PURCHASE_ORDER_ID]) == None.__class__):
                return_cancel_order_details = f"<strong>Purchase Order Id:</strong> {return_cancel_order_data[RETURN_CANCEL_ORDER_FOREIGNKEY_PURCHASE_ORDER_ID]}"


            # Setting Customer Details
            third_party_div = f"""
            <div id="details" class="clearfix">
                <div id="client">
                <div class="to">RETURN/CANCEL RECEIPT:</div><br>
                <div class="name">{return_cancel_order_details}</div>
                <div class="status">Status: {return_cancel_order_data[RETURN_CANCEL_ORDER_STATUS]}</div>
                </div>
                <div id="invoice">
                <h1>RETURN/CANCEL RECEIPT</h1>
                <div class="date"><strong>Date:</strong> {return_cancel_order_data[CREATED_AT].strftime("%B %d, %Y")}<br>{return_cancel_order_data[CREATED_AT].strftime("%I:%M %p")}</div>
                <h3 class="date">Return/Cancel Order Id: {return_cancel_order_data[RETURN_CANCEL_ORDER_ID]}</h3>
                </div>
            </div>
            """

            # Modifying rows for each product
            s_no = 1
            new_table_row = ""
            for product in return_cancel_order_product_data:
                new_table_row = new_table_row + f"""
                <tr>
                    <td class="no">{s_no}</td>
                    <td class="desc" colspan=2>{product[PRODUCT_NAME]}<br>(Product Id: {product[R_C_O_P_FOREIGNKEY_PRODUCT_ID]})</td>
                    <td class="desc">x {product[R_C_O_P_PRODUCT_CANCEL_QUANTITY]}</td>
                    <td class="desc">x {product[R_C_O_P_PRODUCT_RETURN_QUANTITY]}</td>
                    <td class="total">{self.formatINR(product[R_C_O_P_PRODUCT_REFUND_AMOUNT])}</td>
                </tr>
                """
                s_no = s_no + 1
            
            # Setting Product Details in tabular format in html invoice
            table_details = f"""
            <table border="0" cellspacing="0" cellpadding="0">
                <thead>
                <tr>
                    <td class="no">#</td>
                    <td class="desc" colspan=2>PRODUCT NAME</td>
                    <td class="desc">CANCELLED QUANTITY</td>
                    <td class="desc">RETURNED QUANTITY</td>
                    <td class="total">REFUND FOR PRODUCTS</td>
                </tr>
                </thead>
                <tbody>
                {new_table_row}
                </tbody>
                <tfoot>
                <tr>
                    <td colspan="1"></td>
                    <td colspan="2"></td>
                    <td colspan="2">TOTAL AMOUNT REFUNDED</td>
                    <td>{self.formatINR((return_cancel_order_data[RETURN_CANCEL_ORDER_TOTAL_REFUND_AMOUNT]))}</td>
                </tr>
                </tfoot>
            </table>
            """

            # Notice warning messages in invoce
            notice_div = ""



        # Creating or overriding file
        try:
            invoice_file = open(temp_file_path, "w", encoding="utf-8") # UTF-8 encoding for rupee character or else throw errors
        except Exception as error:
            print(f"Development Error (While Creating Sales Order): {error}")
            ErrorModal("Something went wrong while creating sales order, please contact developer.", self)


        print_method_in_text = "function print(){window.print()}; print()"
       
        try:
            # Try to access file path if done successfuly then give logo_name value else goto except
            a = open(path.join(PATH_TO_IMAGES, FILE_APP_LOGO), "r")
            logo_name = FILE_APP_LOGO
            a.close()
        except Exception:
            a = open(path.join(PATH_TO_IMAGES, FILE_APP_DEFAULT_LOGO), "r")
            logo_name = FILE_APP_DEFAULT_LOGO
            a.close()
            
        if len(getShopDetails()[SHOP_GST_NUMBER]) == 0:
            gst_div = ""
        else:
            gst_div = f"<div><strong>GSTIN:</strong> {getShopDetails()[SHOP_GST_NUMBER]}</div>"
        # Creating HTML template for invoice
        html_template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="utf-8" >
            <title>{getShopDetails()[SHOP_NAME]}</title>
            <link rel="icon" href="{PATH_TO_IMAGES}/{logo_name}" type="image/icon type">
            <link rel="stylesheet" href="invoice_style.css" media="all" />
        </head>
        <body>
            <header class="clearfix">
            <div id="logo">
                <img src="{PATH_TO_IMAGES}/{logo_name}", alt="{getShopDetails()[SHOP_NAME]}", width=80, height=200>
            </div>
            <div id="company">
                <h2 class="name">{getShopDetails()[SHOP_NAME]}</h2>
                <div>{getShopDetails()[SHOP_ADDRESS]}</div>
                <div>{getShopDetails()[SHOP_CONTACT_1]}</div>
                <div>{getShopDetails()[SHOP_CONTACT_2]}</div>
                <div><a href="mailto:{getShopDetails()[SHOP_EMAIL]}">{getShopDetails()[SHOP_EMAIL]}</a></div>
                {gst_div}
            </div>
            <div id="company">
                <button id="print_button" onClick="{print_method_in_text}">Print Document</button>
            </div>
            </div>
            </header>
            <main>
                <!-- Invoice Details -->
                {third_party_div}
                
                <!-- Invoice Products Details -->
                {table_details}

                <!-- div for showing notices and warnings -->
                {notice_div}

            </main>
        </body>
        </html>"""

        invoice_file.write(html_template)
        invoice_file.close()

        # Opening the file in webbrowser
        webbrowser.open(temp_file_path, new=2)
        timer = threading.Timer(10,  lambda: remove(temp_file_path))
        timer.start()



    # Notice warning messages in invoce
    def returnAndCancelProductWarning(self, product_list):
        elements = ""
        for product in product_list:
            if product[CANCELLED_QUANTITY] > 0 and product[RETURNED_QUANTITY] > 0:
                elements = elements + f"<li>'{product[PRODUCT_NAME]}' already have x{product[CANCELLED_QUANTITY]} quantity cancelled and x{product[RETURNED_QUANTITY]} quantity returned.</li>"
            elif product[CANCELLED_QUANTITY] > 0:
                elements = elements + f"<li>'{product[PRODUCT_NAME]}' already have x{product[CANCELLED_QUANTITY]} quantity cancelled.</li>"
            elif product[RETURNED_QUANTITY] > 0:
                elements = elements + f"<li>'{product[PRODUCT_NAME]}' already have x{product[RETURNED_QUANTITY]} quantity returned.</li>"
            else:
                elements = elements
        if len(elements) == 0:
            notice = ""
        else:    
            notice = f"""
            <div id="notices">
                <div>NOTICE:</div>
                    <div class="notice">
                        <ul>
                            {elements}
                        </ul>
                    </div>
            </div>
            """
        return notice