import os
import sys
import time # to see if program goes to where it should be. will be removed in the final code
import sqlite3
import tkinter as tk
import customtkinter as ctk
import tkinter.messagebox as tkmb
# from functions.exiting import exiting
#from PIL import Image, ImageTk

connection = sqlite3.connect("hardwareDB.db")
cursor = connection.cursor()

os.system('cls')

choice_list = [0,1,2,3,4] #stores the menu choices
    
from functions.check import check

# from functions.exiting import exiting

# from standalone.functions.display_table import display_table

from functions.add_product import add_product

from functions.order_products import order_products

from functions.add_emp import add_emp

from functions.add_supp import add_supp

from functions.customer_login import customer_login

from standalone.functions.exist_check import exist_check
    
from functions.delete_product import delete_product

from functions.update_product import update_product

from functions.update_people import update_people

from functions.delete_people import delete_people

from functions.employee_login import employee_login

from functions.restock import restock
            
root = ctk.CTk()
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
root.geometry("400x400")
# root.maxsize(400,400)


root.title("Angelite's Enterprise System")

def exiting():
    root.destroy()
    sys.exit()

def clear_frame():
    for widgets in root.winfo_children():
        widgets.destroy()
        
def exist_check(table, table_column, data):  #checks if one data exists in a table, usually if supplier_id is in table or if employee_id in table
    query = f"SELECT COUNT(*) FROM {table} WHERE {table_column} = ?"
    cursor.execute(query, (data,))
    return 1 if cursor.fetchone()[0] else 0        



def entity():
    clear_frame()
    label = ctk.CTkLabel(root, text="Are you a Customer or an Employee?")
    label.pack(pady=5)
    customer = ctk.CTkButton(root, text="CUSTOMER", command=lambda: login_frame("Customer"))
    customer.pack(pady=5)
    employee = ctk.CTkButton(root, text="EMPLOYEE", command=lambda: login_frame("Employee"))
    employee.pack(pady=5)
    returnMenu = ctk.CTkButton(root, text="QUIT", command=lambda:exiting())
    returnMenu.pack(pady=10)
    
def verify_password(table, col_name, name, password):

    check_name = exist_check(table, col_name, name) #kunin 1 if existing, 0  pag wala
    
    if check_name == 0: #if name not in db or incorrect name, then new customer
        return 3
    
    query = f"select password from {table} where {col_name} = ?"
    cursor.execute(query, (name,))
    result = cursor.fetchone()[0]
    
    if result == password: #name and pw are correct
        return 1 
    else:
        return 0  #correct name, mali pw
    
def customer_login():
    global customer_name
    global customer_id
    customer_name = user_entry.get()
    customer_password = password_entry.get()
    
    if not customer_name:
        tkmb.showerror("Error", "Please enter your full name.")
        return
    
    verification = verify_password('customers', 'customer_name', customer_name, customer_password)
    
    if verification == 0:
        tkmb.showinfo("Login Failed", "Incorrect Details.")
    if verification == 3:
        clear_frame()
        label = ctk.CTkLabel(root, text=f"{customer_name} is not registered.")
        label.pack(pady=12, padx=10)
        label = ctk.CTkLabel(root, text="Would you Like to Register?")
        label.pack(pady=12, padx=10)
        yes_button = ctk.CTkButton(root, text='Yes', command=lambda: registering(customer_name))
        yes_button.pack(pady=12, padx=10)
        no_button = ctk.CTkButton(root, text='No', command=lambda: exiting())
        no_button.pack(pady=12, padx=10)
    elif verification == 1:
        label = ctk.CTkLabel(root, text=f"Logging in as {customer_name}...")
        label.pack(pady=12, padx=10)
        proceed = ctk.CTkButton(root, text="Login", command=lambda: customer_submenu())
        proceed.pack(pady=(5,20))
        customer_id = fetchID(customer_name, 'customer_id', 'customers', 'customer_name')


def fetchID(name, col_id, table_name, col_check):
    global employee_id
    cursor.execute(f'select {col_id} from {table_name} where {col_check} = ?', (name,))
    return cursor.fetchone()[0]

def employee_login():
    employee_name = user_entry.get().strip()
    employee_password = password_entry.get()
    
    verification = verify_password('employees', 'employee_name', employee_name, employee_password)
    
    if not employee_name:
        tkmb.showerror("Error", "Please enter your full name.")
        return
    
    if verification == 0 or verification == 3:
        tkmb.showinfo("Login Failed", "Incorrect Details.")
        exiting()
    elif verification == 1:
        label = ctk.CTkLabel(root, text=f"Logging in as {employee_name}...")
        label.pack(pady=(5), padx=10)
        proceed = ctk.CTkButton(root, text="Login", command=lambda: employee_submenu())
        proceed.pack(pady=(5,20))
        
        cursor.execute("SELECT employee_id FROM employees WHERE employee_name = ?", (employee_name,))
        employee_id = fetchID(employee_name, 'employee_id', 'employees', 'employee_name')
        

def registering (data):
    global customer_id
    cursor.execute("insert into customers (customer_name) VALUES (?)", (data,))
    connection.commit()
    customer_id = fetchID(customer_name, 'customer_id', 'customers', 'customer_name')
    label = ctk.CTkLabel(root, text=f"Successfully registered {data}!")
    label.pack(pady=5)
    label = ctk.CTkLabel(root, text=f"Logging in as {data}...")
    label.pack(pady=12, padx=10)
    proceed = ctk.CTkButton(root, text="Login", command=lambda: customer_submenu())
    proceed.pack(pady=5)
    

