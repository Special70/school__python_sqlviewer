from standalone.global_vars import cursor, connection
from standalone.functions.exist_check import exist_check
from time import sleep
from os import system

def customer_login():
    while True:
        print("Enter \"BACK\" to go back")
        customer_name = input("Enter Customer Name [Firstname Lastname]: ")
        # back
        if customer_name.lower() == "back":
            return None

        login = exist_check("customers", "customer_name", customer_name)
        if login == 0:
            password = input("New user entry detected! Enter a password for this account (Enter \"BACK\" to cancel)\n> ")
            if password.lower() == "back":
                continue

            cursor.execute("insert into customers (customer_name, password) values (?, ?)", (customer_name,password,))
            connection.commit()
            print(f"Succesfully Registered {customer_name} in our list!")
        else:
            print("You are already a registered customer!")
            password = input("New user entry detected! Enter a password for this account (Enter \"BACK\" to cancel)\n> ")
            if password.lower() == "back":
                continue

            query = f"SELECT COUNT(*) FROM customers WHERE customer_name = ? and password = ?"
            cursor.execute(query, (customer_name, password))
            if not cursor.fetchone()[0]:
                print("Invalid password. Please try again")
                sleep(2)
                system('cls')
                continue
            else:
                print("Login Successful!")
            

        cursor.execute("select customer_id from customers where customer_name = ?", (customer_name,))
        customer_name = cursor.fetchone()[0]
        return customer_name

