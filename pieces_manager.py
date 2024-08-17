from piece import Piece

from pprint import pprint

HASH_SIZE = 20

class PiecesManager:
    def __init__(self, torrent_file):
        self.pieces = []
        self.pieces_hash_list = torrent_file.pieces
        self.piece_length = torrent_file.piece_length
        self.total_length = torrent_file.total_length
        self.number_of_pieces = torrent_file.number_of_pieces
        self.create_piece_list()

    def create_piece_list(self):
        for index in range(self.number_of_pieces):
            start = index * HASH_SIZE
            end = start + HASH_SIZE
            if index == self.number_of_pieces - 1:
                last_piece_length = self.total_length - (self.number_of_pieces - 1) * self.piece_length
                self.pieces.append(Piece(index, last_piece_length, self.pieces_hash_list[start:end]))
            else:
                self.pieces.append(Piece(index, self.piece_length, self.pieces_hash_list[start:end]))

    def pieces_completed(self):
        return all(piece.is_full for piece in self.pieces)
    # def _load_files(self):
    #     files = []
    #     piece_offset = 0
    #     piece_size_used = 0

    #     for f in self.torrent.file_names:
    #         current_size_file = f["length"]
    #         file_offset = 0

    #         while current_size_file > 0:
    #             id_piece = int(piece_offset / self.torrent.piece_length)
    #             piece_size = self.pieces[id_piece].piece_size - piece_size_used

    #             if current_size_file - piece_size < 0:
    #                 file = {"length": current_size_file,
    #                         "idPiece": id_piece,
    #                         "fileOffset": file_offset,
    #                         "pieceOffset": piece_size_used,
    #                         "path": f["path"]
    #                         }
    #                 piece_offset += current_size_file
    #                 file_offset += current_size_file
    #                 piece_size_used += current_size_file
    #                 current_size_file = 0

    #             else:
    #                 current_size_file -= piece_size
    #                 file = {"length": piece_size,
    #                         "idPiece": id_piece,
    #                         "fileOffset": file_offset,
    #                         "pieceOffset": piece_size_used,
    #                         "path": f["path"]
    #                         }
    #                 piece_offset += piece_size
    #                 file_offset += piece_size
    #                 piece_size_used = 0

    #             files.append(file)
    #     return files