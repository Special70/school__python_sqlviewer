
from standalone.global_vars import cursor, connection
from standalone.functions.print_table import print_table
from standalone.functions.exist_check import exist_check


def order_products():
    print_table("select * from products join inventory using (product_id) where stock > 0")
    date = input("\nEnter Date [YEAR-MONTH-DATE]: ")
    while True:
        product_id = int(input("Enter product_ID: "))
        if exist_check("products", "product_id", product_id) == 0:
            print(f"{product_id} is invalid. Try again.\n")
            input("\nPress Enter to Continue...\n")
            continue
        else:
            break
    quantity = int(input("Enter Quantity: "))
    #adding to tables and computing total
    cursor.execute("select price from products where product_id = ?", (product_id,))
    query = cursor.fetchone()
    total = query[0] * quantity
    print_table("select * from employees")
    employee_id = int(input("\nWhich Employee assisted you today: "))
    cursor.execute("insert into transactions (customer_id, transaction_date, total) values (?, ?, ?)", (customer_name, date, total,))
    transaction_id = cursor.lastrowid
    cursor.execute("insert into orders (transaction_id, employee_id) values (?, ?)", (transaction_id, employee_id,))
    order_id = cursor.lastrowid
    cursor.execute("insert into order_details (order_id, product_id, quantity) values (?, ?, ?)", (order_id, product_id, quantity,))
    cursor.execute("update inventory set stock = stock - ? where product_id = ? ", (quantity, product_id,))
    connection.commit()
    print("Succesfully Ordered!")
    cursor.execute("select product_name from products where product_id = ?", (product_id,))
    result = cursor.fetchone()[0]
    print(f"ORDER SUMMARY:\n\tProduct: {result}\n\tQuantity: {quantity}\n--------------------------------------\n\tTotal: {total}")
    input("\nPress Enter to Continue...\n")
