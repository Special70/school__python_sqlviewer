import os, time

from standalone.global_vars import cursor, connection
from standalone.functions.exist_check import exist_check
from standalone.functions.print_table import print_table

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