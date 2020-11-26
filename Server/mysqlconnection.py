import mysql.connector
cnx = mysql.connector.connect(
    user="root",
    password="password",
    host="localhost",
    database='PonziDB',
    use_pure=True)
cnx.autocommit = True