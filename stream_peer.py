from p2pnetwork.node import Node
from lightning.ln_wallet import LightningWallet
from video_manager import VideoManager
from streamer import VideoStreamer
from message_proto import *
import sys
from time import sleep
from loguru import logger


class StreamPeer(Node):
    """
    A StreamPeer to pay another peer for a video or sending ours.

    Possible APIs:
        - Show available media files
        - Start a streaming handshake session
    """
    def __init__(self, host, port, name=None, id=None, callback=None, max_connections=0):
        super(StreamPeer, self).__init__(host, port, id, callback, max_connections)
        self.id = self.id[:8]
        self.name = name
        print(f"StreamPeer: {self.name} Started")
        self.start()
        
    def add_lightning_wallet(self, ln_wallet:LightningWallet):
        self.ln_wallet = ln_wallet    
        
    def add_video_manager(self, video_manager: VideoManager):
        self.video_manager = video_manager
    
    def add_stream(self, stream: VideoStreamer):
        self.stream = stream
                    
    def get_video_names(self):
        return self.video_manager.get_video_names()
       
    def node_message(self, node, data):
        """Decode command from message received from a peer """
        self.parse_command(node, data)
        
    def parse_command(self, node, data):
        """Parse command from message received from a peer """
        command = data.get("cmd")    
        if command is None:
            raise Exception("Command not found")
        print(f"{self.name} RECEIVED CMD: {command}")
    
        if command == ASK_CATALOG:
            # Send my videos to the peer
            self.send_catalog(node)
        elif command == SEND_CATALOG:
            # Show the catalogue that I requested
            MessageProto.show_catalog(data)
        elif command == ASK_MEDIA:
            # Send the first invoice
            self.ask_first_payment(node, data) 
        elif command == OK_MEDIA:
            # Decide to pay the invoice 
            self.pay_and_start_session(node, data)            
        elif command == START_SEND:
            # CHECK IF THE INVOICE HAS BEEN PAID AND START STREAMING
            self.init_streaming_session(node, data)
        else:
            print(data)
     
    def init_streaming_session(self, node, data):
        received_invoice = data.get("invoice")
        if self.ln_wallet.check_invoice(received_invoice):
            video_name = data.get("video")
            video = self.video_manager.get_video_by_name(video_name)
            if video is not None:
                stream = VideoStreamer(video, node)
                self.start_streaming(stream)
               
    def start_streaming(self, stream):
        self.stream = stream
        # self.stream.start()
        while self.stream.running:
            chunk_price = self.stream.get_chunk_price()
            invoice = self.ln_wallet.generate_invoice(chunk_price)
            print(f"{self.name} STREAMING: PAY INVOICE: {invoice}")
            #TODO: SEND INVOCE
            if self.ln_wallet.check_invoice(invoice):
                # send data to the peer
                video_data = self.stream.get_new_batch()
                self.send_video_metadata(stream.node, video_data)
            else:
                logger.error("Invoice is not valid")
                sleep(1)                 

    def pay_and_start_session(self, node, data):
        """Pay the invoice and start the streaming session"""
        invoice = data.get("invoice")
        receipt = self.ln_wallet.pay_invoice(invoice)
        data = MessageProto.start_streaming(self.id, receipt)
        self.send_message(node, data)
    
    def ask_first_payment(self, node, data):
        video_name = data.get("video")
        video = self.video_manager.get_video_by_name(video_name)
        video_price = video.get_price()
        invoice = self.ln_wallet.generate_invoice(video_price)
        data = MessageProto.send_unpaid_invoice(self.id, video_name, invoice)
        self.send_message(node, data)
        
                   
    def ask_catalog(self, node):
        data = MessageProto.look(self.id)
        self.send_message(node, data)
        
        
    def ask_media_streaming(self, node, video_name):
        data = MessageProto.ask_media(self.id, video_name)
        self.send_message(node, data)

    def send_catalog(self, node):
        """Send video files to node"""
        video_names = self.get_video_names()
        data = MessageProto.catalogue(self.id, video_names)
        self.send_message(node, data)

    def send_video_metadata(self, node, data):
        self.send_message(node, data)

    def send_message(self, node, data):
        print(f"{self.name} SENDING: {data} to {node.name}")
        # self.send_to_node(node.id, data)
        self.send_to_nodes(data)
        sleep(1)