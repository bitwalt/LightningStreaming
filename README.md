# Peer-to-peer video streaming and micropayments on Lightning Network 
A python implementation of a P2P video streaming protocol by using Lightning Network invoices. 

**ONLY FOR LEARNING PURPOSE**

**ONLY FOR USE IN REGTEST**

**NO RESPONSIBILY FOR VIDEO STREAMED** 

This project has the aim to explore the power of micro-payments enabled with LN and Bitcoin protocol,
in a P2P network of video streaming.


Each node on the network has a lightning node and a bitcoind service running. 

Users will be able to open lightning channels to each peer and ask or send video streams.

A stream session is enabled by a micro-payment protocol based on Bolts11 invoices. 


## Protocol
```
Alice   ----------->        
    {"cmd": ASK_MEDIA",
    "video": "Wonderland",
    "auth": "@macaroon" }
    
        <-----------    Bob
                {"cmd": OK_MEDIA", "video":Wonderland", 
                "auth": "@macaroon", "invoice": "lnd123" }

Alice   ----------->
    {"START_SEND", "auth": "@macaroon", "invoice": "lnd123"}

        <Start Streaming over VideoProto (TLS-TCP)>
                //
```                 

Example1:

Alice publish a new video file called weareallsatoshi.mp4 .

Bob wants to see the new video file and ask for a preview.

After the preview Bob is asked to start a micro-payment streamin session based on LN invoices. 


Classes: 
- VideoManager: handle all video files for a peer
- VideoFile: a video file with a price in sats
- Peer: a peer in a P2P network
- LightningWallet: a Lightning wallet with some satoshis and lnd api
- LightWorker: Handle LN invoices 
- Streamer: a process to serve a client streaming request
- ServerPeer: a server peer that handle video streaming


**TODO:**

#### General:

- Connect client-server
- Create docker-compose and docker files 
- Add a backend a DB and a frontend
- Add support to TOR
- DOS protection
- Test code

#### Lightning:
- Setup a Lightning Node in testnet or regtest
- Open a channel with a peer   

#### VideoStream:
- Send chunks of videos in a TCP connection
- FFmpeg and pyAV instead of OpenCV 
- Client stream mux

#### Peer
- Invoice payment logic
- Send Invoice - Wait Payment - Send Chunk of video
- Start a streaming service for a video
-  Send metadata over the network 
- Get bytes of the media stream in the client
- Show with open CV the media file
  
## Resources

- P2P Network: https://github.com/macsnoeren/python-p2p-network

- TOR-python: https://sylvaindurand.org/use-tor-with-python/

- LN-python: https://dev.lightning.community/guides/python-grpc/
