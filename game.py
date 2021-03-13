from gamestate import StateManager, PlayState

def __valid(i):
	return i >= 0 and i < 3

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
		assert value in ['X', 'O'], f'Invalid sign specified ({value})!'
		self.__value = value

class Player():
	def __init__(self, cross):
		self.__sign = 'X' if cross else 'O'
	@property
	def sign(self): return self.__sign

class Game():
	def __init__(self, width, height):
		self.__width, self.__height = width, height
		self.__grid      = [Cell(i//3, i%3) for i in range(9)]
		self.__players   = [Player(i==0) for i in range(2)]
		self.__current   = 0
		self.__sm        = StateManager(self)
		self.should_exit = False
	@property
	def width(self): return self.__width
	@property
	def height(self): return self.__height
	@property
	def player(self): return self.__player[self.__current]
	@property
	def state(self): return self.__sm
	def cell(self, row, col):
		assert type(row) == int and type(col) == int, 'Row and col should be int!'
		idx = row * 3 + col
		assert idx >= 0 and idx < 9, 'Invalid grid position!'
		return self.__grid[idx]
	def move(self, row, col):
		assert type(row) == int and type(col) == int, 'Row and col should be integer!'
		assert __valid(row) and __valid(col), 'Row and/or col out of range (0-2)!'
		idx = row*3 + col
		assert self.__grid[idx].empty(), f'Cell ({row}, {col}) is not empty!'
		self.__grid[idx].tick(self.player.sign)
	def menu(self):
		if len(self.state) != 2: return
		self.state.pop()
	def play(self):
		if len(self.state) != 1: return
		self.state.push(PlayState)
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
