import pymysql
import os
from tabulate import tabulate
from secret import *
conn = pymysql.connect(host=host, user=user, passwd= pword, database= "library")
cursor = conn.cursor()

def signup():
    t = False
    username = input("enter  username: ")
    while t==False:
        password = input("enter password: ")
        if len(password)>= 8:
            if any(char.islower() for char in password) and any(char.isupper() for char in password) and any(char.isdigit() for char in password):
                t = True
        else:
            print("invalid password, length must be min 8 characters with 1 capital letter, 1 small letter and 1 digit")
    t = False
    while t == False:
        cnfm = input("enter password again: ")
        if cnfm == password:
            t = True
        else:
            print("enter the same password")
    sql = "insert into users(username, password) values(%s, %s)"
    val = (username, password)
    try:
        cursor.execute(sql, val)
        conn.commit()
        print("user added successfully")
        s = useroradmin(username)
    except:
        print("failed to add user")
    return s


def login():
    t = False
    username = input("enter username: ")
    while t==False:
        password = input("enter password: ")
        if len(password)>=8:
            if any(char.islower() for char in password) and any(char.isupper() for char in password) and any(char.isdigit() for char in password):
                t = True
        else:
            print("invalid password, length must be min 8 characters with 1 capital letter, 1 small letter and 1 digit")
    sql = "select * from users"
    cursor.execute(sql)
    data = cursor.fetchall()
    t = False
    for i in data:
        if i[1] == username and i[2] == password:
            t = True
            break
    conn.commit()
    if t==True:
        print("log in successful")
        s = useroradmin(username)
        homescreen(username)
    else:
        ch = int(input("user not found\nenter 1 to login again 2 to sign up: "))
        if ch == 1:
            login()
        elif ch == 2:
            signup()
        else:
            print("enter a valid value")
            mainscreen()
    return s
    
# login()

def useroradmin(username):
    # based on admin 1 or 0 it will show the stuff
    admin = 0
    sql = "select * from users"
    cursor.execute(sql)
    data = cursor.fetchall()
    for i in data:
        if i[1] == username:
            if i[3] == 1:
                admin = 1
    return admin


# s = useroradmin("admin")
# print(s)

def mainscreen():
    print("library management system\n")
    ch = input("1. log in\n2. sign up: ")
    if ch.isdigit():
        if int(ch) == 1:
            login()
        elif int(ch) == 2:
            signup()
        else:
            print("enter a valid value")
            mainscreen()


def transactions(username):
    columns = "transactionid, bookid, title, username, date_issued, due_date, ifnull(return_date, 'Pending')"
    sql = "select {} from transactions where username = '{}'".format(columns, username)
    cursor.execute(sql)
    conn.commit()
    data = cursor.fetchall()
    header = ["Transaction ID", "Book ID", "Title", "Username", "Date of Issue", "Due Date", "Date of Return"]
    print(tabulate(data, headers = header))


def homescreen(username):
    os.system('cls')
    admin = useroradmin(username)
    # print(admin)
    if admin == 1:
        columns = "*"
        header = ["UserId", "Username", "Password", "Admin", "Total Books Borrowed"]
    else:
        columns = "username, password, total_books_borrowed"
        header = ["Username", "Password", "Total Books Borrowed"]
    sql = "select {} from users where username = '{}'".format(columns, username)
    cursor.execute(sql)
    conn.commit()
    data = cursor.fetchall()
    print(tabulate(data, headers = header))
    transactions(username)
    
# user screen show past transactions and current fees

mainscreen()