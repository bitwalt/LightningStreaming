from time import sleep
# import codecs
# import rpc_pb2 as ln
# import rpc_pb2_grpc as lnrpc
# import grpc
import os

# Due to updated ECDSA generated tls.cert we need to let gprc know that
# we need to use that cipher suite otherwise there will be a handhsake
# error when we communicate with the lnd rpc server.
os.environ["GRPC_SSL_CIPHER_SUITES"] = 'HIGH+ECDSA'


class LightningWallet:
    """ A lightning wallet for streaming data. """

    def __init__(self, name: str, balance: float):
        self.name = name
        self.balance = balance

    def connect(self):
        # Lnd cert is at ~/.lnd/tls.cert on Linux and
        # ~/Library/Application Support/Lnd/tls.cert on Mac
        # self.cert = open(os.path.expanduser('~/.lnd/tls.cert'), 'rb').read()
        # self.creds = grpc.ssl_channel_credentials(self.cert)
        # self.channel = grpc.secure_channel('localhost:10009', self.creds)
        # self.stub = lnrpc.LightningStub(self.channel)
        return True

    
    def generate_invoice(self, amt):
        """ Generate an invoice for the amount. """
        # response = stub.AddInvoice(ln.Invoice(value=amt))
        # return response.payment_request
        return "LND_" + str(amt)

    def pay_invoice(self, invoice):
        # self.balance -= invoice.amount
        self.balance -= 10
        return invoice

    def check_invoice(self, invoice):
        """ Check if the invoice is valid. """
        return True 

    def get_total_balance(self):
        # Retrieve and display the wallet balance
        # response = stub.WalletBalance(ln.WalletBalanceRequest())
        # return response.total_balance
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
            # request = ln.SendRequest(
            #     dest=dest,
            #     amt=amt,
            # )
            # yield request
            # Alter parameters here
            counter += 1
            sleep(2)

    def __str__(self):
        return f"{self.name}'s wallet:\n\t Balance: {self.balance} BTC"