from enum import Enum

class Piece:
	
	class Type(Enum):
		Pawn = "P"
		Rook = "R"
		Bishop = "B"
		Knight = "N"
		Queen = "Q"
		King = "K"
		Empty = ""
	
	class Color(Enum):
		Black = 1
		White = 2
		Empty = 3
	
	
	def __init__(self, piece: Type, color: Color):
		self.piece = piece
		self.color = color
		self.moved = False
	
	
	def has_moved(self):
		return self.moved
	
	
	def is_empty(self):
		return self.piece == Piece.Type.Empty
	
	
	def is_black(self):
		return self.color == Piece.Color.Black
	
	
	def is_white(self):
		return self.color == Piece.Color.White
	
	
	def __str__(self):
		if self.piece == Piece.Type.Empty:
			return "  "
		return f"{('w', 'b')[self.color == Piece.Color.Black]}{self.piece.value}"
	
	
	# For simlpe equalities l8r
	def __eq__(self, p):
		if isinstance(p, Piece.Type):
			return self.piece == p
		if isinstance(p, Piece.Color):
			return self.color == p


# Generate a new empty piece
def new_empty_piece():
	return Piece(Piece.Type.Empty, Piece.Color.Empty)

