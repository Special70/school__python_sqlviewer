import os
import sys
import time # to see if program goes to where it should be. will be removed in the final code
import sqlite3
# import tkinter as tk
# from tkinter import ttk

connection = sqlite3.connect("hardwareDB.db")
cursor = connection.cursor()

os.system('cls')

choice_list = [0,1,2,3,4] #stores the menu choices

def check(choice_list): #for checking if input is valid
    while True:
        try:
            a = int(input("Enter Choice: "))
            while a not in choice_list:
                print(f"ERROR | {a} is invalid. Try again!") 
                a = int(input("Enter Choice: "))
        except ValueError:
            print("ERROR | Please enter a number.")
            continue
        return a
    
def exiting (num):
    if num == 1:
        print("Thank you for using the program. Exiting...")
        time.sleep(2.5)
        sys.exit()
    else:
        print("Returning to Previous Menu...")
        time.sleep(2.5)

def print_table(table_query: str):
    """
    Enter the select query for the first argument. NO SEMICOLON SYMBOLS
    """

    # checks if table is empty
    query = cursor.execute(table_query)
    if len(list(query)) == 0:
        print("There's nothing to show.")

    query = cursor.execute(table_query)
    col_list = [desc[0] for desc in query.description] #removed the [:1] cuz it removes the emp_id and etc

    # get the max length of each column for proper printing
    col_ljust_vals = []
    for col in range(len(col_list)):
        query_to_perform = f'SELECT MAX(LENGTH("{col_list[col]}")) FROM ({table_query})'
        max_char_length = cursor.execute(query_to_perform).fetchone()[0]
        col_ljust_vals.append(
            max_char_length
            if (max_char_length if max_char_length != None else 0) > len(col_list[col])
            else len(col_list[col])
    )

    # create a horizontal line to separate the columns and rows
    print("_",end="")
    for i in range(len(col_list)):
        print(str("_")*(col_ljust_vals[i]+2)+"_", end="")
    print()

    # print the columns in the first row
    print("|",end="")
    for i in range(len(col_list)):
        print(
            str(col_list[i])
            .replace("_"," ")
            .ljust(col_ljust_vals[i]+2)
            .title()
            +"|"
            , end=""
        )
    print()

    # create a horizontal line to separate the columns and rows
    print("|",end="")
    for i in range(len(col_list)):
        print(str("_")*(col_ljust_vals[i]+2)+"|", end="")
    print()
    
    # print the rows properly now
    query = cursor.execute(table_query)
    for row in query:
        print("|",end="")
        for i in range(len(col_list)):
            print(
                str(row[i])
                .replace("_"," ")
                .ljust(col_ljust_vals[i]+2)
                .title()
                +"|"
                , end=""
            )
        print()
    
    # create a horizontal line to separate the columns and rows
    print("|",end="")
    for i in range(len(col_list)):
        print(str("_")*(col_ljust_vals[i]+2)+"|", end="")
    print()

def exist_data(table, table_column, data):  #checks if one data exists in a table, usually if supplier_id is in table or if employee_id in table
    query = f"SELECT COUNT(*) FROM {table} WHERE {table_column} = ?"
    cursor.execute(query, (data,))
    return 1 if cursor.fetchone()[0] else 0

    
def add_product ():
    os.system('cls')
    print_table("select * from suppliers")
    while True:
        product_name = input("\nEnter Product Name: ")
        check = exist_data("products", "product_name", product_name)
        if check == 1:
            print(f"{product_name} already exists. Try again.\n")
            time.sleep(2.5)
            continue
        else:
            break
    while True:
        supplier_id = int(input("Enter Supplier ID: "))
        if supplier_id < 1:
            print(f"{supplier_id} is invalid.")
            continue
        check = exist_data("suppliers", "supplier_id", supplier_id)
        if check == 0:
            continue
        else: 
            break
    product_dsc = input("Enter Product Description: ")
    print_table("select distinct type_id, type_name from types")
    while True:
        type_id = int(input("Enter Product Type ID: "))
        if type_id not in [1, 2, 3]:
            print(f"{type_id} is invalid.")
            continue
        else: 
            break
    product_price = input("Enter Product Price: ")
    product_stock = input("Enter Product Stock: ")
    #for adding into products
    cursor.execute("insert into products (product_name, supplier_id, product_details, type_id, price) values (?, ?, ?, ?, ?)", (product_name, supplier_id, product_dsc, type_id, product_price))
    cursor.execute("select product_id from products where product_name = ?", (product_name,))
    product_id = cursor.fetchone()[0]
    #for adding into inventory
    cursor.execute("insert into inventory (product_id, stock) values (?, ?)", (product_id, product_stock))
    print_table("select * from inventory")
    connection.commit()
    
def order_products():
    print_table("select * from products join inventory using (product_id) where stock > 0")
    date = input("\nEnter Date [YEAR-MONTH-DATE]: ")
    while True:
        product_id = int(input("Enter product_ID: "))
        check = exist_data("products", "product_id", product_id)
        if check == 0:
            print(f"{product_id} is invalid. Try again.\n")
            time.sleep(2.5)
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
    time.sleep(2.5)

