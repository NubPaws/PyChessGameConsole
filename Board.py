from Pieces import Piece
from Pieces import new_empty_piece


# Create the backline for building the board
def create_back_line(color: Piece.Color):
	rook = Piece.Type.Rook
	knight = Piece.Type.Knight
	bishop = Piece.Type.Bishop
	queen = Piece.Type.Queen
	king = Piece.Type.King
	pieces = [rook, knight, bishop, queen, king, bishop, knight, rook]
	return [Piece(p, color) for p in pieces]


# Create the front line for building a board
def create_front_line(color: Piece.Color):
	return [Piece(Piece.Type.Pawn, color) for i in range(8)]


# Creates an empty line for building a board
def create_empty_line():
	return [new_empty_piece() for i in range(8)]


# Generate the board
def createBoard():
	black = Piece.Color.Black
	white = Piece.Color.White
	
	board = [
		create_back_line(black),
		create_front_line(black),
		create_empty_line(),
		create_empty_line(),
		create_empty_line(),
		create_empty_line(),
		create_front_line(white),
		create_back_line(white)
	]
	return board


# Convert from pos to move
def conv_pos(pos: str):
	return (ord(pos[0]) - 65, 8 - int(pos[1]))


# Convert move from text to actual move
def conv_move(move: str):
	dirs = move.split("->")
	return (conv_pos(dirs[0]), conv_pos(dirs[1]))


