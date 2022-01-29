import socket,cv2, pickle,struct, time
import imutils 

class Server:
    
    def __init__(self):
        pass 

    def connect_to_client(self, ip='127.0.0.1', port=9070):       
        self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client_ip = ip  # Here according to your server ip write the address
        self.client_port = port
        self.client_socket.connect((self.client_ip, self.client_port))
        print("Connected to client")
  
    def send_video(self, video_file):
        self.video = cv2.VideoCapture(video_file)
        if self.client_socket: 
            while (self.video.isOpened()):
                try:
                    ret, frame = self.video.read()
                    frame = imutils.resize(frame,width=380)
                    a = pickle.dumps(frame)
                    message = struct.pack("Q",len(a)) + a
                    self.client_socket.sendall(message)
                    print(f"TO: {self.client_ip}",message)
                    time.sleep(0.3)
                except Exception as exp:
                    print(f"ERROR: {exp}")
                    print('VIDEO FINISHED!')
                    self.client_socket.close()
                    break
                
                
if __name__ == '__main__': 
    server = Server()
    server.connect_to_client(ip='127.0.0.1', port=9071)
    server.send_video('/Users/walter/Development/LightningStreaming/media/mandelbrot_01.mp4')