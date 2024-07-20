# https://github.com/Textualize/textual
import asyncio # Don't need this for now
from torrent_file import TorrentFile
from tracker import Tracker
from pprint import pprint
import bencode

async def main():
    # torrent_file = TorrentFile('Artificial_Intelligence.torrent')
    torrent_file = TorrentFile('torrents/Artificial_Intelligence.torrent')
    tracker = Tracker(torrent_file)
    peers = await tracker.get_peers()
    print(peers)
    # pprint(bencode.decode(peers))

    # while not pieces_manager.all_pieces_completed():
    #     for piece in self.pieces_manager.pieces:
    #         index = piece.piece_index

    #         if pieces_manager.pieces[index].is_full:
    #             continue
       


if __name__ == '__main__':
    asyncio.run(main())