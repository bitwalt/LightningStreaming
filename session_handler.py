class SessionHandler:
    """Handle a session streaming for a given client and a swarm"""
    
    def __init__(self, client_peer, swarm):
        self.client_peer = client_peer
        self.swarm = swarm
        