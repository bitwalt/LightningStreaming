
ASK_CATALOG = "LOOK"
SEND_CATALOG = "MEDIA"
ASK_MEDIA = "ASK_MEDIA"
OK_MEDIA = "OK_MEDIA"
START_SEND = "START_SEND"
BATCH = "BATCH"


class MessageProto:
    """A class to handle the message protocol."""

    def __init__(self):
        """Initialize the class."""
        self.cmd = None
        self.data = None

    def decode(self, message):
        """Parse the message."""
        # Return command and data from the message
        return message['cmd'], message['data']
   
    def encode(self, message):
        pass
     
    def look(node_id):
        json_msg = {
            "cmd": ASK_CATALOG,
            "id": node_id,
        }
        return json_msg
    
    def batch(node_id, data):
        json_msg = {
            "cmd": BATCH,
            "id": node_id,
            "index": data['index'],
            "frame": data['frame'],
        }
        return json_msg
        
        
        
    def catalogue(node_id, video_names):   
        json_msg = {
            "cmd": SEND_CATALOG,
            "id": node_id,
            "videos": video_names
        }
        return json_msg
    
    def ask_media(node_id, video_name):
        json_msg = {
            "cmd": ASK_MEDIA,
            "id": node_id,
            "video": video_name,
            "auth": "@macaroon",
        }
        return json_msg
    
    def send_unpaid_invoice(node_id, video_name, invoice):
        json_msg = {
            "cmd": OK_MEDIA,
            "id": node_id,
            "video": video_name,
            "invoice": invoice,
        }
        return json_msg
      
    def start_streaming(node_id, invoice, video):
        json_msg = {
            "cmd": START_SEND,
            "id": node_id,
            'video': video,
            "invoice": invoice,
        }
        return json_msg
      
    
    def show_catalog(data):
        video_names = data['videos']
        print("\nCatalog:\n")
        for i, video in enumerate(video_names):
            print(f"{i} -- > {video}")
          