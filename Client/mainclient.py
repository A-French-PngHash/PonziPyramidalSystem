from Client.hashing import *
import requests
import os
import sys

token = ""
invitation_code = ""
current_balance = 0


def welcome_message():
    print(
        "Welcome to the \"Hoped Programm\" where you can begin to earn money in juste a few days ! All you need to do"
        " is recruit other persons.")


def begin_menu():
    print("1. Register")
    print("2. Login")
    print("3. Quit")
    choice = input("Your choice : ")
    while choice not in "123":
        os.system("clear")
        print("1. Register")
        print("2. Login")
        print("3. Quit")
        choice = input("Your choice : ")
    if choice == "1":
        os.system('clear')
        register_user()
    elif choice == "2":
        os.system('clear')
        login()
    elif choice == "3":
        sys.exit()



def register_user():
    print(
        "Be aware than you need an invitation code of a friend to register so if you don't have one you won't be able "
        "to register...")
    print("You will need to buy an entry ticket before registering.")
    payment_process()
    do_register_request()


def payment_process():
    # In a real ponzi pyramidal service you would introduce some kind of payment here
    print("Confirm the payment of the entry ticket (10€) by pressing Y.")
    letter = input()
    while letter.lower() != "y":
        letter = input()
    os.system('clear')
    print("Bravo ! Now you can access the system and you will soon be able to begin making some money.")


def read_error_if_one(response):
    if response.status_code != 200:
        # Error happend, explanation of the error can be found in the error field of the respons if
        # the error was raised by the server
        json_response = response.json()
        print(f"Oups, there was an error (error code {response.status_code}) : ")
        if "error" in json_response.keys():
            print(json_response["error"])
        else:
            print(json_response)

        return True

    return False


def do_register_request():
    username = input("Please enter the username you want to use, please note that this must be a unique username : ")

    os.system('clear')
    print(f"Username : {username}")

    password = input(
        "Now enter a password. This password will be strongely encrypted but even with this encryption hackers can "
        "hack your password and steal all your revenues so please choose a strong password : ")

    os.system('clear')
    print(f"Username : {username}")
    print(f"Password : {password}")

    invitation_code = input("As said earlier you need to have an invitation code, please input it here : ")

    os.system('clear')
    print(f"Username : {username}")
    print(f"Password : {password}")
    print(f"Invitation Code : {invitation_code}")

    print("Thank you, your account is being created.")

    hashed_password = hash_password(password, username)

    response = requests.put("http://127.0.0.1:5002/login", params={
        "username": username,
        "hash": hashed_password,
        "invited_by": invitation_code
    })

    os.system('clear')

    json_response = response.json()

    if not read_error_if_one(response):
        print("Vous etes bien inscrit ! ")
        global token
        token = json_response["token"]


def login():
    username = input("Please enter your username : ")
    password = input("Please enter your password : ")
    password = hash_password(password, username)

    response = requests.get("http://127.0.0.1:5002/login", params={
        "username": username,
        "hash": password
    })
    os.system('clear')

    json_response = response.json()

    if not read_error_if_one(response):
        print("You logged in succesfully ! ")
        global token
        token = json_response["token"]


def get_invite_code():
    response = requests.get("http://127.0.0.1:5002/invite", headers={"Authentication": token})
    if response.status_code != 200:
        read_error_if_one(response)
        return None
    json = response.json()
    return json["invite_code"]

def get_current_balance():
    response = requests.get("http://127.0.0.1:5002/money", headers={"Authentication": token})
    if response.status_code != 200:
        read_error_if_one(response)
        return None
    json = response.json()
    return json["balance"]

def retrieve_money():
    amount = 0
    while amount == 0:
        try:
            os.system('clear')
            amount = int(input("How much do you want to retrieve : "))
        except:
            amount = 0
            print("Please enter a number")

    response = requests.get("http://127.0.0.1:5002/money", headers={"Authentication": token}, params={"amount" : amount})
    if response.status_code != 200:
        read_error_if_one(response)
        return None
    json = response.json()
    global current_balance
    print(f"{json['amount']}$ were succesfully retrieved ! You now have {round(current_balance - int(json['amount']), 2)}")


def logged_menu():
    global invitation_code
    global token
    global current_balance
    print(f"Your code to invite friends : {invitation_code}")
    print(f"Your current balance : {current_balance}$")
    print("-------------------")
    print("1. Disconnect")
    print("2. Retrieve money")

    choice = input()
    os.system("clear")

    while choice not in "12":
        os.system("clear")
        print(f"Your code to invite friends : {invitation_code}")
        print(f"Your current balance : {current_balance}$")
        print("-------------------")
        print("1. Disconnect")
        print("2. Retrieve money")
        choice = input()

    if choice == "1":
        token = ""
    elif choice == "2":
        retrieve_money()

def main_loop():
    welcome_message()
    while True:
        global token
        while token == "":
            begin_menu()

        global invitation_code
        invitation_code = get_invite_code()
        global current_balance
        current_balance = get_current_balance()


        logged_menu()


main_loop()