class Board:
	def __init__(self):
		self.board = createBoard()
		self.marked = [[False for i in range(8)] for j in range(8)]
	
	
	# Check if x, y are in the board
	def is_in(self, x: int, y: int):
		return 0 <= x and x < 8 and 0 <= y and y < 8
	
	
	# Check is a spot is empty
	def is_empty(self, x: int, y: int):
		return self.is_in(x, y) and self.board[y][x].piece == Piece.Type.Empty
	
	
	# Check is a spot is marked
	def is_marked(self, x: int, y: int):
		return self.is_in(x, y) and self.marked[y][x]
	
	
	# Check if two pieces are of the same color
	def is_same_color(self, x1: int, y1: int, x2: int, y2: int):
		return self.board[y1][x1].color == self.board[y2][x2].color
	
	
	# Get the color of the piece
	def get_color(self, x: int, y: int):
		return self.board[y][x].color
	
	
	# Get the type of a piece
	def get_type(self, x: int, y: int):
		return self.board[y][x].piece
	
	
	# Get the first piece in the list, it's position
	def get_piece_pos(self, piece: Piece.Type, color: Piece.Color):
		for i in range(8):
			for j in range(8):
				if self.board[i][j] == piece and self.board[i][j] == color:
					return (j, i)
	
	
	# Move a piece to another
	def move(self, x1: int, y1: int, x2: int, y2: int):
		self.board[y1][x1].moved = True
		self.board[y2][x2] = self.board[y1][x1]
		self.board[y1][x1] = new_empty_piece()
	
	
	# Switch two pieces
	def switch(self, x1: int, y1: int, x2: int, y2: int):
		tmp = self.board[y1][x2]
		self.board[y1][x1] = self.board[y2][x2]
		self.board[y2][x2] = tmp
	
	
	# Try and add a movable spot
	def add_spot(self, moves: list, x1: int, y1: int, x2: int, y2: int):
		# Checks if a spot is empty, if so, adds it to the moves list,
		# otherwise, it will check if the block is still a valid spot
		# and if so it will add it but return False.
		if self.is_empty(x2, y2):
			moves.append((x2, y2))
			return True
		else:
			if not self.is_same_color(x1, y1, x2, y2):
				moves.append((x2, y2))
			return False
	
	
	# Get pawn moves
	def get_pawn_moves(self, moves: list, x: int, y: int):
		# Check front
		check = (-1, +1)[self.board[y][x].is_black()]
		if self.is_empty(x, y + check):
			moves.append((x, y + check))
			if self.is_empty(x, y + check * 2):
				moves.append((x, y + check * 2))
		# Check if can eat
		if not self.is_empty(x - 1, y + check):
			moves.append((x - 1, y + check))
		if not self.is_empty(x + 1, y + check):
			moves.append((x + 1, y + check))
	
	
	# Get rook moves
	def get_rook_moves(self, moves: list, x: int, y: int):
		# Check up
		for i in range(y -1, -1, -1):
			if not self.add_spot(moves, x, y, x, i):
				break
		# Check down
		for i in range(y +1, 8, 1):
			if not self.add_spot(moves, x, y, x, i):
				break
		# Check left
		for i in range(x -1, -1, -1):
			if not self.add_spot(moves, x, y, i, y):
				break
		# Check right
		for i in range(x +1, 8, 1):
			if not self.add_spot(moves, x, y, i, y):
				break
	
	
	# Get bishop moves
	def get_bishop_moves(self, moves: list, x: int, y: int):
		# Check top left
		for i, j in zip(range(x -1, -1, -1), range(y -1, -1, -1)):
			if not self.add_spot(moves, x, y, i, j):
				break
		# Check top right
		for i, j in zip(range(x +1, 8), range(y -1, -1, -1)):
			if not self.add_spot(moves, x, y, i, j):
				break
		# Check bottom left
		for i, j in zip(range(x -1, -1, -1), range(y +1, 8)):
			if not self.add_spot(moves, x, y, i, j):
				break
		# Check bottom right
		for i, j in zip(range(x +1, 8), range(y +1, 8)):
			if not self.add_spot(moves, x, y, i, j):
				break
	
	
	# Get knight moves
	def get_knight_moves(self, moves: list, x: int, y: int):
		# Check top
		if y > 1:
			if x > 0:
				self.add_spot(moves, x, y, x - 1, y - 2)
			if x < 7:
				self.add_spot(moves, x, y, x + 1, y - 2)
		# Check bottom
		if y < 6:
			if x > 0:
				self.add_spot(moves, x, y, x - 1, y + 2)
			if x < 7:
				self.add_spot(moves, x, y, x + 1, y + 2)
		# Check left
		if x > 1:
			if y > 0:
				self.add_spot(moves, x, y, x - 2, y - 1)
			if y < 7:
				self.add_spot(moves, x, y, x - 2, y + 1)
		# Check right
		if x < 6:
			if y > 0:
				self.add_spot(moves, x, y, x + 2, y - 1)
			if y < 7:
				self.add_spot(moves, x, y, x + 2, y + 1)
	
	
	# Get all the moves from a team with the specified color
	def get_team_moves(self, color: Piece.Color):
		# Gets all the team's moves
		other_moves = []
		for i in range(8):
			for j in range(8):
				if self.board[j][i] == color:
					if self.board[j][i] == Piece.Type.King:
						# Go around the king and append
						for u in range(i -1, i +2):
							for t in range(j -1, j +2):
								other_moves.append((u, t))
					else:
						other_moves += self.get_moves(i, j)
		return other_moves
	
	
	# Get all the moves from the other team
	def get_other_team_moves(self, color: Piece.Color):
		other_color = (Piece.Color.White, Piece.Color.Black)[color == Piece.Color.White]
		return self.get_team_moves(other_color)
	
	
	# Gets the king moves with a complex alg that is simple.
	# Check all the pieces, for the king, to avoid recursiveness,
	# we just do a simple 3x3 check around our king boi
	def get_king_moves(self, moves: list, x: int, y: int):
		other_moves = self.get_other_team_moves(self.get_color(x, y))
		# Add the moves for the king
		for i in range(x -1, x +2):
			for j in range(y -1, y +2):
				if not (i, j) in other_moves:
					self.add_spot(moves, x, y, i, j)
	
	
	# General function that calls the one above it to get the list
	# of proper moves
	def get_moves(self, x: int, y: int):
		piece = self.board[y][x]
		moves = []
		if piece == Piece.Type.Empty:
			return moves
		elif piece == Piece.Type.Pawn:
			self.get_pawn_moves(moves, x, y)
		elif piece == Piece.Type.Rook:
			self.get_rook_moves(moves, x, y)
		elif piece == Piece.Type.Bishop:
			self.get_bishop_moves(moves, x, y)
		elif piece == Piece.Type.Knight:
			self.get_knight_moves(moves, x, y)
		elif piece == Piece.Type.Queen:
			self.get_rook_moves(moves, x, y)
			self.get_bishop_moves(moves, x, y)
		elif piece == Piece.Type.King:
			self.get_king_moves(moves, x, y)
		return moves
	
	
	# Make sure that this is a valid move that can be done,
	# if so, move it.
	def move_validly(self, x1: int, y1: int, x2: int, y2: int):
		if (x2, y2) in self.get_moves(x1, y1):
			self.move(x1, y1, x2, y2)
			return True
		else:
			return False
	
	
	# Select what to mark or unmark with a list
	def mark(self, moves: list, yes: bool = True):
		self.unmark_all()
		for x, y in moves:
			self.marked[y][x] = yes
	
	
	# Unmarks all places
	def unmark_all(self):
		self.marked = [[False for i in range(8)] for j in range(8)]
	
	
	# Check if a color is losing or winning (son)
	# Returns 1 for check, and 2 for check mate, 0 for none
	def is_check_mate(self, color: Piece.Color):
		other_moves = self.get_other_team_moves(color)
		king_pos = self.get_piece_pos(Piece.Type.King, color)
		king_moves = []
		if king_pos in other_moves:
			self.get_king_moves(king_moves, king_pos[0], king_pos[1])
			if king_moves == []:
				return 2
			else:
				return 1
		else:
			return 0
	
	
	# Nicely display the board
	def display(self):
		r = range(8)
		line_break = "-" * 41
		print("| A  | B  | C  | D  | E  | F  | G  | H  |")
		print(line_break)
		for i in r:
			print("| ", end="")
			for j in r:
				if self.is_empty(j, i):
					if self.is_marked(j, i):
						print("XX", end=" | ")
					else:
						print("  ", end=" | ")
				else:
					print(self.board[i][j], end=" | ")
			print(8 - i)
			print(line_break)