def add_emp ():
    print("Add Employee Records")
    while True:
        emp_name = input("Enter Employee Name: ")
        check = exist_data("employees", "employee_name", emp_name)
        if check == 1:
            print(f"{emp_name} already exists. Try again.")
            continue
        else:
            break
    cursor.execute("insert into employees (employee_name) values (?)", (emp_name,))
    result = cursor.lastrowid
    print(f"{emp_name} has been registered with the Employee ID of {result}")
    connection.commit()

def add_supp ():
    print("Add Supplier Records")
    while True:
        supp_name = input("Enter Supplier Name: ")
        check = exist_data("suppliers", "supplier_name", supp_name)
        if check == 1:
            print(f"{supp_name} already exists. Try again.")
            continue
        else:
            break
    cursor.execute("insert into suppliers (supplier_name) values (?)", (supp_name,))
    result = cursor.lastrowid
    print(f"{supp_name} has been registered with the Employee ID of {result}")
    connection.commit()


print("Welcome to Joe MV Enterprise!\n\t[1] Start the Program\n\t[0] Terminate the Program")
choice = check(choice_list[:2])


#main program
while True:
    if choice == 1:
        os.system('cls')
        print("Please enter entity type:\n\t[1] Customer\n\t[2] Employee\n\t[0] Exit the Program")
        entity_type = check(choice_list[:3])
        if entity_type == 1: #if user is a customer
            customer_name = input("Enter Customer Name [Firstname Lastname]: ")
            login = exist_data("customers", "customer_name", customer_name)
            if login == 0:
                cursor.execute("insert into customers (customer_name) values (?)", (customer_name,))
                connection.commit()
                print(f"Succesfully Registered {customer_name} in our list!")
                time.sleep(2.5)
            else:
                print("You are already a registered customer! Proceeding...")
                time.sleep(2.5)
            cursor.execute("select customer_id from customers where customer_name = ?", (customer_name,))
            customer_name = cursor.fetchone()
            customer_name = customer_name[0]
        if entity_type == 1:
            while True:
                os.system('cls')
                print("CUSTOMER MAIN MENU\n\t[1] View Business Details\n\t[2] View Available Products\n\t[3] Purchase Product\n\t[0] Exit the Program")
                customer_choice = check(choice_list[:4])
                match customer_choice:
                    case 1:
                        print("Welcome to Joe MV Enterprise! We are a family owned business that provides a wide range of hardware, ranging from electronic hardwares to manual equipment. We have been in the business for 50 years, and have built a reputable legacy.")
                        #this is a description of the business. may edit
                        time.sleep(2.5) 
                    case 2:
                        print("display all products")
                        print_table("select * from products")
                        time.sleep(2.5)
                    case 3:
                        order_products()
                    case _:
                        exiting(1)
        elif entity_type == 2: #if user is an employee
            # while True: #for security / confirm if they are employee
            #print("Enter Employee ID: ")
            #condition if employee id not in employee table, return to previous menu which is customer or employee ba sya
            #if employee id in employee table, then this:
            while True:
                os.system('cls')
                print("EMPLOYEE MAIN MENU\n\t[1] Configure Database \n\t[2] View Inventory\n\t[3] View Records\n\t[4] View Purchases List\n\t[0] Exit the Program")
                employee_choice = check(choice_list)
                match employee_choice:
                    case 1: #choice 2 1
                        while True:
                            #this opens a submenu
                            os.system('cls')
                            print("CONFIGURE DATABASE\n\t[1] Configure Product\n\t[2] Configure People Data\n\t[0] Return to Previous Menu")
                            update_choice = check(choice_list[:3])
                            match update_choice:
                                case 1: # choice 2 1 1
                                    while True:
                                        os.system('cls')
                                        print("CONFIGURE PRODUCT\n\t[1] Add Product\n\t[2] Update Product\n\t[3] Delete Product\n\t[0] Return to Previous Menu")
                                        config_prod = check(choice_list[:4])
                                        match config_prod:
                                            case 1: # choice 2 1 1 1
                                                add_product()
                                                time.sleep(2.5)
                                            case 2: # choice 2 1 1 2
                                                print("Update Product")
                                                time.sleep(2)
                                            case 3: # choice 2 1 1 3
                                                print("Delete product")
                                                time.sleep(2)
                                            case _:
                                                exiting(0)
                                                break
                                case 2: # choice 2 1 2
                                    os.system('cls')
                                    print("CONFIGURE PEOPLE DATA\n\t[1] Add People Data\n\t[2] Update People Data\n\t[3] Delete People Data\n\t[0] Return to Previous Menu")
                                    config_ppl = check(choice_list[:3])
                                    match config_ppl:
                                        case 1: # choice 2 1 2 1
                                            while True:
                                                os.system('cls')
                                                print("ADD PEOPLE DATA")
                                                print("\t[1] Employee Records\n\t[2] Supplier Records\n\t[0] Return to Previous Menu")
                                                config_ppl = check(choice_list[:3])
                                                match config_ppl: #just ask for input, no need to display table
                                                    case 1: # choice 2 1 2 1 1
                                                        add_emp()
                                                        time.sleep(2)
                                                    case 2: # choice 2 1 2 1 2
                                                        add_supp()
                                                        time.sleep(2)
                                                    case _:
                                                        exiting(0)
                                                        break
                                        case 2: # choice 2 1 2 2
                                            while True:
                                                os.system('cls')
                                                print("UPDATE PEOPLE DATA")
                                                print("\t[1] Employee Records\n\t[2] Customer Records\n\t[3] Employee Records\n\t[0] Return to Previous Menu")
                                                config_ppl = check(choice_list[:4])
                                                match config_ppl: #just ask for input, no need to display table
                                                    case 1:
                                                        print("Update Employee Records")
                                                        time.sleep(2)
                                                    case 2:
                                                        print("Update Customer Records")
                                                        time.sleep(2)
                                                    case 2:
                                                        print("Update Supplier Records")
                                                        time.sleep(2)
                                                    case _:
                                                        exiting(0)
                                                        break
                                        case 3: # choice 2 1 2 3
                                            while True:
                                                os.system('cls')
                                                print("DELETE PEOPLE DATA")
                                                print("\t[1] Employee Records\n\t[2] Customer Records\n\t[3] Employee Records\n\t[0] Return to Previous Menu")
                                                config_ppl = check(choice_list[:4])
                                                match config_ppl: #just ask for input, no need to display table
                                                    case 1: # choice 2 1 2 3 1
                                                        print("Delete Employee Records")
                                                        time.sleep(2)
                                                    case 2: # choice 2 1 2 3 2
                                                        print("Delete Customer Records")
                                                        time.sleep(2)
                                                    case 2: # choice 2 1 2 3 3
                                                        print("Delete Supplier Records")
                                                        time.sleep(2)
                                                    case _:
                                                        exiting(0)
                                                        break
                                        case _:
                                            exiting(0)
                                            break
                                case _:
                                    exiting(0)
                                    break
                    case 2: # choice 2 2
                        #this opens a submenu
                        while True:
                            os.system('cls')
                            print("VIEW INVENTORY\n\t[1] View Product List\n\t[2] View Inventory Stock\n\t[3] View Supplier List\n\t[0] Return to Main Menu")
                            inv_choice = check(choice_list[:4])
                            match inv_choice:
                                case 1: # choice 2 2 1
                                    #this prints all available products
                                    print("Display all Products")
                                    print_table("select * from products")
                                    time.sleep(2.5)
                                case 2: # choice 2 2 2
                                    while True:
                                        #this opens another submenu
                                        os.system('cls')
                                        print("INVENTORY STOCK\n\t[1] View Inventory Summary\n\t[2] View Products In-Stock\n\t[3] View Products Out-of-Stock\n\t[0] Return to Previous Menu")
                                        stock_choice = check(choice_list[:4])
                                        match stock_choice:
                                            case 1: # choice 2 2 2 1
                                                print("Display All Inventory")
                                                print_table("select product_id, product_name, stock, product_details, type_id, price from inventory left join products using(product_id)", )
                                                time.sleep(2.5)
                                            case 2: # choice 2 2 2 2
                                                print("Display Products In-Stock")
                                                print_table("select product_id, product_name, stock, product_details, type_id, price from inventory left join products using(product_id) where stock > 0")
                                                time.sleep(2.5)
                                            case 3: # choice 2 2 2 3
                                                print_table("select product_id, product_name, stock, product_details, type_id, price from inventory left join products using(product_id) where stock == 0")
                                                time.sleep(2.5)
                                            case _:
                                                exiting(0)
                                                break
                                case 3: # choice 2 2 3
                                    print_table("select * from supliers")
                                    print("Display Suppliers")
                                    time.sleep(2.5)
                                case _:
                                    exiting(0)
                                    break
                    case 3: # choice 2 3
                        #this opens a submenu
                        while True:
                            os.system('cls')
                            print("VIEW RECORDS\n\t[1] Customer Records\n\t[2] Employee Records\n\t[3] Supplier Records\n\t[0] Return to Previous Menu")
                            records_choice = check(choice_list[:4])
                            match records_choice:
                                case 1: # choice 2 3 1
                                    print_table("select * from customers")
                                    time.sleep(2.5)
                                case 2: # choice 2 3 2
                                    print_table("select * from employees")
                                    time.sleep(2.5)
                                case 3:
                                    print_table("select * from suppliers")
                                    time.sleep(2.5)
                                case _:
                                    exiting(0)
                                    break
                    case 4: # choice 2 4
                        #prints all rows from orders table
                        #user inputs an order_id
                        #displays the corresponding transaction and order_details row.
                        print("View Purchase List")
                        print_table("select * from orders ord join transactions tr on ord.transaction_id = tr.transaction_id join order_details od on ord.order_id = od.order_id")
                        time.sleep(2.5)
                    case _:
                        exiting(1)
        
    else:
        exiting(1)