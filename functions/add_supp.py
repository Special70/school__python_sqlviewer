from standalone.global_vars import cursor, connection
from standalone.functions.exist_check import exist_check

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