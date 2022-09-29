# TODO THE DATE THING FOR SAVINGS ACCOUNTS
# ############################################
#      python banking system assignment
#              Matthew Tweedy
#                C20381946
# ############################################

# ============================================
# Global Variables
# ============================================
CUSTOMERS = "customers.txt"
ACCOUNTS = "accounts.txt"
TRANSACTIONS = "accountsTransactions.txt"
LINE_LENGTH = 64
MENU_LINE = "----------------------------------------------------------------"
choice = 0


# ============================================
# Custom Functions
# ============================================
def auto_center(spacing: str, msg, underline):
    """
    This function takes a set length and calculates the padding amount to display a title or text centered underneath a line of "-"s
    """
    # Takes the difference from the set length and the text to display and divides that by 2.
    # Also converts to an int as there could be decimals otherwise which won't work
    padding = int((LINE_LENGTH - spacing.__len__()) / 2)
    padding_amount = ""
    top = ""

    # adds defined amount of "-"s to top and prints it
    for i in range(0, LINE_LENGTH):
        top += "-"

    # adds calculated amount of padding before and after the text
    for i in range(0, padding):
        padding_amount += " "

    print(top)
    print(f"{padding_amount}{spacing}{padding_amount}\n")

    if msg != "":
        print(msg)

    if underline == 1:
        print(top)

    # returns string with "-"s so __str__ can return and finish off print for example
    return top

def printAccounts():
    """This file prints a list of Accounts to transfer to"""

    accounts_read = open(ACCOUNTS, "r")
    num = num_filelines(accounts_read)
    aType = ""
    list_avail_to_transfer = []

    for i in range(num):
        # grabs the information for each account line by line and stores it in list account_info[]
        account_info = getInfo(ACCOUNTS, i)
        customer_info = getInfo(CUSTOMERS, account_info[1])

        if account_info[2] == "savings":
            aType = "Savings  "
        elif account_info[2] == "checkings":
            aType = "Checkings"

        # only prints the account if it is not closed
        if account_info[4] != "1":
            print(f"\tAccount id : {account_info[0]} | {aType} | Customer : {customer_info[1]}")
            list_avail_to_transfer.append((account_info[0]))

    return list_avail_to_transfer


def num_filelines(filename):
    """This function opens a file, count all the lines in it and returns this number."""
    line_count = 0
    for line in filename:
        # if the line isn't empty/a newline character increase the number of lines
        if line != "\n":
            line_count += 1
    filename.close()
    return line_count


def getInfo(filename, id):
    """
    This function goes line by line, splits the strings by ','s and adds the elements to a list.
    If the list element index 0 is equal to the id passed then this is the right information for the cust/acc.
    Finally, returns this list.
    """
    customer_info = []
    f = open(filename, "r")
    for line in f:
        # removes any trailing whitespace from the line and divides line when it finds ","s
        customer_info = line.strip().split(",")
        if customer_info[0] == str(id):
            return customer_info


# ============================================
# Class Definitions
# ============================================

# ============================================
# Exception Classes

# these are used to be called upon when an error they describe has occured
class BalanceTooLow(Exception):
    """Balance too low in acount"""
class CreditTooLow(Exception):
    """Credit too low in account"""
class InvalidTransfer(Exception):
    """Transfer was disallowed"""

# ============================================
# Definition for Customer Class
class Customer(object):
    """
    Customer Class that contains the attributes required to fully manipulate and describe a customer.
    Defines the method addCustomer()

    addCustomer() creates a new instance of the Customer class and writes its information to customers.txt
    """

    def __init__(self, custID, name="", age=0) -> (None):
        self.custID = custID
        self.name = name
        self.age = age

    def __str__(self) -> (str):
        return f"\nCustomer\nName    : {self.name}\nID      : {self.custID}"

    # Creating Customer
    def addCustomer(self, file=CUSTOMERS):
        # read how many lines are in the file so we can make the new custID (custID's are 0 indexed)
        f = open(file, "r")
        num = num_filelines(f)
        f.close()
        f = open(file, "a")

        # setting custID to the new value
        self.custID = num

        # write new customer object info to file
        customer_account = f"\n{num},{self.name},{self.age}"
        f.write(customer_account)
        f.close()


# ============================================

