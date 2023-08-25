import socket

class Peer:
    async def check_peer_connection(self, peer):
        try:
            self.socket = socket.create_connection((peer.ip, peer.port), timeout=2)
            self.healthy = True
        except Exception:
            return False
        return True