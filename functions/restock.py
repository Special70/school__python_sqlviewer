import os,time
from standalone.functions.exist_check import exist_check
from standalone.functions.print_table import print_table
from standalone.global_vars import cursor, connection

def restock():
    print_table("select product_id, product_name, stock from inventory join products using (product_id)")
    while True:
        product_id = input("Enter Product ID: ")
        if exist_check('products', 'product_id', product_id) == 0:
                print(f"Product ID {product_id} is invalid.")
                input("\nPress Enter to Continue...\n")
                continue
        else:
            break
    while True:
        stock = input("Enter Stock: ")
        if stock == 0:
            print("ERROR | Invalid Input. Try again.")
            continue
        else:
            break
    cursor.execute("update inventory set stock = ? where product_id = ?", (stock, product_id,))
    connection.commit()
    cursor.execute("select product_name from products where product_id = ?", (product_id,))
    result = cursor.fetchone()[0]
    print(f"Succesfully restocked {result}!")