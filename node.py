from generators.builder import GeneratorBuilder
import numpy as np
import messages.session_pb2 as proto_session
import messages.session_pb2_grpc as grpc_session
from pillow import Image
from video_util.video_file import VideoFile
import grpc
from concurrent import futures
from queue import Queue

async def payment_received(self, invoice):
    # Send new chunk of data
    pass


class LNS_Peer:
    
    def __init__(self, host, port, name=None, id=None, callback=None, max_connections=5):
        self.id = self.id[:8]
        self.name = name
        print(f"StreamPeer: {self.name} Started")
        self.max_connections = max_connections
        self.web_queue = Queue(maxsize=20)
        
    def generate_image(self, file_path):
        
        pass
        
    def create_new_video(self, seconds, kind):
        """Create a new video with the given args"""    
        return GeneratorBuilder.generate(sec=seconds, kind=kind)
    
    def create_swarm(self, file_path):
        """ Generate a new swarm from the video file
        - hashfile 
        - generate_invoce
        - best_frame
        """
        file_path = self.create_new_video(10, 'julia')
        
        pass
    
    def serve_swarm(self, swarm_id):
        
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
        grpc_session.add_Handshaker_to_server(Handshaker(), server)
        grpc_session.add_CatalogueServicer_to_server(Catalogue(), server)
        
        server.add_insecure_port('[::]:50051')
    
    def ask_for_swarm(self, ip, port, swarm_id):
        """
        Start a new connection 

        - Pay invoice 
        - macaroon 
        """
    
    
