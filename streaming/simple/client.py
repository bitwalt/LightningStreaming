
# Welcome to PyShine
# In this video server is receiving video from clients.
# Lets import the libraries
import socket, cv2, pickle, struct
import imutils
import threading
import pyshine as ps # pip install pyshine
import cv2


class Client:
    
    def __init__(self, host="127.0.0.1", port=9069):
        self.host = host
        self.port = port
  
    def connect(self):       
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        host_name  = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        socket_address = (host_ip, self.port)
        self.server_socket.bind(socket_address)
        self.server_socket.listen()
        print("Listening at", socket_address)

    def receive_video(self, addr,client_socket):
        try:
            print('CLIENT {} CONNECTED!'.format(addr))
            if client_socket: # if a client socket exists
                data = b""
                payload_size = struct.calcsize("Q")
                while True:
                    while len(data) < payload_size:
                        packet = client_socket.recv(4*1024) # 4K
                        if not packet: break
                        data+=packet
                    packed_msg_size = data[:payload_size]
                    data = data[payload_size:]
                    msg_size = struct.unpack("Q",packed_msg_size)[0]
                    while len(data) < msg_size:
                        data += client_socket.recv(4*1024)
                    frame_data = data[:msg_size]
                    data  = data[msg_size:]
                    frame = pickle.loads(frame_data)
                    text  =  f"CLIENT: {addr}"
                    print(f"received: text: {text}")
                     # frame =  ps.putBText(frame,text,10,10,vspace=10,hspace=1,font_scale=0.7, 						background_RGB=(255,0,0),text_RGB=(255,250,250))
                    # cv2.imshow(f"FROM {addr}",frame)
                    # key = cv2.waitKey(1) & 0xFF
                    # if key  == ord('q'):
                    # 	break
                client_socket.close()
        except Exception as e:
            print(f"CLINET {addr} DISCONNECTED")
            pass
    
    def get_new_connection(self):
        client_socket,addr = self.server_socket.accept()
        return (addr,client_socket)
  
if __name__ == '__main__': 
    client = Client(host="127.0.0.1", port=9071)
    while True:
        client.connect()
        client_socket,addr = client.get_new_connection()
        thread = threading.Thread(target=client.receive_video, args=((addr,client_socket)))
        thread.daemon = True
        thread.start()
        print("Listening for clients...") 