# ============================================
# Definition for Account Class
class Account(object):
    """Base Account Class"""

    # ensures _custID is an int
    _custID : int
    # makes custID a protected variable
    @property
    def custID(self):
        return self._custID
    @custID.setter
    def custID(self, value):
        self._custID = value

    # ensures _balance is an int
    _balance : int
    # makes balance a protected variable
    @property
    def balance(self):
        return self._balance
    @balance.setter
    def balance(self, value):
        self._balance = value 

    def __init__(self, accID, custID, accType="", balance=0, closed=0):
        self.custID = custID
        self.accID = accID
        self.accType = accType
        self.balance = balance
        self.closed = closed

    def __str__(self):
        # displays relevant information about account
        string = f"\tAccount ID      : {self.accID}\n\tAccount Type    : {self.accType}\n\tAccount Balance : {self.balance}"
        top = auto_center("Account Info", string, 0)
        return top

    def addAccount(self, file=ACCOUNTS):
        # read how many lines are in the file so we can make the new custID (custID's are 0 indexed)
        f = open(file, "r")
        num = num_filelines(f)
        f.close()

        # sets accID to new value
        self.accID = num

        # write new customer object info to file
        f = open(file, "a")
        account = f"{num},{self.custID},{self.accType},{self.balance},{self.closed}\n"
        f.write(account)
        f.close()

    def deposit(self, amount, transaction):
        # ensures transaction is a Transaction class object
        transaction : Transaction = transaction

        # sets current string that will be replaced
        acc_string = (f"{self.accID},{self.custID},{self.accType},{self.balance},{self.closed}")
        # tries to increase balance by the deposit amount
        try:
            self.balance = self.balance + int(amount)
        # if balance runs into the BalanceTooLow exception (it shouldn't but safe to have)
        except BalanceTooLow:
            return BalanceTooLow
        # same for CreditTooLow
        except CreditTooLow:
            return CreditTooLow
        # open account file to read lines for the deposit
        f = open(ACCOUNTS, "r")
        lines = f.read()
        # set new string to replace current string with
        new_acc_string = f"{self.accID},{self.custID},{self.accType},{self.balance},{self.closed}"
        lines = lines.replace(acc_string, new_acc_string)
        f.close()

        # write the changes
        f = open(ACCOUNTS, "w")
        f.write(lines)
        f.close()

        # if the transaction isn't empty, read and write the transaction
        if transaction is not None:
            f2 = open(TRANSACTIONS, "r")
            num = num_filelines(f2)
            self.transacID = num
            f2.close()

            f2 = open(TRANSACTIONS, "a")
            transac = transaction.line_generate(num)
            f2.write(transac)
            f2.close()
            return True
        else:
            return True

    def withdraw(self, amount, transaction):
        acc_string = (f"{self.accID},{self.custID},{self.accType},{self.balance},{self.closed}")
        try:
            # tries to decrease balance by the withdraw amount
            self.balance = self.balance - int(amount)
        except BalanceTooLow:
            return BalanceTooLow
        except CreditTooLow:
            return CreditTooLow
        # open account file to read lines for the withdraw
        f = open(ACCOUNTS, "r")
        lines = f.read()
        new_acc_string = (f"{self.accID},{self.custID},{self.accType},{self.balance},{self.closed}")
        lines = lines.replace(acc_string, new_acc_string)
        f.close()

        # write the changes
        f = open(ACCOUNTS, "w")
        f.write(lines)
        f.close()

        # if the transaction isn't empty, read and write the transaction
        if transaction is not None:
            f2 = open(TRANSACTIONS, "r")
            num = num_filelines(f2)
            self.transacID = num
            f2.close()

            f2 = open(TRANSACTIONS, "a")
            transac = transaction.line_generate(num)
            f2.write(transac)
            f2.close()
            return True
        else:
            return True

    def transfer(self, amount, receive, transaction):
        f = open(TRANSACTIONS, "r")
        num = num_filelines(f)
        self.transacID = num
        f.close()

        # withdraw from sender account
        withdraw_state = self.withdraw(amount, None)
        if withdraw_state == True:
            pass
        elif withdraw_state == BalanceTooLow:
            print("\tERROR: balance too low")
            return InvalidTransfer
        elif withdraw_state == CreditTooLow:
            print("\tERROR: credit too low")
            return InvalidTransfer
        
        # deposit into target account
        receive.deposit(amount, None)

        f = open(TRANSACTIONS, "a")
        transac = transaction.line_generate(num)
        f.write(transac)
        f.close()
        return True

    def displayTransactions(self):
        # how many lines are in the file
        f = open(TRANSACTIONS, "r")
        num = num_filelines(f)
        num_transactions = 0
        
        # find list of transaction ids that contain customer's accID
        list_of_transactions = []

        for i in range(num):
            # grabs info of transaction id = i and stores in list
            transac_info = getInfo(TRANSACTIONS, i)
            if transac_info[1] == str(self.accID) or transac_info[4] == str(self.accID):
                num_transactions += 1
                list_of_transactions.append((transac_info[0]))

        # if num_transactions is 0 we know that the account has no transactions
        if num_transactions == 0:
            print("\tERROR: account has made no transactions")
        else:
            top = auto_center("Account Transactions", "", 0)
            # otherwise, we iterate through list of ids 
            for j in list_of_transactions:
                # grab the information for the id matching transaction
                transac_info = getInfo(TRANSACTIONS, j)
                # make instance of a transaction and fill with the information
                transac = Transaction(transac_info[2], int(transac_info[0]), int(transac_info[1]), int(transac_info[4]), int(transac_info[3]))
                # and print the info contained within each transaction by calling __str__
                print(transac)
            print(top)

    def deleteAccount(self):
        # setting the current string that will be searched for in the file
        acc_string = (f"{self.accID},{self.custID},{self.accType},{self.balance},{self.closed}")

        # open file to read lines
        f = open(ACCOUNTS, "r")
        lines = f.read()
        # update the attribute of closed to 1 to indicate the account is now closed
        self.closed = "1"
        # update the string with the new value of closed
        new_acc_string = (f"{self.accID},{self.custID},{self.accType},{self.balance},{self.closed}")
        # find the old string in the file and replace with the new string
        lines = lines.replace(acc_string, new_acc_string)
        f.close()

        # open file to write
        f = open(ACCOUNTS, "w")
        f.write(lines)
        f.close()

    # prints the balance of the user's current account they have selected
    def showBalance(self):
        string = f"\tCurrent Balance : {self.balance}"
        return print(string)


