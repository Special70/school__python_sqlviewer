import os, time
from standalone.functions.print_table import print_table
from standalone.functions.exist_check import exist_check
from standalone.global_vars import cursor, connection

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