def login_frame(entity_type):
    global user_entry, password_entry
    clear_frame()
    
    label = ctk.CTkLabel(root, text=f"{entity_type} Log-In System")
    label.pack(pady=(20,5))
    
    frame = ctk.CTkFrame(master=root)
    frame.pack(pady=20, padx=40, fill='both', expand=True)
    
    label = ctk.CTkLabel(master=frame, text='Full Name:')
    label.pack(pady=(20,2), padx=10)
    
    user_entry = ctk.CTkEntry(master=frame, placeholder_text="John Doe")
    user_entry.pack(pady=(1,5), padx=10)
    
    pass_label = ctk.CTkLabel(frame, text="Password:")
    pass_label.pack(pady=(5,2), padx=10)
    password_entry = ctk.CTkEntry(frame, placeholder_text="Password", show="*") 
    password_entry.pack(pady=(1,10), padx=13)
    
    if entity_type == "Customer":
        button = ctk.CTkButton(master=frame, text='Login', command=lambda: customer_login())
        button.pack(pady=12, padx=10)
    else:
        button = ctk.CTkButton(master=frame, text='Login', command=lambda: employee_login())
        button.pack(pady=12, padx=10)

def customer_submenu():
    root.geometry("400x400")
    clear_frame()
    label = ctk.CTkLabel(root, text="CUSTOMER MAIN MENU")
    label.pack(pady=(5, 10))
    view_business = ctk.CTkButton(root, text="View Business Details", command=description)
    view_business.pack(pady=10)
    products = ctk.CTkButton(root, text="View Products", command=lambda: display_return("select product_name, type_name, product_details, stock, price from (select * from products left join types using (type_id)) inner join inventory using (product_id)", 'CUSTOMER'))
    products.pack(pady=10)
    order = ctk.CTkButton(root, text="Purchase Products", command=lambda: order_products(customer_id))
    order.pack(pady=10)
    exitmenu = ctk.CTkButton(root, text="QUIT", command=lambda: exiting())
    exitmenu.pack(pady=10)

def employee_submenu():
    root.geometry("400x400")
    clear_frame()
    label = ctk.CTkLabel(root, text="EMPLOYEE MAIN MENU")
    label.pack(pady=(5, 10))
    configure_database = ctk.CTkButton(root, text="Configure Database", command=lambda:config_db())
    configure_database.pack(pady=10)
    viewInventory = ctk.CTkButton(root, text="View Inventory", command=lambda: view_inventory())
    viewInventory.pack(pady=10)
    viewRecords = ctk.CTkButton(root, text="View Records", command=lambda:view_records())
    viewRecords.pack(pady=10)
    viewPurchases = ctk.CTkButton(root, text="View Purchases List", command=lambda:view_purchase())
    viewPurchases.pack(pady=10)
    exitMenu = ctk.CTkButton(root, text="QUIT", command=lambda: exiting())
    exitMenu.pack(pady=10)
    
def view_purchase():
    root.geometry("400x400")
    clear_frame()
    label = ctk.CTkLabel(root, text="PURCHASES VIEWING MENU")
    label.pack(pady=(5, 10))
    display_return("select * from orders ord join transactions tr on ord.transaction_id = tr.transaction_id join order_details od on ord.order_id = od.order_id", 'EMPLOYEE')
    
def view_inventory():
    root.geometry("400x400")
    clear_frame()
    label = ctk.CTkLabel(root, text="INVENTORY VIEWING MENU")
    label.pack(pady=(5, 10))
    productList = ctk.CTkButton(root, text="View Product List", command=lambda:display_return('select * from products', 'INVENTORY'))
    productList.pack(pady=10)
    invStock = ctk.CTkButton(root, text="View Inventory Stock", command=lambda:view_stock())
    invStock.pack(pady=10)
    returnMenu = ctk.CTkButton(root, text="Return to Main Menu", command=lambda:employee_submenu())
    returnMenu.pack(pady=10)

def view_stock():
    root.geometry("400x400")
    clear_frame()
    label = ctk.CTkLabel(root, text="INVENTORY STOCK VIEWING MENU")
    label.pack(pady=(5, 10))
    
    summary = ctk.CTkButton(root, text="View Inventory Summary", command=lambda:display_return('select product_id, product_name, stock, product_details, type_id, price from inventory left join products using(product_id) where product_id', 'STOCK'))
    summary.pack(pady=10)
    inStock = ctk.CTkButton(root, text="Display Products In-Stock", command=lambda:display_return('select product_id, product_name, stock, product_details, type_id, price from inventory left join products using(product_id) where stock > 0', 'STOCK'))
    inStock.pack(pady=10)
    outStock = ctk.CTkButton(root, text = "View Products Out-of-Stock", command=lambda:display_return('select product_id, product_name, stock, product_details, type_id, price from inventory left join products using(product_id) where stock == 0', 'STOCK'))
    outStock.pack(pady=10)
    returnMenu = ctk.CTkButton(root, text="Return to Previous Menu", command=lambda:view_inventory())
    returnMenu.pack(pady=10)

