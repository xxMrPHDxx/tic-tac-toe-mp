from .state import State
import pygame

_BLACK = (0, 0, 0)
_WHITE = (255, 255, 255)
_RED = (255, 0, 0)

def _is_alphanumeric(letter):
	return any([
		letter >= 'a' and letter <= 'z',
		letter >= 'A' and letter <= 'Z',
		letter >= '0' and letter <= '9'
	])

class CreateGameState(State):
	def __init__(self, game):
		State.__init__(self, game)

		# Font, title and other variables
		self.font1  = pygame.font.Font('freesansbold.ttf', 36)
		self.font2  = pygame.font.Font('freesansbold.ttf', 16)
		self._name  = ''
		self._max_name_length	= 12
		self.name   = self.font2.render(
			f'Name (Max: {self._max_name_length}):  ', True, _BLACK
		)

		# Create static background
		self.bg = pygame.Surface((self.game.width, self.game.height))
		self.bg.fill(_WHITE)
		title   = self.font1.render('Create game!', True, _BLACK)
		self.bg.blit(title, ((self.game.width-title.get_rect().width)/2, 40))
	def draw(self, screen):
		t_name = self.font2.render(self._name, True, _RED)
		w1, w2 = [t.get_rect().width for t in [self.name, t_name]]
		w  = w1 + w2
		ww = self.game.width-w
		screen.blit(self.bg, (0, 0))
		screen.blit(self.name, (ww/2, 120))
		screen.blit(t_name, (ww/2 + w1, 120))
	def key_down(self, event):
		if event.key == pygame.K_ESCAPE:
			self.game.state.pop()
		elif event.key == pygame.K_RETURN:
			self.game.client.socket.send(dict(type='CREATE_GAME', name=self._name))
		if _is_alphanumeric(event.unicode):
			if len(self._name) < self._max_name_length: 
				self._name += event.unicode
	def key_held(self, event):
		if event.key == pygame.K_BACKSPACE:
			self._name = self._name[:-1]
