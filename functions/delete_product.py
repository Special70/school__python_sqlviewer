import os,time
from standalone.functions.exist_check import exist_check
from standalone.functions.print_table import print_table
from standalone.global_vars import cursor, connection

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