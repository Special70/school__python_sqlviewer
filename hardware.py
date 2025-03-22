import os
import time # to see if program goes to where it should be. will be removed in the final code
import sqlite3
import tkinter as tk
import customtkinter as ctk
import tkinter.messagebox as tkmb
from functions.exiting import exiting

connection = sqlite3.connect("hardwareDB.db")
cursor = connection.cursor()

os.system('cls')

choice_list = [0,1,2,3,4] #stores the menu choices
    
from functions.check import check

from functions.exiting import exiting

from standalone.functions.print_table import print_table

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


def hardware():
    print("main program")
    #main program
    # while True:
    #     if choice == 1:
    #         os.system('cls')
    #         print("Please enter entity type:\n\t[1] Customer\n\t[2] Employee\n\t[0] Exit the Program")
    #         entity_type = check(choice_list[:3])
    #         if entity_type == 1: #if user is a customer
    #             customer_id = customer_login()
    #             time.sleep(2.5)
    #         if entity_type == 1:
    #             while True:
    #                 os.system('cls')
    #                 print("CUSTOMER MAIN MENU\n\t[1] View Business Details\n\t[2] View Available Products\n\t[3] Purchase Product\n\t[0] Exit the Program")
    #                 customer_choice = check(choice_list[:4])
    #                 match customer_choice:
    #                     case 1:
    #                         print("Welcome to Joe MV Enterprise! We are a family owned business that provides a wide range of hardware, ranging from electronic hardwares to manual equipment. We have been in the business for 50 years, and have built a reputable legacy.")
    #                         #this is a description of the business. may edit
    #                         input("\nPress Enter to Continue...")
    #                     case 2:
    #                         print_table("select product_name, type_name, product_details, stock, price from (select * from products left join types using (type_id)) inner join inventory using (product_id)")
    #                         input("\nPress Enter to Continue...")
    #                     case 3:
    #                         order_products(customer_id)
    #                     case _:
    #                         exiting(1)
    #         elif entity_type == 2: 
    #             employee_login()
    #             while True:
    #                 os.system('cls')
    #                 print("EMPLOYEE MAIN MENU\n\t[1] Configure Database \n\t[2] View Inventory\n\t[3] View Records\n\t[4] View Purchases List\n\t[0] Exit the Program")
    #                 employee_choice = check(choice_list)
    #                 match employee_choice:
    #                     case 1: #choice 2 1
    #                         while True:
    #                             #this opens a submenu
    #                             os.system('cls')
    #                             print("CONFIGURE DATABASE\n\t[1] Configure Product\n\t[2] Configure People Data\n\t[0] Return to Previous Menu")
    #                             update_choice = check(choice_list[:3])
    #                             match update_choice:
    #                                 case 1: # choice 2 1 1
    #                                     while True:
    #                                         os.system('cls')
    #                                         print("CONFIGURE PRODUCT\n\t[1] Add Product\n\t[2] Update Product\n\t[3] Delete Product\n\t[4] Restock Product\n\t[0] Return to Previous Menu")
    #                                         config_prod = check(choice_list)
    #                                         match config_prod:
    #                                             case 1: # choice 2 1 1 1
    #                                                 add_product()
    #                                                 input("\nPress Enter to Continue...")
    #                                             case 2: # choice 2 1 1 2
    #                                                 update_product()
    #                                                 input("\nPress Enter to Continue...")
    #                                             case 3: # choice 2 1 1 3
    #                                                 delete_product()
    #                                                 input("\nPress Enter to Continue...")
    #                                             case 4:
    #                                                 restock()
    #                                                 input("\nPress Enter to Continue...")
    #                                             case _:
    #                                                 exiting(0)
    #                                                 break
    #                                 case 2: # choice 2 1 2
    #                                     os.system('cls')
    #                                     print("CONFIGURE PEOPLE DATA\n\t[1] Add People Data\n\t[2] Update People Data\n\t[3] Delete People Data\n\t[0] Return to Previous Menu")
    #                                     config_ppl = check(choice_list[:4])
    #                                     match config_ppl:
    #                                         case 1: # choice 2 1 2 1
    #                                             while True:
    #                                                 os.system('cls')
    #                                                 print("ADD PEOPLE DATA")
    #                                                 print("\t[1] Employee Records\n\t[2] Supplier Records\n\t[0] Return to Previous Menu")
    #                                                 config_ppl = check(choice_list[:3])
    #                                                 match config_ppl: #just ask for input, no need to display table
    #                                                     case 1: # choice 2 1 2 1 1
    #                                                         add_emp()
    #                                                         input("\nPress Enter to Continue...")
    #                                                     case 2: # choice 2 1 2 1 2
    #                                                         add_supp()
    #                                                         input("\nPress Enter to Continue...")
    #                                                     case _:
    #                                                         exiting(0)
    #                                                         break
    #                                         case 2: # choice 2 1 2 2
    #                                             while True:
    #                                                 os.system('cls')
    #                                                 print("UPDATE PEOPLE DATA")
    #                                                 print("\t[1] Employee Records\n\t[2] Customer Records\n\t[3] Supplier Records\n\t[0] Return to Previous Menu")
    #                                                 config_ppl = check(choice_list[:4])
    #                                                 match config_ppl: #just ask for input, no need to display table
    #                                                     case 1:
    #                                                         update_people('employees')
    #                                                         input("\nPress Enter to Continue...")
    #                                                     case 2:
    #                                                         update_people('customers')
    #                                                         input("\nPress Enter to Continue...")
    #                                                     case 3:
    #                                                         update_people('suppliers')
    #                                                         input("\nPress Enter to Continue...")
    #                                                     case _:
    #                                                         exiting(0)
    #                                                         break
    #                                         case 3: # choice 2 1 2 3
    #                                             while True:
    #                                                 os.system('cls')
    #                                                 print("DELETE PEOPLE DATA")
    #                                                 print("\t[1] Employee Records\n\t[2] Customer Records\n\t[3] Supplier Records\n\t[0] Return to Previous Menu")
    #                                                 config_ppl = check(choice_list[:4])
    #                                                 match config_ppl: #just ask for input, no need to display table
    #                                                     case 1: # choice 2 1 2 3 1
    #                                                         delete_people('employees')
    #                                                         input("\nPress Enter to Continue...")
    #                                                     case 2: # choice 2 1 2 3 2
    #                                                         delete_people('customers')
    #                                                         input("\nPress Enter to Continue...")
    #                                                     case 3: # choice 2 1 2 3 3
    #                                                         delete_people('suppliers')
    #                                                         input("\nPress Enter to Continue...")
    #                                                     case _:
    #                                                         exiting(0)
    #                                                         break
    #                                         case _:
    #                                             exiting(0)
    #                                             break
    #                                 case _:
    #                                     exiting(0)
    #                                     break
    #                     case 2: # choice 2 2
    #                         #this opens a submenu
    #                         while True:
    #                             os.system('cls')
    #                             print("VIEW INVENTORY\n\t[1] View Product List\n\t[2] View Inventory Stock\n\t[0] Return to Main Menu")
    #                             inv_choice = check(choice_list[:3])
    #                             match inv_choice:
    #                                 case 1: # choice 2 2 1
    #                                     #this prints all available products
    #                                     print("Display all Products")
    #                                     print_table("select * from products")
    #                                     input("\nPress Enter to Continue...")
    #                                 case 2: # choice 2 2 2
    #                                     while True:
    #                                         #this opens another submenu
    #                                         os.system('cls')
    #                                         print("INVENTORY STOCK\n\t[1] View Inventory Summary\n\t[2] View Products In-Stock\n\t[3] View Products Out-of-Stock\n\t[0] Return to Previous Menu")
    #                                         stock_choice = check(choice_list[:4])
    #                                         match stock_choice:
    #                                             case 1: # choice 2 2 2 1
    #                                                 print("Display All Inventory")
    #                                                 print_table("select product_id, product_name, stock, product_details, type_id, price from inventory left join products using(product_id) where product_id")
    #                                                 input("\nPress Enter to Continue...")
    #                                             case 2: # choice 2 2 2 2
    #                                                 print("Display Products In-Stock")
    #                                                 print_table("select product_id, product_name, stock, product_details, type_id, price from inventory left join products using(product_id) where stock > 0")
    #                                                 input("\nPress Enter to Continue...")
    #                                             case 3: # choice 2 2 2 3
    #                                                 print_table("select product_id, product_name, stock, product_details, type_id, price from inventory left join products using(product_id) where stock == 0")
    #                                                 input("\nPress Enter to Continue...")
    #                                             case _:
    #                                                 exiting(0)
    #                                                 break
    #                                 case _:
    #                                     exiting(0)
    #                                     break
    #                     case 3: # choice 2 3
    #                         #this opens a submenu
    #                         while True:
    #                             os.system('cls')
    #                             print("VIEW RECORDS\n\t[1] Customer Records\n\t[2] Employee Records\n\t[3] Supplier Records\n\t[0] Return to Previous Menu")
    #                             records_choice = check(choice_list[:4])
    #                             match records_choice:
    #                                 case 1: # choice 2 3 1
    #                                     print_table("select * from customers")
    #                                     input("\nPress Enter to Continue...")
    #                                 case 2: # choice 2 3 2
    #                                     print_table("select * from employees")
    #                                     input("\nPress Enter to Continue...")
    #                                 case 3:
    #                                     print_table("select * from suppliers")
    #                                     input("\nPress Enter to Continue...")
    #                                 case _:
    #                                     exiting(0)
    #                                     break
    #                     case 4: # choice 2 4
    #                         #prints all rows from orders table
    #                         #user inputs an order_id
    #                         #displays the corresponding transaction and order_details row.
    #                         print("View Purchase List")
    #                         print_table("select * from orders ord join transactions tr on ord.transaction_id = tr.transaction_id join order_details od on ord.order_id = od.order_id")
    #                         input("\nPress Enter to Continue...")
    #                     case _:
    #                         exiting(1)
            
    #     else:
    #         exiting(1)
            
root = ctk.CTk()
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
root.geometry("400x400")
root.title("Angelite's Enterprise System")

def clear_frame():
    for widgets in root.winfo_children():
        widgets.destroy()

def entity():
    clear_frame()
    label = ctk.CTkLabel(root, text="Are you a Customer or an Employee?")
    label.pack(pady=5)
    customer = ctk.CTkButton(root, text="CUSTOMER", command=lambda: customer_login())
    customer.pack(pady=5)
    employee = ctk.CTkButton(root, text="EMPLOYEE", command=lambda: employee_login())
    employee.pack(pady=5)
    

label = ctk.CTkLabel(root, text="Welcome to Angelite's Hardware Enterprise!")
label.pack(pady=5)
start_button = ctk.CTkButton(root, text="START", command=lambda: entity())
start_button.pack(pady=5)
quit_button = ctk.CTkButton(root, text="QUIT", command=root.destroy)
quit_button.pack(pady=5)

root.mainloop()