# ============================================

# ============================================
# Definition for Savings Account SubClass
class SavingsAccount(Account):
    """
    Savings Account Sub Class
    Inherits all methods and attributes from the Account parent class.
    Sets the account type attribute to "savings" to ensure it is a savings account
    """

    # make balance a protected variable
    @property
    def balance(self):
        return super().balance
    @balance.setter
    def balance(self, value):
        # perform checks on balance before it is set so we can raise any exceptions if conditions met
        if(value < 0):
            # if the value is less than 0, the balance won't change and exception raised
            self._balance = self._balance 
            raise BalanceTooLow
        else:
            # else set balance to the value
            self._balance = value

    # initialises savings account attributes
    def __init__(self, accID=0, custID=0, accType="savings", balance=0, closed=0):
        super().__init__(accID, custID, accType, balance, closed)

    # displays current savings account information
    def __str__(self):
        string = f"\tAccount ID      : {self.accID}\n\tAccount Type    : {self.accType}\n\tAccount Balance : {self.balance}"
        top = auto_center("Savings Account Info", string, 0)
        return top


# ============================================

# ============================================
# Definition for Checkings Account SubClass
class CheckingsAccount(Account):
    """
    Checkings Account Sub Class
    Inherits all methods and attributes from the Account parent class.
    Sets the account type attribute to "checkings" to ensure it is a checkings account
    """

    CREDIT_LIMIT = 300

    # make balance a protected variable
    @property
    def balance(self):
        return super().balance
    @balance.setter
    def balance(self, value):
        # if the value passed is less that the credit limit (-300) then balance is not updated
        # and CreditTooLow is raised
        if(value < -(self.CREDIT_LIMIT)):
            self._balance = self._balance 
            raise CreditTooLow
        # otherwise balance is set to the new value
        else:
            self._balance = value

    # initialises checkings account attributes
    def __init__(self, accID=0, custID =0,  accType="checkings", balance=0, closed=0):
        super().__init__(accID, custID, accType, balance, closed)

    # displays current checkings account information
    def __str__(self):
        string = f"\tAccount ID      : {self.accID}\n\tAccount Type    : {self.accType}\n\tAccount Balance : {self.balance}"
        top = auto_center("Checkings Account Info", string, 0)
        return top


# ============================================

