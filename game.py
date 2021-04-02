from gamestate import StateManager, DashboardState

class Cell():
	def __init__(self, row, col):
		self.__row, self.__col = row, col
		self.__value = None
	@property
	def row(self): return self.__row
	@property
	def col(self): return self.__col
	@property
	def value(self): return self.__value
	def empty(self): return self.__value is None
	def tick(self, value): 
		assert value in 'XO', f'Invalid sign specified ({value})!'
		self.__value = value

class Game():
	def __init__(self, width, height):
		self.__width     = width
		self.__height    = height
		self.__grid      = [Cell(i//3, i%3) for i in range(9)]
		self.__sm        = StateManager(self)
		self.should_exit = False
	@property
	def width(self): return self.__width
	@property
	def height(self): return self.__height
	@property
	def state(self): return self.__sm
	def cell(self, row, col):
		assert type(row) == int and type(col) == int, 'Row and col should be int!'
		idx = row * 3 + col
		assert idx >= 0 and idx < 9, 'Invalid grid position!'
		return self.__grid[idx]
	def clear_grid(self):
		# Clear the cells
		for i, cell in enumerate(self.__grid):
			self.__grid[i] = Cell(cell.row, cell.col)
	def exit_game(self, reason='Game ended by user'):
		if self.id == None: return
		self.client.send(dict(type='EXIT_GAME', reason=reason))
	def found_winner(self, winner):
		# Tell the server that the game has ended
		self.client.socket.send(dict(
			type='EXIT_GAME',
			reason='Found a winner!'
		))
		self.winner = winner
		self.state.set(DashboardState)
	def move(self, row, col, sign):
		# Grid indices validation
		assert type(row) == int, 'Row should be integer!'
		assert type(col) == int, 'Column should be integer!'
		idx = row*3 + col
		assert Game.__valid(idx), 'Invalid position (-1<x<9)!'

		# Tick empty cells
		if self.__grid[idx].empty():
			self.__grid[idx].tick(sign)
	def update(self):
		self.state.update()
	def draw(self, screen):
		self.state.draw(screen)
	def key_down(self, event):
		self.state.key_down(event)
	def key_up(self, event):
		self.state.key_up(event)
	def key_held(self, event):
		self.state.key_held(event)
	def mouse_pressed(self, event):
		self.state.mouse_pressed(event)
	@staticmethod
	def __valid(pos):
		return pos >= 0 and pos < 9
	def end_game(self, reason=None):
		# Try to request the server to end the active game
		if self.game.id:
			self.client.socket.send(dict(
				type='EXIT_GAME',
				game_id=self.id,
				player_id=self.player_id,
				reason=reason
			))
