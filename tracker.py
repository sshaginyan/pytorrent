from peer import Peer
from collections import namedtuple
from clients import http, udp, wss

from pprint import pprint


#TODO: Distributed Hash Table (DHT) and Peer Exchange (PEX)

PeerAddr = namedtuple('PeerAddr', ['ip', 'port', 'allowed'])

class Tracker:
    def __init__(self, torrent_file):
        self.torrent_file = torrent_file
        
    async def get_peers(self):
        peer_id = self.torrent_file.peer_id
        total_length = self.torrent_file.total_length
        info_hash = self.torrent_file.info_hash

        for url_tier in self.torrent_file.announce_list:
            for url in url_tier:
                peers = None
                url = url.decode()
                match url:
                    case _ if url.startswith('https'):
                        peers = await http.fetch_trackers(url, peer_id, total_length, info_hash)
                    case _ if url.startswith('udp'):
                        peers = await udp.fetch_trackers(url, peer_id, total_length, info_hash)
                    case _ if url.startswith('wss'):
                        pass
                if peers: return peers