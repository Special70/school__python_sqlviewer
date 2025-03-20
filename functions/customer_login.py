from standalone.global_vars import cursor, connection
from standalone.functions.exist_check import exist_check

def customer_login():
    customer_name = input("Enter Customer Name [Firstname Lastname]: ")
    login = exist_check("customers", "customer_name", customer_name)
    if login == 0:
        cursor.execute("insert into customers (customer_name) values (?)", (customer_name,))
        connection.commit()
        print(f"Succesfully Registered {customer_name} in our list!")
    else:
        print("You are already a registered customer! Proceeding...")
    cursor.execute("select customer_id from customers where customer_name = ?", (customer_name,))
    customer_name = cursor.fetchone()[0]
    return customer_name