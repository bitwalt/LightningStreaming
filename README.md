# DRAFT - Not Completed 
# Peer-to-peer video streaming and micropayments on Lightning Network 
A python implementation of a P2P video streaming protocol by using Lightning Network invoices. 

**ONLY FOR LEARNING PURPOSE**

**ONLY FOR USE IN REGTEST AND NOT SECURE YET**

**NO RESPONSIBILITY FOR VIDEOS STREAMED** 

This project has the aim to explore the power of micro-payments enabled with LN and Bitcoin protocol,
in a P2P network of video streaming and file transfers.

## Bitcoin Lightning Protocol 
Each node on the network has a lightning node and a bitcoind service running, in order to maintain self custody of funds. 

Users will be able to open lightning channels to each peer and ask or send video streams.

A streaming session is enabled by a micro-payment streaming protocol based on BOLTS11 invoices and gRPC callbacks. 

## Peer-to-peer Streaming Video
Based on PyPPSPP implementation of Peer-to-Peer Streaming Peer Protocol (PPSPP) [RFC7574],
enables video streaming in a P2P network.

Videos are represented by Merkle Tree Hash (Swarm ID) and send to other peers by the router peer. 

The connections are in use TCP but soon secured using TLS or macaroons.  

## Video Generation 
You can generate your own videos (Mandelbrot, Julia, Mandelbrot3D, GANs, ...) 
or provide your streaming session (Camera, Windows, URLs, Files).

## Dashboard
A dashboard is available to monitor and visualize the streaming videos. 


# Installation 

A docker-compose file will instantiate the following services:

 - bitcoind
 - lightningd (only LND currently supported)
 - router_peer ( is used to inform all new clients about other clients in the swarm )
 - dashboard ( VUE, React)


# Dashboard
A Web Service to visualize and manage the streaming of videos. 

 - BACKEND in Django to monitor and handle swarms and invoices

 - FRONTEND in VUE/Vuetify to visualize and manage the streaming  


## Protocol
```
1. Alice connects to a list of available nodes (Random, LN wallets, group of people, friends, bots) 
2. She ask for the list of available media
3. She decides to connect to swarm_id: <hash256> 
4. Bob responds and ask for payment streaming start
    5. Alice accept and start paying invoices
    6. Bob sends video chunks 

ASK_MEDIAS = {"from_id" }
MEDIAS_HAVE = {"from_id", [{"swarm_id": {"file_size", ...}}]}
ASK_SWARM = {"swarm_id", "N_MESSAGE"}
OK_SWARM = {"invoice"}
SEND_CHUNK = {"" }

Alice ----------->        
    {"cmd": ASK_MEDIA",
    "video": "Wonderland",
    "auth": "@macaroon" }
        <-----------    Bob
                {"cmd": OK_MEDIA", "auth": "@macaroon", "video":Wonderland", 
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


    
