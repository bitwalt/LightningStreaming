import grpc
import messages.session_pb2 as msg
import messages.session_pb2_grpc as pb2_grpc
from stream_peer import StreamPeer

from settings import SERVER_PORT, CLIENT_PORT

def run():
   stream_peer = StreamPeer("Alice", "localhost", CLIENT_PORT)
   with grpc.insecure_channel(f'localhost:{SERVER_PORT}') as channel:
      stub = pb2_grpc.StreamerStub(channel)
      # 1. Handshake
      response = stub.handshake(stream_peer.ask_handshake())
      print("Handshake request: ", response.handshake_status)  
      # 2. Ask for media
      response = stub.looking(stream_peer.ask_media())
      print("Looking request: ", response.swarms)
if __name__ == '__main__':
   run()