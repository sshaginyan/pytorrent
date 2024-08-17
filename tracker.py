from clients import http, udp

class Tracker:
    def __init__(self, torrent_file):
        self.peer_id = torrent_file.peer_id
        self.info_hash = torrent_file.info_hash
        self.total_length = torrent_file.total_length
        self.announce_list = torrent_file.announce_list
        
    async def fetch_tracker(self):
        peers = None
        
        for url_tier in self.announce_list:
            for url in url_tier:
                url = url.decode()
                match url:
                    case _ if url.startswith('https'):
                        peers = await http.fetch_peer_list(url, self.peer_id, self.total_length, self.info_hash)
                    case _ if url.startswith('udp'):
                        peers = await udp.fetch_peer_list(url, self.peer_id, self.total_length, self.info_hash)
                    # TODO: WSS, distributed Hash Table (DHT) and Peer Exchange (PEX), and Local Peer Discovery (LPD)
                if peers: return peers