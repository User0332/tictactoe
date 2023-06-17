from random import choice
from sys import argv

POSSIBLE_MOVES = [1, 2, 3, 4, 5, 6, 7, 8, 9]*4

if len(argv) == 1:
	FIRST_MOVE_CHOICES = [1, 2, 3, 4, 5, 6, 7, 8, 9]
elif argv[1] == "corner":
	FIRST_MOVE_CHOICES = [1, 3, 7, 9]
elif argv[1] == "middle":
	FIRST_MOVE_CHOICES = [5]
elif argv[1] == "side":
	FIRST_MOVE_CHOICES = [2, 4, 6, 8]
else: raise ValueError("invalid training option")

whofirst = choice(('y', 'n'))
firstmove = choice(FIRST_MOVE_CHOICES) # start moving from outside

print(f"r\n{whofirst}\n{firstmove}")

while firstmove in POSSIBLE_MOVES: POSSIBLE_MOVES.remove(firstmove)

while POSSIBLE_MOVES:
	move = choice(POSSIBLE_MOVES)
	print(move)
	while move in POSSIBLE_MOVES: POSSIBLE_MOVES.remove(move)