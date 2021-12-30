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

  # Client socket loop
  while not client.game.should_exit:
    # Try to receive response from server
    try: obj = client.socket.recv()
    except Exception as e:
      # The server or game closed, so exit and close the socket
      client.socket.send(dict(type='EXIT_GAME', reason='Connection failed!'))
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
      client.game.state.set(PlayState)

    # Assign the active games for listing
    if t == 'GAME_LIST' and 'games' in obj:
      client.game.game_list = obj['games']

    # Join a game (Should already be valid)
    if t == 'JOIN_SUCCESS' and 'game_id' in obj:
      client.game.id = obj['game_id']
      client.game.state.set(PlayState)

    # Something wrong when trying to join a game
    if t == 'JOIN_FAILED' and 'message' in obj:
      print(f'[ERROR]: {obj["message"]}')

    # Make a move (Should already be valid)
    if t == 'MOVE_SUCCESS' and all([
      i in obj for i in ['row', 'col', 'sign']
    ]):
      row, col, sign = obj['row'], obj['col'], obj['sign']
      client.game.move(row, col, sign)

    # Something wrong when trying to make a move
    if t == 'MOVE_FAILED' and 'message' in obj:
      print(f'[ERROR]: {obj["message"]}')

    # A player has won the game
    if t == 'FOUND_WINNER' and 'winner' in obj:
      client.game.found_winner(obj['winner'])

    # Game has ended
    if t == 'GAME_ENDED' and 'reason' in obj:
      print(f'Game ends, reason="{obj["reason"]}"')

if __name__ == '__main__':
  from sys import argv
  import re

  # Checking address from argument or use default
  addr = (len(argv) > 1 and argv[1]) or '127.0.0.1:8000'
  if not any([
      re.match(r'^\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}\:\d{1,5}$', addr),
      re.match(r'^\w{1,4}\:\w{1,4}\:\w{1,4}\:\w{1,4}\:\w{1,4}\:\w{1,4}\:\w{1,4}\:\w{1,4}\:\d{1,5}$', addr)
    ]):
    print('Usage: python3 client.py [ADDRESS:PORT]')
    exit(-1)
  
  # Parsing the address
  *addr, port = addr.split(':')
  addr = ':'.join(addr)

  # Connect to the socket
  print(f'[INFO]: Connecting to server at {addr}:{port}.')
  client = Client(server=None, addr=addr, port=int(port), target=_run_client)

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

