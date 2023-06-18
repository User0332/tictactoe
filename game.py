import os
import utils
from minimax import computer_move, get_player_score
from reinforce import computer_move_rf
from tracemove import (
    get_full_win_contrib,
    get_full_loss_contrib,
    get_full_win_contrib2,
    get_full_loss_contrib2
)
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

def human_first(difficulty: str, use_rf: bool) -> bool:
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
			return True

		if full_board(board):
			print("Draw!")
			if use_rf: add_this_game("draw")
			return None
		
		comp_move = get_comp_move(board, get_possible_moves(board), difficulty)

		clear()

		print(f"Computer Move: {comp_move}")

		place_move(board, comp_move, O, log=True, o_score=get_player_score(board, O)+get_player_score(board, X))

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

		place_move(board, comp_move, O, log=True, o_score=get_player_score(board, O)+get_player_score(board, X))

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

		place_move(board, human_move, X, log=True, o_score=get_player_score(board, O)+get_player_score(board, X))

		bprint(board)

		if win_occurred(board):
			print(f"You win!")
			if use_rf: add_this_game("loss")
			return True

def basic_analyze(human_win: bool):
	loss_contrib = {
	X: get_full_loss_contrib(board, [move["move"] for move in utils.game_moves if move["player"] == X], X),
	O: get_full_loss_contrib(board, [move["move"] for move in utils.game_moves if move["player"] == O], O)
}

	win_contrib = {
		X: get_full_win_contrib(board, [move["move"] for move in utils.game_moves if move["player"] == X], X),
		O: get_full_win_contrib(board, [move["move"] for move in utils.game_moves if move["player"] == O], O)
	}

	while 1:
		clear()
		bprint(board)

		try:
			move = get_move((1, 2, 3, 4, 5, 6, 7, 8, 9), prompt="Move to Analyze: ")

			try: move_num = [i for i, game_move in enumerate(utils.game_moves) if game_move["move"] == move][0]+1
			except IndexError:
				input("No one moved there!\nPress enter to continue ")
				continue

			player = board[(move-1)//3][(move-1) % 3]

			if (player in (X, O)) and (human_win is None): # tie case
				print(f"Move #{move_num}'s contribution to a possible loss (player: {player}): {loss_contrib[player][move]*100}%")
				print(f"Move #{move_num}'s contribution to a possible win (player: {player}): {win_contrib[player][move]*100}%")
				input("Press enter to continue ")
				continue

			if ((player == O) and human_win) or ((player == X) and not human_win):
				print(f"Move #{move_num}'s contribution to loss (player: {player}): {loss_contrib[player][move]*100}%")
				input("Press enter to continue ")
				continue

			if ((player == X) and human_win) or ((player == O) and not human_win):
				print(f"Move #{move_num}'s contribution to win (player: {player}): {win_contrib[player][move]*100}%")
				input("Press enter to continue ")
				continue

			input("No one moved there!\nPress enter to continue ")
			
		except KeyboardInterrupt:
			print("<Exit>")
			exit(0)

def adv_analyze(human_win: bool):
	loss_contrib = {
		X: get_full_loss_contrib2([move["move"] for move in utils.game_moves if move["player"] == X], X),
		O: get_full_loss_contrib2([move["move"] for move in utils.game_moves if move["player"] == O], O)
	}

	win_contrib = {
		X: get_full_win_contrib2([move["move"] for move in utils.game_moves if move["player"] == X], X),
		O: get_full_win_contrib2([move["move"] for move in utils.game_moves if move["player"] == O], O)
	}

	while 1:
		clear()
		bprint(board)

		try:
			move = get_move((1, 2, 3, 4, 5, 6, 7, 8, 9), prompt="Move to Analyze: ")

			try: move_num = [i for i, game_move in enumerate(utils.game_moves) if game_move["move"] == move][0]+1
			except IndexError:
				input("No one moved there!\nPress enter to continue ")
				continue

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

while 1:
	try:
		algorithm = input("Analyzation algorithm (basic/advanced): ").lower()

		if algorithm in ("basic", 'b'):
			basic_analyze(human_win)
			break

		if algorithm in ("advanced", "adv", 'a'):
			algorithm = "advanced"
			adv_analyze(human_win)
			break

		print("Invalid Choice!")
	except KeyboardInterrupt:
		print("<Exit>")
		exit(0)