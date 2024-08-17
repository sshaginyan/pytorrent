# https://github.com/Textualize/textual
import asyncio
from tracker import Tracker
from torrent_file import TorrentFile
from peers_manager import PeersManager
from pieces_manager import PiecesManager

async def main():
    torrent_file = TorrentFile('torrents/grok.torrent')
    exit()
    tracker = Tracker(torrent_file)
    peers_connection_details = await tracker.fetch_tracker()
    peers_manager = PeersManager(peers_connection_details)
    peers_manager.create_peers(torrent_file)
    pieces_manager = PiecesManager(torrent_file)
    
    await peers_manager.run_peers()

    # while not pieces_manager.pieces_completed():
    #     await asyncio.sleep(5)
    #     print('Pieces completed: ', pieces_manager.pieces_completed())
    #     for piece in self.pieces_manager.pieces:
    #         index = piece.piece_index

    #         if pieces_manager.pieces[index].is_full:
    #             continue
       


if __name__ == '__main__':
    asyncio.run(main())