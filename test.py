from dateutil import parser
from datetime import datetime
order_number = input("Enter order number: ")
store_id = input("Enter store ID: ")
cust_id = input("Enter customer ID: ")
today = datetime.today().date()
while True:
        try:
            order_date_str = input("Enter order date (YYYY-MM-DD): ")
            delivery_date_str = input("Enter delivery date (YYYY-MM-DD): ")

            # 使用 dateutil 解析日期
            order_date = parser.parse(order_date_str).date()
            delivery_date = parser.parse(delivery_date_str).date()

            # 检查 delivery_date 和 order_date 的顺序
            if delivery_date < order_date:
                print("Error: Delivery date cannot be earlier than order date.")
                continue

            # 检查 order_date 不能是今天或以后的日期
            if order_date > today:
                print("Error: Order date cannot be a future date.")
                continue

            break
        except ValueError:
            print("Error: Invalid date format. Please use YYYY-MM-DD.")