# ============================================================
# Definiton for Transaction Account
class Transaction(object):
    """Transaction Class that stores information like the transaction type, who its going to, where from and how much money."""

    def __init__(self, transacType = "deposit", transacID=0, accid=0 , acc_receive_ID=0, amount=0):
        self.id = transacID
        self.transaction_type = transacType
        self.acc_id = accid
        self.amount = amount
        self.rec_acc = acc_receive_ID

    # method to generate the transaction line to be written to file
    def line_generate(self, id):
        return f"{id},{self.rec_acc},{self.transaction_type},{self.amount},{self.acc_id}\n"

    # displays current transaction information
    def __str__(self):
        if self.transaction_type == "deposit":
            transac_type = "Deposit  "
        elif self.transaction_type == "withdraw":
            transac_type = "Withdraw "
        elif self.transaction_type == "transfer":
            transac_type = "Transfer "
        string = f"{transac_type} | To : Account({self.acc_id}) | From : Account({self.rec_acc}) | Amount : {self.amount} "
        return string

# ============================================



def main_menu():
    """
    This function displays the main menu and calls different menu functions depending on user's choice.
    Handles input validation on the user's input so function doesn't crash if tehy input character's for example.
    """

    auto_center("Menu", "", 0)
    print("\t1. Login to Customer Account")
    print("\t2. Create Customer Account")
    print("\t3. Exit\n")
    while True:
        # prompts for user input
        choice = input("\tChoice : ")
        # if their input is a number, cast to int
        if choice.isnumeric():
            choice = int(choice)

            if choice == 1:
                # if user chooses option 1, calls login_menu() which returns their selected ID
                choice_id = login_menu()
                # if an id was returned, or if the id returned was 1
                if choice_id or choice_id == 1:
                    # "logs in" the user with their selected it by calling loggedin_menu()
                    loggedin_menu(choice_id)
                    break
                # if the id returned from login_menu() was 0. this means they chose the first customer
                elif choice_id == 0:
                    loggedin_menu(choice_id)
                    break
                else:
                    pass

            elif choice == 2:
                # if the user chooses to create a new customer, calls register_menu()
                choice_id = register_menu()
                # if an id is returned, "logs in" user with their new customer id (custID)
                if choice_id:
                    loggedin_menu(choice_id)

            elif choice == 3:
                # if the user chooses to exit the program
                auto_center("Goodbye", "", 1)
                exit()

            else:
                # if the user enters a number but not a valid option
                print("\tERROR: invalid choice\n")
        else:
            # if the user's input is not numeric (characters)
            print("\tERROR: invalid input")
        break


