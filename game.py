from gamestate import StateManager

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
	def move(self, row, col, sign):
		assert type(row) == int and type(col) == int, 'Row and col should be integer!'
		idx = row*3 + col
		assert Game.__valid(idx), 'Invalid position (-1<x<9)!'
		assert self.__grid[idx].empty(), f'Cell ({row}, {col}) is not empty!'
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
