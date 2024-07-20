import socket
import aiohttp
import asyncio

class Peer:
    def __init__(self, peer_data):
        self.connected = None
        for key, value in peer_data.items():
            setattr(self, key.decode().replace(' ', '_'), value)

    def check_peer_connection(self):
        try:
            self.socket = socket.create_connection((self.ip.decode(), self.port), timeout=5)
            self.socket.setblocking(False)
            self.connected = True
        except Exception as e:
            self.connected = False
        return self