def loggedin_menu(menu_id):
    """This function displays the menu and performs the options when the user is logged in."""
    # collect all cust information with id = id
    customer_info = getInfo(CUSTOMERS, menu_id)

    # resets monthly transactions
    monthly_transaction = 0

    # store in new customer object
    customer = Customer(int(customer_info[0]), customer_info[1], int(customer_info[2]))
    while True:
        auto_center(f"Logged in as {customer.name} id({menu_id})", "", 0)
        print("\t1. Create New Account")
        print("\t2. Select an Account")
        print("\t3. Logout")

        choice = input("\n\tChoice : ")
        if choice.isnumeric():
            choice = int(choice)

            # CREATE ACCOUNT SUB-MENU
            if choice == 1:
                # display create account sub-menu
                auto_center("Create Account", "", 0)
                print("\n\t1. Savings Account")
                print("\t2. Checkings Account")
                print("\t3. Go back to Menu")
                while True:
                    try:
                        # try asking for an input that is an int
                        createAcc_choice = int(input("\n\tChoice : "))
                    except ValueError:
                        # if the ValueError exception is raised, input wasn't an int
                        print("\tERROR: invalid input")
                        # go back to start of loop to ask for input again
                        continue
                    else:
                        break

                # CREATE A SAVINGS ACCOUNT
                if createAcc_choice == 1:
                    # if the customer's age is less than 14 they aren't allowed create a savings account
                    if customer.age < 14:
                        print("\tYou must be 14 or older to do this")
                        break
                    else:
                        # create a new savings account with the custID of the current logged in user
                        new_account = SavingsAccount(custID=menu_id)
                        # writes new savings account to account file (accounts.txt)
                        new_account.addAccount()
                        print("\tSavings account successfully created")

                # CREATE A SAVINGS ACCOUNT
                elif createAcc_choice == 2:
                    # if the customer's age is less than 18 they aren't allowed create a checkings account
                    if customer.age < 18:
                        print("\tYou must be 18 or older to do this")
                        break
                    else:
                        # same as creating new savings account
                        new_account = CheckingsAccount(custID=menu_id)
                        # writes new checkings account to account file (accounts.txt)
                        new_account.addAccount()
                        print("\tCheckings account successfully created")

                # EXIT MENU
                elif createAcc_choice == 3:
                    break
                # if user input was a number but not a valid choice/option
                else:
                    print("\tERROR: invalid choice")

            # SELECT ACCOUNT SUB-MENU
            elif choice == 2:
                accounts_read = open(ACCOUNTS, "r")
                num = num_filelines(accounts_read)
                num_match_accounts = 0
                list_of_matches = []
                aType = ""  # account type, either Savings or Checkings
                ids = ""

                # this finds the number of accounts that have a matching id
                for i in range(num):
                    # grabs the info of the account with id = current i value
                    account_info = getInfo(ACCOUNTS, i)
                    # if the element 1 in account_info is the same as the current user's custID
                    if account_info[1] == str(menu_id):
                        # we know know this account belongs to our user
                        num_match_accounts += 1
                        # add the id of the account to the list of matches
                        list_of_matches.append((account_info[0]))

                # this is used to show the ids for the user to select from, grabbed from the list of matches
                for j in list_of_matches:
                    ids += str(j) + ","
                # removes the last "," so it is clean
                ids = ids.strip(",")

                if num_match_accounts == 0:
                    # displays a message dispay no ids to select if there are no matches
                    auto_center(f"Select from {customer.name}'s Accounts", "", 0)
                else:
                    # displays a message containg all the ids for user to select from (their account ids)
                    auto_center(f"Select from {customer.name}'s Accounts : ids({ids})", "", 0)
                # print only the accounts with a matching accID
                for i in range(num):
                    # grabs the information for each account line by line and stores it in list account_info[]
                    account_info = getInfo(ACCOUNTS, i)

                    # checks if the custID stored in account_info[] matches the current logged in user's id
                    if account_info[1] == str(menu_id):
                        if account_info[2] == "savings":
                            aType = "Savings  "
                        elif account_info[2] == "checkings":
                            aType = "Checkings"

                        # displays accounts to choose from and if its closed or not
                        if account_info[4] == "0":
                            # if the closed attribute for the account is 0, it is open
                            print(f"\t{aType} | Account id : {i} | Balance : {account_info[3]}")
                        else:
                            # if the closed attribute for the account is not 0, it is 1 which means its closed
                            # displays message saying the account is closed
                            print(f"\t{aType} | Account id : {i} | Balance : {account_info[3]} | *CLOSED*")

                # if the customer has no accounts
                if num_match_accounts == 0:
                    print("\tERROR: user has no accounts")
                # if the customer DOES have accounts
                else:
                    exit_loop = 0
                    while exit_loop != 1:
                        acc_choice = input("\n\tid : ")
                        if acc_choice.isnumeric():
                            acc_choice = int(acc_choice)
                        else:
                            print("\tERROR: invalid input")
                            break
                        # if the account id entered is found in the list of users account ids
                        if acc_choice >= 0 and acc_choice <= num - 1:
                            
                            # if the users entered id is in the list of all their accounts
                            if str(acc_choice) in list_of_matches:
                                account_info = getInfo(ACCOUNTS, acc_choice)

                                # if the user trys to select an open account
                                if account_info[4] != "1":
                                    
                                    if account_info[2] == "savings":
                                        aType = "Savings"
                                        account = SavingsAccount(
                                            int(account_info[0]),
                                            int(account_info[1]),
                                            str(account_info[2]),
                                            int(account_info[3]),
                                            int(account_info[4])
                                        )

                                    elif account_info[2] == "checkings":
                                        aType = "Checkings"
                                        account = CheckingsAccount(
                                            int(account_info[0]),
                                            int(account_info[1]),
                                            str(account_info[2]),
                                            int(account_info[3]),
                                            int(account_info[4])
                                        )

                                    auto_center(f"{customer.name}'s {aType} Account id({account.accID})", "", 0)
                                    print("\t1. Display Account Details")
                                    print("\t2. View Balance")
                                    print("\t3. Deposit")
                                    print("\t4. Withdraw")
                                    print("\t5. Transfer")
                                    print("\t6. View Transactions")
                                    print("\t7. Close Account")
                                    print("\t8. Exit")
                                    while exit_loop != 1:
                                        accMenu_choice = input("\n\tChoice : ")
                                        if accMenu_choice.isnumeric():
                                            accMenu_choice = int(accMenu_choice)

                                            if accMenu_choice == 1:
                                                # if user chooses to view account details
                                                print(account)

                                            elif accMenu_choice == 2:
                                                # if user chooses to view balance
                                                account.showBalance()

                                            elif accMenu_choice == 3:
                                                # if user chooses to deposit
                                                amount = input("\tDeposit amount : ")
                                                if amount.isnumeric():
                                                    # create new instance of Transaction with all details
                                                    transac = Transaction("deposit", 0, account.accID, account.accID, amount)
                                                    # call deposit() method to update the balance and write transaction to file
                                                    account.deposit(amount, transac)
                                                    print(f"\tDeposited {amount} Successfully")
                                                else:
                                                    # if the amount isn't numeric
                                                    print("\tERROR: invalid amount")

                                            elif accMenu_choice == 4:
                                                # if user chooses to withdraw

                                                # if savings account, we need to implement increasing how many withdraws/transfers the user has made in a "month"
                                                # counting a user fully logging out and logging back into their customer as a month passing
                                                if account.accType == "savings":

                                                    if monthly_transaction == 0:
                                                        monthly_transaction += 1
                                                        amount = input("\tWithdraw amount : ")

                                                        if amount.isnumeric():
                                                            # create new instance of Transaction with all details
                                                            transac = Transaction("withdraw", 0, account.accID, account.accID, amount)
                                                            # call withdraw() method to update the balance and write transaction to file
                                                            withdraw_state = account.withdraw(amount, transac)

                                                            # check the state after the withdraw() 
                                                            if withdraw_state == True:
                                                                print(f"\tWithdrew {amount} Successfully")
                                                                pass
                                                            elif withdraw_state == BalanceTooLow:
                                                                print("\tERROR: balance too low.")
                                                            elif withdraw_state == CreditTooLow:
                                                                print("\tERROR: credit too low")
                                                        else:
                                                            # if the amount isn't numeric
                                                            print("\tERROR: invalid amount")
                                                        pass
                                                    else:
                                                        print("\tERROR: account has exceeded montly allowed transactions")

                                                elif account.accType == "checkings":
                                                    amount = input("\tWithdraw amount : ")

                                                    if amount.isnumeric():
                                                        # create new instance of Transaction with all details
                                                        transac = Transaction("withdraw", 0, account.accID, account.accID, amount)
                                                        # call withdraw() method to update the balance and write transaction to file
                                                        withdraw_state = account.withdraw(amount, transac)

                                                        # check the state after the withdraw() 
                                                        if withdraw_state == True:
                                                            print(f"\tWithdrew {amount} Successfully")
                                                            pass
                                                        elif withdraw_state == BalanceTooLow:
                                                            print("\tERROR: balance too low.")
                                                        elif withdraw_state == CreditTooLow:
                                                            print("\tERROR: credit too low")
                                                    else:
                                                        # if the amount isn't numeric
                                                        print("\tERROR: invalid amount")
                                                    pass

                                            elif accMenu_choice == 5:
                                                # if user chooses to transfer
                                                if account.accType == "savings":

                                                    if monthly_transaction == 0:
                                                        monthly_transaction += 1
                                                        transfer_menu(account)
                                                    else:
                                                        print("\tERROR: account has exceeded montly allowed transactions")
                                                        
                                                elif account.accType == "checkings":
                                                    transfer_menu(account)

                                            elif accMenu_choice == 6:
                                                # if user chooses to view their account transactions
                                                account.displayTransactions()

                                            elif accMenu_choice == 7:
                                                # if user chooses to delete their account
                                                account.deleteAccount()

                                                print("\n\tAccount Closed Successfully")
                                                exit_loop = 1

                                            elif accMenu_choice == 8:
                                                # if user chooses to exit
                                                exit_loop = 1
                                # if the account user selected has been closed
                                else:
                                    print("\tERROR: account is closed")
                            # if the account id user entered belong to another customer
                            else:
                                print("\tERROR: that is another customer's account")
                        # if the account id entered doesn't exist
                        else:
                            print("\tERROR: account does not exist")

            # lEAVING MENU
            elif choice == 3:
                print("\tReturning to main menu...\n")
                monthly_transaction = 0
                break

            # if the input was numeric but an invalid option
            else:
                print("\tERROR: invalid choice")
        # if not numeric
        else:
            print("\tERROR: invalid input")


