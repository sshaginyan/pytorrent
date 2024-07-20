import aiohttp
import asyncio
from peer import Peer
from pprint import pprint
from urllib.parse import urlencode
from collections import namedtuple
from bencoding import decode, encode

PeerAddr = namedtuple('PeerAddr', ['ip', 'port', 'allowed'])

class PeersManager: 
    def __init__(self, torrent_file):
        self.peer_addrs = []
        self.torrent_file = torrent_file
        # this property is temp
        self.tracker_urls = [url.decode() for url in torrent_file.announce_list if url.startswith(b'http')]
        
    async def get_peers(self):
        loop = asyncio.get_event_loop()
        for url in self.tracker_urls:
            d_peers = await self._get_peers_http(url, self.torrent_file)
            self.interval, peers = d_peers.values() 
            peers_coro = [loop.run_in_executor(None, Peer(peer).check_peer_connection) for peer in peers]
            self.peers = await asyncio.gather(*peers_coro)

    async def _get_peers_http(self, url, torrent_file):
        params = urlencode({
            'upload': 0,
            'port': 6881,
            'download': 0,
            'event': 'started',
            'peer_id' : torrent_file.peer_id,
            'left': torrent_file.total_length,
            'info_hash': torrent_file.info_hash
        })

        async with aiohttp.ClientSession() as session:
            async with session.get(url+'?'+params) as response:
                binary_peers = await response.read()
        return decode(binary_peers)
    
    async def _get_peers_udp(self, torrent_file):
        pass