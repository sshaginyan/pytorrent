import os
#TODO: We're not using this library, but we need too
import urllib.parse
from hashlib import sha1
from pprint import pprint
from bencoding import encode, decode


class TorrentFile:
    def __init__(self, path):
        d_file = self._read_file(path)
        self.peer_id = self._generate_peer_id()
        self.info_hash = self._get_info_hash(d_file[b'info'])
        self.total_length = self._get_total_length(d_file[b'info'][b'files'])
        self.announce_list = self._get_announce_list(d_file[b'announce'], d_file[b'announce-list'])

    def _read_file(self, path):
        with open(path, 'rb') as file:
            file_bytes = file.read()
        return decode(file_bytes)
          
    def _get_info_hash(self, info):
        print(sha1(encode(info)).digest())
        return sha1(encode(info)).digest()
    
    def _get_announce_list(self, announce_url, announce_list): 
        return {announce_url , *{url for [url] in announce_list}}
    
    def _get_total_length(self, files):
        total_length = 0
        for file in files:
            total_length += file[b'length']
        return total_length

    def _generate_peer_id(self):
        # TODO: Why is this prefix used?
        client_prefix = '-XY0001-'
        unique_id = os.urandom(20 - len(client_prefix))
        peer_id = client_prefix.encode() + unique_id
        return peer_id