def transfer_menu(account : Account):
    """Handles menu and validation for the transfer section of the program."""

    accounts_read = open(ACCOUNTS, "r")
    num = num_filelines(accounts_read)

    auto_center("Choose account to transfer to", "", 0)

    # displays all valid accounts to transfer to and stores their ids in a list
    valid_accounts = printAccounts()

    while True:
        try:
            choice_transfer = int(input("\n\tid : "))
            # if users enters id for account that doesn't exist
            if choice_transfer < 0 or choice_transfer > num:
                print("\tERROR: account does not exist")
                continue
            # if user enters id for account that is closed
            if choice_transfer not in valid_accounts:
                print("\tERROR: account is unavailable for transfers")
                continue
        except ValueError:
            # if user entered characters
            print("\tERROR: invalid input")
            continue
        else:
            break

    # grab the info for the user that will be receiving the money
    account_info = getInfo(ACCOUNTS, choice_transfer)

    while True:
        try:
            amount = int(input("\n\tamount : "))
            # if user tries to transfer negative or 0
            if amount <= 0:
                print("\tERROR: invalid amount")
                continue
        except ValueError:
            # if user entered characters
            print("\tERROR: invalid input")
            continue
        else:
            break
    
    # if the account is of type savings, generate the receiver instance as a savings acc with relevant info
    if(account_info[2] == "savings"):
        receiver = SavingsAccount(int(account_info[0]), int(account_info[1]), account_info[2],int(account_info[3]),int(account_info[4]))
    # if the account is of type checkings, generate the receiver instance as a checkings acc with relevant info
    elif(account_info[2] == "checkings"):
        receiver = CheckingsAccount(int(account_info[0]),int(account_info[1]),account_info[2],int(account_info[3]),int(account_info[4]))

    # create new instance of Transaction class with the accID of both sender and receiver
    transac = Transaction("transfer", 0, account.accID, receiver.accID, amount)
    
    # calls transfer() method and passes the amount, the receiver instance and the transaction instance
    transfer_state = account.transfer(amount, receiver, transac)
    if(transfer_state):
        pass
    elif transfer_state == InvalidTransfer:
        # if the transfer was invalidated
        print("\tThe transfer was disallowed")
    print(MENU_LINE)


