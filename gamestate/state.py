class State():
	def __init__(self, game):
		self.__game = game
	@property
	def game(self): return self.__game
	def update(self): pass
	def draw(self, screen): pass
	def key_down(self, event): pass
	def key_up(self, event): pass
	def key_held(self, event): pass
