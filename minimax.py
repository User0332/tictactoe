import utils
from random import choice
from utils import (
	X, O, place_move, 
	get_possible_moves,
	win_occurred,
	get_board_rows,
	Literal
)

from copy import deepcopy


def eval_row(row: tuple[str, str, str], player: Literal['X', 'O']) -> int:
	other_player = X if player == O else O

	if row.count(player) == 3: return 2 
	if (row.count(player) == 2) and (other_player not in row): return 1

	return 0

def get_player_score(board: list[list[str]], player: Literal['X', 'O']) -> int:
	score = 0

	for row in get_board_rows(board):
		score+=eval_row(row, player) ## fix this, make it so that if the computer has the option to win or block the player from winning, the computer always chooses to win

	return score

def position_eval(board: list[list[str]]) -> int:
	"""
	- positive is good for O
	- negative is good for X
	"""

	X_SCORE = get_player_score(board, X)

	O_SCORE = get_player_score(board, O)

	if utils.COMP_FIRST:
		return O_SCORE-X_SCORE
	
	if O_SCORE > X_SCORE:
		return O_SCORE
	
	return -X_SCORE

def make_obvious_move(board: list[list[str]], possible_moves: tuple[int]) -> int:
	"""
	Used to make the obvious move. Should be called when a possible win is detected 
	for either player on the next turn. This will either block the human player's move 
	or make a winning move for the computer.
	"""

	for move in possible_moves:
		if win_occurred(place_move(deepcopy(board), move, O)) == O: return move

	for move in possible_moves:
		if win_occurred(place_move(deepcopy(board), move, X)) == X: return move

def minimax(board: list[list[str]], depth: int, possible_moves: tuple[int], o_move: bool=True) -> tuple[int, list[int]]:
	if depth == 0: return position_eval(board), None

	if not o_move:
		min_score: int = float("inf")
		min_move: int = None

		scores: dict[int, int] = {}
			
		for move in possible_moves:
			new_board = place_move(deepcopy(board), move, 'X')
			
			score = minimax(
				new_board,
				depth-1,
				get_possible_moves(new_board),
				True
			)[0]

			min_score = min(min_score, score)

			scores[move] = score

			if (score <= min_score):
				min_score = score
				min_move = move

		if min_move is not None: del scores[min_move]
		
		possible_best_moves = [min_move]+[move for move, score in scores.items() if min_score == score]


		return min_score, possible_best_moves

	max_score: int = float("-inf")
	max_move: int = None

	scores: dict[int, int] = {}

	for move in possible_moves:
		new_board = place_move(deepcopy(board), move, 'O')
		
		score = minimax(
			new_board,
			depth-1,
			get_possible_moves(new_board),
			False
		)[0]

		scores[move] = score

		if (score >= max_score):
			max_score = score
			max_move = move

	if max_move is not None: del scores[max_move]
	
	possible_best_moves = [max_move]+[move for move, score in scores.items() if max_score == score]

	return max_score, possible_best_moves

def computer_move_impossible(board: list[list[str]], possible_moves: tuple[int]) -> int:
	if len(possible_moves) not in (8, 9):
		return computer_move_hard(board, possible_moves)
	
	best_moves = minimax(
		place_move(deepcopy(board), 5, X) if len(possible_moves) == 9 else board, # assume the middle is not available
		(len(possible_moves)-3),
		[move for move in possible_moves if move != 5] if len(possible_moves) == 9 else possible_moves, 
		True
	)[1]

	return choice(best_moves)

def computer_move_hard(board: list[list[str]], possible_moves: tuple[int]) -> int:
	if (get_player_score(board, X) > 0) or (get_player_score(board, O) > 0): # if someone can win, take that spot
		return make_obvious_move(board, possible_moves)
	
	if len(possible_moves) in (2, 3):
		best_moves = minimax(
			deepcopy(board),
			(len(possible_moves)-1),
			possible_moves, 
			True
		)[1]

		return choice(best_moves)
	
	best_moves = minimax(
		deepcopy(board),
		3,
		possible_moves, 
		True
	)[1]

	return choice(best_moves)

def computer_move_medium(board: list[list[str]], possible_moves: tuple[int]) -> int:
	if len(possible_moves) in (6, 7, 2, 3):
		return computer_move_hard(board, possible_moves)
	
	return computer_move_easy(board, possible_moves)

def computer_move_easy(board: list[list[str]], possible_moves: tuple[int]) -> int:
	if (get_player_score(board, X) > 0) or (get_player_score(board, O) > 0): # if someone can win, take that spot
		return make_obvious_move(board, possible_moves)

	return choice(possible_moves)

def computer_move(board: list[list[str]], possible_moves: tuple[int], difficulty: str) -> int:
	return globals()[f"computer_move_{difficulty}"](board, possible_moves)