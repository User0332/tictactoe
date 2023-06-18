import utils
from random import choice
from utils import (
	load_past_games,
	PastGameEntry,
	Game,
	O
)
from tracemove import (
	get_win_contribution,
	get_loss_contribution,
)
from typing import Literal

BOARD_90_DEG_ROTATION_MAP = {
	1: 3, 2: 6, 3: 9,
	4: 2, 5: 5, 6: 8,
	7: 1, 8: 4, 9: 7
}

def rotate90(moves: Game):
	for move in moves:
		move["move"] = BOARD_90_DEG_ROTATION_MAP[move["move"]]

	return moves

def try_match(curr_game: Game, match_to: Game) -> tuple[bool, Game]:
	i = 0

	if match_to[:-1] == curr_game: return (True, match_to)

	while i != 3:
		rotate90(match_to)
		if match_to[:-1] == curr_game: return (True, match_to)
		i+=1

	return (False, None)

def get_move(move_num: int, possible_moves: tuple[int], past_games: PastGameEntry) -> int:
	move_bias: dict[int, int] = { move: 0 for move in possible_moves}
	curr_comp_move_num = (move_num-((len(possible_moves) % 2)))

	for game in past_games["won"]:
		# if the moves below don't match, try board rotation (and transpose the necessary moves using the same rotation)
		matched, game = try_match(utils.game_moves, game[:curr_comp_move_num+1])
		if not matched: continue

		try: move = game[curr_comp_move_num]["move"]
		except IndexError: continue

		if move not in move_bias: continue

		game_moves = [item["move"] for item in game]
		
		move_bias[move]+=(4*get_win_contribution(move, game_moves, O, game))
	
	for game in past_games["drew"]:
		matched, game = try_match(utils.game_moves, game[:curr_comp_move_num+1])
		if not matched: continue

		try: move = game[curr_comp_move_num]["move"]
		except IndexError: continue
		
		if move not in move_bias: continue

		game_moves = [item["move"] for item in game]

		move_bias[move]+=(
			(2*get_win_contribution(move, game_moves, O, game)) +
			(0.3/get_loss_contribution(move, game_moves, O, game))
		)

	for game in past_games["lost"]:
		matched, game = try_match(utils.game_moves, game[:curr_comp_move_num+1])
		if not matched: continue

		try: move = game[curr_comp_move_num]["move"]
		except IndexError: continue

		if move not in move_bias: continue

		game_moves = [item["move"] for item in game]

		move_bias[move]-=(4*get_loss_contribution(move, game_moves, O, game))

	biased_moves: list[int] = [*possible_moves]

	for move, bias in move_bias.items():
		bias = round(bias)
		if bias < 0:
			biased_moves.remove(move)
			continue

		biased_moves.extend([move]*bias)

	return choice(biased_moves)

# find an algorithm to trace a given move to the game's output (possibly using common strategies or win patterns)
# make a minimax-reinforcement algorithm based off of this
def computer_move_rf(board: list[list[str]], possible_moves: tuple[int], difficulty: Literal["reinforcement"]) -> int:
	past_games = load_past_games()["computerfirst" if utils.COMP_FIRST else "humanfirst"]

	if len(possible_moves) in (8, 9): move_num = 1
	if len(possible_moves) in (6, 7): move_num = 2
	if len(possible_moves) in (4, 5): move_num = 3
	if len(possible_moves) in (2, 3): move_num = 4
	if len(possible_moves) == 1: move_num = 5

	return get_move(move_num, possible_moves, past_games)