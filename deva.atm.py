class ATM:
    def __init__(self, pin, balance=5000):
        self.pin = pin
        self.balance = balance
        self.transaction_history = []

    def check_balance(self):
        print(f"\n my current balance: {self.balance} rupees")
        self.transaction_history.append(f"checking balance: {self.balance} rupees")

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"\n {amount} money has been deposited successfully")
            self.transaction_history.append(f"deposit: {amount} money")
        else:
            print("\n please enter the correct amount of money to deposit")

    def withdraw(self, amount):
        if amount > self.balance:
            print("\n sorry, there are insufficient funds in your account.")
        elif amount <= 0:
            print("\nplease enter a valid amount to withdraw.")
        else:
            self.balance -= amount
            print(f"\n {amount} the money has been successfully withdrawn from your account.")
            self.transaction_history.append(f"withdrawal: {amount} rupees")

    def show_history(self):
        print("\n📜--- Transaction History ---")
        if not self.transaction_history:
            print("No transactions found.")
        else:
            for txn in self.transaction_history:
                print(f"- {txn}")


# --- Main Program starts ---
def start_atm():
    # creating a demo account (PIN: 1234, balance: 5000)
    my_atm = ATM(pin=1234, balance=5000)
    
    print("Welcome to Python ATM System")
    tries = 3
    
    # pin verification loop
    while tries > 0:
        user_pin = int(input("\n Enter your 4-digit PIN: 1234 "))
        if user_pin == my_atm.pin:
            print("\n Pin verified successfully! Welcome to your account.")
            break
        else:
            tries -= 1
            print(f" rong PIN! You have only {tries} left")
    else:
        print("\n🚫 your card has been blocked because the PIN was entered incorrectly 3 times।")
        return

    # ATM menu loop 
    while True:
        print("\n--- select your option ---")
        print("1. (Check Balance)")
        print("2. (Deposit)")
        print("3. (Withdraw)")
        print("4. (Transaction History)")
        print("5. (Exit your card)")
        
        choice = input("\n write your choice (1-5): ")
        
        if choice == '1':
            my_atm.check_balance()
        elif choice == '':
            amount = float(input(" How much money would you like to deposit?: "))
            my_atm.deposit(amount)
        elif choice == '3':
            amount = float(input(" How much money would you like to withdraw?: "))
            my_atm.withdraw(amount)
        elif choice == '৪':
            my_atm.show_history()
        elif choice == '5':
            print("\n Thank you for using our ATM. Have a great day!")
            break
        else:
            print("\n Invalid option! Please select an option between 1 and 5.")

# implementing an atm system
start_atm()
