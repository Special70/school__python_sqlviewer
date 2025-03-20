import os, time
from standalone.functions.exist_check import exist_check
from standalone.functions.print_table import print_table
from standalone.global_vars import cursor, connection

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