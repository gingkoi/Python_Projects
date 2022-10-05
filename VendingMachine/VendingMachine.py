from datetime import datetime
import os
import time
from art import vending_machine as logo
import stdiomask

class VendingMachine:

    coins_collected = 0
    coin_box = 0

    def __init__(self) -> None:

        self.drinks = {
            "coke":1,
            "sprite":1.1,
            "orange":0.9,
            "pepsi":1.2,
            'water':0.8,
        }

        self.stock = {
            "coke":25,
            "sprite":20,
            "orange":10,
            "pepsi":3,
            'water':1,
        }

    def inventory(self,password):
        if password == '0000':
            print("\nINVENTORY")
            for index, items in enumerate(self.stock, start=1):
                print(f"{index}.{items.title()} QTY:{self.stock[items]}")
        else:
            print("Incorrect password.")
            return main()
        
    def dispense(self, drink):
        self.stock[drink] -= 1

    def is_stock_enough(self, drink):
        can_make = True
        if self.stock[drink] <= 0:
            print(f"Sorry {drink} is out of stock.")
            can_make = False
        return can_make

    def display(self):
        for index, items in enumerate(self.drinks, start=1):
            print(f"[{index}] {items.title()} ${self.drinks[items]:.2f}")

    def money_checker(self, money, choice):
        if money >= self.drinks[choice]:
            return True
    
    def menu_choice(self, choice):
        ls = []
        for item in range(1, len(self.drinks)+1): ls.append(str(item))
        if choice in ls:
            return True
    
    def insert_money(self, money):
        self.coins_collected += float(money)

    def log(self):
        print(f"""
        COMPANY: GINGKOI PTE LTD
        VERSION: 1.0
        HELPLINE: +65 89223211
        ISO 123-242
        COINS COLLECTED: ${self.coin_box:.2f}
        """)

    def restock(self,item,quantity):
            self.stock[item] += quantity
            print(f"{quantity} QTY of {item} has been restocked.")
    
    def timestamp(self):
        with open('log.txt', 'a') as f:
            ct = datetime.now()
            f.write(f'Last Logged In: - {ct}\n')
           
vendingmachine = VendingMachine()

def main():
    global coins_collected
    global coin_box

    maching_running = True
    while maching_running:
        print(logo)
        vendingmachine.display()

        choice = input("Enter number choice: ").lower()

        if choice == 'off':
            print("Machine shutting down.")
            exit()

        elif vendingmachine.menu_choice(choice):
            choice = int(choice)
            item = list(vendingmachine.drinks)[choice-1]
            if vendingmachine.is_stock_enough(item):
                print(f"You've selected {item} - the price is ${vendingmachine.drinks[item]:.2f}")
                while vendingmachine.coins_collected < vendingmachine.drinks[item]:
                    print(f"Please insert ${vendingmachine.drinks[item]:.2f} into the machine.")
                    payment = input("Please enter the amount you've like to insert or enter [c] to cancel: $").lower()
                    if payment != 'c':
                        vendingmachine.insert_money(payment)
                    else:
                        print("Canceling order..")
                        time.sleep(2)
                        break        
                    
                    if vendingmachine.coins_collected > vendingmachine.drinks[item]:
                        vendingmachine.dispense(item)
                        print(f"Thank You! Please take your {item}.")
                        print(f"The remaining change in the machine is ${vendingmachine.coins_collected - vendingmachine.drinks[item]:.2f}.")
                        vendingmachine.coin_box += vendingmachine.drinks[item]
                        vendingmachine.coins_collected = 0
                        time.sleep(2)
                        os.system('clear')
                        main()
                    else:
                        print("Not enough. Please insert more.")
        elif choice == 'admin':
            vendingmachine.timestamp()
            password = stdiomask.getpass()
            vendingmachine.inventory(password)
            restock = input("Press ENTER to restock, [l] for log: ").lower()
            os.system('clear')
            if restock == "":
                for index, items in enumerate(vendingmachine.stock, start=1):
                    print(f"{index}.{items.title()} QTY:{vendingmachine.stock[items]}")
                restock = int(input("Select item to restock: "))
                restock_item = list(vendingmachine.drinks)[restock-1]
                running = True
                while running:
                    print(f"Enter [0] to CANCEL.")
                    quantity = int(input(f"How many {restock_item} QTY would you like to restock?: "))
                    if quantity == 0:
                        print("Exting permission mode.")
                        running = False
                    elif quantity > 30:
                        print("Unable to store more than 30.")
                    else:
                        vendingmachine.restock(restock_item,quantity)
                        running = False
            elif restock == 'l':
                vendingmachine.log()
            else: print("Exiting permisson mode.")
        else:
            print("Invalid choice.")

main()
    
