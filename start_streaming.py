from lightning.ln_wallet import LightningWallet
from stream_peer import StreamPeer
from video_manager import VideoManager
from loguru import logger
from settings import *
from time import sleep
from flask import Flask, render_template, Response


app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def index():
    # rendering webpage
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    global alice 
    batch = alice.get_last_batch()
    print(batch)
    return Response(batch, mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    
    # Initialiaze a LN wallet
    alice_wallet = LightningWallet(name="Alice01", balance=START_SATS)
    bob_wallet = LightningWallet(name="Bob01", balance=START_SATS)
    logger.info(f"Created LightningWallet:\n {alice_wallet}")
    
    # Create a video manager for serve a folder of videos
    video_manager = VideoManager(MEDIA_FOLDER)
    logger.info(f"Created VideoManager:\n {video_manager}")
    
    # Create a server peer to serve "media" folder to clients
    bob = StreamPeer(HOST, PORT, name="Bob")
    bob.add_lightning_wallet(bob_wallet)
    bob.add_video_manager(video_manager)    
    
    # Create a client peer
    alice = StreamPeer(HOST, PORT + 1, name="Alice")
    alice.add_lightning_wallet(alice_wallet)
    
    # Connect client and server
    alice.connect_with_node(bob.host, bob.port)
    print(f"Connected client: {alice.name} with server: {alice.host}:{alice.port}")

    # Start bazar
    alice.ask_catalog(bob)
    sleep(1)
    alice.ask_media_streaming(bob, "office")
    sleep(1)

    # start the flask app
    app.run(host="localhost", port=9000, debug=False, threaded=True, use_reloader=False)

    
    
    
    