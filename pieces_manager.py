import bitstring
from piece import Piece

class PiecesManager:
    def __init__(self, torrent_file):
        self.torrent_file = torrent_file
        self.number_of_pieces = torrent_file.number_of_pieces
        self.bitfield = bitstring.BitArray(self.number_of_pieces)
        self.pieces = self._generate_pieces()
        self.files = self._load_files()
    def _generate_pieces(self):
        pieces = []
        for index in range(self.number_of_pieces):
            start = index * 20
            end = start + 20
            if index == self.number_of_pieces - 1:
                piece_length = self.torrent.total_length - (self.number_of_pieces - 1) * self.torrent_file.piece_length
                pieces.append(Piece(index, piece_length, self.torrent_file.pieces[start:end]))
            else:
                pieces.append(Piece(index, self.torrent_file.piece_length, self.torrent_file.pieces[start:end]))
        return pieces
    def _load_files(self):
        files = []
        piece_offset = 0
        piece_size_used = 0

        for f in self.torrent.file_names:
            current_size_file = f["length"]
            file_offset = 0

            while current_size_file > 0:
                id_piece = int(piece_offset / self.torrent.piece_length)
                piece_size = self.pieces[id_piece].piece_size - piece_size_used

                if current_size_file - piece_size < 0:
                    file = {"length": current_size_file,
                            "idPiece": id_piece,
                            "fileOffset": file_offset,
                            "pieceOffset": piece_size_used,
                            "path": f["path"]
                            }
                    piece_offset += current_size_file
                    file_offset += current_size_file
                    piece_size_used += current_size_file
                    current_size_file = 0

                else:
                    current_size_file -= piece_size
                    file = {"length": piece_size,
                            "idPiece": id_piece,
                            "fileOffset": file_offset,
                            "pieceOffset": piece_size_used,
                            "path": f["path"]
                            }
                    piece_offset += piece_size
                    file_offset += piece_size
                    piece_size_used = 0

                files.append(file)
        return files