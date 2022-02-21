"""A class representing a Swarm in LNS"""
from video_util.video_file import VideoFile
from lightning.invoice import Invoice
from messages.session_pb2 import Image, Video, Swarm, LNInvoice


class SwarmGenerator:
    
    def __init__(self, peer_id:str, video_file: VideoFile, invoice: Invoice):
        self.peer_id = peer_id
        self.video_file = video_file
        self.invoice = invoice
        
    def get_video(self):
        print(self.video_file.as_dict())
        return Video(**self.video_file.as_dict())
            
    def get_poster(self):
        poster = self.video_file.get_poster()
        poster_shape = poster.shape
        return Image(width=poster_shape[0],
                      height=poster_shape[1], 
                      data=bytes(1)
                    #   data=poster.tobytes()
                      )
        
    def get_invoice(self):
        return LNInvoice(client_id=self.peer_id, timestamp=self.invoice.timestamp,
                         invoice=self.invoice.invoice, amount=self.invoice.amount)
    
    def generate(self):
        return Swarm(video=self.get_video(), 
                     poster=self.get_poster(),
                     invoice=self.get_invoice(),
                     total_price=self.video_file.get_video_price())
        

if __name__ == '__main__':
    video_file = VideoFile("media/mandelbrot_01.mp4")
    swarm_generator = SwarmGenerator(video_file, Invoice("alice", "ln123abc", 100))
    swarm = swarm_generator.generate()
    print(swarm)