import mysql.connector
import hashlib
import os
from fpdf import FPDF



def login_system():
    # Connect to the database
    connection = mysql.connector.connect(
        host="localhost",
        port=3307,
        user="root",
        password="123456",
        # database="digitalhub"
        database="Digital_Hub"
    )
    cursor = connection.cursor(buffered=True)

    def hash_password(password, salt):
        return hashlib.sha256(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()

    def initialize_admin_account():
        cursor.execute("SELECT COUNT(*) FROM staff WHERE Staff_designation = 'Administrator'")
        count = cursor.fetchone()[0]
        if count == 0:
            print("No administrator account found. Please create the initial administrator account.")
            add_account(is_admin_initialization=True)

    def login():
        while True:
            initialize_admin_account()

            try:
                print("\nWelcome to Digital Hub")
                print("\n1. Login")
                print("2. Exit")
                choice = input("\nEnter your option (1-2): ")

                if choice == '1':
                    print("Please note that the Staff Name is case sensitive.")
                    username = input("Enter Staff Name: ")
                    password = input("Enter Password: ")

                    sql_query = "SELECT Staff_hash, Staff_salt, Staff_designation FROM staff WHERE Staff_name = %s"
                    cursor.execute(sql_query, (username,))
                    result = cursor.fetchone()

                    if result:
                        hashed_password, salt, designation = result
                        if hash_password(password, salt) == hashed_password:
                            print("Login successful!")
                            main_menu_flow(username, designation)
                        else:
                            print("Invalid Staff Name or password. Please try again.")
                    else:
                        print("Invalid Staff Name or password. Please try again.")

                elif choice == '2':
                    print("Exiting...")
                    break

                else:
                    print("Invalid choice. Please try again.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                print("An error occurred. Please try again.")

    def main_menu(username, designation):
        print(f"\nHello {username},")
        print("Role:", designation)
        print("Please choose what you want to do for today:")
        print("\nMain Menu:")
        print("\t1. View Sales Information")
        print("\t2. Manage Products")
        print("\t3. Manage Customers")
        print("\t4. Manage Orders")
        print("\t5. Manage Stores")
        print("\t6. Administrative Matters")
        print("\t7. Update Personal Details")
        print("\t8. Exit")
        choice = input("\nEnter your option (1-8): ")
        return choice

    def main_menu_flow(username, designation):
        while True:
            choice = main_menu(username, designation)

            if choice == '1':
                sub_choice = view_sales_information_menu()
                if sub_choice == '7':
                    continue  # Return to main menu
                # Further implementation based on view sales information choice
            elif choice == '2':
                sub_choice = manage_product_menu(designation)
                if sub_choice == '5':
                    continue  # Return to main menu
                # Further implementation based on manage products choice
            elif choice == '3':
                sub_choice = manage_customers_menu(designation)
                if sub_choice == '5':
                    continue  # Return to main menu
                # Further implementation based on manage customers choice
            elif choice == '4':
                sub_choice = manage_orders_menu()
                if sub_choice == '5':
                    continue  # Return to main menu
                # Further implementation based on manage orders choice
            elif choice == '5':
                sub_choice = manage_stores_menu(designation)
                if sub_choice == '4':
                    continue  # Return to main menu
                    # Further implementation based on manage stores choice
            elif choice == '6':
                if designation == 'Administrator':
                    while True:
                        admin_choice = administrative_matters_menu()
                        if admin_choice == '1':
                            add_account()
                        elif admin_choice == '2':
                            delete_account(username)
                        elif admin_choice == '3':
                            update_designation(username)
                        elif admin_choice == '4':
                            break
                        else:
                            print("Invalid choice. Please try again.")
                else:
                    print("You are not authorized to access this. Please contact the admin.")
            elif choice == '7':
                update_personal_details(username)
            elif choice == '8':
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please try again.")

    def count_total_records(table_name):
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        return cursor.fetchone()[0]


    def view_sales_information_menu():
        while True:
            print("\nView Sales Information")
            print("1. View Sales by Store")
            print("2. View Sales by Product")
            print("3. View Sales by Customer")
            print("4. View Sales by Invoice")
            print("5. Generate Invoice")
            print("6. View All Sales")
            print("7. Back to Main Menu")

            choice = input("\nEnter your option (1-7): ")

            if choice == '1':
                view_sales_by_store()
            elif choice == '2':
                view_sales_by_product()
            elif choice == '3':
                view_sales_by_customer()
            elif choice == '4':
                view_sales_by_invoice()
            elif choice == '5':
                generate_invoice()
            elif choice == '6':
                view_all_sales()
            elif choice == '7':
                break
            else:
                print("Invalid option. Please enter a number between 1 and 7.")

    def view_sales_by_store():
        total_records = count_total_records('store')
        offset = 0
        records_fetched = 0

        while True:
            query = """
            SELECT store.Store_Id, SUM(product.Product_Unit_Price * `order item`.Purchased_Quantity) AS Total_Sales_Amount
            FROM store
            JOIN `order` ON store.Store_Id = `order`.Store_Id
            JOIN `order item` ON `order`.Order_Id = `order item`.Order_Id
            JOIN product ON `order item`.Product_Id = product.Product_Id
            GROUP BY store.Store_Id
            LIMIT 100 OFFSET %s
            """
            cursor.execute(query, (offset,))
            results = cursor.fetchall()
            num_records = len(results)
            records_fetched += num_records

            if num_records == 0:
                print("No more sales records.")
                break

            # Format the total sales amount to avoid scientific notation
            table_data = [[row[0], "{:,.2f}".format(row[1])] for row in results]
            print(tabulate(table_data, headers=["Store ID", "Total Sales Amount"], tablefmt="pipe"))
            print(f"\n{records_fetched} records fetched out of {total_records} records.\n")

            while True:
                more = input("Do you want to view the next 100 records? \n1. Yes\n2. No\n: ")
                if more == '1':
                    offset += 100
                    break
                elif more == '2':
                    return
                else:
                    print("Invalid input. Please enter 1 or 2.")

    def view_sales_by_product():
        total_records = count_total_records('product')
        offset = 0
        records_fetched = 0

        while True:
            cursor.execute(
                "SELECT Product_Id, Product_Name, Product_Brand, Product_Color, Product_Unit_Cost, Product_Unit_Price, Product_Category_Id, discontinued FROM product LIMIT 100 OFFSET %s",
                (offset,))
            results = cursor.fetchall()
            records_fetched += len(results)

            if not results:
                print("No more products.")
                break

            table_data = [row for row in results]
            print(tabulate(table_data,
                           headers=["Product ID", "Product Name", "Brand", "Color", "Unit Cost", "Unit Price",
                                    "Category ID", "Discontinued"], tablefmt="pipe"))
            print(f"\n{records_fetched} records fetched out of {total_records} records.\n")

            while True:
                more = input("Do you want to view the next 100 records? \n1. Yes\n2. No\n: ")
                if more == '1':
                    offset += 100
                    break
                elif more == '2':
                    return
                else:
                    print("Invalid input. Please enter 1 or 2.")

    from tabulate import tabulate
    def view_sales_by_customer():
        total_records = count_total_records('cust')
        offset = 0
        records_fetched = 0

        while True:
            cursor.execute(
                "SELECT CUST_Id, Cust_Name, Cust_City, Cust_State, Cust_State_Code, Cust_Zip_Code, Cust_Country, Cust_Continent, Cust_Birthday, Cust_Gender FROM cust LIMIT 100 OFFSET %s",
                (offset,))
            results = cursor.fetchall()
            records_fetched += len(results)

            if not results:
                print("No more customers.")
                break

            table_data = [row for row in results]
            print(tabulate(table_data,
                           headers=["Customer ID", "Name", "City", "State", "State Code", "Zip Code", "Country",
                                    "Continent", "Birthday", "Gender"], tablefmt="pipe"))
            print(f"\n{records_fetched} records fetched out of {total_records} records.\n")

            while True:
                more = input("Do you want to view the next 100 records? \n1. Yes\n2. No\n: ")

                if more == '1':
                    offset += 100
                    break
                elif more == '2':
                    return
                else:
                    print("Invalid input. Please enter 1 or 2.")

    def view_sales_by_invoice():
        total_records = count_total_records('`order`')
        offset = 0
        records_fetched = 0

        while True:
            query = """
             SELECT o.Order_Number, SUM(oi.Purchased_Quantity * p.Product_Unit_Price) AS Total_Sales_Amount
             FROM `order` o
             JOIN `order item` oi ON o.Order_Id = oi.Order_Id
             JOIN `product` p ON oi.Product_Id = p.Product_Id
             GROUP BY o.Order_Number
             LIMIT 100 OFFSET %s
             """
            cursor.execute(query, (offset,))
            results = cursor.fetchall()
            records_fetched += len(results)

            if not results:
                print("No more sales records.")
                break

            table_data = []
            for row in results:
                total_sales_amount = "{:.1f}".format(row[1])
                table_data.append([row[0], total_sales_amount])

            print(tabulate(table_data, headers=["Order Number", "Total Sales Amount"], tablefmt="pipe"))
            print(f"\n{records_fetched} records fetched out of {total_records} records.\n")

            while True:
                more = input("Do you want to view the next 100 records? \n1. Yes\n2. No\n: ")

                if more == '1':
                    offset += 100
                    break
                elif more == '2':
                    return
                else:
                    print("Invalid input. Please enter 1 or 2.")
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 16)
            self.cell(0, 10, 'Digital Hub', 0, 1, 'C')
            self.set_font('Arial', 'I', 12)
            self.ln(10)
            self.set_font('Arial', '', 12)

            # 设置列宽
            column_width = 90  # 适当设置列宽

            # 计算起始x坐标
            x_start = 10
            x_mid = x_start + column_width

            # 打印客户名称和商店国家
            self.set_x(x_start)
            self.cell(column_width, 10, f'Cust Name: {self.cust_name}', 0, 0, 'L')
            self.cell(column_width, 10, f'Order ID: {self.order_id}', 0, 1, 'L')

            # 打印商店州和订单ID
            self.set_x(x_start)
            self.cell(column_width, 10, f'Store Country: {self.store_country}', 0, 0, 'L')
            self.set_x(x_mid)
            self.cell(column_width, 10, f'Order Date: {self.order_date}', 0, 1, 'L')

            # 打印订单日期和交货日期
            self.set_x(x_start)
            self.cell(column_width, 10, f'Store State: {self.store_state}', 0, 0, 'L')
            self.set_x(x_mid)
            self.cell(column_width, 10, f'Delivery Date: {self.delivery_date}', 0, 1, 'L')

            self.ln(10)

        def invoice_body(self, table_data, total_price):
            self.set_font('Arial', '', 12)
            self.set_font('Arial', 'B', 12)
            self.cell(100, 10, 'ITEM', 1, 0)
            self.cell(30, 10, 'QUANTITY', 1, 0, 'C')
            self.cell(0, 10, 'ITEM PRICE', 1, 1, 'C')
            self.set_font('Arial', '', 12)
            for row in table_data:
                self.cell(100, 10, row[0], 1, 0)
                self.cell(30, 10, str(row[1]), 1, 0, 'C')
                self.cell(0, 10, f'${row[2]:.2f}', 1, 1, 'C')
            self.ln(10)
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, f'Total Price: ${total_price:.2f}', 0, 1)
            self.ln(10)
            self.cell(0, 10, 'Thank you for shopping with us!', 0, 1, 'C')
            self.cell(0, 10, 'Do remember to register to become a member if you wish to receive a membership discount',
                      0, 1, 'C')

        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    from tkinter import Tk, filedialog

    def generate_invoice():
        while True:
            order_id = input("Enter the order Number for the invoice or 'q' to return to the previous menu: ")
            if order_id.lower() == 'q':
                break

            try:
                query = """
                SELECT 
                    o.Order_Number, sl.Store_Country, sl.Store_State, o.Order_Date, o.Delivery_Date, 
                    c.Cust_Name, p.Product_Name, p.Product_Unit_Price, oi.Purchased_Quantity
                FROM 
                    `order` o
                JOIN 
                    `cust` c ON o.CUST_Id = c.CUST_Id
                JOIN 
                    `order item` oi ON o.Order_Id = oi.Order_Id
                JOIN 
                    `product` p ON oi.Product_Id = p.Product_Id
                JOIN 
                    `store` s ON o.Store_Id = s.Store_Id
                JOIN 
                    `store location` sl ON s.Store_Location_Id = sl.Store_Location_Id
                WHERE 
                    o.Order_Number = %s;
                """
                cursor.execute(query, (order_id,))
                results = cursor.fetchall()

                if not results:
                    print("No sales records found for the given order Number.")
                    continue

                table_data = []
                total_price = 0

                cust_name, order_number, store_country, store_state, order_date, delivery_date = None, None, None, None, None, None

                for row in results:
                    order_number, store_country, store_state, order_date, delivery_date, cust_name, product_name, unit_price, quantity = row
                    table_data.append([product_name, quantity, unit_price])
                    total_price += unit_price * quantity

                headers = ["ITEM", "QUANTITY", "ITEM PRICE"]
                print("\nHere is your bill...\n")
                print("------------------ Grocery Bill ------------------")
                print(tabulate(table_data, headers=headers, tablefmt="pipe"))
                print("--------------------------------------------------")
                print("Total Price: ${:<10.2f}".format(total_price))
                print("--------------------------------------------------")
                print("\n---------------- Hello Dear Customer ----------------")
                print("Thank you for shopping with us!")
                print("Do remember to register to become a member if you wish to receive a membership discount")
                print("Please minimize the current window to save the invoice file in pdf format. After saving press q to return to the main menu")

                # 打开保存对话框
                root = Tk()
                root.withdraw()
                pdf_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")],
                                                        title="Save Invoice As")
                root.destroy()

                if pdf_file:
                    pdf = PDF()
                    pdf.cust_name = cust_name
                    pdf.store_country = store_country
                    pdf.store_state = store_state
                    pdf.order_id = order_number
                    pdf.order_date = order_date
                    pdf.delivery_date = delivery_date
                    pdf.add_page()
                    pdf.invoice_body(table_data, total_price)
                    pdf.output(pdf_file)
                    print(f"Invoice generated and saved as {pdf_file}")

            except Exception as e:
                print(f"Error: {e}")
                if pdf_file:
                    pdf = PDF()
                    pdf.cust_name = cust_name
                    pdf.store_country = store_country
                    pdf.store_state = store_state
                    pdf.order_id = order_number
                    pdf.order_date = order_date
                    pdf.delivery_date = delivery_date
                    pdf.add_page()
                    pdf.invoice_body(table_data, total_price)
                    pdf.output(pdf_file)
                    print(f"Invoice generated and saved as {pdf_file}")

            except mysql.connector.Error as err:
                print(f"Error: {err}")
                print("An error occurred. Please try again.")

    from tabulate import tabulate

    def view_all_sales():
        total_records = count_total_records_via_join()  # 计算总记录数的函数
        offset = 0
        total_fetched = 0
        order_by = "product.Product_Name"  # 默认排序

        while True:
            # 如果 order_by 未设置则显示子菜单
            if offset == 0:
                print(
                    "1. Category\n"
                    "2. Price Low to High\n"
                    "3. Price High to Low\n"
                    "4. Return to MAIN PAGE"
                )
                choice = input("Choose how you want to view the records: ")

                if choice == '1':
                    order_by = "category.Category_Name"
                elif choice == '2':
                    order_by = "product.Product_Unit_Price ASC"
                elif choice == '3':
                    order_by = "product.Product_Unit_Price DESC"
                elif choice == '4':
                    break  # 退出子菜单并返回主菜单
                else:
                    print("Invalid choice. Please try again.")
                    continue

            # 使用 JOIN 查询替代对 transactionrecord 表的直接查询
            query = f"""
            SELECT 
                `order item`.Order_Item_Id AS ID, 
                `order`.Order_Number AS `Order Number`, 
                `order item`.Line_Item AS `Line Item`, 
                cust.Cust_Name AS `Cust Name`, 
                cust.Cust_City AS `Cust City`, 
                cust.Cust_State_Code AS `Cust State Code`, 
                cust.Cust_State AS `Cust State`, 
                cust.Cust_Zip_Code AS `Cust Zip Code`, 
                cust.Cust_Country AS `Cust Country`, 
                cust.Cust_Continent AS `Cust Continent`, 
                `store location`.Store_Country AS `Store Country`, 
                `store location`.Store_State AS `Store State`, 
                store.Store_Square_Meters AS `Store Square Meters`, 
                product.Product_Name AS `Product Name`, 
                product.Product_Brand AS `Product Brand`, 
                product.Product_Color AS `Product Color`, 
                product.Product_Unit_Cost AS `Product Unit Cost`, 
                product.Product_Unit_Price AS `Product Unit Price`, 
                category.Category_Name AS `Product Category`, 
                `order item`.Purchased_Quantity AS `Purchased Quantity`, 
                `order`.Order_Date AS `Order Date`, 
                `order`.Delivery_Date AS `Delivery Date`, 
                cust.Cust_Birthday AS `Cust Birthday`, 
                store.Store_Open_Date AS `Store Open Date`, 
                cust.Cust_Gender AS `Cust Gender`
            FROM 
                `order item`
            JOIN 
                `order` ON `order item`.Order_Id = `order`.Order_Id
            JOIN 
                `cust` ON `order`.CUST_Id = cust.CUST_Id
            JOIN 
                `product` ON `order item`.Product_Id = product.Product_Id
            JOIN 
                `category` ON product.Product_Category_Id = category.Category_Id
            JOIN 
                `store` ON `order`.Store_Id = store.Store_Id
            JOIN 
                `store location` ON store.Store_Location_Id = `store location`.Store_Location_Id
            ORDER BY 
                {order_by} 
            LIMIT 100 OFFSET {offset}
            """

            cursor.execute(query)
            results = cursor.fetchall()
            num_results = len(results)
            total_fetched += num_results

            if not results:
                print("No more sales records.")
                break

            column_names = [
                "ID", "Order Number", "Line Item", "Cust Name", "Cust City", "Cust State Code",
                "Cust State", "Cust Zip Code", "Cust Country", "Cust Continent", "Store Country",
                "Store State", "Store Square Meters", "Product Name", "Product Brand",
                "Product Color", "Product Unit Cost", "Product Unit Price", "Product Category",
                 "Purchased Quantity", "Order Date", "Delivery Date",
                "Cust Birthday", "Store Open Date", "Cust Gender"
            ]

            # 使用 tabulate 打印表格
            print(tabulate(results, headers=column_names, tablefmt="grid"))

            # 打印已获取记录数
            print(f"{total_fetched} records fetched out of {total_records} records.")

            # 询问用户是否要查看下 100 条记录
            while True:
                more = input("Do you want to view the next 100 records? \n1. Yes\n2. No\n: ")
                if more == '1':
                    offset += 100
                    break
                elif more == '2':
                    return
                else:
                    print("Invalid input. Please enter 1 or 2.")

    def count_total_records_via_join():
        query = """
        SELECT COUNT(*)
        FROM 
            `order item`
        JOIN 
            `order` ON `order item`.Order_Id = `order`.Order_Id
        JOIN 
            `cust` ON `order`.CUST_Id = cust.CUST_Id
        JOIN 
            `product` ON `order item`.Product_Id = product.Product_Id
        JOIN 
            `category` ON product.Product_Category_Id = category.Category_Id
        JOIN 
            `store` ON `order`.Store_Id = store.Store_Id
        JOIN 
            `store location` ON store.Store_Location_Id = `store location`.Store_Location_Id
        """
        cursor.execute(query)
        total_records = cursor.fetchone()[0]
        return total_records

    def manage_product_menu(designation):
        while True:
            # Display the complete menu
            print("\nManage Products")
            print("1. Add New Product" if designation in ['Administrator',
                                                          'Manager'] else "1. Add New Product(No Access)")
            print("2. Modify Existing Product" if designation in ['Administrator',
                                                                  'Manager'] else "2. Modify Existing Product(No Access)")
            print(
                "3. Delete Product" if designation in ['Administrator', 'Manager'] else "3. Delete Product(No Access)")
            print("4. Search Product")
            print("5. View All Products")
            print("6. Back to Main Menu")

            choice = input("\nEnter your option (1-6): ")

            if choice == '1' and designation in ['Administrator', 'Manager']:
                add_new_product()
            elif choice == '2' and designation in ['Administrator', 'Manager']:
                modify_existing_product()
            elif choice == '3' and designation in ['Administrator', 'Manager']:
                delete_product()
            elif choice == '4':
                search_product()
            elif choice == '5':
                view_all_products()
            elif choice == '6':
                break
            else:
                if choice in ['1', '2', '3']:
                    print("You are not authorized to access this. Please contact the admin.")
                else:
                    print("Invalid option.")

    def add_new_product():
        while True:
            product_name = input("Enter product name: ").strip()
            if not product_name:
                print("Invalid, product name cannot be blank. Please enter a valid product name.")
                continue

            product_brand = input("Enter product brand: ").strip()
            if not product_brand:
                print("Invalid, product brand cannot be blank. Please enter a valid product brand.")
                continue

            product_color = input("Enter product color: ").strip()
            if not product_color:
                print("Invalid, product color cannot be blank. Please enter a valid product color.")
                continue

            try:
                product_unit_cost = float(input("Enter product unit cost: ").strip())
            except ValueError:
                print("Invalid, product unit cost must be a number. Please enter a valid product unit cost.")
                continue

            try:
                product_unit_price = float(input("Enter product unit price: ").strip())
            except ValueError:
                print("Invalid, product unit price must be a number. Please enter a valid product unit price.")
                continue

            try:
                discontinued = int(input("Enter discontinued status (1 for discontinued, 0 for available): ").strip())
                if discontinued not in (0, 1):
                    raise ValueError
            except ValueError:
                print("Invalid, discontinued status must be 0 or 1. Please enter a valid discontinued status.")
                continue

            category_choice = input(
                "Do you want to add the new product to an existing category or a new category? \n1.existing\n2.new\n: ").strip().lower()
            if category_choice == '2':
                category_name = input("Enter new category name: ").strip()
                if not category_name:
                    print("Invalid, category name cannot be blank. Please enter a valid category name.")
                    continue

                subcategory_name = input("Enter new subcategory name: ").strip()
                if not subcategory_name:
                    print("Invalid, subcategory name cannot be blank. Please enter a valid subcategory name.")
                    continue

                try:
                    cursor.execute("""
                        INSERT INTO category (Category_Name, SubCategory_Name) 
                        VALUES (%s, %s)
                    """, (category_name, subcategory_name))
                    category_id = cursor.lastrowid
                    print(f"New category added successfully. Category ID: {category_id}")
                except mysql.connector.Error as err:
                    print(f"Error: {err}")
                    continue
            else:
                try:
                    category_id = int(input("Enter existing product category ID: ").strip())
                except ValueError:
                    print("Invalid, category ID must be a number. Please enter a valid category ID.")
                    continue

            try:
                cursor.execute("""
                    INSERT INTO product (Product_Name, Product_Brand, Product_Color, Product_Unit_Cost, Product_Unit_Price, Product_Category_Id, discontinued) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (product_name, product_brand, product_color, product_unit_cost, product_unit_price, category_id,
                      discontinued))
                print("Product added successfully.")
                connection.commit()
                break
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                connection.rollback()
                print("An error occurred. Please try again.")

    def modify_existing_product():
        product_id = int(input("Enter the product ID to modify: "))
        print("Enter new details for the product. Leave blank to keep current value.")
        product_name = input("Enter new product name: ")
        product_brand = input("Enter new product brand: ")
        product_color = input("Enter new product color: ")
        product_unit_cost = input("Enter new product unit cost: ")
        product_unit_price = input("Enter new product unit price: ")
        product_category_id = input("Enter new product category ID: ")
        discontinued = input("Enter new discontinued status \n1 for discontinued\n0 for available\n: ")

        updates = []
        values = []

        if product_name:
            updates.append("Product_Name = %s")
            values.append(product_name)
        if product_brand:
            updates.append("Product_Brand = %s")
            values.append(product_brand)
        if product_color:
            updates.append("Product_Color = %s")
            values.append(product_color)
        if product_unit_cost:
            updates.append("Product_Unit_Cost = %s")
            values.append(float(product_unit_cost))
        if product_unit_price:
            updates.append("Product_Unit_Price = %s")
            values.append(float(product_unit_price))
        if product_category_id:
            updates.append("Product_Category_Id = %s")
            values.append(int(product_category_id))
        if discontinued:
            updates.append("discontinued = %s")
            values.append(int(discontinued))

        if updates:
            try:
                cursor.execute(f"""
                    UPDATE product SET {', '.join(updates)} WHERE Product_Id = %s
                """, values + [product_id])
                print("Product modified successfully.")
                connection.commit()
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                connection.rollback()
        else:
            print("No updates made.")

    def delete_product():
        product_id = int(input("Enter the product ID to delete: "))
        try:
            # 首先检查产品是否存在
            cursor.execute("SELECT 1 FROM product WHERE Product_Id = %s", (product_id,))
            product = cursor.fetchone()

            if not product:
                print("Product not found.")
                return

            # 产品存在时，进行更新操作
            cursor.execute("UPDATE product SET discontinued = 1 WHERE Product_Id = %s", (product_id,))
            cursor.execute("UPDATE `order item` SET product_status = 'discontinued' WHERE Product_Id = %s",
                           (product_id,))

            # 提交更改
            connection.commit()

            print("Product marked as discontinued and its related order items updated successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()

    def search_product():
        print("1. Search product by ID")
        print("2. Search product by name")

        choice = input("Enter your choice (1 or 2): ")

        if choice == '1':
            search_term = input("Enter product ID to search: ")
            query = "SELECT * FROM product WHERE Product_Id = %s"
            params = (search_term,)
        elif choice == '2':
            search_term = input("Enter product name to search: ")
            query = "SELECT * FROM product WHERE Product_Name LIKE %s"
            params = (f"%{search_term}%",)
        else:
            print("Invalid choice. Please enter 1 or 2.")
            return

        try:
            cursor.execute(query, params)
            results = cursor.fetchall()
            if results:
                headers = ["Product_Id", "Product_Name", "Product_Brand", "Product_Color", "Product_Unit_Cost",
                           "Product_Unit_Price", "Product_Category_Id", "Discontinued"]
                table = tabulate(results, headers, tablefmt="pipe", floatfmt=".2f")
                print(table)
            else:
                print("No products found.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def view_all_products():
        total_records = count_total_records('product')
        offset = 0
        records_fetched = 0
        order_by = "`Product_Name`"

        while True:

            if offset == 0:
                print(
                    "1. Alphabetical\n"
                    "2. Category\n"
                    "3. Price Low to High\n"
                    "4. Price High to Low\n"
                    "5. Return to MAIN PAGE"
                )

                choice = input("Choose how you want to view the records: ")

                if choice == '1':
                    order_by = "`Product_Name`"
                elif choice == '2':
                    order_by = "`Product_Category_Id`"
                elif choice == '3':
                    order_by = "`Product_Unit_Price` ASC"
                elif choice == '4':
                    order_by = "`Product_Unit_Price` DESC"
                elif choice == '5':
                    break
                else:
                    print("Invalid choice. Please try again.")
                    continue

            cursor.execute(f"SELECT * FROM product ORDER BY {order_by} LIMIT 100 OFFSET %s", (offset,))
            results = cursor.fetchall()
            records_fetched += len(results)

            if not results:
                print("No more products.")
                break

            headers = ["Product_Id", "Product_Name", "Product_Brand", "Product_Color", "Product_Unit_Cost",
                       "Product_Unit_Price", "Product_Category_Id", "Discontinued"]
            table = tabulate(results, headers, tablefmt="pipe", floatfmt=".2f")
            print(table)
            print(f"\n{records_fetched} records fetched out of {total_records} records.\n")

            while True:
                more = input("Do you want to view the next 100 records? \n1. Yes\n2. No\n: ")
                if more == '1':
                    offset += 100
                    break
                elif more == '2':
                    return
                else:
                    print("Invalid input. Please enter 1 or 2.")

    def manage_customers_menu(designation):
        while True:
            # Display the complete menu
            print("\nManage Customers")
            print("1. Add New Customer" if designation in ['Administrator',
                                                           'Manager'] else "1. Add New Customer(No Access)")
            print("2. Modify Existing Customer" if designation in ['Administrator',
                                                                   'Manager'] else "2. Modify Existing Customer(No Access)")
            print("3. Delete Customer" if designation in ['Administrator',
                                                          'Manager'] else "3. Delete Customer(No Access)")
            print("4. Search Customer")
            print("5. View All Customers")
            print("6. Back to Main Menu")

            choice = input("\nEnter your option (1-6): ")

            if choice == '1' and designation in ['Administrator', 'Manager']:
                add_new_customer()
            elif choice == '2' and designation in ['Administrator', 'Manager']:
                modify_existing_customer()
            elif choice == '3' and designation in ['Administrator', 'Manager']:
                delete_customer()
            elif choice == '4':
                search_customer()
            elif choice == '5':
                view_all_customers()
            elif choice == '6':
                break
            else:
                if choice in ['1', '2', '3']:
                    print("You are not authorized to access this. Please contact the admin.")
                else:
                    print("Invalid option.")

    def add_new_customer():
        while True:
            name = input("Enter customer name: ")
            city = input("Enter customer city: ")
            state = input("Enter customer state: ")
            state_code = input("Enter customer state code: ")
            zip_code = input("Enter customer zip code: ")
            country = input("Enter customer country: ")
            continent = input("Enter customer continent: ")
            dob = input("Enter date of birth (YYYY-MM-DD): ")
            gender = input("Enter gender \n1. Female\n2. Male\n: ").strip()
            if gender not in ['1', '2']:
                print("Invalid, customer gender cannot be blank. please enter 1 for Female or 2 for Male.")
                continue

            try:
                year, month, day = map(int, dob.split('-'))
                dob = f"{year:04d}-{month:02d}-{day:02d}"
            except ValueError:
                print("Invalid date format, please enter in YYYY-MM-DD format.")
                continue
            try:
                cursor.execute(
                    "INSERT INTO cust (Cust_Name, Cust_City, Cust_State, Cust_State_Code, Cust_Zip_Code, Cust_Country, Cust_Continent, Cust_Birthday, Cust_Gender) VALUES (%s, %s, %s,%s, %s, %s, %s, %s, %s)",
                    (name, city, state, state_code, zip_code, country, continent, dob,
                     'Female' if gender == '1' else 'Male'
                     ))
                connection.commit()
                print("Customer added successfully.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
            break

    def modify_existing_customer():
        customer_id = int(input("Enter the customer ID to modify: "))
        print("Enter new details for the customer. Leave blank to keep current value.")

        name = input("Enter new customer name: ")
        city = input("Enter new customer city: ")
        state = input("Enter new customer state: ")
        state_code = input("Enter new customer state code: ")
        zip_code = input("Enter new customer zip code: ")
        country = input("Enter new customer country: ")
        continent = input("Enter new customer continent: ")
        birthday = input("Enter new customer birthday (YYYY-MM-DD): ")

        print("Enter new customer gender\n 1.Male\n2.Female\n:")
        gender_choice = input("Choose gender (1 or 2): ").strip()

        if gender_choice == '1':
            gender = 'Male'
        elif gender_choice == '2':
            gender = 'Female'
        else:
            gender = None
            print("Invalid choice for gender. No changes will be made to gender.")

        updates = []
        values = []
        if name:
            updates.append("Cust_Name = %s")
            values.append(name)
        if city:
            updates.append("Cust_City = %s")
            values.append(city)
        if state:
            updates.append("Cust_State = %s")
            values.append(state)
        if state_code:
            updates.append("Cust_State_Code = %s")
            values.append(state_code)
        if zip_code:
            updates.append("Cust_Zip_Code = %s")
            values.append(zip_code)
        if country:
            updates.append("Cust_Country = %s")
            values.append(country)
        if continent:
            updates.append("Cust_Continent = %s")
            values.append(continent)
        if birthday:
            updates.append("Cust_Birthday = %s")
            values.append(birthday)
        if gender is not None:  # Check if gender was set
            updates.append("Cust_Gender = %s")
            values.append(gender)

        if updates:
            try:
                cursor.execute(f"""
                    UPDATE cust SET {', '.join(updates)} WHERE CUST_Id = %s
                """, values + [customer_id])
                connection.commit()
                print("Customer modified successfully.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                connection.rollback()
        else:
            print("No updates made.")

    def delete_customer():
        customer_id = int(input("Enter the customer ID to delete: "))
        try:
            cursor.execute("""
                DELETE `order item` FROM `order item`
                JOIN `order` ON `order item`.Order_Id = `order`.Order_Id
                WHERE `order`.Cust_Id = %s
            """, (customer_id,))
            cursor.execute("DELETE FROM `order` WHERE Cust_Id = %s", (customer_id,))
            cursor.execute("DELETE FROM cust WHERE CUST_Id = %s", (customer_id,))

            if cursor.rowcount > 0:
                print("Customer and related orders deleted successfully.")
            else:
                print("Customer not found.")

            connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()

    def search_customer():
        search_term = input("Enter customer name to search: ")
        offset = 0
        limit = 100

        while True:

            cursor.execute("SELECT * FROM cust WHERE Cust_Name LIKE %s LIMIT %s OFFSET %s",
                           (f"%{search_term}%", limit, offset))
            results = cursor.fetchall()
            if not results:
                print("No customer records found.")
                break

            headers = ["CUST_Id", "Cust_Name", "Cust_City", "Cust_State", "Cust_State_Code", "Cust_Zip_Code",
                       "Cust_Country", "Cust_Continent", "Cust_Birthday", "Cust_Gender"]
            table = tabulate(results, headers, tablefmt="pipe")
            print(table)
            while True:
                more = input("Do you want to view the next 100 records? \n1. Yes\n2. No\n: ")
                if more == '1':
                    offset += 100
                    break
                elif more == '2':
                    return
                else:
                    print("Invalid input. Please enter 1 or 2.")

    def view_all_customers():
        total_records = count_total_records('cust')
        offset = 0
        records_fetched = 0
        order_by = "`Cust_Name`"

        while True:

            if offset == 0:
                print(
                    "1. Alphabetical\n"
                    "2. City\n"
                    "3. State\n"
                    "4. Country\n"
                    "5. Return to MAIN PAGE"
                )

                choice = input("Choose how you want to view the records: ")

                if choice == '1':
                    order_by = "`Cust_Name`"
                elif choice == '2':
                    order_by = "`Cust_City`"
                elif choice == '3':
                    order_by = "`Cust_State`"
                elif choice == '4':
                    order_by = "`Cust_Country`"
                elif choice == '5':
                    break
                else:
                    print("Invalid choice. Please try again.")
                    continue

            cursor.execute(f"SELECT * FROM cust ORDER BY {order_by} LIMIT 100 OFFSET %s", (offset,))
            results = cursor.fetchall()
            records_fetched += len(results)

            if not results:
                print("No more customer records.")
                break

            headers = ["CUST_Id", "Cust_Name", "Cust_City", "Cust_State", "Cust_State_Code", "Cust_Zip_Code",
                       "Cust_Country", "Cust_Continent", "Cust_Birthday", "Cust_Gender"]
            table = tabulate(results, headers, tablefmt="pipe")
            print(table)
            print(f"\n{records_fetched} records fetched out of {total_records} records.\n")
            while True:
                more = input("Do you want to view the next 100 records? \n1. Yes\n2. No\n: ")
                if more == '1':
                    offset += 100
                    break
                elif more == '2':
                    return
                else:
                    print("Invalid input. Please enter 1 or 2.")

    def manage_orders_menu():
        while True:
            print("\nManage Orders:")
            print("1. Modify Existing Order")
            print("2. Search Order")
            print("3. Delete Order")
            print("4. View All Orders")
            print("5. Back to Main Menu")

            choice = input("\nEnter your option (1-5): ")

            if choice == '1':
                modify_existing_order()
            elif choice == '2':
                search_order()
            elif choice == '3':
                delete_order()
            elif choice == '4':
                view_all_orders()
            elif choice == '5':
                break
            else:
                print("Invalid option.")

    def modify_existing_order():
        order_number = input("Enter the order number to modify: ")

        cursor.execute("SELECT * FROM `order` WHERE Order_Number = %s", (order_number,))
        order = cursor.fetchone()

        if not order:
            print("Order not found.")
            return

        store_id_input = input(f"Enter new store ID (current: {order[2]}): ")
        cust_id_input = input(f"Enter new customer ID (current: {order[3]}): ")
        delivery_date_input = input(f"Enter new delivery date (current: {order[4]}) (YYYY-MM-DD): ")
        order_date_input = input(f"Enter new order date (current: {order[5]}) (YYYY-MM-DD): ")

        store_id = store_id_input if store_id_input.strip() else order[2]
        cust_id = cust_id_input if cust_id_input.strip() else order[3]
        delivery_date = delivery_date_input if delivery_date_input.strip() else order[4]
        order_date = order_date_input if order_date_input.strip() else order[5]

        try:
            cursor.execute("""
                UPDATE `order`
                SET Store_Id = %s, CUST_Id = %s, Delivery_Date = %s, Order_Date = %s
                WHERE Order_Number = %s
            """, (store_id, cust_id, delivery_date, order_date, order_number))
            print("Order modified successfully.")
            connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    def search_order():
        search_term = input("Enter order ID to search: ").strip()
        try:
            cursor.execute(
                "SELECT Order_Id, Order_Number, Store_Id, CUST_Id, Delivery_Date, Order_Date FROM `order` WHERE Order_Id = %s",
                (search_term,))
            results = cursor.fetchall()
            if results:
                formatted_results = []
                for row in results:
                    formatted_row = list(row)
                    if isinstance(formatted_row[4], datetime.date):  # Delivery_Date
                        formatted_row[4] = formatted_row[4].strftime("%d/%m/%Y")
                    if isinstance(formatted_row[5], datetime.date):  # Order_Date
                        formatted_row[5] = formatted_row[5].strftime("%d/%m/%Y")
                    formatted_results.append(formatted_row)

                headers = ["Order ID", "Order Number", "Store ID", "Customer ID", "Delivery Date", "Order Date"]
                print(tabulate(formatted_results, headers=headers, tablefmt="grid"))
            else:
                print("No orders found.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def delete_order():
        order_id = input("Enter the order ID to delete: ").strip()
        try:

            cursor.execute("SELECT * FROM `order` WHERE Order_Id = %s", (order_id,))
            order = cursor.fetchone()

            if order:

                cursor.execute("DELETE FROM `order item` WHERE Order_Id = %s", (order_id,))
                order_item_deleted = cursor.rowcount

                cursor.execute("DELETE FROM `order` WHERE Order_Id = %s", (order_id,))
                order_deleted = cursor.rowcount

                if order_item_deleted > 0 and order_deleted > 0:
                    print("Order deleted successfully.")
                elif order_deleted > 0:
                    print("Order deleted successfully, but no related items found.")
                else:
                    print("Order not found.")
                connection.commit()
            else:
                print("Order not found.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()

    def view_all_orders():
        total_records = count_total_records('`order`')
        offset = 0
        records_fetched = 0
        order_by = "`Order_Date`"

        while True:

            if offset == 0:
                print(
                    "1. Order Date(Past to the Present)\n"
                    "2. Customer ID(Low to High)\n"
                    "3. Store ID(Low to High)\n"
                    "4. Return to MAIN PAGE"
                )

                choice = input("Choose how you want to view the records: ")

                if choice == '1':
                    order_by = "`Order_Date`"
                elif choice == '2':
                    order_by = "`Cust_Id`"
                elif choice == '3':
                    order_by = "`Store_Id`"
                elif choice == '4':
                    break
                else:
                    print("Invalid choice. Please try again.")
                    continue

            cursor.execute(f"SELECT * FROM `order` ORDER BY {order_by} LIMIT 100 OFFSET %s", (offset,))
            results = cursor.fetchall()
            records_fetched += len(results)

            if not results:
                print("No more orders.")
                break

            headers = ["Order_Id", "Order_Number", "Store_Id", "Cust_Id", "Delivery_Date", "Order_Date"]
            table = tabulate(results, headers, tablefmt="pipe")
            print(table)
            print(f"\n{records_fetched} records fetched out of {total_records} records.\n")
            while True:
                more = input("Do you want to view the next 100 records? \n1. Yes\n2. No\n: ")
                if more == '1':
                    offset += 100
                    break
                elif more == '2':
                    return
                else:
                    print("Invalid input. Please enter 1 or 2.")

    def manage_stores_menu(designation):
        while True:
            print("\nManage Stores:")
            print("1. Add New Store" if designation in ['Administrator', 'Manager'] else "1. Add New Store(No Access)")
            print("2. Search Store")
            print("3. View All Stores")
            print("4. Back to Main Menu")

            choice = input("\nEnter your option (1-4): ")

            if choice == '1' and designation in ['Administrator', 'Manager']:
                add_new_store()
            elif choice == '2':
                search_store()
            elif choice == '3':
                view_all_stores()
            elif choice == '4':
                break
            else:
                print("You are not authorized to access this. Please contact the admin")

    def add_new_store():
        store_square_meters = input("Enter store square meters: ").strip()
        if not store_square_meters:
            print("Store square meters cannot be blank. Please enter a valid value.")
            return

        location_choice = input(
            "Is this a new location or an existing location? \n1. New location\n2. Existing location\n: ").strip().lower()
        if location_choice == '1':
            country = input("Enter new country: ").strip()
            if not country:
                print("Country cannot be blank. Please enter a valid country.")
                return

            store_state = input("Enter new store state: ").strip()
            if not store_state:
                print("Store state cannot be blank. Please enter a valid store state.")
                return

            try:
                cursor.execute("""
                    INSERT INTO `store location` (Store_Country, Store_State) 
                    VALUES (%s, %s)
                """, (country, store_state))
                store_location_id = cursor.lastrowid
                print(f"New location added successfully. Location ID: {store_location_id}")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                return
        elif location_choice == '2':
            try:
                store_location_id = int(input("Enter existing store location ID: ").strip())
            except ValueError:
                print("Invalid location ID. Please enter a valid number.")
                return
        else:
            print("Invalid choice. Please enter 1 for new location or 2 for existing location.")
            return

        store_open_date = input("Enter store open date (YYYY-MM-DD): ").strip()
        try:
            year, month, day = map(int, store_open_date.split('-'))
            store_open_date = f"{year:04d}-{month:02d}-{day:02d}"
        except ValueError:
            print("Invalid date format. Please enter in YYYY-MM-DD format.")
            return

        try:
            cursor.execute("""
                INSERT INTO store (Store_Square_Meters, Store_Location_Id, Store_Open_Date) 
                VALUES (%s, %s, %s)
            """, (store_square_meters, store_location_id, store_open_date))
            connection.commit()
            print("Store added successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()

    import datetime
    def search_store():
        search_choice = input(
            "Do you want to search by store ID or store location ID? \n1. Store ID\n2. Store Location ID\n: ").strip()
        if search_choice not in ['1', '2']:
            print("Invalid choice. Please enter 1 for Store ID or 2 for Store Location ID.")
            return

        search_term = input("Enter the search term: ").strip()
        if not search_term:
            print("Search term cannot be blank. Please enter a valid search term.")
            return

        column = "Store_Id" if search_choice == '1' else "Store_Location_Id"

        try:
            cursor.execute(f"SELECT * FROM store WHERE {column} = %s", (search_term,))
            results = cursor.fetchall()
            if results:
                formatted_results = []
                for row in results:
                    formatted_row = list(row)
                    # Format the date if it's not None and is a date type
                    if isinstance(formatted_row[3], datetime.date):
                        formatted_row[3] = formatted_row[3].strftime("%d/%m/%Y")
                    formatted_results.append(formatted_row)

                headers = ["Store_Id", "Store_Square_Meters", "Store_Location_Id", "Store_Open_Date"]
                print(tabulate(formatted_results, headers=headers, tablefmt="pipe"))
            else:
                print("No store records found.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def view_all_stores():
        total_records = count_total_records('store')
        offset = 0
        records_fetched = 0
        order_by = "`Store_Square_Meters`"

        while True:

            if offset == 0:
                print(
                    "1. Square Meters(Low to High)\n"
                    "2. Location ID(Low to High)\n"
                    "3. Open Date(Past to the Present)\n"
                    "4. Return to MAIN PAGE"
                )

                choice = input("Choose how you want to view the records: ")

                if choice == '1':
                    order_by = "`Store_Square_Meters`"
                elif choice == '2':
                    order_by = "`Store_Location_Id`"
                elif choice == '3':
                    order_by = "`Store_Open_Date`"
                elif choice == '4':
                    break
                else:
                    print("Invalid choice. Please try again.")
                    continue

            cursor.execute(f"SELECT * FROM store ORDER BY {order_by} LIMIT 100 OFFSET %s", (offset,))
            results = cursor.fetchall()
            records_fetched += len(results)

            if not results:
                print("No more store records.")
                break

            headers = ["Store_Id", "Store_Square_Meters", "Store_Location_Id", "Store_Open_Date"]
            table = tabulate(results, headers, tablefmt="pipe")
            print(table)
            print(f"\n{records_fetched} records fetched out of {total_records} records.\n")
            while True:
                more = input("Do you want to view the next 100 records? \n1. Yes\n2. No\n: ")
                if more == '1':
                    offset += 100
                    break
                elif more == '2':
                    return
                else:
                    print("Invalid input. Please enter 1 or 2.")

    def administrative_matters_menu():
        print("\nAdministrative Matters:")
        print("\t1. Add New Account")
        print("\t2. Delete Account")
        print("\t3. Update Designation")
        print("\t4. Back to Main Menu")
        choice = input("\nEnter your option (1-4): ")
        return choice

    def add_account(is_admin_initialization=False):
        try:
            if is_admin_initialization:
                designation = 'Administrator'
                print("Creating initial Administrator account.")
            else:
                designation = None

            name = input("Enter Name: ")
            password = input("Enter Password: ")

            if not is_admin_initialization:
                print("\nChoose Designation:")
                print("1. Administrator")
                print("2. Manager")
                print("3. Staff")
                designation_choice = input("\nEnter your option (1-3): ")

                designations = {
                    '1': 'Administrator',
                    '2': 'Manager',
                    '3': 'Staff'
                }

                designation = designations.get(designation_choice, 'Staff')  # Default to 'Staff' if input is invalid

            salt = os.urandom(16).hex()
            hashed_password = hash_password(password, salt)

            sql_query = "INSERT INTO staff (Staff_name, Staff_hash, Staff_salt, Staff_designation) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql_query, (name, hashed_password, salt, designation))
            connection.commit()
            print("New account created successfully!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            print("An error occurred. Please try again.")

    def delete_account(current_username):
        try:
            staff_name = input("Enter Staff Name to delete: ")

            if staff_name == current_username:
                print("You cannot delete your own account while logged in.")
                return

            sql_query = "SELECT Staff_hash, Staff_salt, Staff_designation FROM staff WHERE Staff_name = %s"
            cursor.execute(sql_query, (staff_name,))
            result = cursor.fetchone()

            if result:
                password = input("Enter Password to confirm: ")
                hashed_password, salt, staff_role = result

                cursor.execute("SELECT Staff_designation FROM staff WHERE Staff_name = %s", (current_username,))
                current_user_role = cursor.fetchone()[0]

                if staff_role == 'Administrator' and current_user_role == 'Administrator':
                    print("You cannot delete another admin account.")
                    return

                if hash_password(password, salt) == hashed_password:
                    sql_query = "DELETE FROM staff WHERE Staff_name = %s"
                    cursor.execute(sql_query, (staff_name,))
                    connection.commit()
                    print("Account deleted successfully!")
                else:
                    print("Password incorrect. Account not deleted.")
            else:
                print("Staff name does not exist.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            print("An error occurred. Please try again.")

    def update_designation(current_username):
        try:
            staff_name = input("Enter Staff Name to update designation: ")

            if staff_name == current_username:
                print("You cannot update your own designation while logged in.")
                return

            sql_query = "SELECT Staff_designation FROM staff WHERE Staff_name = %s"
            cursor.execute(sql_query, (staff_name,))
            result = cursor.fetchone()

            if result:
                current_designation = result[0]
                if current_designation == 'Administrator':
                    print("You cannot update the designation of another Administrator.")
                    return

                print("\nChoose New Designation:")
                print("1. Administrator")
                print("2. Manager")
                print("3. Staff")
                designation_choice = input("\nEnter your option (1-3): ")

                designations = {
                    '1': 'Administrator',
                    '2': 'Manager',
                    '3': 'Staff'
                }

                new_designation = designations.get(designation_choice,
                                                   'Staff')  # Default to 'Staff' if input is invalid

                sql_query = "UPDATE staff SET Staff_designation = %s WHERE Staff_name = %s"
                cursor.execute(sql_query, (new_designation, staff_name))
                connection.commit()
                print("Designation updated successfully!")
            else:
                print("Staff name does not exist.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            print("An error occurred. Please try again.")

    def update_personal_details(current_username):
        try:
            while True:
                print("\nUpdate Personal Details:")
                print("1. Reset Password")
                print("2. Change Username")
                print("3. Back to Main Menu")
                choice = input("Enter your option (1-3): ")

                if choice == '1':
                    new_password = input("Enter new Password: ")
                    if not new_password:
                        print("Password cannot be blank. Please try again.")
                        continue

                    salt = os.urandom(16).hex()
                    hashed_password = hash_password(new_password, salt)
                    sql_query = "UPDATE staff SET Staff_hash = %s, Staff_salt = %s WHERE Staff_name = %s"
                    cursor.execute(sql_query, (hashed_password, salt, current_username))
                    connection.commit()
                    print("Password updated successfully!")

                elif choice == '2':
                    print("Please note that the Staff Name is case sensitive.")
                    new_name = input("Enter new Staff Name: ")
                    if not new_name:
                        print("Username cannot be blank. Please try again.")
                        continue

                    sql_query = "UPDATE staff SET Staff_name = %s WHERE Staff_name = %s"
                    cursor.execute(sql_query, (new_name, current_username))
                    connection.commit()
                    current_username = new_name  # Update current_username to the new name
                    print("Username updated successfully!")

                elif choice == '3':
                    break

                else:
                    print("Invalid choice. Please try again.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            print("An error occurred. Please try again.")

    login()

    # Close the connection when done
    connection.close()


# Call the login_system function to start the program
login_system()
