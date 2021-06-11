# Imports
import argparse
import csv
from datetime import date, datetime
import os
import operator
import pandas as pd

# Do not change these lines.
__winc_id__ = 'a2bc36ea784242e4989deb157d527ba0'
__human_name__ = 'superpy'

current_date = datetime.today().strftime('%Y-%m-%d')

header_bought       = ["product_id", "product_name", "buy_price", "buy_date", "exp_date"]
header_inventory    = ["product_id", "product_name", "exp_date"]
header_sold         = ["product_id", "bought_id",  "product_name", "sell_date", "sell_price"]

# one function to create needed csv files on load
def create_csv(name_csv, header):
    current_dir = os.getcwd() + ("/" + name_csv)
    if not os.path.exists(current_dir):
        with open(name_csv, 'w', newline='') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=header)
            csv_writer.writeheader()

# writes the data from the dictionary passed in through the buy function, to bought.csv 
# writes the "amount" from the buy function to the same number of rows in bought.csv

def write_to_bought(bought_dict): # new_product_dict from buy function gets passed in
    with open('bought.csv', 'a', newline='') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=header_bought)
        csv_writer.writerow(bought_dict)
        

# writes the data from the dictionary passed in through the buy function, to inventory.csv
# writes the "amount" from the buy function to the same number of rows in inventory.csv
# TO DO: ids must increment by 1 (instead of all the same ids)

def write_to_inventory(bought_dict, amount): # product_dict_inv from buy function gets passed in
    for i in range(amount):
        with open('inventory.csv', 'a', newline='') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=header_inventory)
            csv_writer.writerow(bought_dict)

# writes the data from the dictionary passed in through the sell function, to sold.csv
# TO DO: convert the "amount" to the same number of rows in sold.csv
# TO DO: deletes the data from the dictionary passed in through the sell function, from inventory.csv 
def write_to_sold(sold_dict): # new_product_dict from sell function gets passed in
    with open('sold.csv', 'a', newline='') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=header_sold)
        csv_writer.writerow(sold_dict)

def buy(prod_name: str, buy_price: float, buy_date: str, exp_date: str, amount: int):
    number_of_lines = 0
    with open('bought.csv', 'r') as csv_file:
        for line in csv_file:
            number_of_lines += 1

    id = number_of_lines

    new_product_dict = {
        "product_id": id,
        "product_name": prod_name,
        "buy_price": buy_price,
        "buy_date": buy_date,
        "exp_date": exp_date,
    }
    for i in range(amount):
        old_id = new_product_dict["product_id"]
        new_id = old_id + 1
        new_product_dict["product_id"] = new_id
        write_to_bought(new_product_dict)

    product_dict_inv = {
        "product_id": id,
        "product_name": prod_name,
        "exp_date": exp_date,
   
    }
    
    write_to_inventory(product_dict_inv, amount)

def sell(prod_name: str, sell_date: str, sell_price, amount):
    number_of_lines = 0
    with open('sold.csv', 'r') as csv_file:
        for line in csv_file:
            number_of_lines += 1

    id = number_of_lines

    bought_id = find_product_id(prod_name, "inventory.csv")

    new_product_dict = {
        "product_id": id,
        "bought_id": bought_id,
        "product_name": prod_name,
        "sell_date": sell_date,
        "sell_price": sell_price,
        "amount": amount
    }

    write_to_sold(new_product_dict)

    #remove functie schrijven

def read_csv():
    output = []
    with open('bought.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        for line in reader:
            output.append(line)
    
    return output[1:]

def find_product_id(product_name, inventory):
    for list_item in inventory:
        if product_name in list_item:
            return list_item[0]

def sort_inventory_exp_date():
    inventory = pd.read_csv("inventory.csv")
    inventory["exp_date"] = pd.to_datetime(inventory["exp_date"], infer_datetime_format=True)
    inventory.sort_values(by="exp_date", ascending=True, inplace=True)

    return inventory
    
  
# run code    
def main():
    create_csv("bought.csv", header_bought)
    create_csv("inventory.csv", header_inventory)
    #create_csv("sold.csv", header_sold)
    
    buy("shampoobar", 2.32, "2021-02-02", "2025-03-02", 5)
    buy("peanut", 0.03, "2021-01-15", "2030-03-02", 4)
    buy("apple", 0.87, "2021-06-11", "2021-06-25", 7)
    # sell("apple", "2021-11-11", 2.00, 5)

    #print(read_csv())
    #sort_inventory_exp_date()

if __name__ == '__main__':
    main()
    

