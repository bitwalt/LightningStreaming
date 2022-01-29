""" 
API possibili dall'utente, messaggi che può ricevere il nodo:
Callback async:
SERVER
- GET_SWARM_INFO mandami le info di uno swarm id
{ id: <id_swarm>,
 name: <nome_swarm>
 file_size: <dimensione_file>, 
 prezzo_per_chunk: <prezzo_chunk>
 }

- START_PAYMENT mandami la prima invoice e il primo chunk


PAYMENT_DONE(invoice) -> check_

"""
from generators.builder import GeneratorBuilder

async def payment_received(self, invoice):
    # Send new chunk of data
    pass
 

class LNS_Peer:
    
    def __init__(self):
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
        
        while True:
            # Accept new incoming connection
            accept = False
            if accept:
                # Thart new thread with async callback to handle            
        pass

    
    def ask_for_swarm(self, ip, port, swarm_id):
        """
        Start a new connection 

        - Pay invoice 
        - macaroon 
        """
    
    
