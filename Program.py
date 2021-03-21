from Board import Board
from Board import conv_pos
from Board import conv_move
from Pieces import Piece
from os import system, name


# Function to clear the screen
def clear_screen():
	# For Windows
	if name == "nt":
		system("cls")
	# For Linux (posix)
	else:
		system("clear")


# Prints the main menu
def print_main_menu():
	print("1. Select")
	print("2. Move")
	


# Main function boiiiiis
def main():
	board = Board()
	turn = 0
	
	# Store for l8r use
	WHITE_COLOR = Piece.Color.White
	BLACK_COLOR = Piece.Color.Black
	
	print("At any time you can press 0 to terminate")
	
	# Main game loop
	while True:
		# Get the colors based on the turn
		cur_color = (BLACK_COLOR, WHITE_COLOR)[turn %2 == 0]
		other_color = (WHITE_COLOR, BLACK_COLOR)[cur_color == WHITE_COLOR]
		
		# Check if we have a check mate
		check_mate_status = board.is_check_mate(cur_color)
		
		# If we have a mate, well damn
		if check_mate_status == 2:
			print(f"{other_color.name} WINS!")
			return 0
		
		# Display the board, and who's turn it is
		board.display()
		print(f"{cur_color.name} turn.")
		
		# Display main menu and get the option
		print_main_menu()
		option = int(input("> "))
		
		# I don't wanna talk about it
		if option == 0:
			return 0
		elif option == 1: # Select
			pos = conv_pos(input("SELECT> "))
			if board.get_color(*pos) == cur_color:
				if check_mate_status == 1:
					if board.get_type(*pos) == Piece.Type.King:
						board.mark(board.get_moves(*pos))
					else:
						print("King is under check, re-select")
				else:
					board.mark(board.get_moves(*pos))
			else:
				print("Invalid selection, please select again.")
			turn -= 1
		elif option == 2: # Move
			f, t = conv_move(input("MOVE> "))
			if board.get_color(*f) == cur_color:
				if board.move_validly(*f, *t):
					board.unmark_all()
				else:
					print("Invalid move!")
					turn -= 1
		
		turn += 1
		clear_screen()
	

if __name__ == "__main__":
	main()