def config_db():
    root.geometry("400x400")
    clear_frame()
    label = ctk.CTkLabel(root, text="DATABASE CONFIGURATION MENU")
    label.pack(pady=(5, 10))
    
    configProd = ctk.CTkButton(root, text="Configure Product", command=lambda:config_product())
    configProd.pack(pady=10)
    configPeople = ctk.CTkButton(root, text="Configure People Data", command=lambda:config_people())
    configPeople.pack(pady=10)
    returnMenu = ctk.CTkButton(root, text="Return to Main Menu", command=lambda:employee_submenu())
    returnMenu.pack(pady=10)
    
def config_product():
    root.geometry("400x400")
    clear_frame()
    label = ctk.CTkLabel(root, text="PRODUCT CONFIGURATION MENU")
    label.pack(pady=(5, 10))
    
    addProd = ctk.CTkButton(root, text="Add Product", command=lambda:add_products())
    addProd.pack(pady=10)
    updProd = ctk.CTkButton(root, text="Update Product", command=lambda:ID_subprocess('UPDATE', 'PRODUCT', '', ''))
    updProd.pack(pady=10)
    delProd = ctk.CTkButton(root, text="Delete Product", command=lambda:ID_subprocess('DELETE', 'PRODUCT', '', ''))
    delProd.pack(pady=10)
    returnMenu = ctk.CTkButton(root, text="Return to Previous Menu", command=lambda:config_db())
    returnMenu.pack(pady=10)

def config_people():
    root.geometry("400x400")
    clear_frame()
    label = ctk.CTkLabel(root, text="PEOPLE DATA CONFIGURATION MENU")
    label.pack(pady=(5, 10))
    
    addProd = ctk.CTkButton(root, text="Add People Data", command=lambda:configPeople_submenu('ADD'))
    addProd.pack(pady=10)
    updProd = ctk.CTkButton(root, text="Update People Data", command=lambda:configPeople_submenu('UPDATE'))
    updProd.pack(pady=10)
    delProd = ctk.CTkButton(root, text="Delete People Data", command=lambda:configPeople_submenu('DELETE'))
    delProd.pack(pady=10)
    returnMenu = ctk.CTkButton(root, text="Return to Previous Menu", command=lambda:config_db())
    returnMenu.pack(pady=10)


def configPeople_submenu(config_method):
    
    root.geometry("400x400")
    clear_frame()
    
    if config_method == 'ADD':
        label = ctk.CTkLabel(root, text="ADD PEOPLE DATA CONFIGURATION MENU")
        label.pack(pady=(5, 10))
        emp_add = ctk.CTkButton(root, text="Employee Records", command=lambda:addPeople_setup('employees', 'employee_name'))
        emp_add.pack(pady=10)
        sup_add = ctk.CTkButton(root, text="Supplier Records", command=lambda:addPeople_setup('suppliers', 'supplier_name'))
        sup_add.pack(pady=10)

    if config_method == 'UPDATE':
        label = ctk.CTkLabel(root, text="UPDATE PEOPLE DATA CONFIGURATION MENU")
        label.pack(pady=(5, 10))
        emp_up = ctk.CTkButton(root, text="Employee Records", command=lambda:ID_subprocess('UPDATE', 'PEOPLE', 'employees', 'employee_id'))
        emp_up.pack(pady=10)
        sup_up = ctk.CTkButton(root, text="Supplier Records", command=lambda:ID_subprocess('UPDATE', 'PEOPLE', 'suppliers', 'supplier_id'))
        sup_up.pack(pady=10)

    if config_method == "DELETE":
        label = ctk.CTkLabel(root, text="DELETE PEOPLE DATA CONFIGURATION MENU")
        label.pack(pady=(5, 10))
        emp_del = ctk.CTkButton(root, text="Employee Records", command=lambda:ID_subprocess('DELETE', 'PEOPLE', 'employees', 'employee_id'))
        emp_del.pack(pady=10)
        sup_del = ctk.CTkButton(root, text="Supplier Records", command=lambda:ID_subprocess('DELETE', 'PEOPLE', 'suppliers', 'supplier_id'))
        sup_del.pack(pady=10)
        
    returnMenu = ctk.CTkButton(root, text="Return to Previous Menu", command=lambda:config_people())
    returnMenu.pack(pady=10)


def updatePeople_setup(table, col_name):
    global people_nameget, people_passwordget
    
    clear_frame()
    root.minsize(300,400)
    
    secondRoot = ctk.CTkToplevel(root)
    secondRoot.title("Update People Data Form")
    secondRoot.geometry("300x400")
    
    display_table(f"select * from {table}")
    
    label = ctk.CTkLabel(secondRoot, text="Please enter the New following details: ")
    label.pack(pady=(10,0))
    
    label = ctk.CTkLabel(secondRoot, text=f"{table.capitalize()} Name: ")
    label.pack(pady=(2,0))
    people_nameget = ctk.CTkEntry(secondRoot, placeholder_text=f"{table.capitalize()} Name")
    people_nameget.pack(pady=10)

    if table == 'employees':
        label = ctk.CTkLabel(secondRoot, text=f"{table.capitalize()} Password: ")
        label.pack(pady=(2,0))
        people_passwordget = ctk.CTkEntry(secondRoot, placeholder_text=f"{table.capitalize()} Password")
        people_passwordget.pack(pady=10)

    if table == 'employees':      
        button = ctk.CTkButton(secondRoot, text=f"Update {table.capitalize()}", command=lambda:process_updatePeople(table, col_name))
        button.pack(pady=10)
        
    else:
        button = ctk.CTkButton(secondRoot, text=f"Update {table.capitalize()}", command=lambda:process_updatePeople(table, col_name))
        button.pack(pady=10)
        
    returnMenu = ctk.CTkButton(secondRoot, text="Return to Previous Menu", command=lambda:config_people())
    returnMenu.pack(pady=10)

