from standalone.global_vars import cursor, connection
from standalone.functions.exist_check import exist_check

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
