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

    
def add_product ():
    while True:
        try:
            os.system('cls')
            print_table("select * from suppliers")
            while True:
                product_name = input("\nEnter Product Name: ")
                if exist_check("products", "product_name", product_name) == 1:
                    print(f"{product_name} already exists. Try again.\n")
                    input("\nPress Enter to Continue...\n")
                    continue
                else:
                    break
            while True:
                    supplier_id = int(input("Enter Supplier ID: "))
                    if supplier_id < 1 or exist_check("suppliers", "supplier_id", supplier_id) == 0:
                        print(f"{supplier_id} is invalid.")
                        input("\nPress Enter to Continue...\n")
                        continue
                    else:
                        break
                    
            product_dsc = input("Enter Product Description: ")
            print_table("select distinct type_id, type_name from types")
            while True:
                type_id = int(input("Enter Product Type ID: "))
                if type_id not in [1, 2, 3]:
                    print(f"{type_id} is invalid.")
                    input("\nPress Enter to Continue...\n")
                    continue
                else:
                    break
            product_price = int(input("Enter Product Price: "))
            product_stock = int(input("Enter Product Stock: "))
            break
        except ValueError:
            print("ERROR | Invalid Input.")
            input("\nPress Enter to Continue...\n")
            continue
            
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

def add_emp ():
    print("Add Employee Records")
    while True:
        emp_name = input("Enter Employee Name: ")
        check = exist_check("employees", "employee_name", emp_name)
        if check == 1:
            print(f"{emp_name} already exists. Try again.")
            input("\nPress Enter to Continue...\n")
            continue
        else:
            break
    cursor.execute("insert into employees (employee_name) values (?)", (emp_name,))
    result = cursor.lastrowid
    print(f"{emp_name} has been registered with the Employee ID of {result}")
    connection.commit()

def add_supp ():
    print("Add Supplier Records:\n")
    while True:
        supp_name = input("Enter Supplier Name: ")
        check = exist_check("suppliers", "supplier_name", supp_name)
        if check == 1:
            print(f"{supp_name} already exists. Try again.")
            input("\nPress Enter to Continue...\n")
            continue
        else:
            break
    cursor.execute("insert into suppliers (supplier_name) values (?)", (supp_name,))
    result = cursor.lastrowid
    print(f"{supp_name} has been registered with the Employee ID of {result}")
    connection.commit()
    
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

def exist_check(table, table_column, data):  #checks if one data exists in a table, usually if supplier_id is in table or if employee_id in table
    query = f"SELECT COUNT(*) FROM {table} WHERE {table_column} = ?"
    cursor.execute(query, (data,))
    return 1 if cursor.fetchone()[0] else 0
    
def delete_product():

    while True:
        os.system('cls')
        print_table('select * from products') #display for deletion selection
        product_id = input("Enter Product ID [000 to Cancel]: ")

        if product_id == '000':
            print("Deletion of Product is Cancelled.")
            input("\nPress Enter to Continue...\n")
            break
        
        elif exist_check('products', 'product_id', product_id) == 0:
            print(f"Product ID {product_id} is invalid.")
            input("\nPress Enter to Continue...\n")
            continue
        
        else:
            confirmation = input("Are you sure? [YES/NO]: ")
            if confirmation[0].upper() == 'Y':
                cursor.execute("Select product_name from products where product_id = ?", (product_id,))
                product_name = cursor.fetchone()[0]
                cursor.execute('delete from products where product_id = ?', (product_id,))
                print(f"Product {product_name} has been succesfully deleted.")
                connection.commit()
                time.sleep(1.5)
                print("\nDisplaying Updated Product List:")
                print_table('select * from products')
                break
            else:
                print(f"Deletion of Product {product_name} is Cancelled.")
                break    

