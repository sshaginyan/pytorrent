import aiohttp
import bencode
from urllib.parse import urlencode

async def fetch_trackers(url, peer_id, total_length, info_hash):
    params = urlencode({
        'upload': 0,
        'port': 6881,
        'download': 0,
        'event': 'started',
        'peer_id' : peer_id,
        'left': total_length,
        'info_hash': info_hash
    })

    async with aiohttp.ClientSession() as session:
        async with session.get(url + '?' + params) as response:
            if response.status == 200:
                return bencode.decode(await response.read())