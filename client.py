from socket_utils import TCPSocket
from threading import Thread

import pygame
from game import Game
from gamestate import MenuState, PlayState

'''
		Threaded client which contains our custom socket wrapper.
		The Thread's 'target' callback is used in server.py so it
		is passed as argument
'''
class Client(Thread):
	def __init__(self, server, target, addr=None, port=None, **kwargs):
		Thread.__init__(self, group=None, target=target, name=f'client_{id(self)}', args=(self,), **kwargs)
		self.__server = server
		if not (addr is None and port is None):
			self.__socket, self.__addr = TCPSocket(), (addr, port)
			self.socket.connect(self.__addr)
		else:
			self.__socket, self.__addr = server.socket.accept()
	@property
	def server(self): return self.__server
	@property
	def socket(self): return self.__socket
	@property
	def addr(self): return self.__addr

def _run_client(client):
	# Initialize server related stuff
	client.game.id = None
	client.game.game_list = []
	
	# Handshake with client
	client.socket.send(dict(type='HELLO'))

	# Game loop
	while not client.game.should_exit:
		# Try to receive response from server
		try: obj = client.socket.recv()
		except Exception:
			# The server or game closed, so exit and close the socket
			client.socket.close()
			break

		# Assign the type to variable "t" so it's shorter
		t   = obj['type']

		# Assign client or player id from server
		if t == 'ASSIGN_ID' and 'player_id' in obj:
			client.game.player_id = obj['player_id']

		# Game created so assign the id and go to the play state
		if t == 'GAME_CREATED' and 'game_id' in obj and 'player_id' in obj:
			client.game.id = obj['game_id']
			client.game.state.push(PlayState)

		# Assign the active games for listing
		if t == 'GAME_LIST' and 'games' in obj:
			client.game.game_list = obj['games']

		# Join a game (Should already be valid)
		if t == 'JOIN_SUCCESS' and 'game_id' in obj:
			client.game.id = obj['game_id']
			client.game.state.push(PlayState)

		# Something wrong when trying to join a game
		if t == 'JOIN_FAILED' and 'message' in obj:
			print(f'[Error]: {obj["message"]}')

		# Make a move (Should already be valid)
		if t == 'MOVE_SUCCESS' and all([
			i in obj for i in ['row', 'col', 'sign']
		]):
			row, col, sign = obj['row'], obj['col'], obj['sign']
			client.game.move(row, col, sign)

		# Something wrong when trying to make a move
		if t == 'MOVE_FAILED' and 'message' in obj:
			print(f'[Error]: {obj["message"]}')

		# A player has won the game
		if t == 'FOUND_WINNER' and 'winner' in obj:
			# TODO: Go to dashboard or something!
			print('Got winner', obj['winner'])

if __name__ == '__main__':
	# Connect to the socket
	client = Client(server=None, addr='127.0.0.1', port=8000, target=_run_client)

	# Create a game
	client.game = Game(360, 360)
	client.game.client = client

	# Start the game (Ensures game keeps track of client and vice versa)
	client.start()

	# Initialize pygame
	pygame.init()
	screen = pygame.display.set_mode((client.game.width, client.game.height))
	clock  = pygame.time.Clock()

	# Start at main menu
	client.game.state.set(MenuState)

	# Key on hold flags
	keys = {i: False for i in range(256)}

	# Game loop at 30 FPS
	FPS = 30
	while True:
		# Event handling
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				client.game.should_exit = True
				client.socket.send(dict(type='END'))
				exit(0)
			if event.type == pygame.KEYDOWN:
				client.game.key_down(event)
				keys[event.key] = True
			if event.type == pygame.KEYUP:
				client.game.key_up(event)
				keys[event.key] = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				client.game.mouse_pressed(event)
		for key, held in keys.items():
			if not held: continue
			client.game.key_held(pygame.event.Event(1111, key=key))

		# Update and draw
		client.game.update()
		client.game.draw(screen)

		# Update pygame's display and simulate a tick
		pygame.display.update()
		clock.tick(FPS)

