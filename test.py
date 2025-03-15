# importing sqlite3 module
import sqlite3
 
 
# create connection by using object
# to connect with hotel_data database
connection = sqlite3.connect('hotel_data.db')
 
# query to create a table named FOOD1
connection.execute(''' 
create table product_type (
	type_id int primary key auto_increment,
	type_name varchar(50)
);

create table supplier_records (
	supplier_id int primary key auto_increment,
	supplier_name varchar(50),
	delivery_date date,
);

create table products (
	product_id int primary key auto_increment,
	supplier_source_id int,
	type_id int,	
	product_name varchar(50),
	product_brand varchar(50),
	product_details varchar(50),

	foreign key (supplier_source_id) references supplier_records(supplier_id),
	foreign key (type_id) references product_type(type_id)
);

create table transactions (
	transaction_id int primary key auto_increment,
	transaction_method varchar(50),
	transaction_amount float,
	transaction_date date
);

create table orders (
	
);



         ''')
 
# insert query to insert food  details in 
# the above table
 
 
print("All data in food table\n")
 
# create a cousor object for select query
 
# display all data from hotel table