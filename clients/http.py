import aiohttp
import bencode
from urllib.parse import urlencode

async def fetch_peer_list(url, peer_id, total_length, info_hash):
    params = urlencode({
        'upload': 0,
        'port': 6881,
        'download': 0,
        'event': 'started',
        'peer_id' : peer_id,
        'left': total_length,
        'info_hash': info_hash
    })

    def format_peer_data(peer):
        return {
            "ip": peer[b"ip"].decode("utf-8"),
            "port": peer[b"port"],
            "peer_id": peer[b"peer id"].hex()
        }

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{url}?{params}") as response:
            if response.status == 200:
                tracker_response = bencode.decode(await response.read())
                if b'failure reason' in tracker_response:
                    return None
                return {
                    "interval": tracker_response[b'interval'],
                    "peers": list(map(format_peer_data, tracker_response[b'peers']))
                }
