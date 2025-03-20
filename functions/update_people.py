
import os, time
from standalone.functions.print_table import print_table
from standalone.functions.exist_check import exist_check
from standalone.global_vars import cursor, connection

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