def process_updatePeople(table, col_name):
    global people_password
    
    people_name = people_nameget.get()
    
    if table == 'employees':
        people_password = people_passwordget.get().strip()
        
        if len(people_password) < 8:
            tkmb.showerror('Invalid Password', 'Password must have a minimum length of 8.')
            return
        
        if (not people_name or not people_password):
            tkmb.showerror("Error", "Fill Out all Fields.")
            return
    
    if exist_check(table, col_name, people_name) == 1:
        tkmb.showerror(f'Existing {table.capitalize()}', f'{table.capitalize()} already Exists.')
        return
    
    if (not people_name):
        tkmb.showerror("Error", "Fill Out all Fields.")
        return
    
    if table == 'employees':
        cursor.execute('update employees set employee_name = ?, password = ? where employee_id = ?', (people_name, people_password, entity_ID))
    else:
        cursor.execute('update suppliers set supplier_name = ? where supplier_id = ?', (people_name, entity_ID))
    
    connection.commit()
    tkmb.showinfo('Success', f'{table.capitalize()} has been successfully updated!')
    display_return(f'select * from {table}', "PEOPLE")
    
    
def addPeople_setup(table, col_name):
    global people_passwordget, people_nameget, secondRoot
    
    clear_frame()
    root.minsize(300,400)
    
    secondRoot = ctk.CTkToplevel(root)
    secondRoot.title("Add People Data Form")
    secondRoot.geometry("300x400")
    
    display_table(f"select * from {table}")
    
    label = ctk.CTkLabel(secondRoot, text="Please enter the following details: ")
    label.pack(pady=(10,0))
    
    label = ctk.CTkLabel(secondRoot, text=f"{table.capitalize()} Name: ")
    label.pack(pady=(2,0))
    people_nameget = ctk.CTkEntry(secondRoot, placeholder_text=f"{table.capitalize()} Name")
    people_nameget.pack(pady=10)

    if table == 'employees':
        label = ctk.CTkLabel(secondRoot, text=f"{table.capitalize()} Password: ")
        label.pack(pady=(2,0))
        people_passwordget = ctk.CTkEntry(secondRoot, placeholder_text=f"{table.capitalize()} Password")
        people_passwordget.pack(pady=10)

    if table == 'employees':      
        button = ctk.CTkButton(secondRoot, text=f"Add {table.capitalize()}", command=lambda:process_addPeople(table, col_name))
        button.pack(pady=10)
        
    else:
        button = ctk.CTkButton(secondRoot, text=f"Add {table.capitalize()}", command=lambda:process_addPeople(table, col_name))
        button.pack(pady=10)
        
    returnMenu = ctk.CTkButton(secondRoot, text="Return to Previous Menu", command=lambda:config_people())
    returnMenu.pack(pady=10)

def process_addPeople(table, col_name):
    
    people_name = people_nameget.get()
    
    if table == 'employees':
        people_password = people_passwordget.get().strip()
        
        if len(people_password) < 8:
            tkmb.showerror('Invalid Password', 'Password must have a minimum length of 8.')
            return
        
        if (not people_name or not people_password):
            tkmb.showerror("Error", "Fill Out all Fields.")
            return
    
    if exist_check(table, col_name, people_name) == 1:
        tkmb.showerror(f'Existing {table.capitalize()}', f'{table.capitalize()} already Exists.')
        return
    
    if (not people_name):
        tkmb.showerror("Error", "Fill Out all Fields.")
        return
    
    if table == 'employees':
        cursor.execute('insert into employees (employee_name, password) values (?,?)', (people_name, people_password))
    else:
        cursor.execute('insert into suppliers (supplier_name) values (?)', (people_name,))
    
    connection.commit()
    tkmb.showinfo('Success', f'{table.capitalize()} has been successfully added!')
    display_return(f'select * from {table}', "PEOPLE")
    
def process_delete(table, col_id, entity):
        
    cursor.execute(f'delete from {table} where {col_id} = ?', (entity_ID,))
    
    if entity == 'PRODUCT':
        cursor.execute('delete from inventory where product_id = ?', (entity_ID,))
        
    connection.commit()
    
    if entity == 'PRODUCT':
        tkmb.showinfo('Product Deleted', "Product has been succesfully deleted!")
        display_return('select product_id, product_name, stock, product_details, type_id, price from inventory left join products using(product_id)', 'PROD')
    
    if entity == 'EMPLOYEE':
        tkmb.showinfo('Employee Deleted', "Employee has been succesfully deleted!")
        display_return('select * from employees', 'PEOPLE')
        
    if entity == 'SUPPLIER':
        tkmb.showinfo('Supplier Deleted', "Supplier has been succesfully deleted!")
        display_return('select * from suppliers', 'PEOPLE')

