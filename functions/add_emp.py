from standalone.global_vars import cursor, connection
from standalone.functions.exist_check import exist_check
from time import sleep

def add_emp ():
    print("Add Employee Records")
    while True:
        emp_name = input("Enter Employee Name (Type \"BACK\" to cancel): ")
        if emp_name.lower() == "back":
            return 0
        check = exist_check("employees", "employee_name", emp_name)
        if check == 1:
            print(f"{emp_name} already exists. Try again.")
            input("\nPress Enter to Continue...\n")
            continue
        else:
            break
    while True:
        emp_password = input("Enter Employee Password (Type \"BACK\" to cancel): ")
        if emp_password.lower() == "back":
            return 0
        if len(emp_password) == 0:
            print("Invalid input. Please try again.")
            sleep(1)
            continue

        break

    cursor.execute("insert into employees (employee_name, password) values (?, ?)", (emp_name,emp_password,))
    result = cursor.lastrowid
    print(f"{emp_name} has been registered with the Employee ID of {result}")
    connection.commit()
