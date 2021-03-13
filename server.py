from socket_utils import TCPSocket
from client import Client

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

def _run_client(client):
	print('Server receiving...')
	try:
		while True:
			obj = client.socket.recv()
			if 'type' not in obj: return
			t = obj['type']
			if t == 'HELLO':
				print('Server sending EXIT signal to client...')
				client.socket.send({'type': 'END'})
				return
			else:
				client.socket.send({'type': 'IDLE'})
	except ConnectionResetError:
		client.socket.close()

if __name__ == '__main__':
	server = Server('127.0.0.1', 8000)

	try:
		while True:
			Client(server, target=_run_client).start()
	finally:
		exit(-1)
