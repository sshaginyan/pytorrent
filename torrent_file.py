import os
import urllib.parse
import secrets

from bencoding import encode, decode
from hashlib import sha1

class TorrentFile:
    def __init__(self, path):
        # for key, value in self._read_torrent_file(path).items():
        #     setattr(self, key , value)
        t_file = self._read_torrent_file(path)
        self.info_hashed = self._get_info_hash(t_file[b'info'])
        self.peer_id = self._generate_peer_ID()
        self.announce_list = {t_file[b'announce'] , *{item[0] for item in t_file[b'announce-list']}}
        # for a in self.announce_list: 
        #     print(a)

    def _read_torrent_file(self, path):
        with open(path, 'rb') as fd:
            file_bytes = fd.read()

        decoded_file = decode(file_bytes)
        return decoded_file
          
    def _get_info_hash(self, info):
        return sha1(encode(info)).digest()
    
    def _get_announce_list(self, announce_URL, announce_list): 
        if not announce_URL in announce_list: 
            announce_list.append(announce_URL)
        return announce_list
    
    # def _generate_peer_ID(self):
        # rand = os.urandom(20)
        # # hex_rand = rand.hex()
        # return rand



    def _generate_peer_ID(self):
        # This is just a placeholder; use your client's prefix
        client_prefix = '-XY0001-'
        unique_id = os.urandom(20 - len(client_prefix))
        peer_id = client_prefix.encode() + unique_id
        return peer_id

    def generate_encoded_peer_id(self):
        peer_id = self._generate_peer_ID()
        return urllib.parse.quote_plus(peer_id)

    # print(generate_encoded_peer_id())

    



    

            

