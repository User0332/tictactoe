import json
from typing import Literal, TypedDict

X = 'X'
O = 'O'
COMP_FIRST = False
FLAG_O_CAN_WIN = False

class GameMoveEntry(TypedDict):
	player: Literal['X', 'O']
	move: Literal[1, 2, 3, 4, 5, 6, 7, 8, 9]
	o_score: int

Game = list[GameMoveEntry]

class PastGameEntry(TypedDict):
	won: list[Game]
	lost: list[Game]
	drew: list[Game]

class PastGames(TypedDict):
	computerfirst: PastGameEntry
	humanfirst: PastGameEntry

past_games: PastGames = {}
game_moves = Game()

def bprint(board: list[list[str]]):
	for row in board:
		print(' '.join(row))

def get_possible_moves(board: list[list[str]]) -> tuple[int]:
	moves = list[int]()	

	for row in board:
		for char in row:
			try: moves.append(int(char))
			except ValueError: continue

	return tuple(moves)

def get_move(possible_moves: tuple[int]) -> int:
	try:
		move = int(input("Your Move: "))
	except ValueError:
		print("Invalid input!")
		return get_move(possible_moves)

	if move not in possible_moves:
		print("Invalid input!")
		return get_move(possible_moves)


	return move

def win_occurred(board: list[list[str]]) -> Literal['X', 'O']:
	X_WIN = (
		(''.join(board[0]) == "XXX") or
		(''.join(board[1]) == "XXX") or
		(''.join(board[2]) == "XXX") or
		(board[0][0]+board[1][1]+board[2][2] == "XXX") or
		(board[0][2]+board[1][1]+board[2][0] == "XXX") or
		(board[0][0]+board[1][0]+board[2][0] == "XXX") or
		(board[0][1]+board[1][1]+board[2][1] == "XXX") or
		(board[0][2]+board[1][2]+board[2][2] == "XXX")
	)

	O_WIN = (
		(''.join(board[0]) == "OOO") or
		(''.join(board[1]) == "OOO") or
		(''.join(board[2]) == "OOO") or
		(board[0][0]+board[1][1]+board[2][2] == "OOO") or
		(board[0][2]+board[1][1]+board[2][0] == "OOO") or
		(board[0][0]+board[1][0]+board[2][0] == "OOO") or
		(board[0][1]+board[1][1]+board[2][1] == "OOO") or
		(board[0][2]+board[1][2]+board[2][2] == "OOO")
	)

	if X_WIN: return X
	elif O_WIN: return O
	else: return None

def place_move(board: list[list[str]], move_num: int, move_char: str, log=False, o_score: int=0):
	if log:
		game_moves.append(
			{
				"player": move_char,
				"move": move_num,
				"o_score": o_score
			}
		)
	
	for row in board:
		for i, char in enumerate(row):
			if char == str(move_num):
				row[i] = move_char
				return board
			
def full_board(board: list[list[str]]):
	return not get_possible_moves(board)

def load_past_games() -> PastGames:
	with open("./past_games.json", 'r') as f:
		return json.load(f)

def update_past_games(past_games: PastGames) -> None:
	with open("./past_games.json", 'w') as f:
		json.dump(past_games, f)

def add_past_game(game: Game, outcome: str) -> None:
	games = load_past_games()
	
	if outcome == "win": games["computerfirst" if COMP_FIRST else "humanfirst"]["won"].append(game)
	elif outcome == "loss": games["computerfirst" if COMP_FIRST else "humanfirst"]["lost"].append(game)
	else: games["computerfirst" if COMP_FIRST else "humanfirst"]["drew"].append(game)

	update_past_games(games)

def add_this_game(outcome: str) -> None:
	add_past_game(game_moves, outcome)

past_games = load_past_games()