# from p2pnetwork.node import Node
import re
from lightning.ln_wallet import LightningWallet
from video_manager import VideoManager
from streamer import VideoStreamer
from time import sleep
from queue import Queue
import cv2
from dataclasses import dataclass
import hashlib, random
from swarm import SwarmGenerator

import grpc
from concurrent import futures
import messages.session_pb2 as msg
import messages.session_pb2_grpc as pb2_grpc

from logging import getLogger
from loguru import logger

@dataclass
class Macaroon:
    """Class representing a macaroon for authentication"""
    
    @staticmethod
    def generate(peer_id):
        return hashlib.sha256((str(random.random()) + peer_id).encode()).hexdigest()
        
        
@dataclass
class PeerInfo:
    """Class for keeping track of an item in inventory."""
    peer_id: str
    ip: str
    port: int = 9069

    def __init__(self, name, ip, port):
        self.name = name
        self.ip = ip
        self.port = port
        self.peer_id = self.generate_id()
                         
    def generate_id(self):
        """Generates a unique ID for each node."""
        id = hashlib.sha256()
        t = self.name + str(self.port) + str(random.randint(1, 99999999))
        id.update(t.encode('ascii'))
        return id.hexdigest()[:8]
    
    def __str__(self):
        return f"{self.name}<{self.peer_id} at {self.ip}:{self.port}"
    
         
class StreamPeer(pb2_grpc.StreamerServicer):
    """
    A StreamPeer to pay another peer for a video or sending ours.

    Possible APIs:
        - Show available media files
        - Start a streaming handshake session
    """
    def __init__(self, name, host, port, max_connections=5):
        self.peer_info = PeerInfo(name, host, port)
        self.name = name
        self.max_connections = max_connections
        self.web_queue = Queue(maxsize=20)
        
        self.macaroon = msg.Macaroon(id=Macaroon.generate(self.peer_info.peer_id))
        self.ln_wallet = LightningWallet(name, balance=1000)
        logger.debug(self.peer_info)
        self.clients = []
        self.swarms = []
     
                
    def get_peer(self) -> msg.Peer:
        return msg.Peer(peer_id=self.peer_info.peer_id, 
                        ip=self.peer_info.ip,
                        port=self.peer_info.port,
                        macaroon = self.macaroon
                        )
        
    def add_lightning_wallet(self, ln_wallet:LightningWallet):
        self.ln_wallet = ln_wallet    
        
    def add_video_manager(self, video_manager: VideoManager):
        print("VideoManager: ", video_manager)
        self.video_manager = video_manager
    
    def add_stream(self, stream: VideoStreamer):
        self.stream = stream
                    
    def get_video_names(self):
        return self.video_manager.get_video_names()
       
    def get_swarms(self):  
        video_files = self.video_manager.get_all_videos()
        swarms = []
        for video_file in video_files:
            invoice = self.ln_wallet.generate_invoice(video_file.chunk_price)
            swarm_generator = SwarmGenerator(self.peer_info.peer_id, video_file, invoice)
            swarms.append(swarm_generator.generate())    
        return swarms 
    

    def hadle_frame_batch(self, node, data):
        print(f"{self.name} RECEIVED FRAME BATCH ID: {data['index']}")
        frame = data.get("frame")
        _, encodedImage = cv2.imencode(".jpg", frame)
        result = bytearray(encodedImage)
        self.web_queue.put(result)
            
    def get_last_batch(self):
        imagebytes = self.web_queue.get()
        return imagebytes

    def init_streaming_session(self, node, data):
        
        print(f"\n{self.name} RECEIVED START STREAMING\n {data}")
        received_invoice = data.get("invoice")
        print(f"{self.name} RECEIVED INVOICE: {received_invoice}")
        if self.ln_wallet.check_invoice(received_invoice):
            video_name = data.get("video")
            print(f"{self.name} INVOICE IS VALID")
            print(f"{self.name} videos are: {self.video_manager.video_files}" )
            print(f"{self.name} video REQUESTED is: {video_name}")

            video = self.video_manager.get_video_by_name(video_name)
            print(f"{self.name} VIDEO: {video}")
            
            if video is not None:
                stream = VideoStreamer(video, node)    
                print(f"{self.name} STARTING STREAMING: {video_name}")
                self.start_streaming(node, stream)
            else:
                print(f"{self.name} ERROR: Video not found")
                      
    def start_streaming(self, node, stream):
        self.stream = stream
        # self.stream.start()
        while self.stream.running:
            chunk_price = self.stream.get_chunk_price()
            invoice = self.ln_wallet.generate_invoice(chunk_price)
            #TODO: SEND INVOCE
            if self.ln_wallet.check_invoice(invoice):
                # send data to the peer
                video_data = self.stream.get_new_batch()
                self.web_queue.put(video_data['frame'])
                # self.send_video_metadata(node, video_data)
            else:
                logger.error("Invoice is not valid")
                sleep(1)                 

    ### HANDSHAKE

    def ask_handshake(self) -> msg.HandshakeRequest:
        return msg.HandshakeRequest(client_peer=self.get_peer())
        
    def handshake(self, request, context):
        client_peer = request.client_peer
        logger.debug(f"{self.name} Received HANDSHAKE request from {request.client_peer}")  
        client_macaroon = client_peer.macaroon
        if self.ln_wallet.check_macaroon(client_macaroon.id):    
            logger.debug(f"Client authenticated")  
            self.clients.append(client_peer.peer_id)
            return msg.HandshakeResponse(server_peer=self.get_peer(), handshake_status="OK")
        else:
            logger.warning(f"Client NOT authenticated")
            return msg.HandshakeResponse(server_peer=self.get_peer(), handshake_status="FAIL")   
    
    ### MEDIA
        
    def ask_media(self) -> msg.MediaRequest:
        return msg.MediaRequest(client_peer=self.get_peer())
        
    def looking(self, request, context):
        # receive AskMedia, returns MediaRespose
        peer_id = request.client_peer.peer_id
        logger.debug(f"{self.name} Received MEDIA media request: {peer_id}")
    
        if peer_id not in self.clients:
            logger.warning(f"{self.name} Client not authenticated")
            return msg.MediaRespose(server_peer=self.get_peer(),
                                    status=msg.RequestStatus.ERROR,
                                    swarms=[])
        else:
            logger.debug(f"{self.name} Client authenticated")
            logger.debug(f"Sending swarms...")            
            return msg.MediaRespose(server_peer=self.get_peer(), 
                                    status=msg.RequestStatus.OK,
                                    swarms=self.get_swarms())

    def start_stream(self, request, context):
        # receive AskSwarm returns ChunkResponse
        print("Starting streaming")
        return msg.ChunkResponse()
    
    def send_stream(self, request, context):
        # receive stream of AskChunkPayment, returns streams of ChunkResponse
        pass   
    
    def pay_stream(self, request, context):
        # receive stream of ChunkResponse, returns streams of AskChunkPayment
        pass
    

    def serve(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
        pb2_grpc.add_StreamerServicer_to_server(self, server)
        server.add_insecure_port(f'[::]:{self.peer_info.port}')
        logger.debug(f"gRPC server starting at {self.peer_info.port}")
        server.start()
        server.wait_for_termination()