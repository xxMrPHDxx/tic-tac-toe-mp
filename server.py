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

class Player():
	def __init__(self, client, sign):
		self.client = client
		self.id     = client.id
		self.sign   = sign

class Game():
	def __init__(self, first):
		self.first  = first
		self.second = None
		self.__turn   = 0
		self.grid   = [' '] * 9
	@property
	def opponent(self):
		return self.second if self.__turn == 0 else self.first
	@property
	def player(self):
		return self.first if self.__turn == 0 else self.second
	@property
	def players(self):
		return self.first, self.second
	@property
	def ready(self):
		return all([p is not None for p in [self.first, self.second]])
	def empty(self, idx):
		return self.grid[idx] == ' '
	def is_full(self):	
		return all([
			self.first != None,
			self.second != None
		])
	def next(self):
		self.__turn = 1 - self.__turn
	def has_win(self, sign):
		matches = [
			all([self.grid[i] == sign for i in idxs])
			for idxs in [
				# Horizontal
				[0,1,2],
				[3,4,5],
				[6,7,8],
				# Vertical
				[0,3,6],
				[1,4,7],
				[2,5,8],
				# Diagonal
				[0,4,8],
				[2,4,6]
			]
		]
		print('Check for wins', sign, matches)
		return any(matches)

def _run_client(client):
	server = client.server
	try:
		while True:
			obj = client.socket.recv()
			if 'type' not in obj: return
			t = obj['type']
			# Received handshake from client so assign/reply it with an id
			if t == 'HELLO':
				client.socket.send(dict(
					type='ASSIGN_ID',
					player_id=client.id
				))
			if t == 'CREATE_GAME':
				_id = str(int(time.time()))
				sign = 'X' if random() < 0.5 else 'O'
				server.games[_id] = Game(Player(client, sign))
				print(f'Created a (game_id={_id}, player_id={client.id})')
				client.socket.send(dict(
					type='GAME_CREATED', 
					game_id=_id,
					player_id=client.id
				))
			elif t == 'LIST_GAME':
				res = dict(
					type='GAME_LIST',
					games=[
						dict(id=_id, full=game.is_full(), owner=game.first.id)
						for _id, game in server.games.items()
						if not game.ready
					]
				)
				client.socket.send(res)
			elif t == 'TRY_MOVE' and all([
				i in obj for i in ['game_id', 'row', 'col']
			]):
				print('Trying to move', obj)
				# Try to make a move
				game_id = obj['game_id']
				if game_id not in server.games:
					# Game with the given id doesn't exist so ignore
					client.socket.send(dict(
						type='MOVE_FAILED', 
						message='Invalid game id!'
					))
					continue
				game = server.games[game_id]
				# Check if there are 2 players
				if not game.ready:
					# Not enough player!
					client.socket.send(dict(
						type='MOVE_FAILED', 
						message='Not enough player!'
					))
					continue
				# Check the grid position
				row, col = obj['row'], obj['col']
				idx      = row * 3 + col
				if not (idx >= 0 and idx < 9):
					# Invalid grid position (Should never happens unless I'm dumb LOL)
					client.socket.send(dict(
						type='MOVE_FAILED', 
						message='Invalid grid position!'
					))
					continue
				# Check if the grid is empty
				if not game.empty(idx):
					# Trying to mark an occupied cell
					client.socket.send(dict(
						type='MOVE_FAILED', 
						message='Cell is not empty!'
					))
					continue
				# Check if it is this client's turn
				if game.player.id != client.id:
					# Someone else's turn
					client.socket.send(dict(
						type='MOVE_FAILED',
						message='Not your turn!'
					))
					continue
				# Update the game grid
				idx = row * 3 + col
				game.grid[idx] = game.player.sign
				# Tell the client that it's ready to execute a move
				client.socket.send(dict(
					type='MOVE_SUCCESS',
					row=row, col=col, 
					sign=game.player.sign
				))
				# Update opponent with this client's move as well
				game.opponent.client.socket.send(dict(
					type='MOVE_SUCCESS',
					row=row, col=col, 
					sign=game.player.sign
				))
				# It's the next player's turn
				game.next()
				# Check for winners and send an update to all players
				winners = [game.has_win(p.sign) for p in game.players]
				print('Winners', winners)
				if all(winners) or not any(winners): continue
				for player in game.players:
					player.client.socket.send(dict(
						type='FOUND_WINNER',
						winner=game.players[0 if winners[0] else 1].sign
					))
			elif t == 'JOIN_GAME' and 'game_id' in obj:
				game_id = obj['game_id']
				# Game with the given id doesn't exists
				if game_id not in server.games:
					client.socket.send(dict(
						type='JOIN_FAILED', 
						message='Invalid game!'
					))
					continue
				game = server.games[game_id]
				# Check if the game has enough player
				if game.ready:
					# Can't join when there's enough player
					client.socket.send(dict(
						type='JOIN_FAILED',
						message='Game is full'
					))
					continue
				# Add this client as 2nd player
				sign = 'O' if game.player.sign == 'X' else 'X'
				game.second = Player(client, sign)
				# Successfully joined a game
				client.socket.send(dict(
					type='JOIN_SUCCESS',
					game_id=game_id
				))
			elif t == 'END':
				# Close the socket and break out of the loop
				client.socket.close()
				break
			else:
				client.socket.send(dict(type='IDLE'))
	except ConnectionResetError:
		client.socket.close()

if __name__ == '__main__':
	# Create a server instance
	server = Server('127.0.0.1', 8000)

	# Assign active games mapped by a unique id (Currently empty)
	server.games = {}

	# Handle exceptions and server's socket
	error = False
	try:
		# Accept clients
		while True:
			client = Client(server, target=_run_client, daemon=True)
			client.id = int(time.time())
			client.start()
	except:
		# Set the error flag
		error = True
	finally:
		# Close the socket
		server.socket.close()
	exit(-1 if error else 0)