def update_product():
    os.system('cls')
    print_table('select * from products')
    
    while True:
        product_id = input("Enter Product ID to Edit [000 to Cancel]: ")
        
        if product_id == '000':
            print("Editing Product is Cancelled.")
            time.sleep(1.5)
            break
        
        elif exist_check('products', 'product_id', product_id) == 0:
            print(f"Product ID {product_id} is invalid.")
            input("\nPress Enter to Continue...\n")
            continue
        
        else:
            print("Enter New Product Details:")
            
            product_name = input("Enter Product Name: ")
            
            print_table('select * from suppliers')
                
            while True:
                supplier_id = input("Enter Supplier ID: ")
                if supplier_id < '1' or exist_check('suppliers', 'supplier_id', supplier_id) == 0:
                    print(f"{supplier_id} is invalid.")
                    input("\nPress Enter to Continue...\n")
                    continue
                else: 
                    break
                
            product_dsc = input("\nEnter Product Description: ")
            print_table("select distinct type_id, type_name from types")
            
            while True:
                type_id = int(input("Enter Product Type ID: "))
                if type_id not in [1, 2, 3]:
                    print(f"{type_id} is invalid.")
                    input("\nPress Enter to Continue...\n")
                    continue
                else: 
                    break
        
            product_price = input("\nEnter Product Price: ")
            product_stock = input("\nEnter Product Stock: ")
            
            cursor.execute('update products set product_name = ?, supplier_id = ?, product_details = ?, type_id = ?, price = ? where product_id = ?',(product_name, supplier_id, product_dsc, type_id, product_price, product_id))
            cursor.execute("select product_id from products where product_name = ?", (product_name,))
            product_id = cursor.fetchone()[0]
            #for adding into inventory
            cursor.execute('update inventory set product_id = ?, stock = ? where product_id = ?', (product_id, product_stock, product_id))
            connection.commit()
            
            print("Product Succesfully Updated!")
            time.sleep(1)
            print("\nDisplaying Updated Products Table:")
            print_table("select * from inventory")
            break

def update_people(table_name):
    os.system('cls')
    print_table(f'select * from {table_name}')
    if table_name == 'employees':
        col_id = 'employee_id'
        col_name = 'employee_name'
        
    elif table_name == 'customers':
        col_id = 'customer_id'
        col_name = 'customer_name'
    else:
        col_id = 'supplier_id'
        col_name = 'supplier_name'
        
    while True:
        id_input = input(f"Enter ID to Edit [000 to Cancel]: ")
        
        if id_input == '000':
            print(f"{table_name.capitalize()} Editing is Cancelled.")
            time.sleep(1)
            break
        

        elif exist_check(table_name, col_id, id_input) == 0:
            print(f"ID {id_input} is Invalid.")
            input("\nPress Enter to Continue...\n")
            continue
        else:
            name = input("\nEnter New Name: ").capitalize()
            cursor.execute(f'select count(*) from {table_name} where {col_name} LIKE ?', ('%' + name + '%',))
        
            if cursor.fetchone()[0] == 1:
                print(f"Name: {name} is the same.")
                input("\nPress Enter to Continue...\n")
                continue
            
            else: 
                cursor.execute(f'update {table_name} set {col_name} = ? where {col_id}= ?', (name, id_input))
                connection.commit()
                print(f"\n{table_name.capitalize()} Record Successfully Updated!\n\nDisplaying Updated {table_name.capitalize()} List:")
                print_table(f'select * from {table_name}')
                break
            
def delete_people(table_name):
    os.system('cls')
    print_table(f'select * from {table_name}')
    if table_name == 'employees':
        col_id = 'employee_id'
        
    elif table_name == 'customers':
        col_id = 'customer_id'
        
    else:
        col_id = 'supplier_id'
    
    while True:
        id_input = input("Enter ID to be Deleted [000 to Cancel]: ")
        
        if id_input == '000':
            print(f"{table_name.capitalize()} Deletion is Cancelled.")
            time.sleep(1)
            break

        elif exist_check(table_name, col_id, id_input) == 0:
            print(f"ID {id_input} is Invalid.")
            input("\nPress Enter to Continue...\n")
            continue
        
        else:
            confirmation = input("Are you sure? [YES/NO]: ")
            if confirmation[0].upper() == 'Y':
                cursor.execute(f'delete from {table_name} where {col_id} = ?', (id_input,))
                connection.commit()
                print(f"\nData Successfully Deleted!\n")
                
                time.sleep(1.5)
                
                print(f"\nDisplaying Updated {table_name.capitalize()} List:")
                print_table(f'select * from {table_name}')
                break
            else:
                print(f"{table_name.capitalize()} Deletion is Cancelled.")
                break    
        

print("Welcome to Joe MV Enterprise!\n\t[1] Start the Program\n\t[0] Terminate the Program")
choice = check(choice_list[:2])


