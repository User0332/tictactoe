import os
import utils
from copy import deepcopy
from minimax import computer_move
from reinforce import computer_move_rf
from tracemove import (
    get_full_win_contrib2,
    get_full_loss_contrib2,
    highlight_moves
)
from utils import (
	X, O, bprint, place_move,
	get_possible_moves, get_move,
	win_occurred, full_board,
	add_this_game,
	HIGHLIGHT_FOCUS_MOVE
)

clear = lambda: os.system("cls" if os.name == "nt" else "clear")

board = [
	['1', '2', '3'],
	['4', '5', '6'],
	['7', '8', '9']
]

def human_first(difficulty: str, use_rf: bool) -> bool:
	if use_rf: get_comp_move = computer_move_rf
	else: get_comp_move = computer_move

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
			if use_rf: add_this_game("loss")
			return True

		if full_board(board):
			print("Draw!")
			if use_rf: add_this_game("draw")
			return None
		
		comp_move = get_comp_move(board, get_possible_moves(board), difficulty)

		clear()

		print(f"Computer Move: {comp_move}")

		place_move(board, comp_move, O, log=True)

		if win_occurred(board):
			bprint(board)
			print(f"Computer wins!")
			if use_rf: add_this_game("win")
			return False

def computer_first(difficulty: str, use_rf: bool) -> bool:
	utils.COMP_FIRST = True

	if use_rf: get_comp_move = computer_move_rf
	else: get_comp_move = computer_move
	
	while 1:
		clear()

		comp_move = get_comp_move(board, get_possible_moves(board), difficulty)

		print(f"Computer Move: {comp_move}")

		place_move(board, comp_move, O, log=True)

		bprint(board)

		if win_occurred(board):
			print(f"Computer wins!")
			if use_rf: add_this_game("win")
			return False

		if full_board(board):
			print("Draw!")
			if use_rf: add_this_game("draw")
			return None

		human_move = get_move(
			get_possible_moves(board)
		)

		place_move(board, human_move, X, log=True)

		bprint(board)

		if win_occurred(board):
			print(f"You win!")
			if use_rf: add_this_game("loss")
			return True

def analyze_game(human_win: bool):
	loss_contrib = {
		X: get_full_loss_contrib2([move["move"] for move in utils.game_moves if move["player"] == X], X),
		O: get_full_loss_contrib2([move["move"] for move in utils.game_moves if move["player"] == O], O)
	}

	win_contrib = {
		X: get_full_win_contrib2([move["move"] for move in utils.game_moves if move["player"] == X], X),
		O: get_full_win_contrib2([move["move"] for move in utils.game_moves if move["player"] == O], O)
	}

	printing_board = deepcopy(board)

	highlight_moves(printing_board, { **loss_contrib[X], **loss_contrib[O] })
	
	for i, move in enumerate(utils.game_moves, start=1):
		move_num = move["move"]
		row = move["board_after"][(move_num-1)//3]
		idx = (move_num-1) % 3

		row[idx] = f"{HIGHLIGHT_FOCUS_MOVE}{row[idx]}"

	while 1:
		clear()

		print("-- Tic-Tac-Toe Game Review --")

		for i, move in enumerate(utils.game_moves, start=1):
			print(f"{i}. {move['player']} played {move['move']}")

			bprint(move["board_after"], highlight=True, prepend="  ")

		print("\n-- Board Analyzation --")
		
		bprint(printing_board, highlight=True)
		print() # newline

		try:
			move_num = get_move((i for i in range(1, len(utils.game_moves)+1)), prompt="Move Number to Analyze: ")

			move = utils.game_moves[move_num-1]["move"]
			
			player = board[(move-1)//3][(move-1) % 3]

			if (player in (X, O)) and (human_win is None): # tie case
				print(f"Move #{move_num}'s contribution to a possible loss (player: {player}): {loss_contrib[player][move][0]*100}% ({loss_contrib[player][move][1]})")
				print(f"Move #{move_num}'s contribution to a possible win (player: {player}): {win_contrib[player][move][0]*100}% ({win_contrib[player][move][1]})")
				input("Press enter to continue ")
				continue

			if ((player == O) and human_win) or ((player == X) and not human_win):
				print(f"Move #{move_num}'s contribution to loss (player: {player}): {loss_contrib[player][move][0]*100}% ({loss_contrib[player][move][1]})")
				input("Press enter to continue ")
				continue

			if ((player == X) and human_win) or ((player == O) and not human_win):
				print(f"Move #{move_num}'s contribution to win (player: {player}): {win_contrib[player][move][0]*100}% ({win_contrib[player][move][1]})")
				input("Press enter to continue ")
				continue
			
		except KeyboardInterrupt:
			print("<Exit>")
			exit(0)

while 1:
	algo = input("Algorithm (reinforcement learning/minimax): ").lower()

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
		try: human_win = human_first(difficulty, reinforcement)
		except KeyboardInterrupt:
			print("<Exit>")
			exit(0)
		break

	if gofirst in ("no", 'n'):
		try: human_win = computer_first(difficulty, reinforcement)
		except KeyboardInterrupt:
			print("<Exit>")
			exit(0)
		break

	print("Invalid Input!")

while 1:
	analyze = input("Analyze game? (yes/no) ").lower()

	if analyze in ("yes", 'y'): break

	if analyze in ("no", 'n'): exit()

	print("Invalid Choice!")

try: analyze_game(human_win)
except KeyboardInterrupt:
	print("<Exit>")
	exit(0)