def login_menu():
    """
    This function reads all lines in the customers.txt file to see how many customers there currently are.
    This is used to prompt the user to choose from the amount of customer ids currently available.
    Handles if the id is not a number, as well as if it is invalid (below 0 or above the current amount of customers)
    """

    customers_read = open(CUSTOMERS, "r+")
    numberoflines = num_filelines(customers_read)
    customers_read.close()

    while True:
        auto_center("Login", "", 0)
        # prints the amount of ids to select from
        print(f"\tSelect id (0-{numberoflines-1})")

        while True:
            choice_id = input("\n\tid : ")
            if choice_id.isnumeric():
                choice_id = int(choice_id)
            else:
                print("\tERROR: invalid input")
                break

            # if the selected id is not less than 0, and not greater than the amount of accounts available
            if choice_id >= 0 and choice_id <= numberoflines - 1:
                return choice_id
            else:
                print("\tERROR: customer does not exist")


def register_menu():
    """
    This function displays the part of the menu where a user can register/create a new Customer.
    Handles error checking on the user's input also.
    """

    # display menu title
    auto_center("Register", "", 0)

    # prompting for user input
    print("\tEnter :\n")
    new_cust = Customer(0)
    new_cust.name = input("\tName : ")
    age = input("\tAge  : ")

    # while loop to ensure age is a valid number
    while True:
        try:
            age = int(input("\tAge  : "))
            if age <= 0:
                print("\tERROR: invalid age")
        except ValueError:
            print("\tERROR: age must have a numerical value")
            continue
        else:
            break

    # now that age is correct, set new_cust age attribute to age
    new_cust.age = age

    # call addCustomer() to add the information to our text file
    new_cust.addCustomer()
    # set choice_id to our customer's generated ID and return it to menu to be used
    choice_id = new_cust.custID
    return choice_id


# continually display the main menu to the user until they choose option 3 to exit
while choice != 3:
    choice = 0
    main_menu()