#main program
while True:
    if choice == 1:
        os.system('cls')
        print("Please enter entity type:\n\t[1] Customer\n\t[2] Employee\n\t[0] Exit the Program")
        entity_type = check(choice_list[:3])
        if entity_type == 1: #if user is a customer
            customer_name = customer_login()
            time.sleep(2.5)
        if entity_type == 1:
            while True:
                os.system('cls')
                print("CUSTOMER MAIN MENU\n\t[1] View Business Details\n\t[2] View Available Products\n\t[3] Purchase Product\n\t[0] Exit the Program")
                customer_choice = check(choice_list[:4])
                match customer_choice:
                    case 1:
                        print("Welcome to Joe MV Enterprise! We are a family owned business that provides a wide range of hardware, ranging from electronic hardwares to manual equipment. We have been in the business for 50 years, and have built a reputable legacy.")
                        #this is a description of the business. may edit
                        input("\nPress Enter to Continue...")
                    case 2:
                        print("display all products")
                        print_table("select * from products")
                        input("\nPress Enter to Continue...")
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
                                                input("\nPress Enter to Continue...")
                                            case 2: # choice 2 1 1 2
                                                update_product()
                                                input("\nPress Enter to Continue...")
                                            case 3: # choice 2 1 1 3
                                                delete_product()
                                                input("\nPress Enter to Continue...")
                                            case _:
                                                exiting(0)
                                                break
                                case 2: # choice 2 1 2
                                    os.system('cls')
                                    print("CONFIGURE PEOPLE DATA\n\t[1] Add People Data\n\t[2] Update People Data\n\t[3] Delete People Data\n\t[0] Return to Previous Menu")
                                    config_ppl = check(choice_list[:4])
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
                                                        input("\nPress Enter to Continue...")
                                                    case 2: # choice 2 1 2 1 2
                                                        add_supp()
                                                        input("\nPress Enter to Continue...")
                                                    case _:
                                                        exiting(0)
                                                        break
                                        case 2: # choice 2 1 2 2
                                            while True:
                                                os.system('cls')
                                                print("UPDATE PEOPLE DATA")
                                                print("\t[1] Employee Records\n\t[2] Customer Records\n\t[3] Supplier Records\n\t[0] Return to Previous Menu")
                                                config_ppl = check(choice_list[:4])
                                                match config_ppl: #just ask for input, no need to display table
                                                    case 1:
                                                        update_people('employees')
                                                        input("\nPress Enter to Continue...")
                                                    case 2:
                                                        update_people('customers')
                                                        input("\nPress Enter to Continue...")
                                                    case 3:
                                                        update_people('suppliers')
                                                        input("\nPress Enter to Continue...")
                                                    case _:
                                                        exiting(0)
                                                        break
                                        case 3: # choice 2 1 2 3
                                            while True:
                                                os.system('cls')
                                                print("DELETE PEOPLE DATA")
                                                print("\t[1] Employee Records\n\t[2] Customer Records\n\t[3] Supplier Records\n\t[0] Return to Previous Menu")
                                                config_ppl = check(choice_list[:4])
                                                match config_ppl: #just ask for input, no need to display table
                                                    case 1: # choice 2 1 2 3 1
                                                        delete_people('employees')
                                                        input("\nPress Enter to Continue...")
                                                    case 2: # choice 2 1 2 3 2
                                                        delete_people('customers')
                                                        input("\nPress Enter to Continue...")
                                                    case 3: # choice 2 1 2 3 3
                                                        delete_people('suppliers')
                                                        input("\nPress Enter to Continue...")
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
                                    input("\nPress Enter to Continue...")
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
                                                input("\nPress Enter to Continue...")
                                            case 2: # choice 2 2 2 2
                                                print("Display Products In-Stock")
                                                print_table("select product_id, product_name, stock, product_details, type_id, price from inventory left join products using(product_id) where stock > 0")
                                                input("\nPress Enter to Continue...")
                                            case 3: # choice 2 2 2 3
                                                print_table("select product_id, product_name, stock, product_details, type_id, price from inventory left join products using(product_id) where stock == 0")
                                                input("\nPress Enter to Continue...")
                                            case _:
                                                exiting(0)
                                                break
                                case 3: # choice 2 2 3
                                    print_table("select * from supliers")
                                    print("Display Suppliers")
                                    input("\nPress Enter to Continue...")
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
                                    input("\nPress Enter to Continue...")
                                case 2: # choice 2 3 2
                                    print_table("select * from employees")
                                    input("\nPress Enter to Continue...")
                                case 3:
                                    print_table("select * from suppliers")
                                    input("\nPress Enter to Continue...")
                                case _:
                                    exiting(0)
                                    break
                    case 4: # choice 2 4
                        #prints all rows from orders table
                        #user inputs an order_id
                        #displays the corresponding transaction and order_details row.
                        print("View Purchase List")
                        print_table("select * from orders ord join transactions tr on ord.transaction_id = tr.transaction_id join order_details od on ord.order_id = od.order_id")
                        input("\nPress Enter to Continue...")
                    case _:
                        exiting(1)
        
    else:
        exiting(1)