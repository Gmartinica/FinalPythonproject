# This is my Programming Principles I final project
# It is a program where you register a purchase with a Customer ID and the
# product, then the program recommends a product based on the Customer's
# preference and it also creates an email with the customer's name, in order
# to give another product recommendation.

# Made by Gabriel Martinica, December 2018

import csv
import random


def customer_file():
    """ This function converts the csv file into a dictionary"""
    with open("Customers.csv", 'r') as customer_file:
        reader = csv.reader(customer_file)
        # Create a dictionary, but skip the first line, which is the titles
        cust_dict = {row[0]: row[1] for row in reader if row[0].isdigit()}
        return cust_dict


def transaction_file():
    """This function converts the csv file into a list"""
    with open("Transactions.csv", 'r') as transaction_file:
        reader = csv.reader(transaction_file)
        # This creates a list skipping the columns by checking if there is a number
        transac_list = [row for row in reader if row[0].isdigit()]
        return transac_list


def categories_file():
    """This functions converts the csv file into a dictionary"""
    with open("Categories.csv", 'r', encoding='utf-8-sig') as categories_file:
        reader = csv.reader(categories_file)
        categories_dict = {row[0]: row[1] for row in reader}
        return categories_dict


def register_transac(customerID, product, categ_dict):
    """This function creates a new transaction"""
    purchase = []
    purchase.append(customerID)

    # This makes sure the product typed exists
    if product in categ_dict.keys():
        purchase.append(product)
    else:
        raise KeyError
    return purchase


def products_costumer(transac_list, cust_id):
    """This generates a list of products bought by the customer"""
    customer_purchases = [transaction[1] for transaction in transac_list if transaction[0] == cust_id]

    return customer_purchases


def customer_name(cust_dict, cust_id):
    """This function gets the name of the customer"""
    name = cust_dict[cust_id]

    return name


def customer_preferences(cust_id, categ_dict):
    """This function finds the customer's buying preferences"""
    global transac_list

    # Create a list of the products bought by the Customer
    customer_purchases = products_costumer(transac_list, cust_id)

    # I established a counter to find the customer preference, it works by
    # counting the number of times a category arises in the transaction lists
    # and then it finds the maximum value of the counters to find the preferred
    # category
    electronics_counter = 0
    food_counter = 0
    kitchen_counter = 0

    for purchase in customer_purchases:
        if categ_dict[purchase] == "Electronics":
            electronics_counter += 1
        elif categ_dict[purchase] == "Kitchen":
            kitchen_counter += 1
        elif categ_dict[purchase] == "Food":
            food_counter += 1
    preference = max(electronics_counter, food_counter, kitchen_counter)

    if preference == electronics_counter:
        return "Electronics"
    elif preference == kitchen_counter:
        return "Kitchen"
    elif preference == food_counter:
        return "Food"


def products_by_category(categ_dict):
    """This creates a list of the products by category"""
    electronics = []
    food = []
    kitchen = []

    for key, value in categ_dict.items():
        if value == "Electronics":
            electronics.append(key)
        elif value == "Food":
            food.append(key)
        elif value == "Kitchen":
            kitchen.append(key)
    products_category = {"Electronics": electronics, "Food": food, "Kitchen": kitchen}

    return products_category


def get_recommendation(preference, categ_dict, cust_id):
    """This gets a recommendation based on the customer's preference"""
    global transac_list

    categories = products_by_category(categ_dict)
    # This tries to get an item that the customer has not bought by searching
    # if the recommended product is already in the products bought by customer list
    if preference == "Electronics":
        # If the randomly chosen item is not already bought, return it
        while True:
            recommendation = random.choice(categories["Electronics"])
            if recommendation not in products_costumer(transac_list, cust_id):
                return recommendation
    elif preference == "Kitchen":
        while True:
            recommendation = random.choice(categories["Kitchen"])
            if recommendation not in products_costumer(transac_list, cust_id):
                return recommendation
    elif preference == "Food":
        while True:
            recommendation = random.choice(categories["Food"])
            if recommendation not in products_costumer(transac_list, cust_id):
                return recommendation


def update_transac_list(transaction):
    """This updates the transaction list by appending a list(ID, product)"""
    global transac_list
    transac_list.append(transaction)


def write_email(preference, categ_dict, cust_dictionary, cust_id):
    """This creates an email to the customer with a recommended product"""

    recommendation = get_recommendation(preference, categ_dict, cust_id)
    cust_name = customer_name(cust_dictionary, cust_id)

    return """
    Hello, {}:

    Thank you for visiting us! We’re glad that you found what you were
    looking for. It is our goal that you are always happy with what you
    bought from us, so please let us know if your buying experience was
    anything short of excellent.

    By the way, based on your buying preferences,
    here is a product that is selling hot:

    {}""".format(cust_name, recommendation)


def create_email_file(email):
    """This function creates a text file with the sample email"""
    with open("customer_email.txt", "w") as textfile:
        textfile.write(email)


def append_transac_file(purchase):
    """This function appends the new transaction to the csv file"""
    with open("Transactions.csv", "a") as transac_file:
        transac_file = csv.writer(transac_file)

        transac_file.writerow(purchase)


def main():
    print("""
    Welcome to this final project, I hope that you enjoy my
    recommendations and save a lot of time by not writing
    repetitive e-mails and dealing with boring stuff :)

    To register a purchase, please provide the Costumer ID and the product name
    -Gabriel Martinica""")
    # This creates the lists and dictionaries of the database

    cust_dict = customer_file()

    global transac_list

    transac_list = transaction_file()

    categ_dict = categories_file()

    while True:
        try:
            cust_id = input("What is the Customer ID? ")
            product = input("What is the product? ")

            # This gets customer's name

            cust_name = customer_name(cust_dict, cust_id)

            # This updates registers and updates the transactions database

            purchase = register_transac(cust_id, product, categ_dict)

            update_transac_list(purchase)

            # This gets the customer preferences

            cust_preference = customer_preferences(cust_id, categ_dict)

        except KeyError:
            print("The customer ID or the product name is wrong. Try again")
        else:
            break

    recommendation = get_recommendation(cust_preference, categ_dict, cust_id)

    # This prints a message for the seller, it says the name and preferences
    # of the customer, as well as a product recommendation

    print(
          "{} prefers {}, so you should recommend: {}".
          format(cust_name, cust_preference, recommendation))

    # Creates the email

    email = write_email(cust_preference, categ_dict, cust_dict, cust_id)

    create_email_file(email)

    append_transac_file(purchase)

    #///////////////////////////////////////////////////////////////////
    # Add a try except to avoid keyerrors due to an incorrect name of a product
    # or a product that does not exist in the database. Then, try to add a while
    # loop to register as many products as you want in the same time.


if __name__ == '__main__':
    main()
