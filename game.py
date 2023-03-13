import os
import locals
from algorithm import computer_move
from locals import (
	X, O, bprint, place_move,
	get_possible_moves, get_move,
	win_occurred, full_board
)

clear = lambda: os.system("cls" if os.name == "nt" else "clear")

board = [
	['1', '2', '3'],
	['4', '5', '6'],
	['7', '8', '9']
]

def human_first(difficulty: str):
	clear()

	while 1:
		bprint(board)

		human_move = get_move(
			get_possible_moves(board)
		)

		place_move(board, human_move, X, log=True)

		bprint(board)

		if win_occurred(board):
			print(f"You win!")
			break

		if full_board(board):
			print("Draw!")
			break
		
		comp_move = computer_move(board, get_possible_moves(board), difficulty)

		clear()

		print(f"Computer Move: {comp_move}")

		place_move(board, comp_move, O, log=True)

		if win_occurred(board):
			bprint(board)
			print(f"Computer wins!")
			break

def computer_first(difficulty: str):
	locals.COMP_FIRST = True
	
	while 1:
		clear()

		comp_move = computer_move(board, get_possible_moves(board), difficulty)

		print(f"Computer Move: {comp_move}")

		place_move(board, comp_move, O, log=True)

		bprint(board)

		if win_occurred(board):
			print(f"Computer wins!")
			# add_this_game("win")
			break

		if full_board(board):
			print("Draw!")
			# add_this_game("draw")
			break

		human_move = get_move(
			get_possible_moves(board)
		)

		place_move(board, human_move, X, log=True)

		bprint(board)

		if win_occurred(board):
			print(f"You win!")
			# add_this_game("loss")
			break
		
while 1:
	difficulty = input("Difficulty (easy/med/hard/impossible): ").lower()
	
	if difficulty in ("easy", "ez", 'e'):
		difficulty = "easy"
		break
	
	if difficulty in ("medium", "med", 'm'):
		difficulty = "medium"
		break

	if difficulty in ("hard", 'h'):
		difficulty = "hard"
		break

	if difficulty in ("impossible", 'i'):
		difficulty = "impossible"
		break

	print("Invalid Input!")

while 1:
	gofirst = input("You go first? (yes/no): ").lower()
	
	if gofirst in ("yes", 'y'):
		human_first(difficulty)
		break

	if gofirst in ("no", 'n'):
		computer_first(difficulty)
		break

	print("Invalid Input!")

