import sys

import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", password="", database="bank_management")


# WELCOMING TYPE MESSAGE

def welcome():
    print("""
        A hearty welcome to the bank. We always take care of our client's requirement. You have to follow some guidelines, to avoid last time rush.
        1. Minimum Rs. 1000 is required to open the account
        2. You must have original id proof (Aadhar card)
    """)
    print("*" * 250)
    agreement()


# SELECTION OF MOVING FORWARD

def agreement():
    agg = input("Select 1 to move forward with us \nselect any key to exit ")

    if agg == "1":
        print()
        intro()
    else:
        print("Thanks for contacting us")
        sys.exit(0)


# SELECTION OF CHOICE

def intro():
    print("""How would you like to proceed?
            Press '1' to  create  your account
            Press '2' to deposit money
            Press '3' to withdraw money
            Press '4' to check balance
            Press '5' to display details
            Press '6' to update pin
            Press '7' to close your account
            Press any other key to exit
             """)
    user_menu()


# CREATING THE ACCOUNT

def create():

    name = input("Enter your name: ")
    accnumber = input("Enter your account number: ")
    a = 'select  * from account where accno=%s'
    data = (accnumber,)
    x = mydb.cursor()
    x.execute(a, data)
    res = x.fetchone()

    if res:

        print("Account  exists")

    else:

        pin = input("Enter your pin: ")
        confirm_pin = input("Please confirm your pin: ")

        if pin != confirm_pin:

            print("Password does not match")

        else:

            adhar_number = input("Enter your aadhar number: ")
            address = input("Enter your address: ")
            openingBalance = input("Enter your opening balance: ")

            if int(openingBalance) < 1000:

                print("Minimum Rs. 1000 is required to open the account")

            else:

                data1 = (name, accnumber, adhar_number, address, openingBalance, pin)
                data2 = (accnumber, openingBalance, pin)
                sql1 = ('insert into account values (%s,%s,%s,%s,%s,%s)')
                sql2 = 'insert into amount  values (%s,%s,%s)'
                x = mydb.cursor()
                x.execute(sql1, data1)
                x.execute(sql2, data2)
                mydb.commit()
                print("Account Created by the name of " + name)

    intro()


def deposit():

    amount = input("Enter the amount you want to deposit ")
    acno = input("Enter the account number ")
    a = 'select balance from amount where accno=%s'
    data = (acno,)
    x = mydb.cursor()
    x.execute(a, data)
    res = x.fetchone()

    if res:

        t = res[-1] + int(amount)
        sql = ('update amount set balance=%s where accno=%s')
        d = (t, acno)
        x.execute(sql, d)
        mydb.commit()
        print("Amount successfully deposited")

    else:

        print("Account does not exist")

    intro()


def withdraw():

    amount = input("Enter the amount you want to withdraw ")
    acno = input("Enter the account number ")
    a = 'select balance from amount where accno=%s'
    data = (acno,)
    x = mydb.cursor()
    x.execute(a, data)
    res = x.fetchone()

    if res:
        t = res[-1] - int(amount)

        if t < 0:

            print("You have " + str(res[-1]) + " in your account")

        else:

            sql = ('update amount set balance=%s where accno=%s')
            d = (t, acno)
            x.execute(sql, d)
            mydb.commit()
            print("Amount successfully withdrawn")

    else:

        print("Account does not exist")

    intro()

def check_balance():

    ac = input("Enter the account number ")
    a = 'select * from amount where accno=%s'
    data = (ac,)
    x = mydb.cursor()
    x.execute(a, data)
    res = x.fetchone()

    if res:

        print("Balance for account:", ac, "is", res[-2])

    else:

        print("Account does not exist")

    intro()

def DisDetails():

    ac = input("Enter the account number ")
    a = 'select  name,accno,address from account where accno=%s'
    data = (ac,)
    x = mydb.cursor()
    x.execute(a, data)
    res = x.fetchone()

    if res:

        for i in res:

            print(i)

    else:

        print("Account does not exist")

    intro()


def update_password():

    ac = input("Enter the account number ")
    a = 'select * from amount where accno=%s'
    data = (ac,)
    x = mydb.cursor()
    x.execute(a, data)
    res = x.fetchone()

    if res:

        old_pin = input("Enter the last pin: ")
        db_pin = 'select pin from account where accno=%s'
        data = (ac,)
        x = mydb.cursor()
        x.execute(db_pin, data)
        res = x.fetchone()

        if res:

            for i in res:

                if i == old_pin:
                    print("You can now change your pin")
                    new_pin = input("Enter the new pin: ")
                    new_pin_sql = 'update account set pin=%s WHERE accno=%s'
                    new_pin_sql1= 'update amount set pin=%s WHERE accno=%s'
                    data1 = (new_pin, ac)
                    data2=(new_pin, ac)
                    x = mydb.cursor()
                    x.execute(new_pin_sql, data1)
                    x.execute(new_pin_sql1,data2)
                    mydb.commit()
                    print("Pin changed successfully")

                    intro()

                else:

                    print("Your old pin does not match  ")

                    update_password()


    else:

        print("Account does not exists")

        create()


def CloseApp():

    ac = input("Enter the account number ")
    a = 'select  * from account where accno=%s'
    data = (ac,)
    x = mydb.cursor()
    x.execute(a, data)
    res = x.fetchone()

    if res:

        sql1 = 'delete from account where accno=%s'
        sql2 = 'delete from amount where accno=%s'
        data = (ac,)
        x = mydb.cursor()
        x.execute(sql1, data)
        x.execute(sql2, data)
        mydb.commit()

    else:

        print("Account does not exits")

    user_menu()


def user_menu():

    user_input = input("Enter the task you want to perform: ")

    if user_input == "1":

        create()

    elif user_input == "2":

        deposit()

    elif user_input == "3":

        withdraw()

    elif user_input == "4":

        check_balance()

    elif user_input == "5":

        DisDetails()

    elif user_input == "6":

        update_password()

    elif user_input == "7":

        CloseApp()

    else:

        print("Have a nice day!!!")

        sys.exit(0)


welcome()
