import time

class Invoice:
    """ A Lightning Invoice """

    def __init__(self, invoice: str, amount: int):
        
        self.invoice = invoice
        self.amount = amount
        self.timestamp = time.time()
        
    def as_dict(self):
        return {
            "timestamp": self.timestamp,
            "invoice": self.invoice,
            "amount": self.amount
        }
        
    def __str__(self):
        return f"{self.client_id}'s invoice:\n\t Invoice: {self.invoice}\n\t Amount: {self.amount} BTC"