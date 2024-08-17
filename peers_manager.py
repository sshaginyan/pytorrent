import asyncio
from peer import Peer

class PeersManager: 
    def __init__(self, peers_connection_details):
        self.peers = []
        self.peers_connection_details = peers_connection_details["peers"]
        self.interval = peers_connection_details["interval"]
        
    def create_peers(self, torrent_file):
        arguments = [torrent_file, self.remove_peer]
        self.peers = [
            Peer(peer_connection_details, *arguments)
            for peer_connection_details in self.peers_connection_details
        ]
    
    async def run_peers(self):
        peers_run = [peer.run() for peer in self.peers]
        await asyncio.gather(*peers_run)

    def remove_peer(self, peer):
        self.peers.remove(peer)
        print("Number of Peers left: ", len(self.peers))