def delete_products():
    global entity_ID
    
    clear_frame()
    root.minsize(300,400)
    
    
    addPRod = ctk.CTkToplevel(root)
    addPRod.title("Delete Product Form")
    addPRod.geometry("300x400")
    
    display_table(f"select product_id, product_name, stock, product_details, type_id, price from inventory left join products using(product_id)")
    
    label = ctk.CTkLabel(addPRod, text="Are you sure you want to delete: ")
    label.pack(pady=(2,0))

    button = ctk.CTkButton(addPRod, text="YES", command=lambda:process_delete('products', 'product_id', 'PRODUCT'))
    button.pack(pady=10)
    button = ctk.CTkButton(addPRod, text="NO", command=lambda:config_db())
    button.pack(pady=10)

def delete_people(table):
    
    clear_frame()
    root.minsize(300,400)
    
    
    addPRod = ctk.CTkToplevel(root)
    addPRod.title("Delete People Form")
    addPRod.geometry("300x400")
    
    display_table(f"select * from {table}")
    
    label = ctk.CTkLabel(addPRod, text="Are you sure you want to delete: ")
    label.pack(pady=(2,0))
    
    if table == 'employees':
        button = ctk.CTkButton(addPRod, text="YES", command=lambda:process_delete(table, 'employee_id', 'EMPLOYEE'))

    if table == 'suppliers':
        button = ctk.CTkButton(addPRod, text="YES", command=lambda:process_delete(table, 'supplier_id', 'SUPPLIER'))
        
    button.pack(pady=10)
    button = ctk.CTkButton(addPRod, text="NO", command=lambda:config_people())
    button.pack(pady=10)
    
def get_confirmId(config_method, table, col_id):
    global entity_ID

    entity_ID = entity_idGet.get().strip()
    
    if exist_check(table, col_id, entity_ID) == 0 or not entity_ID.isdigit():
        tkmb.showerror("Error", f"Invalid ID.")
        return
    
    tkmb.showinfo('Success', 'The ID is Valid.')
    
    if config_method == 'UPDATE':
        if table == 'employees' or table == 'suppliers':
            updatePeople_setup(table, col_id)
        else: 
            update_products()
        
    if config_method == 'DELETE':
        if table == 'employees' or table == 'suppliers':
            delete_people(table)
        else: 
            delete_products()
        
def ID_subprocess(config_method, entity, table, col_name):
    global entity_idGet
        
    clear_frame()
    root.minsize(300,400)
    
    
    addPRod = ctk.CTkToplevel(root)
    addPRod.geometry("300x400")
    addPRod.protocol("WM_DELETE_WINDOW", lambda: None)
    
    if entity == 'PRODUCT':
        display_table("select product_id, product_name, product_details, supplier_id, type_id, stock, price from inventory left join products using(product_id)")
        
    if entity == 'PEOPLE':
        display_table(f'select * from {table}')
        
    if config_method == 'UPDATE':
        addPRod.title(f"Update {entity.capitalize()} Form")
        label = ctk.CTkLabel(addPRod, text="Enter ID to be Edited: ")
        label.pack(pady=(2,0))
        
    if config_method == 'DELETE':
        addPRod.title(f"Delete {table.capitalize()} Form")
        label = ctk.CTkLabel(addPRod, text="Enter ID to be Deleted: ")
        label.pack(pady=(2,0))
        
    entity_idGet = ctk.CTkEntry(addPRod, placeholder_text="ID")
    entity_idGet.pack(pady=10)
    
    if entity == 'PRODUCT':
        button = ctk.CTkButton(addPRod, text="Proceed", command=lambda:get_confirmId(config_method, 'products', 'product_id'))
        button.pack(pady=10)
        
    if entity == 'PEOPLE':
        button = ctk.CTkButton(addPRod, text="Proceed", command=lambda:get_confirmId(config_method, table, col_name))
        button.pack(pady=10)
        
    button = ctk.CTkButton(addPRod, text="Cancel", command=lambda:config_db())
    button.pack(pady=10)
    
def update_products():
    global product_name, supplier_id, product_details, price, type_id, stock, entity_ID
    
    clear_frame()
    root.minsize(300,600)
    
    
    addPRod = ctk.CTkToplevel(root)
    addPRod.title("Update Product Form")
    addPRod.geometry("300x600")
    addPRod.protocol("WM_DELETE_WINDOW", lambda: None)
    
    display_table("select product_id, product_name, product_details, supplier_id, type_id, stock, price from inventory left join products using(product_id)")

    
    label = ctk.CTkLabel(addPRod, text="Please enter the New Product details: ")
    label.pack(pady=(10,0))
    
    label = ctk.CTkLabel(addPRod, text="Name: ")
    label.pack(pady=(2,0))
    product_name = ctk.CTkEntry(addPRod, placeholder_text="Product Name")
    product_name.pack(pady=10)

    label = ctk.CTkLabel(addPRod, text="Product Description: ")
    label.pack(pady=(2,0))
    product_details = ctk.CTkEntry(addPRod, placeholder_text="Product Description")
    product_details.pack(pady=10)

    label = ctk.CTkLabel(addPRod, text="Supplier ID: ")
    label.pack(pady=(2,0))
    supplier_id = ctk.CTkEntry(addPRod, placeholder_text="Supplier ID")
    supplier_id.pack(pady=10)
    
    label = ctk.CTkLabel(addPRod, text="Type ID: ")
    label.pack(pady=(2,0))
    type_id = ctk.CTkEntry(addPRod, placeholder_text="Type ID")
    type_id.pack(pady=10)

    label = ctk.CTkLabel(addPRod, text="Price per Unit: ")
    label.pack(pady=(2,0))
    price = ctk.CTkEntry(addPRod, placeholder_text="Price")
    price.pack(pady=10)
    
    label = ctk.CTkLabel(addPRod, text="Stock: ")
    label.pack(pady=(2,0))
    stock = ctk.CTkEntry(addPRod, placeholder_text="Stock")
    stock.pack(pady=10)

    addProduct = ctk.CTkButton(addPRod, text="Update Product", command=lambda: process_updateProduct())
    addProduct.pack(pady=10)
    button = ctk.CTkButton(addPRod, text="Cancel", command=lambda:config_db())
    button.pack(pady=10)
    
