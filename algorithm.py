import locals
from random import randint
from locals import (
	X, O, place_move, 
	get_possible_moves,
	Literal
)

from copy import deepcopy

def eval_row(row: tuple[str, str, str], player: Literal['X', 'O']) -> int:
	other_player = X if player == O else O

	if row.count(player) == 3: return 10 # overpower all other scores
	if (row.count(player) == 2) and (other_player not in row): return 1

	return 0

def get_board_rows(board: list[list[str]]) -> tuple[tuple[str, str, str]]:
	return (
		board[0],
		board[1],
		board[2],
		(board[0][0], board[1][1], board[2][2]),
		(board[0][2], board[1][1], board[2][0]),
		(board[0][0], board[1][0], board[2][0]),
		(board[0][1], board[1][1], board[2][1]),
		(board[0][2], board[1][2], board[2][2])
	)

def get_player_score(board: list[list[str]], player: Literal['X', 'O']) -> int:
	score = 0

	for row in get_board_rows(board):
		score+=eval_row(row, player)

	return score


def position_eval(board: list[list[str]]) -> int:
	"""
	- positive is good for O
	- negative is good for X
	"""

	X_SCORE = get_player_score(board, X)

	O_SCORE = get_player_score(board, O)

	if locals.COMP_FIRST:
		return O_SCORE-X_SCORE
	
	if O_SCORE > X_SCORE:
		return O_SCORE
	
	return -X_SCORE

def minimax(board: list[list[str]], depth: int, possible_moves: tuple[int], o_move: bool=True) ->tuple[int, int]:
	if depth == 0: return position_eval(board), None

	if not o_move:
		min_score: int = float("inf")
			
		for move in possible_moves:
			new_board = place_move(deepcopy(board), move, 'X')
			
			score = minimax(
				new_board,
				depth-1,
				get_possible_moves(new_board),
				True
			)[0]

			min_score = min(min_score, score)

		return min_score, None

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
		deepcopy(board),
		(len(possible_moves)-3),
		possible_moves, 
		True
	)[1]

	return best_moves[
		randint(0, len(best_moves)-1)
	]

def computer_move_hard(board: list[list[str]], possible_moves: tuple[int]) -> int:
	if len(possible_moves) in (2, 3):
		best_moves = minimax(
			deepcopy(board),
			(len(possible_moves)-1),
			possible_moves, 
			True
		)[1]

		return best_moves[
			randint(0, len(best_moves)-1)
		]
	
	best_moves = minimax(
		deepcopy(board),
		3,
		possible_moves, 
		True
	)[1]

	return best_moves[
		randint(0, len(best_moves)-1)
	]

def computer_move_medium(board: list[list[str]], possible_moves: tuple[int]) -> int:
	if len(possible_moves) in (6, 7, 2, 3):
		return computer_move_hard(board, possible_moves)
	
	return computer_move_easy(board, possible_moves)

def computer_move_easy(board: list[list[str]], possible_moves: tuple[int]) -> int:
	if (get_player_score(board, X) > 0) or (get_player_score(board, O) > 0): # if someone can win, take that spot
		return minimax(
			deepcopy(board),
			2,
			possible_moves,
			True
		)[1][0]

	return possible_moves[
		randint(0, len(possible_moves)-1)
	]

def computer_move(board: list[list[str]], possible_moves: tuple[int], difficulty: str) -> int:
	return globals()[f"computer_move_{difficulty}"](board, possible_moves)