import struct
from dataclasses import dataclass


@dataclass
class Message:
    def pack(self):
        raise NotImplementedError

    @classmethod
    def unpack(cls, data):
        raise NotImplementedError

@dataclass
class HandShake(Message):
    pstrlen: int
    pstr: bytes
    reserved: bytes
    info_hash: bytes
    peer_id: bytes

    def pack(self):
        return struct.pack(f">B{self.pstrlen}s8s20s20s", self.pstrlen, self.pstr, self.reserved, self.info_hash, self.peer_id)

    @classmethod
    def unpack(cls, data):
        pstrlen, = struct.unpack(">B", data[0:1])
        pstr, reserved, info_hash, peer_id = struct.unpack(f">{pstrlen}s8s20s20s", data[1:])
        return cls(pstrlen, pstr, reserved, info_hash, peer_id)