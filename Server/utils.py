import mysql.connector
import random
from Server.mysqlconnection import *
from Server.user import *


def value_in_database(columnName, value) -> bool:
    cursor = cnx.cursor(dictionary=True)
    query = f"""SELECT * FROM UserData
        WHERE {columnName} = '{value}';"""
    cursor.execute(query)
    results = None
    try:
        results = cursor.fetchall()
    except mysql.connector.Error as err:
        pass
    cursor.close()
    return len(results) == 1

def get_token(username, hash) -> str:
    cursor = cnx.cursor(dictionary=True)
    query = f"""SELECT * FROM UserData
    WHERE username = '{username}' AND hash = '{hash}';"""
    cursor.execute(query)
    results = cursor.fetchall()
    if len(results) == 0:
        return ""

    cursor.close()
    return results[0]["token"]

def get_invite_code(token) -> str:
    cursor = cnx.cursor(dictionary=True)
    query = f"""SELECT invite_code FROM UserData
        WHERE token = '{token}';"""
    cursor.execute(query)
    results = cursor.fetchall()
    if len(results) == 0:
        return ""

    cursor.close()
    return results[0]["invite_code"]


def generate_token() -> str:
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    token = ""
    for i in range(50):
        token += random.choice(letters)
    return token

def generate_invite_code() -> str:
    numbers = "0123456789"
    invite_code = ""
    for i in range(10):
        invite_code += random.choice(numbers)
    return invite_code

def share_money_from(user : User):
    money = user.money
    organisator = User(cnx, "Organisator")
    organisator.money += money * 0.2
    money *= 0.8
    addingMoneyToUser : User = user.was_invited_by_user
    while addingMoneyToUser != organisator:
        addingMoneyToUser.money += money * 0.2
        money *= 0.8
        addingMoneyToUser = addingMoneyToUser.was_invited_by_user
    addingMoneyToUser.money += money
    user.money = 0