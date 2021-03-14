from .state import State

_WHITE = (255, 255, 255)

class StateManager():
	def __init__(self, game):
		self.__game = game
		self.__states = []
	def __len__(self):
		return len(self.__states)
	def pop(self):
		if len(self.__states) == 0: return
		self.__states = self.__states[:-1]
	def push(self, cls, *args, **kwargs):
		try:
			state = cls(self.__game, *args, **kwargs)
			assert isinstance(state, State), '"state" is not instance of State!'
			self.__states.append(state)
		except Exception as e: 
			raise RuntimeError(e)
	def set(self, state):
		self.pop()
		self.push(state)
	def update(self):
		if len(self) == 0: return
		self.__states[-1].update()
	def draw(self, screen):
		if len(self) == 0: return
		screen.fill(_WHITE)
		self.__states[-1].draw(screen)
	def key_down(self, event):
		if len(self) == 0: return
		self.__states[-1].key_down(event)
	def key_up(self, event):
		if len(self) == 0: return
		self.__states[-1].key_up(event)
	def key_held(self, event):
		if len(self) == 0: return
		self.__states[-1].key_held(event)
	def mouse_pressed(self, event):
		if len(self) == 0: return
		self.__states[-1].mouse_pressed(event)
