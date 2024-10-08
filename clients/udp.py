import struct
import random
import asyncio
from urllib.parse import urlparse

async def fetch_peer_list(url, peer_id, total_length, info_hash):
    parsed_url = urlparse(url)
    
    loop = asyncio.get_running_loop()

    transport, protocol = await loop.create_datagram_endpoint(
        lambda: TrackerProtocol(info_hash, peer_id),
        remote_addr=(parsed_url.hostname, parsed_url.port)
    )
    try:
        await protocol.on_connection_made()
        await protocol.on_announce(total_length)
    finally:
        transport.close()
    return protocol.peers

class TrackerProtocol:
    def __init__(self, info_hash, peer_id):
        self.peers = None
        self.transport = None
        
        self.peer_id = peer_id
        self.info_hash = info_hash
        
        self.transaction_id = random.randint(0, 0xFFFFFFFF)
        self.connection_id = 0x41727101980
        self.event = asyncio.Event()

    async def on_connection_made(self):
        action = 0
        connect_request = struct.pack("!QII", self.connection_id, action, self.transaction_id)
        self.transport.sendto(connect_request)
        await self.event.wait()
        self.event.clear()

    async def on_announce(self, total_length):
        action = 1
        downloaded = 0
        left = total_length
        uploaded = 0
        event = 0  # 0: none; 1: completed; 2: started; 3: stopped
        ip = 0
        key = random.randint(0, 0xFFFFFFFF)
        num_want = -1  # default
        port = 6881
        announce_request = struct.pack("!QII20s20sQQQIIIiH", self.connection_id, action, self.transaction_id, self.info_hash, self.peer_id, downloaded, left, uploaded, event, ip, key, num_want, port)
        self.transport.sendto(announce_request)
        await self.event.wait()
        self.event.clear()

    def connection_made(self, transport):
        self.transport = transport
    
    def connection_lost(self, exc):
        print("Connection lost:", exc)
    
    def error_received(self, exc):
        print('Error received:', exc)

    def datagram_received(self, data, addr):
        if len(data) == 16:
            action, transaction_id, connection_id = struct.unpack('!IIQ', data)
            self.connection_id = connection_id
            self.event.set()
        elif len(data) >= 20:
            n = len(data) - 20
            fixed_format = '!IIIII'
            peers_format = f'{n}s'
            format_string = fixed_format + peers_format
            unpacked_data = struct.unpack(format_string, data)
            action, transaction_id, interval, leechers, seeders = unpacked_data[:5]
            peers_data = unpacked_data[5]
            peers = []
            for i in range(0, len(peers_data), 6):
                ip_bytes = peers_data[i:i+4]
                port_bytes = peers_data[i+4:i+6]
                
                ip = '.'.join(map(str, ip_bytes))
                port = struct.unpack('!H', port_bytes)[0]
                
                peers.append({"ip": ip, "port": port, "peer_id": None})
            self.event.set()
            self.peers = {
                "interval": interval,
                "peers": peers
            }