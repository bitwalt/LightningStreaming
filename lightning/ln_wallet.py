from time import sleep
import os

class LightningWallet:
    """ A lightning wallet for streaming data. """

    def __init__(self, name: str, balance: float):
        self.name = name
        self.balance = balance
        self.generated_invoice = 0

    def connect(self):
        return True

    
    def generate_invoice(self, amt):
        """ Generate an invoice for the amount. """
        self.generated_invoice += 1 
        return f"LN_{str(amt + self.generated_invoice * 2)}"

    def pay_invoice(self, invoice):
        self.balance -= 10
        return invoice

    def check_invoice(self, invoice):
        """ Check if the invoice is valid. """
        return True 

    def get_total_balance(self):
        return self.balance 


    def cash_invoice(self, amount):
        """ Make a deposit to the wallet. """
        self.balance += amount
        return self.balance
    
    def is_valid(self):
        return self.balance > 0 
    
    def create_invoice(self, amount):
        """ Make a withdrawal from the wallet. """
        self.balance -= amount
        return self.balance

    def request_generator(dest, amt):
        # Initialization code here
        counter = 0
        print("Starting up")
        while True:
            counter += 1
            sleep(2)

    def __str__(self):
        return f"{self.name}'s wallet:\n\t Balance: {self.balance} BTC"