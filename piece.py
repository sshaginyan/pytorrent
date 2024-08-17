class Piece:
    def __init__(self, piece_index, piece_size, piece_hash):
        self.is_full = False
        self.piece_size = piece_size
        self.piece_hash = piece_hash
        self.piece_index = piece_index
        