def process_updateProduct():
    global product_name, product_description, supplier_id, type_id, price, quantity, stock, entity_ID
    
    # Fetch the data entered in the form
    prod_id = entity_ID
    prod_name = product_name.get().strip()
    product_desc = product_details.get().strip()
    sup_id = supplier_id.get().strip()
    typeId = type_id.get().strip()
    price_product = price.get().strip()
    stock_prod = stock.get().strip()

    if (not prod_name or not product_desc or not sup_id or not typeId or not price_product or not stock_prod):
        tkmb.showerror("Error", "Fill Out all Fields.")
    
    else:
        if exist_check('suppliers', 'supplier_id', sup_id) == 0:
            tkmb.showerror("Error", "Supplier ID is Invalid.")
            return
        
        if exist_check('types', 'type_id', typeId) == 0:
            tkmb.showerror("Error", "Type ID is Invalid.")
            return
        
        if not price_product.isdigit() or int(price_product) <= 0:
            tkmb.showerror("Error", "Price is Invalid.")
            return
        
        if not stock_prod.isdigit() or int(stock_prod) <= 0:
            tkmb.showerror("Error", "Stock is Invalid.")
            return
    
        else:
            cursor.execute('update products set product_name = ?, supplier_id = ?, product_details = ?, type_id = ?, price = ? where product_id = ?',(prod_name, sup_id, product_desc, typeId, price_product, prod_id))

            cursor.execute('update inventory set stock = ? where product_id = ?', (stock_prod, prod_id))
            
            connection.commit()
            
            tkmb.showinfo("Success", "Product has been succesfully updted!")
            display_return(f'select product_id, product_name, product_details, supplier_id, type_id, stock, price from inventory left join products using(product_id) where product_id = {prod_id}', 'PROD')
    
def add_products():
    global product_name, supplier_id, product_details, price, type_id, stock
    
    clear_frame()
    root.minsize(300,600)
    display_table("select * from suppliers")
    display_table('select * from types')
    
    addPRod = ctk.CTkToplevel(root)
    addPRod.title("Insert Product Form")
    addPRod.geometry("300x600")
    addPRod.protocol("WM_DELETE_WINDOW", lambda: None)
    
    label = ctk.CTkLabel(addPRod, text="Please enter the following details: ")
    label.pack(pady=(10,0))
    
    label = ctk.CTkLabel(addPRod, text="Name: ")
    label.pack(pady=(2,0))
    product_name = ctk.CTkEntry(addPRod, placeholder_text="Product Name")
    product_name.pack(pady=10)

    label = ctk.CTkLabel(addPRod, text="Product Description: ")
    label.pack(pady=(2,0))
    product_details = ctk.CTkEntry(addPRod, placeholder_text="Product Description")
    product_details.pack(pady=10)

    label = ctk.CTkLabel(addPRod, text="Supplier ID: ")
    label.pack(pady=(2,0))
    supplier_id = ctk.CTkEntry(addPRod, placeholder_text="Supplier ID")
    supplier_id.pack(pady=10)
    
    label = ctk.CTkLabel(addPRod, text="Type ID: ")
    label.pack(pady=(2,0))
    type_id = ctk.CTkEntry(addPRod, placeholder_text="Type ID")
    type_id.pack(pady=10)

    label = ctk.CTkLabel(addPRod, text="Price per Unit: ")
    label.pack(pady=(2,0))
    price = ctk.CTkEntry(addPRod, placeholder_text="Price")
    price.pack(pady=10)
    
    label = ctk.CTkLabel(addPRod, text="Stock: ")
    label.pack(pady=(2,0))
    stock = ctk.CTkEntry(addPRod, placeholder_text="Stock")
    stock.pack(pady=10)

    addProduct = ctk.CTkButton(addPRod, text="Add Product", command=lambda: process_addProduct())
    addProduct.pack(pady=10)
    button = ctk.CTkButton(addPRod, text="Cancel", command=lambda:config_db())
    button.pack(pady=10)

