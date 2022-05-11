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
      print(f"SERVER: {response.server_peer.peer_id}")
      print(f"REQUEST: {response.status}")
      print(f"SWARMS: {response.swarms}")
      swarm = response.swarms[0]
      response = stub.start_stream(stream_peer.ask_for_start_stream(swarm))
      print()
      print("Done")
if __name__ == '__main__':
   run()