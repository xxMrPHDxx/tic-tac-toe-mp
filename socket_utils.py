from socket import socket as Socket, AF_INET, AF_INET6, SOCK_STREAM
from socket import SOL_SOCKET, SO_REUSEADDR
from base64 import b64encode, b64decode
import json

'''
	A class which wraps the socket to send and receive json-like data.
	It defaults to TCP and set to reuse the address to avoid a known error
	which is "Address already in use".
'''
class TCPSocket(Socket):
	def __init__(self, socket=None):
		# Create a default socket if given None
		self.__socket = Socket(AF_INET6, SOCK_STREAM) if socket is None else socket
		# Set to re-use the address to avoid error: "Address already in use"
		self.__socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	@property
	def socket(self): return self.__socket
	def accept(self):
		# Wraps the socket in our custom TCPSocket class
		socket, addr = self.socket.accept()
		return TCPSocket(socket), addr
	def bind(self, addr):
		self.socket.bind(addr)
	def close(self):
		self.socket.close()
	def connect(self, addr):
		self.socket.connect(addr)
	def listen(self):
		self.socket.listen()
	def recv(self, size=None):
		# If size isn't valid, get 4 bytes of data and use that instead
		if type(size) != int:
			size = int.from_bytes(self.socket.recv(4), 'big')
		# Our data is encoded using base64 encoder (smaller size and more secure)
		try:
			return json.loads(b64decode(self.socket.recv(size)).decode('utf-8'))
		except:
			return dict()
	def send(self, obj):
		# Only accept strings or dict objects
		if type(obj) == str:
			obj = {'type': 'MESSAGE', 'message': obj}
		if type(obj) != dict:
			raise Exception('TCPSocket::send(...) expects a str or dict at argument 1!')
		# Encode our stringified json using base64
		content = b64encode(json.dumps(obj).encode('utf-8'))
		# Get the size (4-bytes with big-endian encoding)
		size		= len(content).to_bytes(4, 'big')
		# Send the data
		self.socket.send(size + content)