def process_addProduct():
    global product_name, product_description, supplier_id, type_id, price, quantity, stock
    
    # Fetch the data entered in the form
    prod_name = product_name.get().strip()
    product_desc = product_details.get().strip()
    sup_id = supplier_id.get().strip()
    typeId = type_id.get().strip()
    price_product = price.get().strip()
    stock_prod = stock.get().strip()

    if (not prod_name or not product_desc or not sup_id or not typeId or not price_product or not stock_prod):
        tkmb.showerror("Error", "Fill Out all Fields.")
    
    else:
        if exist_check('suppliers', 'supplier_id', sup_id) == 0:
            tkmb.showerror("Error", "Supplier ID is Invalid.")
            return
        
        if exist_check('types', 'type_id', typeId) == 0:
            tkmb.showerror("Error", "Type ID is Invalid.")
            return
        
        if not price_product.isdigit() or int(price_product) < 0:
            tkmb.showerror("Error", "Price is Invalid.")
            return
        
        if not stock_prod.isdigit() or int(stock_prod) <= 0:
            tkmb.showerror("Error", "Stock is Invalid.")
            return
    
        else:
            cursor.execute('insert into products (product_name, product_details, supplier_id, type_id, price) values (?,?,?,?,?)', (prod_name, product_desc, sup_id, typeId, price_product))
        
            cursor.execute('select product_id from products where product_name = ?', (prod_name,))
            prod_id = cursor.fetchone()[0]
            cursor.execute('insert into inventory (product_id, stock) values (?,?)',(prod_id, stock_prod))
            
            tkmb.showinfo("Success", "Product has been succesfully added.")
            
            connection.commit()
            
            display_return(f'select product_id, product_name, product_details, supplier_id, type_id, stock, price from inventory left join products using(product_id) where product_id = {prod_id}', 'PROD')
    

def view_records():
    root.geometry("400x400")
    clear_frame()
    label = ctk.CTkLabel(root, text="RECORD VIEWING MENU")
    label.pack(pady=(5, 10))
    customerRecords = ctk.CTkButton(root, text="Customer Records", command=lambda:display_return('select * from customers', 'RECORD'))
    customerRecords.pack(pady=10)
    employeeRecords = ctk.CTkButton(root, text="Employee Records", command=lambda:display_return('select * from employees', 'RECORD'))
    employeeRecords.pack(pady=10)
    returnMenu = ctk.CTkButton(root, text="Return to Main Menu", command=lambda:employee_submenu())
    returnMenu.pack(pady=10)
    
    
def description():
    clear_frame()
    label = ctk.CTkLabel(root, text="Angelite's Hardware Enterprise")
    label.pack(pady=(80,0))
    description = ctk.CTkLabel(root, text="Welcome to Joe MV Enterprise! We are a family owned business that provides a wide range of hardware, ranging from electronic hardwares to manual equipment. We have been in the business for 50 years, and have built a reputable legacy.", wraplength=350)
    description.pack(pady=30,padx=15)
    proceed = ctk.CTkButton(root, text="Return to Previous Menu", command=lambda: customer_submenu())
    proceed.pack(pady=5)
    
def display_return(table_query:str, entity):
    clear_frame()
    display_table(table_query)
    
    if entity.upper() == 'CUSTOMER':
        button = ctk.CTkButton(root, text="Return to Previous Menu", command=lambda: customer_submenu())
    elif entity.upper() == 'EMPLOYEE':
        button = ctk.CTkButton(root, text="Return to Previous Menu", command=lambda: employee_submenu())
    elif entity.upper() == 'STOCK':
        button = ctk.CTkButton(root, text="Return to Previous Menu", command=lambda: view_stock())
    elif entity.upper() == 'INVENTORY':
        button = ctk.CTkButton(root, text="Return to Previous Menu", command=lambda: view_inventory())
    elif entity.upper() == 'RECORD':
        button = ctk.CTkButton(root, text="Return to Previous Menu", command=lambda: view_records())
    elif entity.upper() == "PROD":
        button = ctk.CTkButton(root, text="Return to Previous Menu", command=lambda: config_db())
    elif entity.upper() == "PEOPLE":
        button = ctk.CTkButton(root, text="Return to Previous Menu", command=lambda: config_people())
        
    button.pack(pady=10)
    
def display_table(table_query: str):
    root.geometry("700x500")
    query = cursor.execute(table_query)
    
    column_list = [desc[0].title().replace("_", " ") for desc in query.description]
    frame = ctk.CTkScrollableFrame(root, width=550, height=350)
    frame.pack(padx=10, pady=10, fill="both", expand=True)

    for column_index, col_name in enumerate(column_list):
        header = ctk.CTkLabel(frame, text=col_name, font=("Arial", 12, "bold"), padx=5, pady=5)
        header.grid(row=0, column=column_index, sticky="w")
        
    rows = query.fetchall()
    for row_index, row in enumerate(rows, 1):
        for column_index, value in enumerate(row):
            value_label = ctk.CTkLabel(frame, text=value, padx=5, pady=5, anchor="w")
            value_label.grid(row=row_index, column=column_index, sticky="w")


def product_validator(product_id: str):
    query = f"select product_id, product_name, type_name, product_details, stock, price from (select * from products left join types using (type_id)) inner join inventory using (product_id) where stock > 0 and product_id = {product_id}"
    cursor.execute(query)
    return 1 if cursor.fetchone() else 0

def date_validator(date: str):
    if len(date) < 10:
        return 0
    if int(date[0]) not in range(1970, 3001):
        return 0
    if int(date[1]) not in range(1, 13):
        return 0
    if int(date[2]) not in range(1, 32):
        return 0
    
    return 1

def quantity_validator(stock_input: str, product_id: str):
    query = f"select stock from (select * from products left join types using (type_id)) inner join inventory using (product_id) where stock > 0 and product_id = {product_id}"
    cursor.execute(query)
    result = cursor.fetchone()
    if result == None:
        return 0
    elif int(result[0]) < int(stock_input):
        return 0
    else:
        return 1

