import os
import utils
from minimax import computer_move, get_player_score
from reinforce import computer_move_rf
from utils import (
	X, O, bprint, place_move,
	get_possible_moves, get_move,
	win_occurred, full_board,
	add_this_game
)

clear = lambda: os.system("cls" if os.name == "nt" else "clear")

board = [
	['1', '2', '3'],
	['4', '5', '6'],
	['7', '8', '9']
]

def human_first(difficulty: str, use_rf: bool):
	if use_rf: get_comp_move = computer_move_rf
	else: get_comp_move = computer_move

	clear()

	while 1:
		bprint(board)

		human_move = get_move(
			get_possible_moves(board)
		)

		place_move(board, human_move, X, log=True, o_score=get_player_score(board, O)+get_player_score(board, X))

		bprint(board)

		if win_occurred(board):
			print(f"You win!")
			if use_rf: add_this_game("loss")
			break

		if full_board(board):
			print("Draw!")
			if use_rf: add_this_game("draw")
			break
		
		comp_move = get_comp_move(board, get_possible_moves(board), difficulty)

		clear()

		print(f"Computer Move: {comp_move}")

		place_move(board, comp_move, O, log=True, o_score=get_player_score(board, O)+get_player_score(board, X))

		if win_occurred(board):
			bprint(board)
			print(f"Computer wins!")
			if use_rf: add_this_game("win")
			break

def computer_first(difficulty: str, use_rf: bool):
	utils.COMP_FIRST = True

	if use_rf: get_comp_move = computer_move_rf
	else: get_comp_move = computer_move
	
	while 1:
		clear()

		comp_move = get_comp_move(board, get_possible_moves(board), difficulty)

		print(f"Computer Move: {comp_move}")

		place_move(board, comp_move, O, log=True, o_score=get_player_score(board, O)+get_player_score(board, X))

		bprint(board)

		if win_occurred(board):
			print(f"Computer wins!")
			if use_rf: add_this_game("win")
			break

		if full_board(board):
			print("Draw!")
			if use_rf: add_this_game("draw")
			break

		human_move = get_move(
			get_possible_moves(board)
		)

		place_move(board, human_move, X, log=True, o_score=get_player_score(board, O)+get_player_score(board, X))

		bprint(board)

		if win_occurred(board):
			print(f"You win!")
			if use_rf: add_this_game("loss")
			break
		
while 1:
	algo = input("Algorithm (reinforcement learning/minimax): ")

	if algo in ("reinforcement", "reinforcement learning", "reinforce", "rf", "rf learning", 'r'):
		reinforcement = True
		break

	if algo in ("minimax", 'm'):
		reinforcement = False
		break

	print("Invalid Choice!")

if not reinforcement:

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

		print("Invalid Choice!")
else: 
	print("Note: reinforcement mode has no difficulty selection")
	difficulty = "reinforcement"

while 1:
	gofirst = input("You go first? (yes/no): ").lower()
	
	if gofirst in ("yes", 'y'):
		try: human_first(difficulty, reinforcement)
		except KeyboardInterrupt: print("<Exit>")
		break

	if gofirst in ("no", 'n'):
		try: computer_first(difficulty, reinforcement)
		except KeyboardInterrupt: print("<Exit>")
		break

	print("Invalid Input!")