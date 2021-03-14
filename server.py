from socket_utils import TCPSocket
from client import Client
from random import random
import time

class Server():
	def __init__(self, addr, port, **kwargs):
		self.__name   = str(f'server_{id(self)}')
		self.__socket = TCPSocket()
		self.socket.bind((addr, port))
		self.socket.listen()
	@property
	def name(self): return self.__name
	@property
	def socket(self): return self.__socket
	def _send_string(self, string):
		assert type(message) == str, 'Argument supplied is not a type of "str"!'
		self.socket.send(string)
	def send_message(self, message):
		self._send_string(message)
	def send_error(self, message):
		self._send_string(message)
	def send(self, obj):
		self.socket.send(obj)

class Game():
	def __init__(self, first, second):
		self._first  = first
		self._second = second

def _run_client(client):
	server = client.server
	try:
		while True:
			obj = client.socket.recv()
			if 'type' not in obj: return
			t = obj['type']
			if t == 'CREATE_GAME':
				_id = str(time.time())
				cross, circle = 'XO' if random() else 'OX'
				server.games[_id] = []
				print('Created a game with id={_id}')
				client.socket.send(dict(type='GAME_CREATED', id=_id))
			elif t == 'LIST_GAME':
				res = dict(
					type='GAME_LIST',
					games=[
						dict(players=len(game))
						for _id, game in server.games.items()
					]
				)
				client.socket.send(res)
			elif t == 'JOIN_GAME':
				# TODO: Join a game based on id
				pass
			elif t == 'END':
				# Close the socket and break out of the loop
				client.socket.close()
				break
			else:
				client.socket.send(dict(type='IDLE'))
	except ConnectionResetError:
		client.socket.close()

if __name__ == '__main__':
	server = Server('127.0.0.1', 8000)

	# Assign active games mapped by a unique id (Currently empty)
	server.games = {}

	try:
		# Accept clients
		while True:
			Client(server, target=_run_client).start()
	finally:
		# Close the socket and exit
		server.socket.close()
		exit(-1)