def employee_validator(emp_id: str):
    query = f"select * from employees where employee_id = {emp_id}"
    cursor.execute(query)
    result = cursor.fetchone()

    if result:
        return 1
    else:
        return 0


def order_products(customer_Id):
    global date, quantity, product_id, employee_id, customer_id, order
    clear_frame()
    root.minsize(400,570)
    display_table("select product_id, product_name, type_name, product_details, stock, price from (select * from products left join types using (type_id)) inner join inventory using (product_id) where stock > 0")
    display_table("select * from employees")
    
    order = ctk.CTkToplevel(root)
    order.title("Order Purchase Form")
    order.geometry("300x300")
    
    label = ctk.CTkLabel(order, text="Please enter the following details: ")
    label.pack(pady=(10,0))
    date = ctk.CTkEntry(order, placeholder_text="[YEAR-MONTH-DATE]")
    date.pack(pady=10)

    product_id = ctk.CTkEntry(order, placeholder_text="Product ID")
    product_id.pack(pady=10)

    quantity = ctk.CTkEntry(order, placeholder_text="Quantity")
    quantity.pack(pady=10)

    employee_id = ctk.CTkEntry(order, placeholder_text="Employee ID")
    employee_id.pack(pady=10)

    purchase = ctk.CTkButton(order, text="Place Order", command=lambda: process())
    purchase.pack(pady=10)



def process():
        global order
        order_date = date.get().strip()
        if not order_date:
            tkmb.showerror("Error", "Please enter the date.")
            return
        elif date_validator(order_date):
            tkmb.showerror("Date Error", f"{order_date} is Invalid. Try again!")
            return
        
        order_product_id = product_id.get().strip()
        if not order_product_id:
            tkmb.showerror("Error", "Please enter the product ID.")
            return
        elif product_validator(order_product_id) == 0:
            tkmb.showerror("Error", "Please enter the valid product ID.")
            return

        order_quantity = quantity.get().strip()
        if not order_product_id:
            tkmb.showerror("Error", "Please enter quantity.")
            return
        elif quantity_validator(order_quantity, order_product_id) == 0 or int(order_quantity) == 0:
            tkmb.showerror("Error", "Please enter valid quantity.")
            return
        
        order_employee_id = employee_id.get().strip()
        if not order_employee_id:
            tkmb.showerror("Error", "Please enter employee ID.")
            return
        elif employee_validator(order_employee_id) == 0:
            tkmb.showerror("Error", "Please enter valid ID.")
            return
        
        cursor.execute("select price from products where product_id = ?", (order_product_id,))
        query = cursor.fetchone()
        total = query[0] * int(order_quantity)
        
        order.destroy()
        place_order(customer_id, order_employee_id, order_product_id, order_quantity, total, order_date)
        
def place_order(customer_id, employee_id, product_id, quantity, total, date):
    cursor.execute("insert into transactions (customer_id, transaction_date, total) values (?, ?, ?)", (customer_id, date, total,))
    transaction_id = cursor.lastrowid
    cursor.execute("insert into orders (transaction_id, employee_id) values (?, ?)", (transaction_id, employee_id,))
    order_id = cursor.lastrowid
    cursor.execute("insert into order_details (order_id, product_id, quantity) values (?, ?, ?)", (order_id, product_id, quantity,))
    cursor.execute("update inventory set stock = stock - ? where product_id = ? ", (quantity, product_id,))
    connection.commit()
    label = ctk.CTkLabel(root, text="Successfully Placed an Order!")
    label.pack(pady=10)
    cursor.execute("select product_name from products where product_id = ?", (product_id,))
    result = cursor.fetchone()[0]

    receipt = ctk.CTkToplevel(root)
    receipt.geometry("270x300")
    frame = ctk.CTkFrame(receipt)
    frame.pack(pady=20, padx=40, fill='both', expand=True)
    receipt.title("Order Receipt")
    cursor.execute("select product_name from products where product_id = ?", (product_id,))
    result = cursor.fetchone()[0]
    label = ctk.CTkLabel(frame, text="ORDER SUMMARY")
    label.pack(pady=10)
    label = ctk.CTkLabel(frame, text=f"Product: {result}")
    label.pack(pady=10)
    label = ctk.CTkLabel(frame, text=f"Quantity: {quantity}")
    label.pack(pady=10)
    label = ctk.CTkLabel(frame, text=f"----------------------------------\nProduct: {total}")
    label.pack(pady=10)
    button = ctk.CTkButton(frame, text="Return to Previous Menu", command=lambda:customer_submenu())
    button.pack(pady=10)


label = ctk.CTkLabel(root, text="Welcome to Angelite's Hardware Enterprise!")
label.pack(pady=5)
frame = ctk.CTkFrame(root)
frame.pack(pady=20, padx=40, fill='both', expand=True)

button_frame = ctk.CTkFrame(root, fg_color="transparent")
button_frame.pack(pady=30)
start_button = ctk.CTkButton(button_frame, text="START", width=100, height=40, command=lambda: entity())
start_button.pack(side="left", padx=10)
quit_button = ctk.CTkButton(button_frame, text="QUIT", width=100, height=40, command=lambda: exiting())
quit_button.pack(side="left", padx=10)

root.mainloop()