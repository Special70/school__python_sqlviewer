import customtkinter as ctk
import tkinter.messagebox as tkmb
from standalone.global_vars import cursor, connection
from standalone.functions.exist_check import exist_check
from functions.exiting import exiting
from functions.print_table import print_table

root = ctk.CTk()
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
root.geometry("400x400")
root.title("Angelite's Enterprise System")

user_entry = None

def login():
    customer_name = user_entry.get().strip()
    if not customer_name:
        tkmb.showerror("Error", "Please enter your full name.")
        return
    login_status = exist_check("customers", "customer_name", customer_name)
    if login_status == 0:
        label = ctk.CTkLabel(root, text=f"{customer_name} is not registered.")
        label.pack(pady=12, padx=10)
        register = ctk.CTkToplevel(root)
        label = ctk.CTkLabel(master=register, text="Would you Like to Register?")
        label.pack(pady=12, padx=10)
        yes_button = ctk.CTkButton(register, text='Yes', command=lambda: registering(customer_name))
        yes_button.pack(pady=12, padx=10)
        no_button = ctk.CTkButton(register, text='No', command=lambda: exiting(1))
        no_button.pack(pady=12, padx=10)
    else:
        label = ctk.CTkLabel(root, text=f"Logging in as {customer_name}...")
        label.pack(pady=12, padx=10)
        cursor.execute("SELECT customer_id FROM customers WHERE customer_name = ?", (customer_name,))
        customer_id = cursor.fetchone()[0]
        print(f"Logged in as Customer ID: {customer_id}")
    customer_submenu()


def registering (customer_name):
    cursor.execute("INSERT INTO customers (customer_name) VALUES (?)", (customer_name,))
    connection.commit()
    tkmb.showinfo("Registration Successful", f"Successfully registered {customer_name}!")
    

def clear_frame():
    for widgets in root.winfo_children():
        widgets.destroy()

def customer_submenu():
    clear_frame()
    label = ctk.CTkLabel(root, "MAIN MENU")
    label.pack(pady=5)
    view_business = ctk.CTkButton(root, "View Business Details", command=description)
    view_business.pack(pady=5)
    view_products = ctk.CTkButton(root, "View Business Details", command=lambda: print_table("select product_name, type_name, product_details, stock, price from (select * from products left join types using (type_id)) inner join inventory using (product_id)"))
    view_products.pack(pady=5)
    
def description():
    clear_frame
    label = ctk.CTkLabel(root, "Angelite's Hardware Enterprise")
    label.pack(pady=5)
    description = ctk.CTkLabel(root, "Welcome to Joe MV Enterprise! We are a family owned business that provides a wide range of hardware, ranging from electronic hardwares to manual equipment. We have been in the business for 50 years, and have built a reputable legacy.")
    description.pack(pady=5)

def customer_login():
    global user_entry
    clear_frame()
    
    label = ctk.CTkLabel(root, text="Customer Log-In System")
    label.pack(pady=20)
    
    frame = ctk.CTkFrame(master=root)
    frame.pack(pady=20, padx=40, fill='both', expand=True)
    
    label = ctk.CTkLabel(master=frame, text='Log-In Form')
    label.pack(pady=12, padx=10)
    
    user_entry = ctk.CTkEntry(master=frame, placeholder_text="Full Name")
    user_entry.pack(pady=12, padx=10)
    
    button = ctk.CTkButton(master=frame, text='Login', command=login)
    button.pack(pady=12, padx=10)
    
    root.mainloop()
    