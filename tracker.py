import requests
from bencoding import decode, encode

class Tracker:
    def __init__(self, torrent_file):
        self.torrent_file = torrent_file
        self.get_peers()
        self.tracker_URL = None

    def get_peers(self):
        for a in self.torrent_file.announce_list: 
            if a.startswith(b'https://ip'):
                self.tracker_URL = a 
                
                
                # break
        print(self.tracker_URL)
        # print("peer_id : ",  self.torrent_file.peer_id)
        # print("peer_id len: ",  len(self.torrent_file.peer_id))
        # print(self.torrent_file.info_hashed)
        self.http_request()
        

    def http_request(self):
        # print("info hash is: ", self.torrent_file.info_hashed)
        params = {'info_hash': self.torrent_file.info_hashed,
                    'peer_id': b'u{U\x07\x98p\x97\xc4V\x8f\xbe\xe4\x80\xe7\xe9\x84\x15\x03\xaa\x90',
                    'upload': 0,
                    'download': 0,
                    'left': 2601915325,
                    'event': 'started',
                    'port': 6881
                  }
        response = requests.get(self.tracker_URL, params = params, timeout= 5)
        list_peers  = decode(response.content)
        print(list_peers)



            

        