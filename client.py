from socket_utils import TCPSocket
from threading import Thread

import pygame
from game import Game
from gamestate import MenuState

class Client(Thread):
	def __init__(self, server, target, addr=None, port=None):
		Thread.__init__(self, group=None, target=target, name=f'client_{id(self)}', args=(self,))
		if not (addr is None and port is None):
			self.__socket, self.__addr = TCPSocket(), (addr, port)
			self.socket.connect(self.__addr)
		else:
			self.__socket, self.__addr = server.socket.accept()
	@property
	def socket(self): return self.__socket
	@property
	def addr(self): return self.__addr

__EVENT_LOOP = {}
def _run_client(client):
	print('Sending JOIN handshake to server...')
	client.socket.send({'type': 'JOIN'})
	client.should_exit = False
	while not client.should_exit:
		msg = client.socket.recv()
		if not 'type' in msg: continue
		t = msg['type']
		if t == 'END':
			print('Client received EXIT signal from server!')
			return
		elif t == 'JOINED':
			print('Client successfully joined a game')
			# game.add_player()
		else:
			client.socket.send({'type': 'IDLE'})

if __name__ == '__main__':
	client = Client(server=None, addr='127.0.0.1', port=8000, target=_run_client)
	client.start()

	# Create a game
	game = Game(360, 360)
	FPS  = 30

	# Initialize pygame
	pygame.init()
	screen = pygame.display.set_mode((game.width, game.height))
	clock  = pygame.time.Clock()

	# Start at main menu
	game.state.set(MenuState)

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				client.should_exit = True
				exit(0)
			if event.type == pygame.KEYDOWN:
				game.key_down(event.key)
			if event.type == pygame.KEYUP:
				game.key_up(event.key)
			# if event.type == pygame.KEYDOWN and event.key != pygame.K_ESCAPE:
			# 	game.play()
		game.update()
		game.draw(screen)
		pygame.display.update()
		clock.tick(FPS)

