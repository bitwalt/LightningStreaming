import time
from stream_peer import StreamPeer
import random
from settings import HOST, PORT

class NetworkManager:
    
    def __init__(self, n_peers):
        self.n_peers = n_peers
        self.client_peers = self.create_peer(n_peers)

    def create_peer(self, n_peers):
        peers = {} 
        self.ids = []
        for i in range(n_peers):
            node = StreamPeer(HOST, PORT + i)
            peers[node.id] = node
            self.ids.append(node.id)
        return peers

    def start_peers(self):
        for peer in self.client_peers.values():
            peer.start()
            time.sleep(0.1)
        print("Peers started")

    def connect_random_nodes(self, p=0.3): 
        # connect to n nodes with probability p
        for i in range(self.n_peers):
            for j in range(self.n_peers):
                if (i < j):
                    # Take random number R.
                    R = random.random()	
                    # Check if R<P add the edge to the graph else ignore.
                    if (R < p):
                        start_node = self.client_peers[self.ids[i]]
                        target_node = self.client_peers[self.ids[j]]
                        print("Connecting " + start_node.id + " to " + target_node.id)
                        print(f"Node: {i} with Node: {j}")
                        start_node.connect_with_node(target_node.host, target_node.port)

    def stop_peers(self):
        for peer in self.client_peers.values():
            peer.stop()
        print("Peers stopped\n")
    
    def send_data_from_node(self, node_id, data):
        self.peers[node_id].send_to_nodes(data)

    def print_peers_connections(self):
        for i, peer in enumerate(self.client_peers.values()):
            print(f"{i} -> Peer: {peer.id} connected with {len(peer.nodes_outbound)} nodes = {peer.nodes_outbound}")
    
    
if __name__ == "__main__":
    manager = NetworkManager(5)
    manager.start_peers()
    manager.connect_random_nodes()
    manager.print_peers_connections()
