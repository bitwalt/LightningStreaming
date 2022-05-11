import grpc
from concurrent import futures
import messages.session_pb2_grpc as pb2_grpc
from video_manager import VideoManager
from stream_peer import StreamPeer
from settings import SERVER_PORT, MEDIA_FOLDER


def parse_swarms(swarms):
   pass
   

def serve():
   
   stream_peer = StreamPeer("Bob", "localhost", SERVER_PORT)
   video_manager = VideoManager(MEDIA_FOLDER)
   stream_peer.add_video_manager(video_manager)
   stream_peer.get_swarms()
   server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
   pb2_grpc.add_StreamerServicer_to_server(stream_peer, server)
   server.add_insecure_port(f'[::]:{SERVER_PORT}')
   print("gRPC starting")
   server.start()
   server.wait_for_termination()
   
if __name__ == "__main__":
   serve()  