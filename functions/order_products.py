
from standalone.global_vars import cursor, connection
from standalone.functions.print_table import print_table
from standalone.functions.exist_check import exist_check

def product_validator(product_id: str):
    query = f"select product_id, product_name, type_name, product_details, stock, price from (select * from products left join types using (type_id)) inner join inventory using (product_id) where stock > 0 and product_id = {product_id}"
    cursor.execute(query)
    return 1 if cursor.fetchone() else 0

def date_validator(input_arg: str):
    input = input_arg.split("-")
    if len(input) < 3:
        print("The format of your input is wrong. Please try again")
        return 0
    if int(input[0]) not in range(1970, 3001):
        print(int(input[0]))
        print("Invalid Year. Please try again.")
        return 0
    if int(input[1]) not in range(1, 13):
        print("Invalid Month. Please try again.")
        return 0
    if int(input[2]) not in range(1, 32):
        print("Invalid Day. Please try again.")
        return 0
    
    return 1

def quantity_validator(stock_input: str, product_id: str):
    query = f"select stock from (select * from products left join types using (type_id)) inner join inventory using (product_id) where stock > 0 and product_id = {product_id}"
    cursor.execute(query)
    result = cursor.fetchone()
    if result == None:
        return 0
    elif int(result[0]) < int(stock_input):
        return 0
    else:
        return 1

def employee_validator(emp_id: str):
    query = f"select * from employees where employee_id = {emp_id}"
    cursor.execute(query)
    result = cursor.fetchone()

    if result:
        return 1
    else:
        return 0

def order_products(customer_name):
    print_table("select product_id, product_name, type_name, product_details, stock, price from (select * from products left join types using (type_id)) inner join inventory using (product_id) where stock > 0")
    while True:
        date = input("\nEnter Date [YEAR-MONTH-DATE]: ")
        if date_validator(date):
            break
        input("Press Enter to Continue...\n")

    while True:
        product_id = int(input("Enter product_ID: "))
        if product_validator(product_id):
            break
        input("Press Enter to Continue...\n")


    while True:
        quantity = int(input("Enter Quantity: "))
        if quantity_validator(quantity, product_id):
            break
        input("Press Enter to Continue...\n")
    #adding to tables and computing total
    cursor.execute("select price from products where product_id = ?", (product_id,))
    query = cursor.fetchone()
    total = query[0] * quantity
    print_table("select * from employees")

    while True:
        employee_id = int(input("\nWhich Employee assisted you today: "))
        if employee_validator(employee_id):
            break
        input("Press Enter to Continue...\n")

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
