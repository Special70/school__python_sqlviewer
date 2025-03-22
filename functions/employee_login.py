from standalone.global_vars import cursor, connection
from standalone.functions.exist_check import exist_check
from functions.exiting import exiting
import time

def employee_login():
    employee_name = input("Enter Employee Name [Firstname Lastname]: ")
    login = exist_check("employees", "employee_name", employee_name)
    if login == 0:
        print(f"{employee_name} is not a registered employee. Exiting the system per protocol.\n")
        exiting(1)
        
    else:
        password = input("Password : ")

        query = f"SELECT COUNT(*) FROM employees WHERE employee_name = ? and password = ?"
        cursor.execute(query, (employee_name, password))
        if not cursor.fetchone()[0]:
            print(f"Invalid username/password. Exiting the system per protocol.\n")
            exiting(1)
        else:
            print("Login Successful!")
        print(f"Logging in as {employee_name}..")
        time.sleep(2.5)
    cursor.execute("select employee_id from employees where employee_name = ?", (employee_name,))
    employee_id = cursor.fetchone()[0]
    return employee_id