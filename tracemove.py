import utils
from utils import (
	get_board_rows,
	get_possible_moves,
	Game,
	X, O,
	HIGHLIGHT_SUBOPTIMAL_MOVE,
	HIGHLIGHT_LOSING_MOVE,
	HIGHLIGHT_GOOD_MOVE,
	HIGHLIGHT_OPTIMAL_MOVE
)
from minimax import minimax
from copy import deepcopy

ROW_YIELD_TO_MOVES_MAP = [
	(1, 2, 3),
	(4, 5, 6),
	(7, 8, 9),
	(1, 5, 9),
	(3, 5, 7),
	(1, 4, 7),
	(2, 5, 8),
	(3, 6, 9)
]

def get_loss_contribution(move: int, game_moves: list[int], player: str, game: Game) -> float:
	return get_full_loss_contrib2(game_moves, player, game)[move][0]

def get_win_contribution(move: int, game_moves: list[int], player: str, game: Game) -> float:
	return get_full_win_contrib2(game_moves, player, game)[move][0]

def get_full_loss_contrib(board: list[list[str]], moves: list[int], player: str) -> dict[int, float]:
	contrib: dict[int, int] = {
		move: -len(get_blocked_rows_of(board, move, X if player == O else O))
		for move in moves
	} 

	least = min(contrib.values())

	if least < 0:
		for key in contrib:
			contrib[key]+=abs(least)

	total_contrib_points = sum(contrib.values())

	if total_contrib_points == 0:
		return { move: 1/len(moves) for move in moves }

	return {
		move: value/total_contrib_points for move, value in contrib.items()
	}

