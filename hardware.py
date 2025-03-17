import os
import sys
import time # to see if program goes to where it should be. will be removed in the final code
import sqlite3
# import tkinter as tk
# from tkinter import ttk

connection = sqlite3.connect("hardwareDB.db")
cursor = connection.cursor()

os.system('cls')

choice_list = [0,1,2,3,4] #stores the menu choices

def check(choice_list): #for checking if input is valid
    while True:
        try:
            a = int(input("Enter Choice: "))
            while a not in choice_list:
                print(f"ERROR | {a} is invalid. Try again!") 
                a = int(input("Enter Choice: "))
        except ValueError:
            print("ERROR | Please enter a number.")
            continue
        return a
    
def exiting (num):
    if num == 1:
        print("Thank you for using the program. Exiting...")
        time.sleep(2.5)
        sys.exit()
    else:
        print("Returning to Previous Menu...")
        time.sleep(2.5)
    
    
    
print("Welcome to Joe MV Enterprise!\n\t[1] Start the Program\n\t[0] Terminate the Program")
choice = check(choice_list[:2])

#main program
while True:
    if choice == 1:
        os.system('cls')
        print("Please enter entity type:\n\t[1] Customer\n\t[2] Employee\n\t[0] Exit the Program")
        entity_type = check(choice_list[:3])
        
        if entity_type == 1: #if user is a customer
            while True:
                os.system('cls')
                print("CUSTOMER MAIN MENU\n\t[1] View Business Details\n\t[2] View Available Products\n\t[3] Purchase Product\n\t[0] Exit the Program")
                customer_choice = check(choice_list[:4])
                match customer_choice:
                    case 1:
                        print("Welcome to Joe MV Enterprise! We are a family owned business that provides a wide range of hardware, ranging from electronic hardwares to manual equipment. We have been in the business for 50 years, and have built a reputable legacy.")
                        #this is a description of the business. may edit
                        time.sleep(2.5) 
                    case 2:
                        #this prints all available products
                        print("View available products.")
                        time.sleep(2.5)
                    case 3:
                        #display all available products
                        #user inputs one product at a time.
                        #product id and quantity
                        #payment method
                        #here compute total. confirm if place order.
                        #if user places order, will prompt user to enter customer details. name, phone_num, email. then save to db. if customer customer name exists, then skip.
                        print("Place an Order")
                        time.sleep(2.5)
                    case _:
                        exiting(1)
                        
        elif entity_type == 2: #if user is an employee
            # while True: #for security / confirm if they are employee
            #print("Enter Employee ID: ")
            #condition if employee id not in employee table, return to previous menu which is customer or employee ba sya
            #if employee id in employee table, then this:
            while True:
                os.system('cls')
                print("EMPLOYEE MAIN MENU\n\t[1] Configure Database \n\t[2] View Inventory\n\t[3] View Records\n\t[4] View Purchases List\n\t[0] Exit the Program")
                employee_choice = check(choice_list)
                match employee_choice:
                    case 1:
                        while True:
                            #this opens a submenu
                            os.system('cls')
                            print("CONFIGURE DATABASE\n\t[1] Add New Product\n\t[2] Update Product\n\t[3] Add Information\n\t[4] Update Information\n\t[0] Return to Previous Menu")
                            update_choice = employee_choice = check(choice_list)
                            match update_choice:
                                case 1:
                                    #display suppliers table
                                    #dapat supplier_id is in suppliers table. if not, return error.
                                    #this will let user input to product, inventory, and suppliers table. another query to add
                                    #input product_name, supplier_id, product_details, type, price, stock, suppliers_name
                                    print("Add new Product ...")
                                    time.sleep(2.5)
                                case 2:
                                    #display products table
                                    #enter product id, then update after user inputs product_name, etc...
                                    #update inventory
                                    print("Update Products..")
                                    time.sleep(2.5)
                                case 3:
                                    while True:
                                        os.system('cls')
                                        print("ADD INFORMATION\n\t[1] Employee Records\n\t[2] Supplier Records\n\t[0] Return to Previous Menu")
                                        config_choice = check(choice_list[:3])
                                        match config_choice:
                                            case 1:
                                                print("Adding Employee Records...")
                                                time.sleep(2.5)
                                            case 2:
                                                print("Adding Supplier Records...")
                                                time.sleep(2.5)
                                            case _:
                                                exiting(0)
                                                break
                                case 4:
                                    while True:
                                        os.system('cls')
                                        print("UPDATE INFORMATION\n\t[1] Employee Records\n\t[2] Customer Records\n\t[3] Supplier Records\n\t[0] Return to Previous Menu")
                                        config_choice = check(choice_list[:4])
                                        match config_choice:
                                            case 1:
                                                print("Updating Employee Records...")
                                                time.sleep(2.5)
                                            case 2:
                                                print("Updating Employee Records...")
                                                time.sleep(2.5)
                                            case 3:
                                                print("Updating Supplier Records...")
                                                time.sleep(2.5)
                                            case _:
                                                exiting(0)
                                                break
                                case _:
                                    exiting(0)
                                    break
                    case 2:
                        #this opens a submenu
                        while True:
                            os.system('cls')
                            print("VIEW INVENTORY\n\t[1] View Product List\n\t[2] View Inventory Stock\n\t[3] View Supplier List\n\t[0] Return to Main Menu")
                            inv_choice = check(choice_list[:4])
                            match inv_choice:
                                case 1:
                                    #this prints all available products
                                    print("Display all Products")
                                    time.sleep(2.5)
                                case 2:
                                    while True:
                                        #this opens another submenu
                                        os.system('cls')
                                        print("INVENTORY STOCK\n\t[1] View Inventory Summary\n\t[2] View Products In-Stock\n\t[3] View Products Out-of-Stock\n\t[0] Return to Previous Menu")
                                        stock_choice = check(choice_list[:4])
                                        match stock_choice:
                                            case 1:
                                                #display all rows in inventory table
                                                print("Display All Inventory")
                                                time.sleep(2.5)
                                            case 2:
                                                #display all rows where stock > 0
                                                print("Display Products In-Stock")
                                                time.sleep(2.5)
                                            case 3:
                                                #display all rows where stock == 0
                                                print("Display Products Out of Stock")
                                                time.sleep(2.5)
                                            case _:
                                                exiting(0)
                                                break
                                case 3:
                                    #print all rows in the suppliers table
                                    print("Display Suppliers")
                                    time.sleep(2.5)
                                case _:
                                    exiting(0)
                                    break
                    case 3:
                        #this opens a submenu
                        while True:
                            os.system('cls')
                            print("VIEW RECORDS\n\t[1] Customer Records\n\t[2] Employee Records\n\t[0] Return to Previous Menu")
                            records_choice = check(choice_list[:3])
                            match records_choice:
                                case 1:
                                    #print all customer records
                                    print("Display All Customer Records")
                                    time.sleep(2.5)
                                case 2:
                                    #print all employee records
                                    print("Display All Employee Records")
                                    time.sleep(2.5)
                                case _:
                                    exiting(0)
                                    break
                    case 4:
                        #prints all rows from orders table
                        #user inputs an order_id
                        #displays the corresponding transaction and order_details row.
                        print("View Purchase List")
                        time.sleep(2.5)
                    case _:
                        exiting(1)
        
    else:
        exiting(1)