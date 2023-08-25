import urllib.parse
import aiohttp
import requests
import asyncio
from peer import Peer
from pprint import pprint
from bencoding import decode, encode
from collections import namedtuple

SockAddr = namedtuple('SockAddr', ['ip', 'port', 'allowed'])

class Tracker:
    def __init__(self, torrent_file):
        self.torrent_file = torrent_file
        self.dict_sock_addr = {}
        self.tracker_url = 'https://academictorrents.com/announce.php'
        
    async def get_peers(self):
        await self.http_request()
        # self.try_peer_connect()

    async def http_request(self):
        params = urllib.parse.urlencode({
            'upload': 0,
            'port': 6881,
            'download': 0,
            'event': 'started',
            'peer_id' : self.torrent_file.peer_id,
            'left': self.torrent_file.total_length,
            'info_hash': self.torrent_file.info_hash
        })
        
        # response = requests.get(self.tracker_url, params = params, timeout= 10)
        # print(response.request.url)

        async with aiohttp.ClientSession() as session:
            async with session.get(self.tracker_url+'?'+params) as response:
                binary_data = await response.read()
        peers = decode(binary_data)
        pprint(peers)

        
        
        # async with httpx.AsyncClient() as client:
        #     response = await client.get(self.tracker_url, params=params)
        # print(response.content)

        # response = requests.get(url=self.tracker_url, params=params, timeout=10)
        # list_peers = decode(response.content)
        
        # pprint(list_peers)
        
        # for peer in list_peers[b'peers']:
        #     sock_addr = SockAddr(peer[b'ip'], peer[b'port'], allowed = True)
        #     self.dict_sock_addr[str(peer[b'ip'])+ ':' + str(peer[b'port'])] = sock_addr
    
    def try_peer_connect(self):
        with asyncio.TaskGroup as tg:
            for peer in self.dict_sock_addr.values():
                tg.create_task(Peer().check_peer_connection(peer))
        


            

        