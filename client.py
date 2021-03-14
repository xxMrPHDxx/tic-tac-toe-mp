from socket_utils import TCPSocket
from threading import Thread

import pygame
from game import Game
from gamestate import MenuState, PlayState

class Client(Thread):
	def __init__(self, server, target, addr=None, port=None):
		Thread.__init__(self, group=None, target=target, name=f'client_{id(self)}', args=(self,))
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

__EVENT_LOOP = {}
def _run_client(client):
	while not client.game.should_exit:
		try: msg = client.socket.recv()
		except: break
		if not 'type' in msg: continue
		t = msg['type']
		if t != 'IDLE': print('Got', msg)
		if t == 'GAME_CREATED' and 'id' in msg:
			_id = msg['id']
			client.game.state.push(PlayState)
		elif t == 'GAME_LIST' and 'games' in msg:
			games = msg['games']
		else:
			client.socket.send({'type': 'IDLE'})

if __name__ == '__main__':
	# Connect to the socket
	client = Client(server=None, addr='127.0.0.1', port=8000, target=_run_client)

	# Create a game and start
	client.game = Game(360, 360)
	client.game.client = client
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
		for key, held in keys.items():
			if not held: continue
			client.game.key_held(pygame.event.Event(1111, key=key))
		client.game.update()
		client.game.draw(screen)
		pygame.display.update()
		clock.tick(FPS)

