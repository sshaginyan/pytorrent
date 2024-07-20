import re
import os
import math
import bencode
import hashlib
import functools

class TorrentFile:
    def __init__(self, path):
        bencoded_torrent_data = self._read_file(path)
        torrent_data = bencode.decode(bencoded_torrent_data)
        
        for key, value in torrent_data.items():
            key = key.decode('utf-8')
            setattr(self, "_" + re.sub(r"[ -]", "_", key), value)

    def _read_file(self, path):
        with open(path, 'rb') as file:
            return file.read()

    @property
    def info_hash(self):
        return hashlib.sha1(bencode.encode(self._info)).digest()
    
    @property
    @functools.cache
    def announce_list(self):
        self._announce_list.append([self._announce])
        return self._announce_list
    
    @property
    def total_length(self):
        total_length = 0
        for file in self._info[b'files']:
            total_length += file[b'length']
        return total_length
    
    @property
    def number_of_pieces(self):
        return math.ceil(self.total_length / self._info[b"piece length"])
    
    @property
    def peer_id(self):
        client_prefix = '-PT010-'
        unique_id = os.urandom(20 - len(client_prefix))
        peer_id = client_prefix.encode() + unique_id
        return peer_id
    
    # def create_files(self, torrent_file):
    #     root = torrent_file[b'info'][b'name']

    #     if b'files' in torrent_file[b'info']:
    #         if not os.path.exists(root):
    #             os.mkdir(root, 0o0766 )

    #         for file in torrent_file[b'info'][b'files']:
    #             path_file = os.path.join(root, *file[b"path"])

    #             if not os.path.exists(os.path.dirname(path_file)):
    #                 os.makedirs(os.path.dirname(path_file))

    #             self.file_names.append({"path": path_file , "length": file[b"length"]})
    #             self.total_length += file[b"length"]

    #     else:
    #         self.file_names.append({"path": root , "length": torrent_file[b'info'][b'length']})
    #         self.total_length = torrent_file[b'info'][b'length']