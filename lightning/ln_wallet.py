from time import sleep
import os
import hashlib, random
from lightning.invoice import Invoice

class LightningWallet:
    """ A lightning wallet for streaming data. """

    def __init__(self, name: str, balance: float):
        self.name = name
        self.balance = balance
        self.generated_invoice = 0
        self.invoices = []
        self.macaroons = [] # list of macaroons emitted by node

    def connect(self):
        return True

    def check_macaroon(self, macaroon: str): 
        # return macaroon in self.macaroons
        return True
        
    def generate_invoice(self, amt):
        """ Generate an invoice for the amount. """
        self.generated_invoice += 1 
        invoice_hash = f"LN_{str(amt)}{hashlib.sha256(str(random.random()).encode()).hexdigest()}"
        return Invoice(invoice_hash, amt)

    def pay_invoice(self, invoice):
        self.balance -= invoice.amount
        return invoice

    def check_invoice(self, invoice):
        """ Check if the invoice is valid. """
        return True 

    def is_paid_receipt(self, recepit):
        """ Check if the receipt has been paid correctly. """
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