import logging
import asyncio

from messages import HandShake

logging.basicConfig(level=logging.DEBUG)

class Peer:
    def __init__(self, connection_details, torrent_file, remove_peer):
        self.remove_peer = remove_peer
        
        self.read_buffer = b''
        
        self.peer_id = torrent_file.peer_id
        self.info_hash = torrent_file.info_hash
        
        self.reader, self.writer = None, None
        self.ip = connection_details["ip"]
        self.port = connection_details["port"]

        self.connected = False
        self.handshake = False
        
        self.statuses = {
            "choking": True, "interested": False, "leecher": True,
            "seeder": False, "connected": False, "handshake": False
        }
    
    @property
    def connected(self):
        return self.writer and not self.writer.is_closing()
    
    async def run(self):
        
        if not await self.connect():
            return False
        if not await self.send_handshake():
            return False

        while self.connected:
            message_type, message_bytes = await self.process_buffer()
            match message_type:
                case "handshake":
                    self.on_handshake(message_bytes)
                case _:
                    print("Other message")

            await asyncio.sleep(2)

    async def connect(self):
        try:
            self.reader, self.writer = await asyncio.wait_for(
                asyncio.open_connection(self.ip, self.port),
                timeout=5
            )
            self.on_connect()
            return True
        except asyncio.TimeoutError as e:
            print(f"Connection attempt to {self.ip}:{self.port} timed out.")
            await self.clean_up()
            return False
        except Exception as e:
            print(f"{self.ip}:{self.port}: {e}")
            await self.clean_up()
            return False
    
    def on_connect(self):
        print(f"Connected to {self.ip}:{self.port}")
    
    async def send_handshake(self):
        try:
            pstr = b'BitTorrent protocol'
            pstrlen = len(pstr)
            reserved = bytes([0]*8)
            handshake = HandShake(pstrlen, pstr, reserved, self.info_hash, self.peer_id)
            self.writer.write(handshake.pack())
            await self.writer.drain()
            return True
        except Exception as e:
            print(f"{self.ip}:{self.port}: {e}")
            await self.clean_up()
            return False
    
    def on_handshake(self, handshake_data_bytes):
        handshake_data = HandShake.unpack(handshake_data_bytes)
        if handshake_data.info_hash != self.info_hash:
            print(f"{self.ip}:{self.port}: Invalid info hash")
            self.clean_up()
        else:
            self.handshake = True
    
    async def process_buffer(self):
        
        self.read_buffer += await self.reader.read(65536)

        if not self.handshake and len(self.read_buffer) >= 68:
            message_bytes = self.read_buffer[:68]
            self.read_buffer = self.read_buffer[68:]
            return "handshake", message_bytes
      
        while len(self.read_buffer) >= 4:
            message_length = int.from_bytes(self.read_buffer[:4], byteorder='big')
            self.read_buffer = self.read_buffer[4:]

            match message_length:
                case 0:
                    return "keep_alive", b''
                case 1:
                    if len(self.read_buffer) >= 1:
                        message_id = int.from_bytes(self.read_buffer[:1], byteorder='big')
                        self.read_buffer = self.read_buffer[1:]
                        match message_id:
                            case 0:
                                return "choke", b''
                            case 1:
                                return "unchoke", b''
                            case 2:
                                return "interested", b''
                            case 3:
                                return "not_interested", b''
                            case _:
                                # raise exception
                                pass
                # not 2
                case 2:
                    # bitfield
                    pass
                case _:
                    self.on_message(message_length)
            
            if message_length == 0:
                self.on_keep_alive()
                return
            if len(self.read_buffer) < 4 + message_length:
                # Full messages not accumulated yet
                return
            message = self.read_buffer[4:4+message_length]
            self.read_buffer = self.read_buffer[4+message_length:]
            print("Message: ", message)
    
    async def clean_up(self):
        if self.connected:
            self.writer.close()
            await self.writer.wait_closed()
        self.remove_peer(self)
        