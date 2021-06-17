# Imports
import argparse
import csv
import datetime as dt
from datetime import date as date
import os
import operator
from types import new_class


# Do not change these lines.
__winc_id__ = 'a2bc36ea784242e4989deb157d527ba0'
__human_name__ = 'superpy'

#current_date = datetime.today().strftime('%Y-%m-%d')

header_bought       = ["product_id", "product_name", "buy_price", "buy_date", "exp_date"]
header_sold         = ["product_id", "bought_id",  "product_name", "sell_date", "sell_price"]

# one function to create needed csv files on load
def create_csv(name_csv, header):
    current_dir = os.getcwd() + ("/" + name_csv)
    if not os.path.exists(current_dir):
        with open(name_csv, 'w', newline='') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=header)
            csv_writer.writeheader()

# writes the data from the dictionary passed in through the buy function, to bought.csv 
def write_to_bought(bought_dict): # new_product_dict from buy function gets passed in
    with open('bought.csv', 'a', newline='') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=header_bought)
        csv_writer.writerow(bought_dict)

# writes the data from the dictionary passed in through the sell function, to sold.csv
def write_to_sold(sold_dict): # new_product_dict from sell function gets passed in
    with open('sold.csv', 'a', newline='') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=header_sold)
        csv_writer.writerow(sold_dict)

# opens bought.csv looks at current total line count
# increments total line count with 1 = id
# creates new dict from arguments passed in and adds id
# writes this data passed in by user to bought.csv
# writes the "amount" from the buy function to the same number of rows in bought.csv

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

# opens sold.csv looks at current total line count
# increments total line count with 1 = id
# creates new dict from arguments passed in, adds id + finds bought_id and adds that
# writes data passed in by user to sold.csv
# writes the "amount" from the sell function to the same number of rows in sold.csv

def sell(prod_name: str, sell_date: str, sell_price, amount):
    number_of_lines = 0
    with open('sold.csv', 'r') as csv_file:
        for line in csv_file:
            number_of_lines += 1

    id = number_of_lines

     
    new_product_dict = {
        "product_id": id,
        "bought_id": 0,
        "product_name": prod_name,
        "sell_date": sell_date,
        "sell_price": sell_price,
        
    }
    
    # makes sure product id is incremented by 1 for each row so each product has unique sold id
    # searches bought_id for each product and adds that to each product
    # calls write_to_sold, row created for each unique product 
    for number in range(amount):
        old_id = new_product_dict["product_id"]
        new_id = old_id + 1
        new_product_dict["product_id"] = new_id

        bought_id = find_product_id(prod_name, "bought.csv", (number + 1))

        new_product_dict["bought_id"] = bought_id

        write_to_sold(new_product_dict)

# variable bought_list gets the output (list) of get_bought() and sold_list gets the output (list) of get_sold() with the date passed into get_inventory
# checks if id bought_id in sold.csv is the same as product_id in bought_csv, if this is True it removes the product from from bought_list, this is the current inventory
# it then stores the function count_inventory which displays the current amount of all products in inventory in a variable called inv_list
# if user passes in argument "all" he gets complete inventory (up to and including passed in date)
# if user passes in argument "product" he gets the inventory for this product (up to and including passed in date)
def get_inventory(date, product):
    bought_list = get_bought(date)
    sold_list = get_sold(date)
    
    if len(sold_list) == 0:
        return(bought_list)
    
    for sold_product in sold_list:
        for bought_product in bought_list:
            if sold_product[1] == bought_product[0]:
                bought_list.remove(bought_product)

    inv_list = count_inventory(bought_list)

    if product == "all":
        print_dict(inv_list)
    elif type(product) == str:
        if product in inv_list:
            print_dict({product: inv_list[product]})
        else:
            print("Product not found.")        
    else:
        print("Format not correct.")

# HELPER FUNCTIONS
# finds bought id (in bought.csv) of the Nth product given to sell function
# return bought_id for each product
def find_product_id(product_name, csv, n):
    found = 0
    with open(csv, 'r') as csv_file:
        for list_item in csv_file:
            if product_name in list_item:
                found += 1
                if found == n:
                    li = list(list_item.split(","))
                    return li[0]

# reads bought.csv and skips header line
# looks for buy date (str) in line, stores this date as date-object
# compares buy date to date passed in as argument in get_inventory()
# if buy date is before or equal to date passed in, adds line to bought_list as list
# returns bought_list
def get_bought(date):
    date = dt.datetime.strptime(date, "%Y-%m-%d").date()
    bought_list = []

    with open('bought.csv', 'r') as csv_file:
        for line in csv_file:
            if "product_id" in line:
                continue
            line = line[:-1]
            buy_date = line.split(",")[3]
            buy_date2 = dt.datetime.strptime(buy_date, "%Y-%m-%d").date()

            if buy_date2 <= date:
                bought_list.append(line.split(","))
             
    return bought_list 

# reads sold.csv and skips header line
# looks for sell date (str) in line, stores this date as date-object
# compares sell date to date passed in as argument in get_inventory()
# if sell date is before or equal to date passed in, adds line to sold_list as list
# returns sold_list
def get_sold(date):
    date = dt.datetime.strptime(date, "%Y-%m-%d").date()
    sold_list = []

    with open('sold.csv', 'r') as csv_file:
        for line in csv_file:
            if "product_id" in line:
                continue
            line = line[:-1]
            sell_date = line.split(",")[3]
            sell_date2 = dt.datetime.strptime(sell_date, "%Y-%m-%d").date()

            if sell_date2 <= date:
                sold_list.append(line.split(","))

    return sold_list

# variable "list" is a list of the first elements of the lists in the bought_list, which is passed in via get_inventory()
# list items from list are stored in new_dict with their amount
# returns new_dict
def count_inventory(list1):
    list = [item[1] for item in list1]
    new_dict = {}

    for product in list:
        if product not in new_dict:
            count = list.count(product)
            new_dict[product] = count
    return new_dict        

def print_dict(dict):
    print(f"Product, Amount")
    for product, count in dict.items():
        print(f"{product}, {count}")
        
def expired():
    with open("bought.csv", "r") as csv_file:
        for line in csv_file:
            if "product_id" in line:
                continue
            exp_date = line.split(",")[4]
            breakpoint()

            exp_date2 = dt.datetime.strptime(exp_date, "%Y-%m-%d").date()
            

# run code    
def main():
    # create_csv("bought.csv", header_bought)
    # create_csv("sold.csv", header_sold)
    
    # buy("shampoobar", 1.32, "2021-6-16", "2025-3-02", 5)
    # buy("peanut", 0.03, "2021-6-16", "2030-3-02", 4)
    # buy("apple", 0.87, "2021-6-11", "2021-6-25", 7)
    # buy("shampoobar", 2.32, "2021-2-02", "2025-3-02", 10)

    # sell("shampoobar", "2021-6-17", 2.00, 3)
    # sell("peanut", "2021-6-17", 0.10, 1)
    # print(get_inventory("2021-6-16"))
    # print(get_inventory("2021-6-17"), len(get_inventory("2021-6-17")))
    # get_inventory("2021-6-17", 2)
    print(expired())
        

    
if __name__ == '__main__':
    main()
    