def highlight_moves(board: list[list[str]], combined_analysis: dict[int, tuple[float, str]]):
	for move in combined_analysis:
		move_type = combined_analysis[move][1]
		row = board[(move-1)//3]
		idx = (move-1) % 3

		if move_type == "Optimal Move":
			row[idx] = f"{HIGHLIGHT_OPTIMAL_MOVE}{row[idx]}"
			continue

		if move_type == "Good Move":
			row[idx] = f"{HIGHLIGHT_GOOD_MOVE}{row[idx]}"
			continue

		if move_type == "Suboptimal Move":
			row[idx] = f"{HIGHLIGHT_SUBOPTIMAL_MOVE}{row[idx]}"
			continue

		if move_type == "Losing Move":
			row[idx] = f"{HIGHLIGHT_LOSING_MOVE}{row[idx]}"
			continue

	return board

def get_full_loss_contrib2(moves: list[int], player: str, game: Game=utils.game_moves) -> dict[int, tuple[float, str]]:
	contrib: dict[int, tuple[int, str]] = {}
	opponent = (X if player == O else O)

	board_before_move1 = game[0]["board_before"] if ((player == O) and (utils.COMP_FIRST)) or ((player == X) and (not utils.COMP_FIRST)) else game[1]["board_before"]

	possible_moves = get_possible_moves(board_before_move1)

	if game[0]["move"] == moves[0]:
		if moves[0] in (1, 3, 7, 9):
			contrib[moves[0]] = (1, "Optimal Move")
		elif moves[0] == 5:
			contrib[moves[0]] = (2, "Good Move")
		else:
			contrib[moves[0]] = (3, "Suboptimal Move")
	else:
		if moves[0] in minimax(
			deepcopy(board_before_move1),
			(len(possible_moves)-3),
			possible_moves, 
			True if player == O else False
		)[1]: contrib[moves[0]] = (1, "Optimal Move")
		elif (
			opponent in 
			(
				board_before_move1[0][0], 
				board_before_move1[2][0],
				board_before_move1[0][2],
				board_before_move1[2][2]
			)
		) and moves[0] != 5: contrib[moves[0]] = (10, "Losing Move") # basically a loss, make the lose contribution large
		elif moves[0] in minimax(
			deepcopy(board_before_move1),
			4,
			possible_moves, 
			True if player == O else False
		)[1]: contrib[moves[0]] = (2, "Good Move")
		else: contrib[moves[0]] = (3, "Suboptimal Move")

	for move in moves[1:]:
		board_before_move = game[0]["board_before"] if ((player == O) and (utils.COMP_FIRST)) or ((player == X) and (not utils.COMP_FIRST)) else game[1]["board_before"]

		possible_moves = get_possible_moves(board_before_move)
		
		if len(possible_moves) in (2, 3):
			best_moves = minimax(
				deepcopy(board_before_move),
				(len(possible_moves)-1),
				possible_moves, 
				True if player == O else False
			)[1]
			sub_moves = ()
		else:	
			best_moves = minimax(
				deepcopy(board_before_move),
				3,
				possible_moves, 
				True if player == O else False
			)[1]
			sub_moves = minimax(
				deepcopy(board_before_move),
				2,
				possible_moves, 
				True if player == O else False
			)[1]

		if move in best_moves:
			contrib[move] = (1, "Optimal Move")
		elif move in sub_moves:
			contrib[move] = (2, "Good Move")
		else:
			contrib[move] = (3, "Suboptimal Move") # check - this might never get triggered

	total_contrib_points = sum(val[0] for val in contrib.values())	

	return {
		move: (value[0]/total_contrib_points, value[1]) for move, value in contrib.items()
	}

def get_full_win_contrib2(moves: list[int], player: str, game: Game=utils.game_moves) -> dict[int, tuple[float, str]]:
	contrib: dict[int, tuple[int, str]] = {}

	board_before_move1 = game[0]["board_before"] if ((player == O) and (utils.COMP_FIRST)) or ((player == X) and (not utils.COMP_FIRST)) else game[1]["board_before"]

	possible_moves = get_possible_moves(board_before_move1)

	if game[0]["move"] == moves[0]:
		if moves[0] in (1, 3, 7, 9):
			contrib[moves[0]] = (3, "Optimal Move")
		elif moves[0] == 5:
			contrib[moves[0]] = (2, "Good Move")
		else:
			contrib[moves[0]] = (1, "Suboptimal Move")
	else:
		if moves[0] in minimax(
			deepcopy(board_before_move1), # assume the middle is not available
			(len(possible_moves)-3),
			possible_moves, 
			True if player == O else False
		)[1]: contrib[moves[0]] = (3, "Optimal Move")
		elif (
			(X if player == O else O) in 
			(
				board_before_move1[0][0], 
				board_before_move1[2][0],
				board_before_move1[0][2],
				board_before_move1[2][2]
			)
		) and moves[1] != 5: contrib[moves[0]] = (0, "Losing Move")
		elif moves[0] in minimax(
			deepcopy(board_before_move1),
			4,
			possible_moves, 
			True if player == O else False
		)[1]: contrib[moves[0]] = (2, "Good Move")
		else: contrib[moves[0]] = (1, "Suboptimal Move")

	for move in moves[1:]:
		board_before_move = game[0]["board_before"] if ((player == O) and (utils.COMP_FIRST)) or ((player == X) and (not utils.COMP_FIRST)) else game[1]["board_before"]

		possible_moves = get_possible_moves(board_before_move)
		
		if len(possible_moves) in (2, 3):
			best_moves = minimax(
				deepcopy(board_before_move),
				(len(possible_moves)-1),
				possible_moves, 
				True if player == O else False
			)[1]
			sub_moves = ()
		else:	
			best_moves = minimax(
				deepcopy(board_before_move),
				3,
				possible_moves, 
				True if player == O else False
			)[1]
			sub_moves = minimax(
				deepcopy(board_before_move),
				2,
				possible_moves, 
				True if player == O else False
			)[1]

		if move in best_moves:
			contrib[move] = (3, "Optimal Move")
		elif move in sub_moves:
			contrib[move] = (2, "Good Move")
		else:
			contrib[move] = (1, "Suboptimal Move") # check - this might never get triggered

	total_contrib_points = sum(val[0] for val in contrib.values())	

	return {
		move: (value[0]/total_contrib_points, value[1]) for move, value in contrib.items()
	}

def get_full_win_contrib(board: list[list[str]], moves: list[int], player: str) -> dict[int, float]:
	contrib: dict[int, int] = {}

	for move in moves:
		contrib[move] = 0

		if move in get_win_row(board, player):
			contrib[move]+=2

		contrib[move]+=len(get_blocked_rows_of(board, move, X if player == O else O))

	total_contrib_points = sum(contrib.values())

	return {
		move: value/total_contrib_points for move, value in contrib.items()
	}

def get_win_row(board: list[list[str]], player: str) -> tuple[int, int, int]:
	for i, row in enumerate(get_board_rows(board)):
		if row.count(player) == 3: return ROW_YIELD_TO_MOVES_MAP[i]

	return (0, 0, 0)

def get_blocked_rows_of(board: list[list[str]], move: int, opponent: str) -> list[tuple[str, str, str]]:
	return [row for row in get_rows_of(board, move) if row.count(opponent) == 2]

def get_rows_of(board: list[list[str]], move: int) -> list[tuple[int, int, int]]:
	first_idx = (move-1)//3
	second_idx = (move-1) % 3

	working = deepcopy(board)

	working[first_idx][second_idx] = None # set it to `None` (some object that we can track)

	return [row for row in get_board_rows(working) if None in row]