from .state import State
import pygame

_BLACK = (0, 0, 0)
_RED   = (255, 0, 0)

class DashboardState(State):
	def __init__(self, game):
		State.__init__(self, game)

		self.font1  = pygame.font.Font('freesansbold.ttf', 36)
		self.font2  = pygame.font.Font('freesansbold.ttf', 18)

		self._title = self.font1.render(f"'{game.winner}' WINS!", True, _RED)
		self._info1 = self.font2.render(
			'Press ESC to go back to main menu!', True, _BLACK
		)
	def draw(self, screen):
		w = self._title.get_rect().width
		screen.blit(self._title, ((self.game.width-w)/2, 60))
		w = self._info1.get_rect().width
		screen.blit(self._info1, ((self.game.width-w)/2, 150))
	def key_down(self, event):
		if event.key == pygame.K_ESCAPE:
			self.game.state.pop()
